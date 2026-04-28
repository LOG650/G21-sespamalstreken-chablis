from __future__ import annotations

import csv
import json
from collections import defaultdict
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
BASELINE_MONTH_CSV = OUTPUT_DIR / "res_baseline_model_v1_by_month.csv"
BASELINE_PORT_CSV = OUTPUT_DIR / "res_baseline_model_v1_by_port.csv"
BASELINE_SUMMARY_JSON = OUTPUT_DIR / "res_baseline_model_v1_summary.json"
BASELINE_SUMMARY_MD = METADATA_DIR / "res_baseline_model_v1_summary.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_parameters() -> dict[str, object]:
    return json.loads(PARAMETERS_JSON.read_text(encoding="utf-8"))


def load_price_lookup() -> dict[tuple[str, str], dict[str, object]]:
    lookup: dict[tuple[str, str], dict[str, object]] = {}
    for row in read_csv(PRICE_CSV):
        key = (row["delivery_month"], row["port"])
        lookup[key] = {
            "price": float(row["price_value"]),
            "source": row["price_source"],
        }
    return lookup


def load_availability_lookup() -> dict[tuple[str, str], int]:
    return {
        (row["delivery_month"], row["port"]): int(row["available_flag"])
        for row in read_csv(AVAILABILITY_CSV)
    }


def load_demand_lookup() -> dict[str, dict[str, object]]:
    return {
        row["delivery_month"]: {
            "demand_qty": float(row["demand_qty"]),
            "observed_port_count": int(row["observed_port_count"]),
        }
        for row in read_csv(DEMAND_CSV)
    }


def load_historical_monthly_costs() -> dict[str, float]:
    costs: dict[str, float] = defaultdict(float)
    for row in read_csv(MONTHLY_BY_PORT_CSV):
        month = row["delivery_month"]
        qty = float(row["total_qty"])
        price = float(row["weighted_avg_price"])
        costs[month] += qty * price
    return dict(costs)


