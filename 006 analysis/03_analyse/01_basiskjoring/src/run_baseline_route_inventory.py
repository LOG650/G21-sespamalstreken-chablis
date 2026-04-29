from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[4]
MODEL_OUTPUT_DIR = (
    ROOT / "006 analysis" / "02_modellutvikling" / "04_implementere_modell" / "output"
)
ACTIVITY_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ACTIVITY_DIR / "output"
METADATA_DIR = ACTIVITY_DIR / "metadata"
FIGURES_DIR = ACTIVITY_DIR / "figures"

MODEL_SUMMARY_JSON = MODEL_OUTPUT_DIR / "res_route_inventory_summary.json"
MODEL_BY_VESSEL_CSV = MODEL_OUTPUT_DIR / "res_route_inventory_by_vessel.csv"
MODEL_BY_LEG_CSV = MODEL_OUTPUT_DIR / "res_route_inventory_by_leg.csv"
MODEL_PURCHASES_CSV = MODEL_OUTPUT_DIR / "res_route_inventory_purchases.csv"

BASELINE_SUMMARY_JSON = OUTPUT_DIR / "res_baseline_route_inventory_summary.json"
BASELINE_BY_VESSEL_CSV = OUTPUT_DIR / "res_baseline_route_inventory_by_vessel.csv"
BASELINE_BY_PORT_CSV = OUTPUT_DIR / "res_baseline_route_inventory_by_port.csv"
BASELINE_BY_MONTH_CSV = OUTPUT_DIR / "res_baseline_route_inventory_by_month.csv"
BASELINE_SUMMARY_MD = METADATA_DIR / "res_baseline_route_inventory_summary.md"
BASELINE_MONTHLY_SPLIT_FIG = FIGURES_DIR / "fig_baseline_monthly_split.png"

COST_TOL = 0.05
QTY_TOL = 0.05
EXPECTED_EXTERNAL_PRICE_MULTIPLIER = 1.25


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"Kan ikke skrive tom baseline-tabell til `{relative(path)}`.")
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


def build_by_vessel(by_vessel: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in by_vessel:
        total_consumption = as_float(row, "total_consumption")
        rows.append(
            {
                "vessel_file_id": row["vessel_file_id"],
                "vessel_class": row["vessel_class"],
                "leg_count": int(row["leg_count"]),
                "priced_leg_count": int(row["priced_leg_count"]),
                "purchased_leg_count": int(row["purchased_leg_count"]),
                "total_consumption": rounded(total_consumption),
                "model_purchase_qty": rounded(as_float(row, "model_purchase_qty")),
                "model_external_qty": rounded(as_float(row, "model_external_qty")),
                "priced_share_of_consumption": rounded(
                    as_float(row, "priced_share_of_consumption"), 4
                ),
                "external_share_of_consumption": rounded(
                    as_float(row, "external_share_of_consumption"), 4
                ),
                "priced_cost": rounded(as_float(row, "priced_cost")),
                "external_cost": rounded(as_float(row, "external_cost")),
                "total_model_cost": rounded(as_float(row, "total_model_cost")),
            }
        )
    return rows


def build_by_port(
    purchases: list[dict[str, str]],
    model_ports: list[str],
) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, float]] = defaultdict(
        lambda: {"purchase_count": 0.0, "purchase_qty": 0.0, "priced_cost": 0.0}
    )
    for row in purchases:
        if "port" not in row:
            raise ValueError(f"`{relative(MODEL_PURCHASES_CSV)}` mangler kolonnen `port`.")
        values = grouped[row["port"]]
        values["purchase_count"] += 1
        values["purchase_qty"] += as_float(row, "purchase_qty")
        values["priced_cost"] += as_float(row, "priced_cost")

    rows: list[dict[str, object]] = []
    for port in sorted(model_ports):
        values = grouped[port]
        purchase_qty = values["purchase_qty"]
        priced_cost = values["priced_cost"]
        rows.append(
            {
                "port": port,
                "purchase_count": int(values["purchase_count"]),
                "purchase_qty": rounded(purchase_qty),
                "priced_cost": rounded(priced_cost),
                "weighted_avg_actual_purchase_price": rounded(priced_cost / purchase_qty)
                if purchase_qty
                else 0.0,
            }
        )
    return rows


