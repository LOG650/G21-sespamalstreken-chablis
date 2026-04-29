from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[4]
ACTIVITY_DIR = Path(__file__).resolve().parent.parent
STRUCTURED_DATA_DIR = (
    ROOT / "006 analysis" / "01_datagrunnlag" / "03_strukturering_av_datasett" / "data"
)

LEGS_CSV = STRUCTURED_DATA_DIR / "tab_voyage_legs_2025.csv"
CAPACITY_CSV = STRUCTURED_DATA_DIR / "tab_vessel_class_capacity.csv"
PRICE_CSV = STRUCTURED_DATA_DIR / "tab_bunker_monthly_by_port.csv"

OUTPUT_DIR = ACTIVITY_DIR / "output"
METADATA_DIR = ACTIVITY_DIR / "metadata"
SUMMARY_JSON = OUTPUT_DIR / "res_route_inventory_summary.json"
BY_VESSEL_CSV = OUTPUT_DIR / "res_route_inventory_by_vessel.csv"
BY_LEG_CSV = OUTPUT_DIR / "res_route_inventory_by_leg.csv"
PURCHASES_CSV = OUTPUT_DIR / "res_route_inventory_purchases.csv"
SENSITIVITY_CSV = OUTPUT_DIR / "res_route_inventory_proxy_sensitivity.csv"
SUMMARY_MD = METADATA_DIR / "res_route_inventory_summary.md"

DEFAULT_EXTERNAL_PRICE_MULTIPLIER = 1.25
SENSITIVITY_MULTIPLIERS = (1.10, 1.25, 1.50)


@dataclass(frozen=True)
class Leg:
    vessel_file_id: str
    vessel_class: str
    voyage_number: str
    leg_sequence: int
    period_month: str
    from_port: str
    to_port: str
    available_ports: tuple[str, ...]
    consumption: float
    rob_start: float
    rob_end: float | None
    data_quality_flag: str


@dataclass(frozen=True)
class PurchaseOpportunity:
    leg_index: int
    port: str
    price: float
    price_source: str


@dataclass(frozen=True)
class PriceData:
    exact_prices: dict[tuple[str, str], float]
    port_average_prices: dict[str, float]
    external_price: float
    external_price_multiplier: float


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_float(value: str | None, default: float | None = None) -> float | None:
    if value is None or value == "":
        return default
    return float(value)


def load_capacities() -> dict[str, float]:
    return {
        row["vessel_class"]: float(row["bunker_capacity_m3"])
        for row in read_csv(CAPACITY_CSV)
    }


def load_price_data(external_price_multiplier: float = 1.25) -> PriceData:
    exact_prices: dict[tuple[str, str], float] = {}
    port_totals: dict[str, dict[str, float]] = {}
    for row in read_csv(PRICE_CSV):
        port = row["port"]
        month = row["delivery_month"]
        qty = float(row["total_qty"])
        price = float(row["weighted_avg_price"])
        exact_prices[(month, port)] = price
        if port not in port_totals:
            port_totals[port] = {"qty": 0.0, "cost": 0.0}
        port_totals[port]["qty"] += qty
        port_totals[port]["cost"] += qty * price

    port_average_prices = {
        port: totals["cost"] / totals["qty"]
        for port, totals in port_totals.items()
        if totals["qty"] > 0
    }
    external_price = max(port_average_prices.values()) * external_price_multiplier
    return PriceData(
        exact_prices=exact_prices,
        port_average_prices=port_average_prices,
        external_price=external_price,
        external_price_multiplier=external_price_multiplier,
    )


def load_legs() -> list[Leg]:
    legs: list[Leg] = []
    for row in read_csv(LEGS_CSV):
        rob_start = parse_float(row["rob_start"])
        if rob_start is None:
            raise RuntimeError(
                f"Mangler rob_start for {row['vessel_file_id']} etappe {row['leg_sequence']}"
            )
        available_ports = tuple(
            port for port in row["available_ports_P00X"].split("|") if port
        )
        legs.append(
            Leg(
                vessel_file_id=row["vessel_file_id"],
                vessel_class=row["vessel_class"],
                voyage_number=row["voyage_number"],
                leg_sequence=int(row["leg_sequence"]),
                period_month=row["period_month"],
                from_port=row["from_port_P00X"],
                to_port=row["to_port_P00X"],
                available_ports=available_ports,
                consumption=float(row["fuel_consumption_total"]),
                rob_start=rob_start,
                rob_end=parse_float(row["rob_end"]),
                data_quality_flag=row["data_quality_flag"],
            )
        )
    return sorted(legs, key=lambda leg: (leg.vessel_file_id, leg.leg_sequence))