def run_baseline() -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    parameters = load_parameters()
    ports = list(parameters["sets"]["ports"])
    months = list(parameters["sets"]["months"])
    price_lookup = load_price_lookup()
    availability_lookup = load_availability_lookup()
    demand_lookup = load_demand_lookup()
    historical_costs = load_historical_monthly_costs()

    month_rows: list[dict[str, object]] = []
    historical_total_unrounded = 0.0
    model_total_unrounded = 0.0
    by_port: dict[str, dict[str, float]] = {
        port: {"selected_months": 0, "solution_qty": 0.0, "solution_cost": 0.0}
        for port in ports
    }

    for month in months:
        demand = float(demand_lookup[month]["demand_qty"])
        candidates: list[dict[str, object]] = []

        for port in ports:
            if availability_lookup.get((month, port), 0) != 1:
                continue
            price_info = price_lookup[(month, port)]
            candidates.append(
                {
                    "port": port,
                    "price": float(price_info["price"]),
                    "price_source": str(price_info["source"]),
                }
            )

        if not candidates:
            raise RuntimeError(f"Mangler tilgjengelig havn for {month}")

        selected = min(candidates, key=lambda item: (float(item["price"]), str(item["port"])))
        selected_port = str(selected["port"])
        selected_price = float(selected["price"])
        model_cost = demand * selected_price
        historical_cost = historical_costs[month]
        saving = historical_cost - model_cost
        historical_total_unrounded += historical_cost
        model_total_unrounded += model_cost

        by_port[selected_port]["selected_months"] += 1
        by_port[selected_port]["solution_qty"] += demand
        by_port[selected_port]["solution_cost"] += model_cost

        month_rows.append(
            {
                "delivery_month": month,
                "selected_port": selected_port,
                "demand_qty": round(demand, 2),
                "selected_price": round(selected_price, 2),
                "selected_price_source": selected["price_source"],
                "available_port_count": len(candidates),
                "historical_cost": round(historical_cost, 2),
                "baseline_model_cost": round(model_cost, 2),
                "estimated_saving": round(saving, 2),
                "estimated_saving_pct": round((saving / historical_cost) * 100, 2)
                if historical_cost
                else 0.0,
            }
        )

    port_rows = [
        {
            "port": port,
            "selected_months": int(values["selected_months"]),
            "solution_qty": round(values["solution_qty"], 2),
            "solution_cost": round(values["solution_cost"], 2),
        }
        for port, values in sorted(by_port.items())
    ]

    historical_total = historical_total_unrounded
    model_total = model_total_unrounded
    saving_total = historical_total - model_total
    summary = {
        "model_version": "v1",
        "scenario": "baseline",
        "method": "solver-uavhengig simulering: månedlig behov legges til billigste tilgjengelige havn",
        "months": len(month_rows),
        "ports": ports,
        "historical_total_cost": round(historical_total, 2),
        "baseline_model_total_cost": round(model_total, 2),
        "estimated_total_saving": round(saving_total, 2),
        "estimated_total_saving_pct": round((saving_total / historical_total) * 100, 2)
        if historical_total
        else 0.0,
        "selected_months_by_port": {
            row["port"]: row["selected_months"] for row in port_rows
        },
        "input_files": {
            "prices": str(PRICE_CSV.relative_to(ROOT)).replace("\\", "/"),
            "demand": str(DEMAND_CSV.relative_to(ROOT)).replace("\\", "/"),
            "availability": str(AVAILABILITY_CSV.relative_to(ROOT)).replace("\\", "/"),
            "historical_costs": str(MONTHLY_BY_PORT_CSV.relative_to(ROOT)).replace("\\", "/"),
        },
        "output_files": {
            "monthly": str(BASELINE_MONTH_CSV.relative_to(ROOT)).replace("\\", "/"),
            "by_port": str(BASELINE_PORT_CSV.relative_to(ROOT)).replace("\\", "/"),
            "summary": str(BASELINE_SUMMARY_JSON.relative_to(ROOT)).replace("\\", "/"),
        },
    }
    return month_rows, port_rows, summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_summary_md(summary: dict[str, object]) -> None:
    selected = summary["selected_months_by_port"]
    lines = [
        "# Basiskjøring for modellen",
        "",
        "Basiskjøringen bruker samme solver-uavhengige beslutningslogikk som modelltesten: for hver måned legges observert månedlig behov til billigste tilgjengelige havn i modellgrunnlaget.",
        "",
        "## Resultat",
        "",
        f"- Antall måneder: {summary['months']}",
        f"- Havnene i modellgrunnlaget: {', '.join(summary['ports'])}",
        f"- Historisk kostnad i modellgrunnlaget: {summary['historical_total_cost']:,.2f}",
        f"- Beregnet kostnad i basiskjøring: {summary['baseline_model_total_cost']:,.2f}",
        f"- Estimert differanse mot historisk praksis: {summary['estimated_total_saving']:,.2f}",
        f"- Estimert differanse i prosent: {summary['estimated_total_saving_pct']:.2f} %",
        "",
        "## Valgt havn per antall måneder",
        "",
        "| Havn | Antall måneder valgt |",
        "| --- | ---: |",
    ]
    for port, count in selected.items():
        lines.append(f"| {port} | {count} |")

    lines.extend(
        [
            "",
            "## Filer",
            "",
            f"- `{summary['output_files']['monthly']}`",
            f"- `{summary['output_files']['by_port']}`",
            f"- `{summary['output_files']['summary']}`",
            "",
            "## Tolkning",
            "",
            "Basiskjøringen er et kontrollert standardscenario for modellen. Resultatene skal brukes videre som sammenligningsgrunnlag i sensitivitetsanalysen og senere resultattolkning.",
        ]
    )
    BASELINE_SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    month_rows, port_rows, summary = run_baseline()
    write_csv(BASELINE_MONTH_CSV, month_rows)
    write_csv(BASELINE_PORT_CSV, port_rows)
    BASELINE_SUMMARY_JSON.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_summary_md(summary)

    print("Basiskjøring gjennomført.")
    print(f"Historisk kostnad: {summary['historical_total_cost']:.2f}")
    print(f"Basiskostnad: {summary['baseline_model_total_cost']:.2f}")
    print(f"Estimert differanse: {summary['estimated_total_saving']:.2f}")
    print(f"Output: {BASELINE_MONTH_CSV}")


if __name__ == "__main__":
    main()