def build_by_month(
    by_leg: list[dict[str, str]],
    purchases: list[dict[str, str]],
) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, float]] = defaultdict(
        lambda: {
            "leg_count": 0.0,
            "priced_leg_count": 0.0,
            "purchased_leg_count": 0.0,
            "total_consumption": 0.0,
            "model_purchase_qty": 0.0,
            "model_external_qty": 0.0,
            "external_cost": 0.0,
            "priced_cost": 0.0,
        }
    )
    for row in by_leg:
        month = row["period_month"]
        values = grouped[month]
        purchase_qty = as_float(row, "model_purchase_qty")
        values["leg_count"] += 1
        if row["available_priced_ports"]:
            values["priced_leg_count"] += 1
        if purchase_qty > 1e-6:
            values["purchased_leg_count"] += 1
        values["total_consumption"] += as_float(row, "consumption")
        values["model_purchase_qty"] += purchase_qty
        values["model_external_qty"] += as_float(row, "model_external_qty")
        values["external_cost"] += as_float(row, "model_external_cost")

    for row in purchases:
        grouped[row["period_month"]]["priced_cost"] += as_float(row, "priced_cost")

    rows: list[dict[str, object]] = []
    for month, values in sorted(grouped.items()):
        priced_cost = values["priced_cost"]
        external_cost = values["external_cost"]
        rows.append(
            {
                "period_month": month,
                "leg_count": int(values["leg_count"]),
                "priced_leg_count": int(values["priced_leg_count"]),
                "purchased_leg_count": int(values["purchased_leg_count"]),
                "total_consumption": rounded(values["total_consumption"]),
                "model_purchase_qty": rounded(values["model_purchase_qty"]),
                "model_external_qty": rounded(values["model_external_qty"]),
                "priced_cost": rounded(priced_cost),
                "external_cost": rounded(external_cost),
                "total_model_cost": rounded(priced_cost + external_cost),
            }
        )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> list[str]:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return lines


