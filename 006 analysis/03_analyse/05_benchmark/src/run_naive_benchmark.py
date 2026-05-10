from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ACTIVITY_DIR = Path(__file__).resolve().parent.parent
STRUCTURED_DATA_DIR = (
    ROOT / "006 analysis" / "01_datagrunnlag" / "03_strukturering_av_datasett" / "data"
)
MODEL_OUTPUT_DIR = (
    ROOT / "006 analysis" / "02_modellutvikling" / "04_implementere_modell" / "output"
)

LEGS_CSV = STRUCTURED_DATA_DIR / "tab_voyage_legs_2025.csv"
CAPACITY_CSV = STRUCTURED_DATA_DIR / "tab_vessel_class_capacity.csv"
PRICE_CSV = STRUCTURED_DATA_DIR / "tab_bunker_monthly_by_port.csv"
MODEL_SUMMARY_JSON = MODEL_OUTPUT_DIR / "res_route_inventory_summary.json"

OUTPUT_DIR = ACTIVITY_DIR / "output"
METADATA_DIR = ACTIVITY_DIR / "metadata"
SUMMARY_JSON = OUTPUT_DIR / "res_naive_benchmark_summary.json"
BY_VESSEL_CSV = OUTPUT_DIR / "res_naive_benchmark_by_vessel.csv"
BY_LEG_CSV = OUTPUT_DIR / "res_naive_benchmark_by_leg.csv"
SUMMARY_MD = METADATA_DIR / "res_naive_benchmark_summary.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_capacities() -> dict[str, float]:
    return {
        row["vessel_class"]: float(row["bunker_capacity_m3"])
        for row in read_csv(CAPACITY_CSV)
    }


def load_price_data() -> tuple[dict[tuple[str, str], float], dict[str, float], float]:
    exact_prices: dict[tuple[str, str], float] = {}
    port_totals: dict[str, dict[str, float]] = {}
    for row in read_csv(PRICE_CSV):
        port = row["port"]
        month = row["delivery_month"]
        qty = float(row["total_qty"])
        price = float(row["weighted_avg_price"])
        exact_prices[(month, port)] = price
        port_totals.setdefault(port, {"qty": 0.0, "cost": 0.0})
        port_totals[port]["qty"] += qty
        port_totals[port]["cost"] += qty * price

    port_average_prices = {
        port: totals["cost"] / totals["qty"]
        for port, totals in port_totals.items()
        if totals["qty"] > 0
    }

    with MODEL_SUMMARY_JSON.open(encoding="utf-8") as handle:
        model_summary = json.load(handle)
    external_price = float(model_summary["external_price"])

    return exact_prices, port_average_prices, external_price


def available_priced_options(
    row: dict[str, str],
    exact_prices: dict[tuple[str, str], float],
    port_average_prices: dict[str, float],
) -> list[dict[str, object]]:
    options: list[dict[str, object]] = []
    month = row["period_month"]
    for port in sorted(port for port in row["available_ports_P00X"].split("|") if port):
        if port not in port_average_prices:
            continue
        exact_price = exact_prices.get((month, port))
        if exact_price is None:
            options.append(
                {
                    "port": port,
                    "price": port_average_prices[port],
                    "price_source": "historical_port_average",
                }
            )
        else:
            options.append(
                {
                    "port": port,
                    "price": exact_price,
                    "price_source": "monthly_observation",
                }
            )
    return sorted(options, key=lambda item: (float(item["price"]), str(item["port"])))


