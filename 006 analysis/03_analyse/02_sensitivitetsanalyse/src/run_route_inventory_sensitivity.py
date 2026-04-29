from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[4]
MODEL_OUTPUT_DIR = (
    ROOT / "006 analysis" / "02_modellutvikling" / "04_implementere_modell" / "output"
)
BASELINE_DIR = ROOT / "006 analysis" / "03_analyse" / "01_basiskjoring" / "output"
ACTIVITY_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ACTIVITY_DIR / "output"
METADATA_DIR = ACTIVITY_DIR / "metadata"
FIGURES_DIR = ACTIVITY_DIR / "figures"

MODEL_SENSITIVITY_CSV = MODEL_OUTPUT_DIR / "res_route_inventory_proxy_sensitivity.csv"
BASELINE_SUMMARY_JSON = BASELINE_DIR / "res_baseline_route_inventory_summary.json"

SENSITIVITY_SUMMARY_JSON = OUTPUT_DIR / "res_sensitivity_route_inventory_summary.json"
SENSITIVITY_SCENARIOS_CSV = OUTPUT_DIR / "res_sensitivity_route_inventory_scenarios.csv"
SENSITIVITY_SUMMARY_MD = METADATA_DIR / "res_sensitivity_route_inventory_summary.md"
FIG_TOTAL_COST = FIGURES_DIR / "fig_sensitivity_total_cost.png"
FIG_COST_COMPONENTS = FIGURES_DIR / "fig_sensitivity_cost_components.png"

EXPECTED_MULTIPLIERS = {1.10, 1.25, 1.50}
BASELINE_MULTIPLIER = 1.25
COST_TOL = 0.05
QTY_TOL = 0.05


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"Kan ikke skrive tom sensitivitetsfil til `{relative(path)}`.")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def as_float(row: dict[str, str], column: str) -> float:
    value = row.get(column)
    if value is None or value.strip() == "":
        return 0.0
    numeric_value = float(value)
    if math.isnan(numeric_value):
        raise ValueError(f"Kolonnen `{column}` inneholder NaN-verdi.")
    return numeric_value


