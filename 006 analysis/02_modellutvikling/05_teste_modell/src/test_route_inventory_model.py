from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
MODEL_DIR = ROOT / "006 analysis" / "02_modellutvikling" / "04_implementere_modell"
STRUCTURED_DATA_DIR = (
    ROOT / "006 analysis" / "01_datagrunnlag" / "03_strukturering_av_datasett" / "data"
)
ACTIVITY_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ACTIVITY_DIR / "output"
METADATA_DIR = ACTIVITY_DIR / "metadata"

LEGS_CSV = STRUCTURED_DATA_DIR / "tab_voyage_legs_2025.csv"
CAPACITY_CSV = STRUCTURED_DATA_DIR / "tab_vessel_class_capacity.csv"
PRICE_CSV = STRUCTURED_DATA_DIR / "tab_bunker_monthly_by_port.csv"

SUMMARY_JSON = MODEL_DIR / "output" / "res_route_inventory_summary.json"
BY_VESSEL_CSV = MODEL_DIR / "output" / "res_route_inventory_by_vessel.csv"
BY_LEG_CSV = MODEL_DIR / "output" / "res_route_inventory_by_leg.csv"
PURCHASES_CSV = MODEL_DIR / "output" / "res_route_inventory_purchases.csv"
SENSITIVITY_CSV = MODEL_DIR / "output" / "res_route_inventory_proxy_sensitivity.csv"

TEST_JSON = OUTPUT_DIR / "res_route_inventory_test_summary.json"
TEST_MD = METADATA_DIR / "res_route_inventory_test_summary.md"

TOL = 1e-3
# Kostnads- og prissjekker bruker 0,05 fordi modelloutput avrundes til 2 desimaler
# for kostnader/priser og 6 desimaler for mengder i CSV-filene.
COST_TOL = 0.05
# Modellhavnene er eksplisitt avgrenset i rapportens modellkapittel.
MODEL_PORTS = {"P001", "P002", "P003", "P004"}
EXPECTED_SENSITIVITY_MULTIPLIERS = {1.10, 1.25, 1.50}
OPTIMAL_SOLVER_STATUS = "Optimization terminated successfully. (HiGHS Status 7: Optimal)"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(row: dict[str, str], column: str) -> float:
    value = row.get(column, "")
    if value == "":
        return 0.0
    return float(value)


def close_enough(left: float, right: float, tolerance: float = TOL) -> bool:
    return abs(left - right) <= tolerance


def split_ports(value: str) -> set[str]:
    return {port for port in value.split("|") if port}


def file_metadata(path: Path) -> dict[str, object]:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "mtime": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
        "sha256": digest,
    }


def add_check(
    checks: list[dict[str, object]],
    name: str,
    passed: bool,
    value: object,
    expected: object,
) -> None:
    checks.append(
        {
            "check": name,
            "passed": passed,
            "value": value,
            "expected": expected,
        }
    )