def write_summary_md(
    summary: dict[str, object],
    by_vessel: list[dict[str, object]],
    by_port: list[dict[str, object]],
    by_month: list[dict[str, object]],
    consistency_checks: list[dict[str, object]],
) -> None:
    lines = [
        "# Basiskjøring av operasjonell hovedmodell",
        "",
        "Basiskjøringen dokumenterer hovedscenarioet fra den operative rute- og beholdningsmodellen. Scenarioet bruker ekstern proxyfaktor 1,25 og resultatfilene fra `04_implementere_modell` som kilde.",
        "",
        "## Nøkkeltall",
        "",
        f"- Fartøyfiler: {summary['vessel_file_count']}",
        f"- Etapper: {summary['leg_count']}",
        f"- Etapper med priset modellhavn tilgjengelig: {summary['priced_leg_count']}",
        f"- Etapper med modellert kjøp i priset modellhavn: {summary['purchased_leg_count']}",
        f"- Samlet forbruk: {summary['total_consumption']:,.2f}",
        f"- Modellert kjøp i prisede havner: {summary['model_purchase_qty']:,.2f}",
        f"- Ekstern/ukjent bunkring: {summary['model_external_qty']:,.2f}",
        f"- Kostnad i prisede havner: {summary['priced_cost']:,.2f}",
        f"- Kostnad for ekstern/ukjent bunkring: {summary['external_cost']:,.2f}",
        f"- Total modellkostnad: {summary['total_model_cost']:,.2f}",
        "",
        "## Per fartøyfil",
        "",
    ]
    lines.extend(
        markdown_table(
            by_vessel,
            [
                "vessel_file_id",
                "vessel_class",
                "leg_count",
                "priced_leg_count",
                "purchased_leg_count",
                "total_consumption",
                "model_purchase_qty",
                "model_external_qty",
                "priced_share_of_consumption",
                "external_share_of_consumption",
                "total_model_cost",
            ],
        )
    )
    lines.extend(["", "## Per modellhavn", ""])
    lines.extend(
        markdown_table(
            by_port,
            [
                "port",
                "purchase_count",
                "purchase_qty",
                "priced_cost",
                "weighted_avg_actual_purchase_price",
            ],
        )
    )
    lines.extend(["", "## Per måned", ""])
    lines.extend(
        markdown_table(
            by_month,
            [
                "period_month",
                "leg_count",
                "priced_leg_count",
                "purchased_leg_count",
                "model_purchase_qty",
                "model_external_qty",
                "total_model_cost",
            ],
        )
    )
    lines.extend(["", "## Konsistenssjekker", ""])
    lines.extend(markdown_table(consistency_checks, ["check", "status", "value", "expected"]))
    BASELINE_SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_consistency_checks(
    summary: dict[str, object],
    by_vessel: list[dict[str, object]],
    by_port: list[dict[str, object]],
    by_month: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check": "Basiskjøring bruker hovedscenarioets proxyfaktor",
            "value": float(summary["external_price_multiplier"]),
            "expected": EXPECTED_EXTERNAL_PRICE_MULTIPLIER,
            "tolerance": 1e-9,
        },
        {
            "check": "Kostnad i prisede havner per havn stemmer med sammendrag",
            "value": round(sum(float(row["priced_cost"]) for row in by_port), 2),
            "expected": summary["priced_cost"],
            "tolerance": COST_TOL,
        },
        {
            "check": "Total modellkostnad per fartøy stemmer med sammendrag",
            "value": round(sum(float(row["total_model_cost"]) for row in by_vessel), 2),
            "expected": summary["total_model_cost"],
            "tolerance": COST_TOL,
        },
        {
            "check": "Kjøpsmengde per måned stemmer med sammendrag",
            "value": round(sum(float(row["model_purchase_qty"]) for row in by_month), 2),
            "expected": round(float(summary["model_purchase_qty"]), 2),
            "tolerance": QTY_TOL,
        },
    ]
    result: list[dict[str, object]] = []
    for check in checks:
        passed = close_enough(
            float(check["value"]),
            float(check["expected"]),
            float(check["tolerance"]),
        )
        result.append(
            {
                "check": check["check"],
                "status": "OK" if passed else "FEIL",
                "value": check["value"],
                "expected": check["expected"],
            }
        )
        if not passed:
            raise RuntimeError(
                f"Konsistenssjekk feilet: {check['check']} "
                f"({check['value']} != {check['expected']})"
            )
    return result


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