def run_benchmark() -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    capacities = load_capacities()
    exact_prices, port_average_prices, external_price = load_price_data()
    legs = sorted(
        read_csv(LEGS_CSV),
        key=lambda row: (row["vessel_file_id"], int(row["leg_sequence"])),
    )

    by_leg: list[dict[str, object]] = []
    by_vessel: list[dict[str, object]] = []

    grouped: dict[str, list[dict[str, str]]] = {}
    for row in legs:
        grouped.setdefault(row["vessel_file_id"], []).append(row)

    for vessel_file_id, vessel_legs in sorted(grouped.items()):
        vessel_class = vessel_legs[0]["vessel_class"]
        capacity = capacities[vessel_class]
        inventory = float(vessel_legs[0]["rob_start"])

        total_consumption = 0.0
        purchase_qty_total = 0.0
        external_qty_total = 0.0
        priced_cost_total = 0.0
        external_cost_total = 0.0
        priced_leg_count = 0
        purchased_leg_count = 0

        for leg in vessel_legs:
            consumption = float(leg["fuel_consumption_total"])
            total_consumption += consumption
            options = available_priced_options(leg, exact_prices, port_average_prices)
            priced_leg_count += 1 if options else 0

            purchase_qty = 0.0
            purchase_port = ""
            purchase_price = ""
            price_source = ""
            if options:
                cheapest = options[0]
                purchase_qty = max(capacity - inventory, 0.0)
                purchase_port = str(cheapest["port"])
                purchase_price = float(cheapest["price"])
                price_source = str(cheapest["price_source"])
                priced_cost_total += purchase_qty * purchase_price
                inventory += purchase_qty
                if purchase_qty > 1e-6:
                    purchased_leg_count += 1

            external_qty = 0.0
            if inventory < consumption:
                external_qty = consumption - inventory
                external_cost_total += external_qty * external_price
                inventory += external_qty

            inventory -= consumption
            purchase_qty_total += purchase_qty
            external_qty_total += external_qty

            by_leg.append(
                {
                    "vessel_file_id": vessel_file_id,
                    "vessel_class": vessel_class,
                    "leg_sequence": int(leg["leg_sequence"]),
                    "period_month": leg["period_month"],
                    "available_priced_ports": "|".join(str(option["port"]) for option in options),
                    "benchmark_purchase_port": purchase_port,
                    "benchmark_purchase_price": round(purchase_price, 2) if purchase_price != "" else "",
                    "benchmark_price_source": price_source,
                    "benchmark_purchase_qty": round(purchase_qty, 6),
                    "benchmark_external_qty": round(external_qty, 6),
                    "benchmark_inventory_end": round(inventory, 6),
                    "consumption": round(consumption, 6),
                    "capacity": round(capacity, 6),
                }
            )

        total_cost = priced_cost_total + external_cost_total
        by_vessel.append(
            {
                "vessel_file_id": vessel_file_id,
                "vessel_class": vessel_class,
                "leg_count": len(vessel_legs),
                "priced_leg_count": priced_leg_count,
                "purchased_leg_count": purchased_leg_count,
                "total_consumption": round(total_consumption, 6),
                "benchmark_purchase_qty": round(purchase_qty_total, 6),
                "benchmark_external_qty": round(external_qty_total, 6),
                "priced_share_of_consumption": round(purchase_qty_total / total_consumption, 6),
                "external_share_of_consumption": round(external_qty_total / total_consumption, 6),
                "priced_cost": round(priced_cost_total, 2),
                "external_cost": round(external_cost_total, 2),
                "total_benchmark_cost": round(total_cost, 2),
            }
        )

    total_consumption = sum(float(row["total_consumption"]) for row in by_vessel)
    purchase_qty = sum(float(row["benchmark_purchase_qty"]) for row in by_vessel)
    external_qty = sum(float(row["benchmark_external_qty"]) for row in by_vessel)
    priced_cost = sum(float(row["priced_cost"]) for row in by_vessel)
    external_cost = sum(float(row["external_cost"]) for row in by_vessel)
    total_benchmark_cost = priced_cost + external_cost

    with MODEL_SUMMARY_JSON.open(encoding="utf-8") as handle:
        model_summary = json.load(handle)

    model_cost = float(model_summary["total_model_cost"])
    summary = {
        "analysis_name": "naive_fill_to_capacity_benchmark",
        "benchmark_rule": "Fyll til kapasitet i billigste tilgjengelige prisede modellhavn på etappen. Dersom beholdning fortsatt ikke dekker forbruket, brukes ekstern/ukjent bunkring.",
        "external_price": external_price,
        "vessel_file_count": len(by_vessel),
        "leg_count": len(by_leg),
        "priced_leg_count": sum(int(row["priced_leg_count"]) for row in by_vessel),
        "purchased_leg_count": sum(int(row["purchased_leg_count"]) for row in by_vessel),
        "total_consumption": round(total_consumption, 6),
        "benchmark_purchase_qty": round(purchase_qty, 6),
        "benchmark_external_qty": round(external_qty, 6),
        "priced_share_of_consumption": round(purchase_qty / total_consumption, 6),
        "external_share_of_consumption": round(external_qty / total_consumption, 6),
        "priced_cost": round(priced_cost, 2),
        "external_cost": round(external_cost, 2),
        "total_benchmark_cost": round(total_benchmark_cost, 2),
        "model_total_cost": round(model_cost, 2),
        "cost_difference_benchmark_minus_model": round(total_benchmark_cost - model_cost, 2),
        "cost_difference_pct_of_benchmark": round(
            (total_benchmark_cost - model_cost) / total_benchmark_cost,
            6,
        )
        if total_benchmark_cost
        else 0.0,
        "source_files": {
            "voyage_legs": str(LEGS_CSV.relative_to(ROOT)).replace("\\", "/"),
            "capacity": str(CAPACITY_CSV.relative_to(ROOT)).replace("\\", "/"),
            "prices": str(PRICE_CSV.relative_to(ROOT)).replace("\\", "/"),
            "model_summary": str(MODEL_SUMMARY_JSON.relative_to(ROOT)).replace("\\", "/"),
        },
        "output_files": {
            "summary": str(SUMMARY_JSON.relative_to(ROOT)).replace("\\", "/"),
            "by_vessel": str(BY_VESSEL_CSV.relative_to(ROOT)).replace("\\", "/"),
            "by_leg": str(BY_LEG_CSV.relative_to(ROOT)).replace("\\", "/"),
            "metadata": str(SUMMARY_MD.relative_to(ROOT)).replace("\\", "/"),
        },
    }
    return by_leg, by_vessel, summary