def validate() -> dict[str, object]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    checks: list[dict[str, object]] = []
    input_files = [
        LEGS_CSV,
        CAPACITY_CSV,
        PRICE_CSV,
    ]
    required_files = [
        *input_files,
        SUMMARY_JSON,
        BY_VESSEL_CSV,
        BY_LEG_CSV,
        PURCHASES_CSV,
        SENSITIVITY_CSV,
    ]
    missing_files = [str(path.relative_to(ROOT)) for path in required_files if not path.exists()]
    add_check(checks, "Alle modellresultatfiler finnes", not missing_files, missing_files, [])
    if missing_files:
        return write_result(checks)

    summary = json.loads(SUMMARY_JSON.read_text(encoding="utf-8"))
    by_vessel = read_csv(BY_VESSEL_CSV)
    by_leg = read_csv(BY_LEG_CSV)
    purchases = read_csv(PURCHASES_CSV)
    sensitivity = read_csv(SENSITIVITY_CSV)
    input_legs = read_csv(LEGS_CSV)
    capacities = {
        row["vessel_class"]: float(row["bunker_capacity_m3"])
        for row in read_csv(CAPACITY_CSV)
    }
    price_rows = read_csv(PRICE_CSV)
    priced_ports = {row["port"] for row in price_rows}
    exact_prices = {
        (row["delivery_month"], row["port"]): float(row["weighted_avg_price"])
        for row in price_rows
    }
    port_totals: dict[str, dict[str, float]] = {}
    for row in price_rows:
        port = row["port"]
        qty = float(row["total_qty"])
        price = float(row["weighted_avg_price"])
        port_totals.setdefault(port, {"qty": 0.0, "cost": 0.0})
        port_totals[port]["qty"] += qty
        port_totals[port]["cost"] += qty * price
    port_average_prices = {
        port: values["cost"] / values["qty"]
        for port, values in port_totals.items()
        if values["qty"] > 0
    }

    input_leg_by_key = {
        (row["vessel_file_id"], row["leg_sequence"]): row for row in input_legs
    }
    by_leg_by_key = {
        (row["vessel_file_id"], row["leg_sequence"]): row for row in by_leg
    }

    add_check(
        checks,
        "Antall etapper stemmer med sammendrag",
        len(by_leg) == int(summary["leg_count"]),
        len(by_leg),
        summary["leg_count"],
    )
    add_check(
        checks,
        "Antall fartøyfiler stemmer med sammendrag",
        len(by_vessel) == int(summary["vessel_file_count"]),
        len(by_vessel),
        summary["vessel_file_count"],
    )
    add_check(
        checks,
        "Alle fartøyløsninger er optimale",
        all(row["solver_status"] == OPTIMAL_SOLVER_STATUS for row in by_vessel),
        f"{sum(1 for row in by_vessel if row['solver_status'] == OPTIMAL_SOLVER_STATUS)} optimale løsninger",
        OPTIMAL_SOLVER_STATUS,
    )
    add_check(
        checks,
        "Antall etapper stemmer med inputdata",
        len(by_leg) == len(input_legs),
        len(by_leg),
        len(input_legs),
    )

    negative_inventory = 0
    over_end_capacity = 0
    over_pre_capacity = 0
    balance_breaks = 0
    purchase_without_priced_port = 0
    duplicate_legs = 0
    missing_input_legs = 0
    consumption_mismatches = 0
    first_rob_mismatches = 0
    capacity_mismatches = 0
    available_priced_port_mismatches = 0
    sequence_breaks = 0
    first_balance_breaks = 0
    seen_legs: set[tuple[str, str]] = set()
    previous_inventory_by_vessel: dict[str, float] = {}
    previous_sequence_by_vessel: dict[str, int] = {}

    for row in by_leg:
        key = (row["vessel_file_id"], row["leg_sequence"])
        if key in seen_legs:
            duplicate_legs += 1
        seen_legs.add(key)

        vessel = row["vessel_file_id"]
        leg_sequence = int(row["leg_sequence"])
        capacity = as_float(row, "capacity")
        consumption = as_float(row, "consumption")
        purchase_qty = as_float(row, "model_purchase_qty")
        external_qty = as_float(row, "model_external_qty")
        inventory_end = as_float(row, "model_inventory_end")
        start_inventory = previous_inventory_by_vessel.get(
            vessel, as_float(row, "rob_start_observed")
        )
        pre_consumption_inventory = start_inventory + purchase_qty + external_qty
        expected_inventory_end = pre_consumption_inventory - consumption

        if inventory_end < -TOL:
            negative_inventory += 1
        if inventory_end > capacity + TOL:
            over_end_capacity += 1
        if pre_consumption_inventory > capacity + TOL:
            over_pre_capacity += 1
        if not close_enough(inventory_end, expected_inventory_end):
            balance_breaks += 1
        if purchase_qty > TOL and row["available_priced_ports"] == "":
            purchase_without_priced_port += 1

        input_row = input_leg_by_key.get(key)
        if input_row is None:
            missing_input_legs += 1
        else:
            if not close_enough(consumption, float(input_row["fuel_consumption_total"])):
                consumption_mismatches += 1
            if vessel not in previous_sequence_by_vessel:
                input_rob_start = float(input_row["rob_start"])
                input_consumption = float(input_row["fuel_consumption_total"])
                if not close_enough(as_float(row, "rob_start_observed"), input_rob_start):
                    first_rob_mismatches += 1
                if not close_enough(
                    inventory_end,
                    input_rob_start + purchase_qty + external_qty - input_consumption,
                ):
                    first_balance_breaks += 1
            expected_capacity = capacities[input_row["vessel_class"]]
            if not close_enough(capacity, expected_capacity):
                capacity_mismatches += 1
            expected_priced_ports = sorted(
                split_ports(input_row["available_ports_P00X"]) & priced_ports & MODEL_PORTS
            )
            actual_priced_ports = sorted(split_ports(row["available_priced_ports"]))
            if actual_priced_ports != expected_priced_ports:
                available_priced_port_mismatches += 1

        previous_sequence = previous_sequence_by_vessel.get(vessel)
        if previous_sequence is not None and leg_sequence != previous_sequence + 1:
            sequence_breaks += 1
        previous_sequence_by_vessel[vessel] = leg_sequence
        previous_inventory_by_vessel[vessel] = inventory_end

    add_check(checks, "Ingen dupliserte fartøy-etapper", duplicate_legs == 0, duplicate_legs, 0)
    add_check(checks, "Alle output-etapper finnes i inputdata", missing_input_legs == 0, missing_input_legs, 0)
    add_check(checks, "Etapperekkefølge er kronologisk per fartøy", sequence_breaks == 0, sequence_breaks, 0)
    add_check(checks, "Forbruk per etappe stemmer med inputdata", consumption_mismatches == 0, consumption_mismatches, 0)
    add_check(checks, "Første ROB per fartøy stemmer med inputdata", first_rob_mismatches == 0, first_rob_mismatches, 0)
    add_check(
        checks,
        "Første lagerbalanse per fartøy stemmer direkte med inputdata",
        first_balance_breaks == 0,
        first_balance_breaks,
        0,
    )
    add_check(checks, "Kapasitet per etappe stemmer med kapasitetstabell", capacity_mismatches == 0, capacity_mismatches, 0)
    add_check(
        checks,
        "Tilgjengelige prisede havner stemmer med inputdata",
        available_priced_port_mismatches == 0,
        available_priced_port_mismatches,
        0,
    )
    add_check(checks, "Ingen negativ sluttbeholdning", negative_inventory == 0, negative_inventory, 0)
    add_check(checks, "Ingen sluttbeholdning over kapasitet", over_end_capacity == 0, over_end_capacity, 0)
    add_check(checks, "Ingen beholdning før forbruk over kapasitet", over_pre_capacity == 0, over_pre_capacity, 0)
    add_check(checks, "Lagerbalansen holder på etappenivå", balance_breaks == 0, balance_breaks, 0)
    add_check(
        checks,
        "Ingen kjøp uten tilgjengelig priset modellhavn",
        purchase_without_priced_port == 0,
        purchase_without_priced_port,
        0,
    )

    positive_leg_purchases = sum(1 for row in by_leg if as_float(row, "model_purchase_qty") > TOL)
    add_check(
        checks,
        "Antall etapper med kjøp stemmer med sammendrag",
        positive_leg_purchases == int(summary["purchased_leg_count"]),
        positive_leg_purchases,
        summary["purchased_leg_count"],
    )
    add_check(
        checks,
        "Antall kjøpsrader stemmer med sammendrag",
        len(purchases) == int(summary["purchased_leg_count"]),
        len(purchases),
        summary["purchased_leg_count"],
    )

    leg_purchase_qty = sum(as_float(row, "model_purchase_qty") for row in by_leg)
    purchase_qty = sum(as_float(row, "purchase_qty") for row in purchases)
    leg_external_qty = sum(as_float(row, "model_external_qty") for row in by_leg)
    vessel_total_cost = sum(as_float(row, "total_model_cost") for row in by_vessel)
    purchase_priced_cost = sum(as_float(row, "priced_cost") for row in purchases)
    purchase_port_not_available = 0
    purchase_cost_breaks = 0
    nonpositive_purchase_prices = 0
    purchase_price_mismatches = 0

    for row in purchases:
        key = (row["vessel_file_id"], row["leg_sequence"])
        leg_row = by_leg_by_key.get(key)
        if leg_row is None or row["port"] not in split_ports(leg_row["available_priced_ports"]):
            purchase_port_not_available += 1
        qty = as_float(row, "purchase_qty")
        price = as_float(row, "price")
        if price <= 0:
            nonpositive_purchase_prices += 1

        exact_price = exact_prices.get((row["period_month"], row["port"]))
        if row["price_source"] == "monthly_observation":
            expected_price = exact_price
        elif row["price_source"] == "historical_port_average":
            expected_price = port_average_prices.get(row["port"])
        else:
            expected_price = None
        if expected_price is None or not close_enough(
            as_float(row, "priced_cost"),
            qty * expected_price,
            COST_TOL,
        ):
            purchase_cost_breaks += 1
        if expected_price is None or not close_enough(price, expected_price, COST_TOL):
            purchase_price_mismatches += 1

    add_check(
        checks,
        "Kjøpsmengde stemmer mellom etapper og kjøpsfil",
        close_enough(leg_purchase_qty, purchase_qty, COST_TOL),
        round(leg_purchase_qty - purchase_qty, 6),
        0,
    )
    add_check(
        checks,
        "Kjøpsmengde stemmer med sammendrag",
        close_enough(leg_purchase_qty, float(summary["model_purchase_qty"]), COST_TOL),
        round(leg_purchase_qty, 3),
        summary["model_purchase_qty"],
    )
    add_check(
        checks,
        "Ekstern mengde stemmer med sammendrag",
        close_enough(leg_external_qty, float(summary["model_external_qty"]), COST_TOL),
        round(leg_external_qty, 3),
        summary["model_external_qty"],
    )
    add_check(
        checks,
        "Totalkostnad per fartøy stemmer med sammendrag",
        close_enough(vessel_total_cost, float(summary["total_model_cost"]), COST_TOL),
        round(vessel_total_cost, 2),
        summary["total_model_cost"],
    )
    add_check(
        checks,
        "Kostnad i prisede havner stemmer med sammendrag",
        close_enough(purchase_priced_cost, float(summary["priced_cost"]), COST_TOL),
        round(purchase_priced_cost, 2),
        summary["priced_cost"],
    )
    add_check(
        checks,
        "Kjøpshavn finnes blant prisede havner på samme etappe",
        purchase_port_not_available == 0,
        purchase_port_not_available,
        0,
    )
    add_check(
        checks,
        "Alle kjøpspriser er positive",
        nonpositive_purchase_prices == 0,
        nonpositive_purchase_prices,
        0,
    )
    add_check(
        checks,
        "Kjøpskostnad stemmer med mengde ganger pris",
        purchase_cost_breaks == 0,
        purchase_cost_breaks,
        0,
    )
    add_check(
        checks,
        "Kjøpspriser stemmer med prisdata",
        purchase_price_mismatches == 0,
        purchase_price_mismatches,
        0,
    )

    price_source_counts = Counter(row["price_source"] for row in purchases)
    add_check(
        checks,
        "Prisgrunnlag for kjøp stemmer med sammendrag",
        dict(price_source_counts) == summary["purchase_price_sources"],
        dict(price_source_counts),
        summary["purchase_price_sources"],
    )

    actual_sensitivity_multipliers = {
        round(as_float(row, "external_price_multiplier"), 2) for row in sensitivity
    }
    add_check(
        checks,
        "Sensitivitetsfil har forventede proxyfaktorer",
        actual_sensitivity_multipliers == EXPECTED_SENSITIVITY_MULTIPLIERS,
        sorted(actual_sensitivity_multipliers),
        sorted(EXPECTED_SENSITIVITY_MULTIPLIERS),
    )
    add_check(
        checks,
        "Sensitivitetsfil har forventet antall rader",
        len(sensitivity) == len(EXPECTED_SENSITIVITY_MULTIPLIERS),
        len(sensitivity),
        len(EXPECTED_SENSITIVITY_MULTIPLIERS),
    )

    sensitivity_cost_breaks = 0
    sensitivity_external_cost_breaks = 0
    for row in sensitivity:
        if not close_enough(
            as_float(row, "priced_cost") + as_float(row, "external_cost"),
            as_float(row, "total_model_cost"),
            COST_TOL,
        ):
            sensitivity_cost_breaks += 1
        if not close_enough(
            as_float(row, "model_external_qty") * as_float(row, "external_price"),
            as_float(row, "external_cost"),
            COST_TOL,
        ):
            sensitivity_external_cost_breaks += 1
    add_check(
        checks,
        "Sensitivitetsrader har konsistent totalkostnad",
        sensitivity_cost_breaks == 0,
        sensitivity_cost_breaks,
        0,
    )
    add_check(
        checks,
        "Sensitivitetsrader har konsistent eksternkostnad",
        sensitivity_external_cost_breaks == 0,
        sensitivity_external_cost_breaks,
        0,
    )

    main_sensitivity = [
        row for row in sensitivity if close_enough(as_float(row, "external_price_multiplier"), 1.25)
    ]
    main_sensitivity_matches = (
        len(main_sensitivity) == 1
        and close_enough(
            as_float(main_sensitivity[0], "total_model_cost"),
            float(summary["total_model_cost"]),
            COST_TOL,
        )
    )
    add_check(
        checks,
        "Hovedscenario i sensitivitetsfil stemmer med sammendrag",
        main_sensitivity_matches,
        main_sensitivity[0]["total_model_cost"] if main_sensitivity else None,
        summary["total_model_cost"],
    )

    return write_result(checks, input_files, required_files)