def write_monthly_split_figure(by_month: list[dict[str, object]]) -> None:
    months = [str(row["period_month"]) for row in by_month]
    priced_qty = [float(row["model_purchase_qty"]) for row in by_month]
    external_qty = [float(row["model_external_qty"]) for row in by_month]

    plt.figure(figsize=(10, 5))
    plt.plot(months, priced_qty, marker="o", label="Kjøp i prisede havner")
    plt.plot(months, external_qty, marker="o", label="Ekstern/ukjent bunkring")
    plt.title("Basiskjøring: månedlig fordeling av bunkring")
    plt.xlabel("Måned")
    plt.ylabel("Mengde")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(BASELINE_MONTHLY_SPLIT_FIG, dpi=160)
    plt.close()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    summary = json.loads(MODEL_SUMMARY_JSON.read_text(encoding="utf-8"))
    if not close_enough(
        float(summary["external_price_multiplier"]),
        EXPECTED_EXTERNAL_PRICE_MULTIPLIER,
        1e-9,
    ):
        raise RuntimeError(
            "Basiskjøringen skal bygge på hovedscenarioet med "
            f"external_price_multiplier={EXPECTED_EXTERNAL_PRICE_MULTIPLIER}, "
            f"men modellsummary har {summary['external_price_multiplier']}."
        )
    by_vessel_source = read_csv(MODEL_BY_VESSEL_CSV)
    by_leg_source = read_csv(MODEL_BY_LEG_CSV)
    purchases_source = read_csv(MODEL_PURCHASES_CSV)
    require_columns(
        by_vessel_source,
        {
            "vessel_file_id",
            "vessel_class",
            "leg_count",
            "priced_leg_count",
            "purchased_leg_count",
            "total_consumption",
            "model_purchase_qty",
            "model_external_qty",
            "priced_share_of_consumption",
            "external_share_of_consumption",
            "priced_cost",
            "external_cost",
            "total_model_cost",
        },
        MODEL_BY_VESSEL_CSV,
    )
    require_columns(
        by_leg_source,
        {
            "period_month",
            "available_priced_ports",
            "consumption",
            "model_purchase_qty",
            "model_external_qty",
            "model_external_cost",
        },
        MODEL_BY_LEG_CSV,
    )
    require_columns(
        purchases_source,
        {"period_month", "port", "purchase_qty", "priced_cost"},
        MODEL_PURCHASES_CSV,
    )

    by_vessel = build_by_vessel(by_vessel_source)
    model_ports = sorted(summary["port_average_prices"].keys())
    by_port = build_by_port(purchases_source, model_ports)
    by_month = build_by_month(by_leg_source, purchases_source)
    consistency_checks = build_consistency_checks(summary, by_vessel, by_port, by_month)

    baseline_summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "baseline_name": "operational_route_inventory_main_scenario",
        "external_price_multiplier": summary["external_price_multiplier"],
        "external_price": summary["external_price"],
        "vessel_file_count": summary["vessel_file_count"],
        "leg_count": summary["leg_count"],
        "priced_leg_count": summary["priced_leg_count"],
        "purchased_leg_count": summary["purchased_leg_count"],
        "total_consumption": summary["total_consumption"],
        "model_purchase_qty": summary["model_purchase_qty"],
        "model_external_qty": summary["model_external_qty"],
        "priced_share_of_consumption": summary["priced_share_of_consumption"],
        "external_share_of_consumption": summary["external_share_of_consumption"],
        "priced_cost": summary["priced_cost"],
        "external_cost": summary["external_cost"],
        "total_model_cost": summary["total_model_cost"],
        "source_files": {
            "summary": file_metadata(MODEL_SUMMARY_JSON),
            "by_vessel": file_metadata(MODEL_BY_VESSEL_CSV),
            "by_leg": file_metadata(MODEL_BY_LEG_CSV),
            "purchases": file_metadata(MODEL_PURCHASES_CSV),
        },
        "output_files": {
            "summary": relative(BASELINE_SUMMARY_JSON),
            "by_vessel": relative(BASELINE_BY_VESSEL_CSV),
            "by_port": relative(BASELINE_BY_PORT_CSV),
            "by_month": relative(BASELINE_BY_MONTH_CSV),
            "monthly_split_figure": relative(BASELINE_MONTHLY_SPLIT_FIG),
            "metadata": relative(BASELINE_SUMMARY_MD),
        },
        "consistency_checks": consistency_checks,
    }

    write_csv(BASELINE_BY_VESSEL_CSV, by_vessel)
    write_csv(BASELINE_BY_PORT_CSV, by_port)
    write_csv(BASELINE_BY_MONTH_CSV, by_month)
    write_monthly_split_figure(by_month)
    write_summary_md(baseline_summary, by_vessel, by_port, by_month, consistency_checks)
    BASELINE_SUMMARY_JSON.write_text(
        json.dumps(baseline_summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    output_file_checks = build_output_file_checks(
        [
            BASELINE_SUMMARY_JSON,
            BASELINE_BY_VESSEL_CSV,
            BASELINE_BY_PORT_CSV,
            BASELINE_BY_MONTH_CSV,
            BASELINE_MONTHLY_SPLIT_FIG,
            BASELINE_SUMMARY_MD,
        ]
    )
    all_checks = consistency_checks + output_file_checks
    baseline_summary["consistency_checks"] = all_checks
    BASELINE_SUMMARY_JSON.write_text(
        json.dumps(baseline_summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_summary_md(baseline_summary, by_vessel, by_port, by_month, all_checks)

    print("Basiskjøring er generert.")
    print(f"Etapper: {baseline_summary['leg_count']}")
    print(f"Modellert kjøp i prisede havner: {baseline_summary['model_purchase_qty']:.2f}")
    print(f"Ekstern/ukjent bunkring: {baseline_summary['model_external_qty']:.2f}")
    print(f"Total modellkostnad: {baseline_summary['total_model_cost']:.2f}")
    print(f"Oppsummering: {BASELINE_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
