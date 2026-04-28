from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ACTIVITY_DIR = Path(__file__).resolve().parent.parent

MODEL_INPUT_DIR = (
    ROOT / "006 analysis" / "02_modellutvikling" / "04_implementere_modell" / "input"
)
STRUCTURED_DATA_DIR = (
    ROOT / "006 analysis" / "01_datagrunnlag" / "03_strukturering_av_datasett" / "data"
)

PRICE_CSV = MODEL_INPUT_DIR / "tab_model_v1_price_by_port_month.csv"
DEMAND_CSV = MODEL_INPUT_DIR / "tab_model_v1_demand_by_month.csv"
AVAILABILITY_CSV = MODEL_INPUT_DIR / "tab_model_v1_availability_by_port_month.csv"
PARAMETERS_JSON = MODEL_INPUT_DIR / "data_model_v1_parameters.json"
MONTHLY_BY_PORT_CSV = STRUCTURED_DATA_DIR / "tab_bunker_monthly_by_port.csv"

OUTPUT_DIR = ACTIVITY_DIR / "output"
METADATA_DIR = ACTIVITY_DIR / "metadata"
SCENARIO_CSV = OUTPUT_DIR / "res_sensitivity_model_scenarios.csv"
MONTH_CSV = OUTPUT_DIR / "res_sensitivity_model_by_month.csv"
SUMMARY_JSON = OUTPUT_DIR / "res_sensitivity_model_summary.json"
SUMMARY_MD = METADATA_DIR / "res_sensitivity_model_summary.md"


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    scenario_type: str
    description: str
    changed_port: str
    price_multiplier: float
    demand_multiplier: float
    price_multiplier_by_port: dict[str, float]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_parameters() -> dict[str, object]:
    return json.loads(PARAMETERS_JSON.read_text(encoding="utf-8"))


def load_price_lookup() -> dict[tuple[str, str], dict[str, object]]:
    lookup: dict[tuple[str, str], dict[str, object]] = {}
    for row in read_csv(PRICE_CSV):
        lookup[(row["delivery_month"], row["port"])] = {
            "price": float(row["price_value"]),
            "source": row["price_source"],
        }
    return lookup


def load_availability_lookup() -> dict[tuple[str, str], int]:
    return {
        (row["delivery_month"], row["port"]): int(row["available_flag"])
        for row in read_csv(AVAILABILITY_CSV)
    }


def load_demand_lookup() -> dict[str, float]:
    return {
        row["delivery_month"]: float(row["demand_qty"])
        for row in read_csv(DEMAND_CSV)
    }


def load_historical_monthly_costs() -> dict[str, float]:
    costs: dict[str, float] = defaultdict(float)
    for row in read_csv(MONTHLY_BY_PORT_CSV):
        month = row["delivery_month"]
        costs[month] += float(row["total_qty"]) * float(row["weighted_avg_price"])
    return dict(costs)


def format_port_counts(counter: Counter[str], ports: list[str]) -> str:
    return "; ".join(f"{port}:{counter.get(port, 0)}" for port in ports)


def scenario_definitions(ports: list[str]) -> list[Scenario]:
    scenarios = [
        Scenario("baseline", "baseline", "Opprinnelig pris og etterspørsel", "all", 1.0, 1.0, {}),
    ]

    for pct, multiplier in [(-10, 0.90), (-5, 0.95), (5, 1.05), (10, 1.10)]:
        scenarios.append(
            Scenario(
                f"price_all_{pct:+d}pct",
                "price_all",
                f"Alle havnepriser {pct:+d} %",
                "all",
                multiplier,
                1.0,
                {},
            )
        )

    for port in ports:
        for pct, multiplier in [(-10, 0.90), (10, 1.10)]:
            scenarios.append(
                Scenario(
                    f"price_{port}_{pct:+d}pct",
                    "price_port",
                    f"Pris i {port} {pct:+d} %",
                    port,
                    multiplier,
                    1.0,
                    {port: multiplier},
                )
            )

    for pct, multiplier in [(-10, 0.90), (-5, 0.95), (5, 1.05), (10, 1.10)]:
        scenarios.append(
            Scenario(
                f"demand_all_{pct:+d}pct",
                "demand_all",
                f"Etterspørsel {pct:+d} %",
                "all",
                1.0,
                multiplier,
                {},
            )
        )

    scenarios.extend(
        [
            Scenario(
                "stress_price_demand_+10pct",
                "combined_stress",
                "Pris og etterspørsel +10 %",
                "all",
                1.10,
                1.10,
                {},
            ),
            Scenario(
                "stress_price_demand_-10pct",
                "combined_stress",
                "Pris og etterspørsel -10 %",
                "all",
                0.90,
                0.90,
                {},
            ),
        ]
    )
    return scenarios