def group_legs_by_vessel(legs: list[Leg]) -> dict[str, list[Leg]]:
    grouped: dict[str, list[Leg]] = {}
    for leg in legs:
        grouped.setdefault(leg.vessel_file_id, []).append(leg)
    return grouped


def build_purchase_opportunities(
    legs: list[Leg],
    price_data: PriceData,
) -> list[PurchaseOpportunity]:
    opportunities: list[PurchaseOpportunity] = []
    for leg_index, leg in enumerate(legs):
        for port in sorted(set(leg.available_ports)):
            if port not in price_data.port_average_prices:
                continue
            exact_price = price_data.exact_prices.get((leg.period_month, port))
            if exact_price is not None:
                opportunities.append(
                    PurchaseOpportunity(
                        leg_index=leg_index,
                        port=port,
                        price=exact_price,
                        price_source="monthly_observation",
                    )
                )
            else:
                opportunities.append(
                    PurchaseOpportunity(
                        leg_index=leg_index,
                        port=port,
                        price=price_data.port_average_prices[port],
                        price_source="historical_port_average",
                    )
                )
    return opportunities


def solve_vessel(
    vessel_file_id: str,
    legs: list[Leg],
    capacity: float,
    price_data: PriceData,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    opportunities = build_purchase_opportunities(legs, price_data)
    n_x = len(opportunities)
    n_l = len(legs)
    u_offset = n_x
    inv_offset = n_x + n_l
    n_vars = n_x + (2 * n_l)

    bounds: list[tuple[float, float | None]] = []
    bounds.extend((0.0, None) for _ in opportunities)
    bounds.extend((0.0, None) for _ in legs)
    bounds.extend((0.0, capacity) for _ in legs)

    a_eq: list[list[float]] = []
    b_eq: list[float] = []
    for leg_index, leg in enumerate(legs):
        row = [0.0] * n_vars
        for opp_index, opp in enumerate(opportunities):
            if opp.leg_index == leg_index:
                row[opp_index] = 1.0
        row[u_offset + leg_index] = 1.0
        row[inv_offset + leg_index] = -1.0
        if leg_index > 0:
            row[inv_offset + leg_index - 1] = 1.0
            b_value = leg.consumption
        else:
            b_value = leg.consumption - leg.rob_start
        a_eq.append(row)
        b_eq.append(b_value)

    a_ub_capacity: list[list[float]] = []
    b_ub_capacity: list[float] = []
    for leg_index, leg in enumerate(legs):
        row = [0.0] * n_vars
        for opp_index, opp in enumerate(opportunities):
            if opp.leg_index == leg_index:
                row[opp_index] = 1.0
        row[u_offset + leg_index] = 1.0
        if leg_index > 0:
            row[inv_offset + leg_index - 1] = 1.0
            b_value = capacity
        else:
            b_value = capacity - leg.rob_start
        a_ub_capacity.append(row)
        b_ub_capacity.append(b_value)

    objective = [0.0] * n_vars
    for opp_index, opp in enumerate(opportunities):
        objective[opp_index] = opp.price
    for leg_index in range(n_l):
        objective[u_offset + leg_index] = price_data.external_price

    result = linprog(
        c=objective,
        A_ub=a_ub_capacity,
        b_ub=b_ub_capacity,
        A_eq=a_eq,
        b_eq=b_eq,
        bounds=bounds,
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"V2 feilet for {vessel_file_id}: {result.message}")

    values = result.x
    purchases_by_leg: dict[int, list[dict[str, object]]] = {}
    purchase_rows: list[dict[str, object]] = []
    for opp_index, opp in enumerate(opportunities):
        qty = float(values[opp_index])
        if qty <= 1e-6:
            continue
        leg = legs[opp.leg_index]
        cost = qty * opp.price
        row = {
            "vessel_file_id": vessel_file_id,
            "vessel_class": leg.vessel_class,
            "leg_sequence": leg.leg_sequence,
            "period_month": leg.period_month,
            "voyage_number": leg.voyage_number,
            "port": opp.port,
            "purchase_qty": round(qty, 6),
            "price": round(opp.price, 2),
            "price_source": opp.price_source,
            "priced_cost": round(cost, 2),
        }
        purchase_rows.append(row)
        purchases_by_leg.setdefault(opp.leg_index, []).append(row)

    leg_rows: list[dict[str, object]] = []
    for leg_index, leg in enumerate(legs):
        purchase_qty = sum(
            float(row["purchase_qty"]) for row in purchases_by_leg.get(leg_index, [])
        )
        external_qty = float(values[u_offset + leg_index])
        inventory_end = float(values[inv_offset + leg_index])
        observed_diff = (
            inventory_end - leg.rob_end if leg.rob_end is not None else None
        )
        available_priced_ports = sorted(
            {
                opp.port
                for opp in opportunities
                if opp.leg_index == leg_index
            }
        )
        leg_rows.append(
            {
                "vessel_file_id": vessel_file_id,
                "vessel_class": leg.vessel_class,
                "leg_sequence": leg.leg_sequence,
                "period_month": leg.period_month,
                "voyage_number": leg.voyage_number,
                "from_port": leg.from_port,
                "to_port": leg.to_port,
                "available_ports": "|".join(leg.available_ports),
                "available_priced_ports": "|".join(available_priced_ports),
                "consumption": round(leg.consumption, 6),
                "rob_start_observed": round(leg.rob_start, 6),
                "rob_end_observed": round(leg.rob_end, 6) if leg.rob_end is not None else "",
                "model_purchase_qty": round(purchase_qty, 6),
                "model_external_qty": round(external_qty, 6),
                "model_external_cost": round(external_qty * price_data.external_price, 2),
                "model_inventory_end": round(inventory_end, 6),
                "inventory_end_minus_observed": round(observed_diff, 6)
                if observed_diff is not None
                else "",
                "capacity": round(capacity, 6),
                "data_quality_flag": leg.data_quality_flag,
            }
        )

    priced_cost = sum(float(row["priced_cost"]) for row in purchase_rows)
    total_consumption = sum(leg.consumption for leg in legs)
    total_purchase = sum(float(row["model_purchase_qty"]) for row in leg_rows)
    total_external = sum(float(row["model_external_qty"]) for row in leg_rows)
    external_cost = total_external * price_data.external_price
    priced_leg_count = sum(1 for row in leg_rows if row["available_priced_ports"])
    purchased_leg_count = sum(1 for row in leg_rows if float(row["model_purchase_qty"]) > 1e-6)

    vessel_summary = {
        "vessel_file_id": vessel_file_id,
        "vessel_class": legs[0].vessel_class,
        "leg_count": len(legs),
        "priced_leg_count": priced_leg_count,
        "purchased_leg_count": purchased_leg_count,
        "total_consumption": round(total_consumption, 6),
        "initial_rob": round(legs[0].rob_start, 6),
        "capacity": round(capacity, 6),
        "model_purchase_qty": round(total_purchase, 6),
        "model_external_qty": round(total_external, 6),
        "external_share_of_consumption": round(total_external / total_consumption, 6)
        if total_consumption
        else 0.0,
        "priced_share_of_consumption": round(total_purchase / total_consumption, 6)
        if total_consumption
        else 0.0,
        "priced_cost": round(priced_cost, 2),
        "external_cost": round(external_cost, 2),
        "total_model_cost": round(priced_cost + external_cost, 2),
        "solver_status": result.message,
    }
    return leg_rows, purchase_rows, vessel_summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_summary_md(summary: dict[str, object], by_vessel: list[dict[str, object]]) -> None:
    lines = [
        "# Operasjonell hovedmodell",
        "",
        "Modellen bruker voyage-etapper, forbruk, ROB og fartøykapasitet som operative restriksjoner. Prisdata brukes for modellhavnene P001-P004. Dersom en rutehavn har prisgrunnlag, men ikke eksakt prisobservasjon i 2025-måneden, brukes historisk havnesnitt som prisproxy. Havner utenfor P001-P004 får ikke egen estimert pris; nødvendig bunkring utenfor prisgrunnlaget vises som ekstern/ukjent bunkring med konservativ proxykostnad.",
        "",
        "## Resultat",
        "",
        f"- Fartøyfiler: {summary['vessel_file_count']}",
        f"- Etapper: {summary['leg_count']}",
        f"- Etapper med priset havn tilgjengelig: {summary['priced_leg_count']}",
        f"- Etapper med modellert kjøp i priset havn: {summary['purchased_leg_count']}",
        f"- Samlet forbruk: {summary['total_consumption']:,.2f}",
        f"- Modellert kjøp i prisede havner: {summary['model_purchase_qty']:,.2f}",
        f"- Ekstern/ukjent bunkring: {summary['model_external_qty']:,.2f}",
        f"- Andel ekstern/ukjent av forbruk: {summary['external_share_of_consumption']:.2%}",
        f"- Pris per ekstern/ukjent enhet: {summary['external_price']:,.2f}",
        f"- Kostnad i prisede havner: {summary['priced_cost']:,.2f}",
        f"- Kostnad for ekstern/ukjent bunkring: {summary['external_cost']:,.2f}",
        f"- Total modellkostnad: {summary['total_model_cost']:,.2f}",
        "",
        "## Per fartøyfil",
        "",
        "| Fartøyfil | Klasse | Etapper | Prisede etapper | Kjøp-etapper | Forbruk | Kjøp i prisede havner | Ekstern/ukjent | Total kostnad |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in by_vessel:
        lines.append(
            "| {vessel_file_id} | {vessel_class} | {leg_count} | {priced_leg_count} | "
            "{purchased_leg_count} | {total_consumption:,.2f} | "
            "{model_purchase_qty:,.2f} | {model_external_qty:,.2f} | "
            "{total_model_cost:,.2f} |".format(**row)
        )

    lines.extend(
        [
            "",
            "## Tolkning",
            "",
            "Modellen er et faktisk lineært optimeringsproblem fordi den må balansere kjøp, forbruk, beholdning og tankkapasitet gjennom fartøyenes etapperekkefølge. Den gir Odfjell en konkret, kvantitativ plan for når det lønner seg å fylle i prisede modellhavner, og hvor mye som fortsatt må dekkes utenfor prisgrunnlaget. Ekstern/ukjent bunkring er ikke en anbefalt havn, men en kostnadsatt markør for datagapet modellen ikke kan løse uten bedre prisdekning.",
        ]
    )
    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_model(
    external_price_multiplier: float,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    legs = load_legs()
    capacities = load_capacities()
    price_data = load_price_data(external_price_multiplier)
    grouped = group_legs_by_vessel(legs)

    all_leg_rows: list[dict[str, object]] = []
    all_purchase_rows: list[dict[str, object]] = []
    by_vessel: list[dict[str, object]] = []

    for vessel_file_id, vessel_legs in sorted(grouped.items()):
        vessel_class = vessel_legs[0].vessel_class
        capacity = capacities[vessel_class]
        leg_rows, purchase_rows, vessel_summary = solve_vessel(
            vessel_file_id,
            vessel_legs,
            capacity,
            price_data,
        )
        all_leg_rows.extend(leg_rows)
        all_purchase_rows.extend(purchase_rows)
        by_vessel.append(vessel_summary)

    total_consumption = sum(float(row["total_consumption"]) for row in by_vessel)
    model_purchase_qty = sum(float(row["model_purchase_qty"]) for row in by_vessel)
    model_external_qty = sum(float(row["model_external_qty"]) for row in by_vessel)
    priced_cost = sum(float(row["priced_cost"]) for row in by_vessel)
    external_cost = sum(float(row["external_cost"]) for row in by_vessel)
    total_model_cost = sum(float(row["total_model_cost"]) for row in by_vessel)
    priced_leg_count = sum(int(row["priced_leg_count"]) for row in by_vessel)
    purchased_leg_count = sum(int(row["purchased_leg_count"]) for row in by_vessel)
    purchase_price_sources: dict[str, int] = {}
    for row in all_purchase_rows:
        source = str(row["price_source"])
        purchase_price_sources[source] = purchase_price_sources.get(source, 0) + 1

    summary = {
        "model_version": "operational_route_inventory",
        "method": "lineær kostnadsminimering med scipy.optimize.linprog",
        "external_price_multiplier": external_price_multiplier,
        "external_price": round(price_data.external_price, 6),
        "port_average_prices": {
            port: round(price, 6)
            for port, price in sorted(price_data.port_average_prices.items())
        },
        "vessel_file_count": len(by_vessel),
        "leg_count": len(all_leg_rows),
        "priced_leg_count": priced_leg_count,
        "purchased_leg_count": purchased_leg_count,
        "total_consumption": round(total_consumption, 6),
        "model_purchase_qty": round(model_purchase_qty, 6),
        "model_external_qty": round(model_external_qty, 6),
        "external_share_of_consumption": round(model_external_qty / total_consumption, 6)
        if total_consumption
        else 0.0,
        "priced_share_of_consumption": round(model_purchase_qty / total_consumption, 6)
        if total_consumption
        else 0.0,
        "priced_cost": round(priced_cost, 2),
        "external_cost": round(external_cost, 2),
        "total_model_cost": round(total_model_cost, 2),
        "purchase_price_sources": purchase_price_sources,
        "input_files": {
            "legs": str(LEGS_CSV.relative_to(ROOT)).replace("\\", "/"),
            "capacity": str(CAPACITY_CSV.relative_to(ROOT)).replace("\\", "/"),
            "prices": str(PRICE_CSV.relative_to(ROOT)).replace("\\", "/"),
        },
        "output_files": {
            "summary": str(SUMMARY_JSON.relative_to(ROOT)).replace("\\", "/"),
            "by_vessel": str(BY_VESSEL_CSV.relative_to(ROOT)).replace("\\", "/"),
            "by_leg": str(BY_LEG_CSV.relative_to(ROOT)).replace("\\", "/"),
            "purchases": str(PURCHASES_CSV.relative_to(ROOT)).replace("\\", "/"),
            "sensitivity": str(SENSITIVITY_CSV.relative_to(ROOT)).replace("\\", "/"),
            "metadata": str(SUMMARY_MD.relative_to(ROOT)).replace("\\", "/"),
        },
        "assumptions": [
            "Eksakt månedlig pris brukes først for P001-P004.",
            "Historisk havnesnitt brukes som prisproxy for P001-P004 når eksakt månedspris mangler.",
            "Havner utenfor P001-P004 får ikke egen estimert pris.",
            "Ekstern/ukjent bunkring kostnadssettes med konservativ out-of-network proxypris.",
            "ROB_Fuel_Total behandles som relevant totalbeholdning.",
            "Oppgitt bunkerskapasitet brukes som øvre beholdningsgrense.",
        ],
    }
    return all_leg_rows, all_purchase_rows, by_vessel, summary


def build_sensitivity_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for multiplier in SENSITIVITY_MULTIPLIERS:
        _, _, _, summary = run_model(multiplier)
        rows.append(
            {
                "external_price_multiplier": multiplier,
                "external_price": summary["external_price"],
                "total_model_cost": summary["total_model_cost"],
                "priced_cost": summary["priced_cost"],
                "external_cost": summary["external_cost"],
                "model_purchase_qty": summary["model_purchase_qty"],
                "model_external_qty": summary["model_external_qty"],
                "external_share_of_consumption": summary["external_share_of_consumption"],
            }
        )
    return rows


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    all_leg_rows, all_purchase_rows, by_vessel, summary = run_model(
        DEFAULT_EXTERNAL_PRICE_MULTIPLIER
    )
    sensitivity_rows = build_sensitivity_rows()

    write_csv(BY_LEG_CSV, all_leg_rows)
    write_csv(PURCHASES_CSV, all_purchase_rows)
    write_csv(BY_VESSEL_CSV, by_vessel)
    write_csv(SENSITIVITY_CSV, sensitivity_rows)
    SUMMARY_JSON.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_summary_md(summary, by_vessel)

    print("Operasjonell hovedmodell er kjørt.")
    print(f"Fartøyfiler: {summary['vessel_file_count']}")
    print(f"Etapper: {summary['leg_count']}")
    print(f"Etapper med priset havn: {summary['priced_leg_count']}")
    print(f"Etapper med kjøp i priset havn: {summary['purchased_leg_count']}")
    print(f"Ekstern/ukjent bunkring: {summary['model_external_qty']:.2f}")
    print(f"Total modellkostnad: {summary['total_model_cost']:.2f}")
    print(f"Oppsummering: {SUMMARY_JSON}")


if __name__ == "__main__":
    main()