def write_result(
    checks: list[dict[str, object]],
    input_files: list[Path] | None = None,
    validated_files: list[Path] | None = None,
) -> dict[str, object]:
    failed = [check for check in checks if not check["passed"]]
    input_files = input_files or []
    validated_files = validated_files or []
    result = {
        "test_status": "passed" if not failed else "failed",
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "checks": checks,
        "tested_at": datetime.now(timezone.utc).isoformat(),
        "model_output_dir": str((MODEL_DIR / "output").relative_to(ROOT)).replace("\\", "/"),
        "input_files": [file_metadata(path) for path in input_files if path.exists()],
        "validated_files": [file_metadata(path) for path in validated_files if path.exists()],
    }
    TEST_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Test av operasjonell hovedmodell",
        "",
        f"Status: {'bestått' if not failed else 'feilet'}",
        f"Antall kontroller: {len(checks)}",
        f"Feilede kontroller: {len(failed)}",
        "",
        "| Kontroll | Status | Verdi | Forventet |",
        "| --- | --- | ---: | ---: |",
    ]
    for check in checks:
        status = "OK" if check["passed"] else "FEIL"
        lines.append(
            f"| {check['check']} | {status} | `{check['value']}` | `{check['expected']}` |"
        )
    TEST_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


def main() -> None:
    result = validate()
    print(f"Teststatus: {result['test_status']}")
    print(f"Kontroller: {result['check_count']}")
    print(f"Feilede kontroller: {result['failed_check_count']}")
    print(f"Oppsummering: {TEST_JSON}")
    if result["failed_check_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