def adjusted_price(base_price: float, scenario: Scenario, port: str) -> float:
    if port in scenario.price_multiplier_by_port:
        return base_price * scenario.price_multiplier_by_port[port]
    if scenario.price_multiplier_by_port:
        return base_price
    return base_price * scenario.price_multiplier


def run_scenario(
    scenario: Scenario,
    months: list[str],
    ports: list[str],
    price_lookup: dict[tuple[str, str], dict[str, object]],
    availability_lookup: dict[tuple[str, str], int],
    demand_lookup: dict[str, float],
    historical_costs: dict[str, float],
    baseline_month_costs: dict[str, float],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    month_rows: list[dict[str, object]] = []
    selected_counter: Counter[str] = Counter()
    total_cost = 0.0
    historical_total = 0.0

    for month in months:
        demand = demand_lookup[month] * scenario.demand_multiplier
        candidates: list[dict[str, object]] = []

        for port in ports:
            if availability_lookup.get((month, port), 0) != 1:
                continue
            base_price = float(price_lookup[(month, port)]["price"])
            scenario_price = adjusted_price(base_price, scenario, port)
            candidates.append(
                {
                    "port": port,
                    "base_price": base_price,
                    "scenario_price": scenario_price,
                    "price_source": str(price_lookup[(month, port)]["source"]),
                }
            )

        if not candidates:
            raise RuntimeError(f"Mangler tilgjengelig havn for {month}")

        selected = min(candidates, key=lambda item: (float(item["scenario_price"]), str(item["port"])))
        selected_port = str(selected["port"])
        scenario_cost = demand * float(selected["scenario_price"])
        historical_cost = historical_costs[month]
        baseline_cost = baseline_month_costs.get(month, scenario_cost)

        total_cost += scenario_cost
        historical_total += historical_cost
        selected_counter[selected_port] += 1

        month_rows.append(
            {
                "scenario_id": scenario.scenario_id,
                "delivery_month": month,
                "selected_port": selected_port,
                "demand_qty": round(demand, 2),
                "selected_price": round(float(selected["scenario_price"]), 2),
                "base_price": round(float(selected["base_price"]), 2),
                "selected_price_source": selected["price_source"],
                "available_port_count": len(candidates),
                "scenario_cost": round(scenario_cost, 2),
                "baseline_model_cost": round(baseline_cost, 2),
                "delta_vs_baseline_month": round(scenario_cost - baseline_cost, 2),
            }
        )

    summary = {
        "scenario_id": scenario.scenario_id,
        "scenario_type": scenario.scenario_type,
        "description": scenario.description,
        "changed_port": scenario.changed_port,
        "price_multiplier": scenario.price_multiplier,
        "demand_multiplier": scenario.demand_multiplier,
        "total_cost": total_cost,
        "historical_total_cost": historical_total,
        "selected_months_by_port": dict(sorted(selected_counter.items())),
    }
    return month_rows, summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_summary_md(summary: dict[str, object]) -> None:
    top_increases = summary["largest_cost_increases"]
    top_decreases = summary["largest_cost_decreases"]
    lines = [
        "# Sensitivitetsanalyse for modellen",
        "",
        "Sensitivitetsanalysen bruker samme beslutningslogikk som basiskjøringen: månedlig behov legges til billigste tilgjengelige havn i modellgrunnlaget. Scenarioene endrer priser og/eller etterspørsel, mens tilgjengelighet og historisk sammenligningsgrunnlag holdes fast.",
        "",
        "## Referanse",
        "",
        f"- Antall måneder: {summary['months']}",
        f"- Havnene i modellgrunnlaget: {', '.join(summary['ports'])}",
        f"- Historisk kostnad: {summary['historical_total_cost']:,.2f}",
        f"- Basiskostnad modell: {summary['baseline_model_total_cost']:,.2f}",
        "",
        "## Største kostnadsøkninger mot basis",
        "",
        "| Scenario | Endring mot basis | Endring i prosent |",
        "| --- | ---: | ---: |",
    ]
    for row in top_increases:
        lines.append(
            f"| {row['scenario_id']} | {row['delta_vs_baseline']:,.2f} | {row['delta_pct_vs_baseline']:.2f} % |"
        )

    lines.extend(
        [
            "",
            "## Største kostnadsreduksjoner mot basis",
            "",
            "| Scenario | Endring mot basis | Endring i prosent |",
            "| --- | ---: | ---: |",
        ]
    )
    for row in top_decreases:
        lines.append(
            f"| {row['scenario_id']} | {row['delta_vs_baseline']:,.2f} | {row['delta_pct_vs_baseline']:.2f} % |"
        )

    lines.extend(
        [
            "",
            "## Filer",
            "",
            f"- `{summary['output_files']['scenarios']}`",
            f"- `{summary['output_files']['monthly']}`",
            f"- `{summary['output_files']['summary']}`",
        ]
    )
    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    parameters = load_parameters()
    ports = list(parameters["sets"]["ports"])
    months = list(parameters["sets"]["months"])
    price_lookup = load_price_lookup()
    availability_lookup = load_availability_lookup()
    demand_lookup = load_demand_lookup()
    historical_costs = load_historical_monthly_costs()

    baseline_month_costs: dict[str, float] = {}
    baseline_rows, baseline_summary = run_scenario(
        scenario_definitions(ports)[0],
        months,
        ports,
        price_lookup,
        availability_lookup,
        demand_lookup,
        historical_costs,
        {},
    )
    for row in baseline_rows:
        baseline_month_costs[str(row["delivery_month"])] = float(row["scenario_cost"])

    baseline_total = float(baseline_summary["total_cost"])
    historical_total = float(baseline_summary["historical_total_cost"])

    all_month_rows: list[dict[str, object]] = []
    scenario_rows: list[dict[str, object]] = []

    for scenario in scenario_definitions(ports):
        month_rows, scenario_summary = run_scenario(
            scenario,
            months,
            ports,
            price_lookup,
            availability_lookup,
            demand_lookup,
            historical_costs,
            baseline_month_costs,
        )
        all_month_rows.extend(month_rows)

        total_cost = float(scenario_summary["total_cost"])
        delta_vs_baseline = total_cost - baseline_total
        estimated_saving_vs_historical = historical_total - total_cost
        selected_counter = Counter(scenario_summary["selected_months_by_port"])

        scenario_rows.append(
            {
                "scenario_id": scenario.scenario_id,
                "scenario_type": scenario.scenario_type,
                "description": scenario.description,
                "changed_port": scenario.changed_port,
                "price_multiplier": scenario.price_multiplier,
                "demand_multiplier": scenario.demand_multiplier,
                "total_cost": round(total_cost, 2),
                "delta_vs_baseline": round(delta_vs_baseline, 2),
                "delta_pct_vs_baseline": round((delta_vs_baseline / baseline_total) * 100, 2)
                if baseline_total
                else 0.0,
                "estimated_saving_vs_historical": round(estimated_saving_vs_historical, 2),
                "estimated_saving_pct_vs_historical": round(
                    (estimated_saving_vs_historical / historical_total) * 100, 2
                )
                if historical_total
                else 0.0,
                "selected_months_by_port": format_port_counts(selected_counter, ports),
            }
        )

    scenario_rows_sorted = sorted(
        scenario_rows,
        key=lambda row: float(row["delta_vs_baseline"]),
        reverse=True,
    )
    summary = {
        "scenario": "sensitivity",
        "method": "solver-uavhengig simulering: månedlig behov legges til billigste tilgjengelige havn",
        "months": len(months),
        "ports": ports,
        "scenario_count": len(scenario_rows),
        "historical_total_cost": round(historical_total, 2),
        "baseline_model_total_cost": round(baseline_total, 2),
        "largest_cost_increases": scenario_rows_sorted[:5],
        "largest_cost_decreases": list(reversed(scenario_rows_sorted[-5:])),
        "input_files": {
            "prices": str(PRICE_CSV.relative_to(ROOT)).replace("\\", "/"),
            "demand": str(DEMAND_CSV.relative_to(ROOT)).replace("\\", "/"),
            "availability": str(AVAILABILITY_CSV.relative_to(ROOT)).replace("\\", "/"),
            "historical_costs": str(MONTHLY_BY_PORT_CSV.relative_to(ROOT)).replace("\\", "/"),
        },
        "output_files": {
            "scenarios": str(SCENARIO_CSV.relative_to(ROOT)).replace("\\", "/"),
            "monthly": str(MONTH_CSV.relative_to(ROOT)).replace("\\", "/"),
            "summary": str(SUMMARY_JSON.relative_to(ROOT)).replace("\\", "/"),
            "metadata": str(SUMMARY_MD.relative_to(ROOT)).replace("\\", "/"),
        },
    }

    write_csv(SCENARIO_CSV, scenario_rows)
    write_csv(MONTH_CSV, all_month_rows)
    SUMMARY_JSON.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_summary_md(summary)

    print("Sensitivitetsanalyse gjennomført.")
    print(f"Scenarioer: {len(scenario_rows)}")
    print(f"Basiskostnad modell: {baseline_total:.2f}")
    print(f"Output: {SCENARIO_CSV}")


if __name__ == "__main__":
    main()