def rounded(value: float, decimals: int = 2) -> float:
    return round(value, decimals)


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def file_metadata(path: Path) -> dict[str, object]:
    return {
        "path": relative(path),
        "mtime": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def close_enough(left: float, right: float, tolerance: float) -> bool:
    return abs(left - right) <= tolerance


def require_columns(rows: list[dict[str, str]], required_columns: set[str], source: Path) -> None:
    if not rows:
        raise ValueError(f"`{relative(source)}` er tom.")
    missing_columns = sorted(required_columns - set(rows[0].keys()))
    if missing_columns:
        raise ValueError(
            f"`{relative(source)}` mangler påkrevde kolonner: {', '.join(missing_columns)}"
        )


def require_summary_keys(
    summary: dict[str, object],
    required_keys: set[str],
    source: Path,
) -> None:
    missing_keys = sorted(required_keys - set(summary.keys()))
    if missing_keys:
        raise ValueError(
            f"`{relative(source)}` mangler påkrevde nøkler: {', '.join(missing_keys)}"
        )


def build_scenarios(
    sensitivity_rows: list[dict[str, str]],
    baseline_summary: dict[str, object],
) -> list[dict[str, object]]:
    require_summary_keys(
        baseline_summary,
        {"total_model_cost", "model_purchase_qty", "model_external_qty"},
        BASELINE_SUMMARY_JSON,
    )
    baseline_cost = float(baseline_summary["total_model_cost"])
    scenarios: list[dict[str, object]] = []
    for row in sorted(sensitivity_rows, key=lambda item: as_float(item, "external_price_multiplier")):
        total_model_cost = as_float(row, "total_model_cost")
        cost_change = total_model_cost - baseline_cost
        scenarios.append(
            {
                "external_price_multiplier": rounded(
                    as_float(row, "external_price_multiplier"), 2
                ),
                "external_price": rounded(as_float(row, "external_price"), 2),
                "total_model_cost": rounded(total_model_cost),
                "cost_change_vs_baseline": rounded(cost_change),
                "cost_change_pct_vs_baseline": rounded(cost_change / baseline_cost, 6),
                "priced_cost": rounded(as_float(row, "priced_cost")),
                "external_cost": rounded(as_float(row, "external_cost")),
                "model_purchase_qty": rounded(as_float(row, "model_purchase_qty"), 3),
                "model_external_qty": rounded(as_float(row, "model_external_qty"), 3),
                "external_share_of_consumption": rounded(
                    as_float(row, "external_share_of_consumption"), 6
                ),
            }
        )
    return scenarios


def build_checks(
    sensitivity_rows: list[dict[str, str]],
    scenarios: list[dict[str, object]],
    baseline_summary: dict[str, object],
) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    actual_multipliers = {
        round(as_float(row, "external_price_multiplier"), 2) for row in sensitivity_rows
    }
    checks.append(
        {
            "check": "Forventede proxyfaktorer finnes",
            "status": "OK" if actual_multipliers == EXPECTED_MULTIPLIERS else "FEIL",
            "value": sorted(actual_multipliers),
            "expected": sorted(EXPECTED_MULTIPLIERS),
        }
    )

    baseline_rows = [
        row
        for row in scenarios
        if close_enough(float(row["external_price_multiplier"]), BASELINE_MULTIPLIER, 1e-9)
    ]
    baseline_matches = (
        len(baseline_rows) == 1
        and close_enough(
            float(baseline_rows[0]["total_model_cost"]),
            float(baseline_summary["total_model_cost"]),
            COST_TOL,
        )
    )
    checks.append(
        {
            "check": "Basisscenario stemmer med basiskjøring",
            "status": "OK" if baseline_matches else "FEIL",
            "value": baseline_rows[0]["total_model_cost"] if baseline_rows else None,
            "expected": baseline_summary["total_model_cost"],
        }
    )

    cost_breaks = 0
    external_cost_breaks = 0
    quantity_breaks = 0
    baseline_purchase_qty = float(baseline_summary["model_purchase_qty"])
    baseline_external_qty = float(baseline_summary["model_external_qty"])
    for row in sensitivity_rows:
        if not close_enough(
            as_float(row, "priced_cost") + as_float(row, "external_cost"),
            as_float(row, "total_model_cost"),
            COST_TOL,
        ):
            cost_breaks += 1
        if not close_enough(
            as_float(row, "model_external_qty") * as_float(row, "external_price"),
            as_float(row, "external_cost"),
            COST_TOL,
        ):
            external_cost_breaks += 1
        if not close_enough(as_float(row, "model_purchase_qty"), baseline_purchase_qty, QTY_TOL):
            quantity_breaks += 1
        if not close_enough(as_float(row, "model_external_qty"), baseline_external_qty, QTY_TOL):
            quantity_breaks += 1

    checks.extend(
        [
            {
                "check": "Alle scenarioer har konsistent totalkostnad",
                "status": "OK" if cost_breaks == 0 else "FEIL",
                "value": cost_breaks,
                "expected": 0,
            },
            {
                "check": "Alle scenarioer har konsistent eksternkostnad",
                "status": "OK" if external_cost_breaks == 0 else "FEIL",
                "value": external_cost_breaks,
                "expected": 0,
            },
            {
                "check": "Kjøps- og eksternmengde er stabil på tvers av scenarioer",
                "status": "OK" if quantity_breaks == 0 else "FEIL",
                "value": quantity_breaks,
                "expected": 0,
            },
        ]
    )

    failed = [check for check in checks if check["status"] != "OK"]
    if failed:
        raise RuntimeError(f"Sensitivitetskontroller feilet: {failed}")
    return checks


def build_output_file_checks(paths: list[Path]) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    for path in paths:
        exists_with_content = path.exists() and path.stat().st_size > 0
        checks.append(
            {
                "check": f"Outputfil er skrevet: {relative(path)}",
                "status": "OK" if exists_with_content else "FEIL",
                "value": "skrevet" if exists_with_content else "mangler/tom",
                "expected": "skrevet",
            }
        )
        if not exists_with_content:
            raise RuntimeError(f"Outputfil mangler eller er tom: {relative(path)}")
    return checks


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> list[str]:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return lines


def write_figures(scenarios: list[dict[str, object]]) -> None:
    labels = [str(row["external_price_multiplier"]).replace(".", ",") for row in scenarios]
    total_costs = [float(row["total_model_cost"]) for row in scenarios]
    priced_costs = [float(row["priced_cost"]) for row in scenarios]
    external_costs = [float(row["external_cost"]) for row in scenarios]

    plt.figure(figsize=(8, 5))
    plt.plot(labels, total_costs, marker="o", color="#1f77b4")
    for label, total_cost in zip(labels, total_costs):
        plt.annotate(
            f"{total_cost / 1_000_000:.1f} mill.",
            (label, total_cost),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=9,
        )
    plt.title("Sensitivitet: total modellkostnad")
    plt.xlabel("Proxyfaktor for ekstern/ukjent bunkring")
    plt.ylabel("Total modellkostnad")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_TOTAL_COST, dpi=160)
    plt.close()

    x_positions = range(len(labels))
    plt.figure(figsize=(8, 5))
    plt.bar(x_positions, priced_costs, label="Kostnad i prisede havner", color="#4c78a8")
    plt.bar(
        x_positions,
        external_costs,
        bottom=priced_costs,
        label="Ekstern/ukjent kostnad",
        color="#f58518",
    )
    for index, (priced_cost, external_cost) in enumerate(zip(priced_costs, external_costs)):
        plt.annotate(
            f"{(priced_cost + external_cost) / 1_000_000:.1f} mill.",
            (index, priced_cost + external_cost),
            textcoords="offset points",
            xytext=(0, 4),
            ha="center",
            fontsize=9,
        )
    plt.title("Sensitivitet: kostnadskomponenter")
    plt.xlabel("Proxyfaktor for ekstern/ukjent bunkring")
    plt.ylabel("Modellkostnad")
    plt.xticks(list(x_positions), labels)
    plt.grid(axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_COST_COMPONENTS, dpi=160)
    plt.close()