def write_summary_md(summary: dict[str, object], by_vessel: list[dict[str, object]]) -> None:
    lines = [
        "# Naiv benchmark",
        "",
        str(summary["benchmark_rule"]),
        "",
        "Benchmarken er en enkel referanseregel, ikke en rekonstruksjon av faktisk Odfjell-praksis.",
        "",
        "## Hovedtall",
        "",
        f"- Total benchmarkkostnad: {summary['total_benchmark_cost']:,.2f}",
        f"- Total LP-kostnad: {summary['model_total_cost']:,.2f}",
        f"- Kostnadsforskjell benchmark minus LP: {summary['cost_difference_benchmark_minus_model']:,.2f}",
        f"- Kjøp i prisede havner: {summary['benchmark_purchase_qty']:,.2f}",
        f"- Ekstern/ukjent bunkring: {summary['benchmark_external_qty']:,.2f}",
        f"- Ekstern/ukjent andel: {summary['external_share_of_consumption']:.2%}",
        "",
        "## Per fartøyfil",
        "",
        "| Fartøyfil | Klasse | Etapper | Prisede etapper | Kjøp-etapper | Forbruk | Kjøp i prisede havner | Ekstern/ukjent | Total benchmarkkostnad |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in by_vessel:
        lines.append(
            "| {vessel_file_id} | {vessel_class} | {leg_count} | {priced_leg_count} | "
            "{purchased_leg_count} | {total_consumption:,.2f} | "
            "{benchmark_purchase_qty:,.2f} | {benchmark_external_qty:,.2f} | "
            "{total_benchmark_cost:,.2f} |".format(**row)
        )
    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    by_leg, by_vessel, summary = run_benchmark()
    write_csv(BY_LEG_CSV, by_leg)
    write_csv(BY_VESSEL_CSV, by_vessel)
    SUMMARY_JSON.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_summary_md(summary, by_vessel)

    print("Naiv benchmark er kjørt.")
    print(f"Total benchmarkkostnad: {summary['total_benchmark_cost']:.2f}")
    print(f"Kostnadsforskjell benchmark minus LP: {summary['cost_difference_benchmark_minus_model']:.2f}")


if __name__ == "__main__":
    main()