def write_summary_md(
    summary: dict[str, object],
    scenarios: list[dict[str, object]],
    checks: list[dict[str, object]],
) -> None:
    lines = [
        "# Sensitivitetsanalyse for operasjonell hovedmodell",
        "",
        "Analysen viser hvordan total modellkostnad endres når proxykostnaden for ekstern/ukjent bunkring varierer. Basisscenarioet er proxyfaktor 1,25 og skal stemme med basiskjøringen.",
        "",
        "Dette er en smal én-veis proxysensitivitet. Kjøps- og eksternmengdene er stabile i alle tre scenarioer, slik at analysen primært dokumenterer kostnadseffekten av ekstern/ukjent proxypris, ikke endringer i anbefalt kjøpsplan.",
        "",
        "## Nøkkeltall",
        "",
        f"- Scenarioer: {summary['scenario_count']}",
        f"- Laveste total modellkostnad: {summary['min_total_model_cost']:,.2f}",
        f"- Høyeste total modellkostnad: {summary['max_total_model_cost']:,.2f}",
        f"- Kostnadsspenn: {summary['total_cost_range']:,.2f}",
        f"- Basisscenario total modellkostnad: {summary['baseline_total_model_cost']:,.2f}",
        "",
        "## Scenarioer",
        "",
    ]
    lines.extend(
        markdown_table(
            scenarios,
            [
                "external_price_multiplier",
                "external_price",
                "total_model_cost",
                "cost_change_vs_baseline",
                "cost_change_pct_vs_baseline",
                "priced_cost",
                "external_cost",
                "model_purchase_qty",
                "model_external_qty",
                "external_share_of_consumption",
            ],
        )
    )
    lines.extend(["", "## Kontroller", ""])
    lines.extend(markdown_table(checks, ["check", "status", "value", "expected"]))
    SENSITIVITY_SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    sensitivity_rows = read_csv(MODEL_SENSITIVITY_CSV)
    require_columns(
        sensitivity_rows,
        {
            "external_price_multiplier",
            "external_price",
            "total_model_cost",
            "priced_cost",
            "external_cost",
            "model_purchase_qty",
            "model_external_qty",
            "external_share_of_consumption",
        },
        MODEL_SENSITIVITY_CSV,
    )
    baseline_summary = json.loads(BASELINE_SUMMARY_JSON.read_text(encoding="utf-8"))

    scenarios = build_scenarios(sensitivity_rows, baseline_summary)
    checks = build_checks(sensitivity_rows, scenarios, baseline_summary)

    total_costs = [float(row["total_model_cost"]) for row in scenarios]
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "analysis_name": "route_inventory_proxy_sensitivity",
        "scenario_count": len(scenarios),
        "expected_multipliers": sorted(EXPECTED_MULTIPLIERS),
        "baseline_multiplier": BASELINE_MULTIPLIER,
        "baseline_total_model_cost": baseline_summary["total_model_cost"],
        "min_total_model_cost": min(total_costs),
        "max_total_model_cost": max(total_costs),
        "total_cost_range": max(total_costs) - min(total_costs),
        "source_files": {
            "model_sensitivity": file_metadata(MODEL_SENSITIVITY_CSV),
            "baseline_summary": file_metadata(BASELINE_SUMMARY_JSON),
        },
        "output_files": {
            "summary": relative(SENSITIVITY_SUMMARY_JSON),
            "scenarios": relative(SENSITIVITY_SCENARIOS_CSV),
            "metadata": relative(SENSITIVITY_SUMMARY_MD),
            "total_cost_figure": relative(FIG_TOTAL_COST),
            "cost_components_figure": relative(FIG_COST_COMPONENTS),
        },
        "checks": checks,
    }

    write_csv(SENSITIVITY_SCENARIOS_CSV, scenarios)
    write_figures(scenarios)
    write_summary_md(summary, scenarios, checks)
    SENSITIVITY_SUMMARY_JSON.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    output_checks = build_output_file_checks(
        [
            SENSITIVITY_SUMMARY_JSON,
            SENSITIVITY_SCENARIOS_CSV,
            SENSITIVITY_SUMMARY_MD,
            FIG_TOTAL_COST,
            FIG_COST_COMPONENTS,
        ]
    )
    all_checks = checks + output_checks
    summary["checks"] = all_checks
    SENSITIVITY_SUMMARY_JSON.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_summary_md(summary, scenarios, all_checks)

    print("Sensitivitetsanalyse er generert.")
    print(f"Scenarioer: {summary['scenario_count']}")
    print(f"Kostnadsspenn: {summary['total_cost_range']:.2f}")
    print(f"Oppsummering: {SENSITIVITY_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
