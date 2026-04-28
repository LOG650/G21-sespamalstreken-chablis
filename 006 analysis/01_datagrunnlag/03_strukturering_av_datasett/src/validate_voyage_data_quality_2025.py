from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ACTIVITY_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ACTIVITY_DIR / "data"
METADATA_DIR = ACTIVITY_DIR / "metadata"

EVENTS_CSV = DATA_DIR / "tab_voyage_events_2025.csv"
LEGS_CSV = DATA_DIR / "tab_voyage_legs_2025.csv"
CAPACITY_CSV = DATA_DIR / "tab_vessel_class_capacity.csv"
ISSUES_CSV = DATA_DIR / "tab_voyage_data_quality_issues_2025.csv"
REPORT_MD = METADATA_DIR / "tab_voyage_data_quality_2025.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    return float(value)


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.strip())


def capacity_by_class() -> dict[str, float]:
    rows = read_csv(CAPACITY_CSV)
    return {
        row["vessel_class"]: float(row["bunker_capacity_m3"])
        for row in rows
        if row.get("vessel_class") and row.get("bunker_capacity_m3")
    }


def add_issue(
    issues: list[dict[str, str]],
    level: str,
    row_id: str,
    issue_type: str,
    severity: str,
    description: str,
) -> None:
    issues.append(
        {
            "level": level,
            "row_id": row_id,
            "issue_type": issue_type,
            "severity": severity,
            "description": description,
        }
    )


def validate_events(events: list[dict[str, str]], capacities: dict[str, float]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    for index, row in enumerate(events, start=1):
        row_id = f"event_{index}"
        capacity = capacities.get(row.get("vessel_class", ""))
        total_consumption = parse_float(row.get("total_consumption"))
        rob = parse_float(row.get("rob_fuel_total"))

        if not row.get("voyage_number"):
            add_issue(issues, "event", row_id, "missing_voyage", "high", "Manglende voyage-nummer.")
        if not row.get("from_port_P00X") or not row.get("to_port_P00X"):
            add_issue(issues, "event", row_id, "missing_port", "high", "Manglende start- eller slutthavn.")
        if rob is None:
            add_issue(issues, "event", row_id, "missing_rob", "medium", "Manglende ROB_Fuel_Total.")
        elif capacity is not None and rob > capacity:
            add_issue(issues, "event", row_id, "rob_above_capacity", "high", "ROB er høyere enn oppgitt tankkapasitet.")
        if total_consumption is None:
            add_issue(issues, "event", row_id, "missing_consumption", "high", "Manglende totalforbruk.")
        elif total_consumption < 0:
            add_issue(issues, "event", row_id, "negative_consumption", "high", "Negativt totalforbruk.")
        elif total_consumption == 0:
            add_issue(issues, "event", row_id, "zero_consumption", "low", "Nullforbruk på rapporteringsrad.")

    by_file: dict[str, list[dict[str, str]]] = {}
    for row in events:
        by_file.setdefault(row.get("vessel_file_id", ""), []).append(row)

    for rows in by_file.values():
        rows.sort(key=lambda item: item.get("event_datetime_utc", ""))
        for previous, current in zip(rows, rows[1:]):
            previous_time = parse_datetime(previous["event_datetime_utc"])
            current_time = parse_datetime(current["event_datetime_utc"])
            if current_time < previous_time:
                add_issue(
                    issues,
                    "event",
                    current.get("event_datetime_utc", ""),
                    "time_sequence_error",
                    "high",
                    "Rapporteringsrader ligger ikke kronologisk innen fartøyfil.",
                )

    return issues


def validate_legs(legs: list[dict[str, str]], capacities: dict[str, float]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    for index, row in enumerate(legs, start=1):
        row_id = f"leg_{index}"
        capacity = capacities.get(row.get("vessel_class", ""))
        fuel = parse_float(row.get("fuel_consumption_total"))
        duration = parse_float(row.get("duration_hours_total"))
        rob_start = parse_float(row.get("rob_start"))
        rob_end = parse_float(row.get("rob_end"))

        if not row.get("from_port_P00X") or not row.get("to_port_P00X"):
            add_issue(issues, "leg", row_id, "missing_port", "high", "Manglende start- eller slutthavn.")
        if rob_start is None or rob_end is None:
            add_issue(issues, "leg", row_id, "missing_rob", "medium", "Manglende start- eller slutt-ROB.")
        else:
            if capacity is not None and max(rob_start, rob_end) > capacity:
                add_issue(issues, "leg", row_id, "rob_above_capacity", "high", "ROB er høyere enn oppgitt tankkapasitet.")
            if rob_end > rob_start and row.get("bunkering_inferred") != "1":
                add_issue(
                    issues,
                    "leg",
                    row_id,
                    "rob_increase_without_bunkering_flag",
                    "medium",
                    "ROB øker uten at bunkring er flagget.",
                )

        if fuel is None:
            add_issue(issues, "leg", row_id, "missing_fuel_consumption", "high", "Manglende aggregert forbruk.")
        elif fuel < 0:
            add_issue(issues, "leg", row_id, "negative_fuel_consumption", "high", "Negativt aggregert forbruk.")
        elif fuel == 0:
            add_issue(issues, "leg", row_id, "zero_fuel_consumption", "low", "Nullforbruk på etappe.")

        if duration is None:
            add_issue(issues, "leg", row_id, "missing_duration", "medium", "Manglende varighet.")
        elif duration < 0:
            add_issue(issues, "leg", row_id, "negative_duration", "high", "Negativ varighet.")

        departure = parse_datetime(row["departure_datetime_utc"])
        arrival = parse_datetime(row["arrival_datetime_utc"])
        if arrival < departure:
            add_issue(issues, "leg", row_id, "arrival_before_departure", "high", "Ankomst er før avgang.")

    return issues


def write_issues(issues: list[dict[str, str]]) -> None:
    fieldnames = ["level", "row_id", "issue_type", "severity", "description"]
    with ISSUES_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(issues)


def write_report(events: list[dict[str, str]], legs: list[dict[str, str]], issues: list[dict[str, str]]) -> None:
    issue_counts = Counter(issue["issue_type"] for issue in issues)
    severity_counts = Counter(issue["severity"] for issue in issues)

    usable_legs = [
        row
        for row in legs
        if parse_float(row.get("fuel_consumption_total")) is not None
        and (parse_float(row.get("fuel_consumption_total")) or 0.0) > 0
        and row.get("from_port_P00X")
        and row.get("to_port_P00X")
    ]
    contract_legs = sum(1 for row in legs if row.get("contract_port_flag") == "1")
    bunkering_legs = sum(1 for row in legs if row.get("bunkering_inferred") == "1")

    lines = [
        "# Datakvalitet for voyage-data 2025",
        "",
        "Denne kontrollen vurderer om de strukturerte voyage-dataene er klare for direkte modellbruk.",
        "",
        "## Omfang",
        "",
        f"- Rapporteringsrader kontrollert: {len(events)}",
        f"- Voyage-etapper kontrollert: {len(legs)}",
        f"- Etapper med positivt forbruk og havnekobling: {len(usable_legs)}",
        f"- Etapper med inferert bunkring: {bunkering_legs}",
        f"- Etapper med kontraktsflagg: {contract_legs}",
        "",
        "## Avvik",
        "",
        "| Avvikstype | Antall |",
        "| --- | ---: |",
    ]

    for issue_type, count in sorted(issue_counts.items()):
        lines.append(f"| `{issue_type}` | {count} |")
    if not issue_counts:
        lines.append("| Ingen avvik | 0 |")

    lines.extend(
        [
            "",
            "## Alvorlighetsgrad",
            "",
            "| Grad | Antall |",
            "| --- | ---: |",
        ]
    )
    for severity, count in sorted(severity_counts.items()):
        lines.append(f"| `{severity}` | {count} |")
    if not severity_counts:
        lines.append("| Ingen avvik | 0 |")

    lines.extend(
        [
            "",
            "## Modellvurdering",
            "",
            "- Pris- og volumdatasettet fra bunkringslisten bør fortsatt være primærkilde for modellversjon 1.",
            "- Voyage-dataene er egnet som operasjonell støtte for forbruk, ROB, tankkapasitet og havnetilgjengelighet.",
            "- Direkte bruk i en fartøybasert modell krever at kontraktsflagg og drivstofftypekobling valideres faglig før de brukes som harde restriksjoner.",
            "- Avvikene er begrenset i omfang, men bør dokumenteres eksplisitt dersom voyage-dataene brukes i analyse eller resultatdrøfting.",
            "",
            f"Detaljerte avvik er lagret i `{ISSUES_CSV.relative_to(ROOT).as_posix()}`.",
        ]
    )

    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    events = read_csv(EVENTS_CSV)
    legs = read_csv(LEGS_CSV)
    capacities = capacity_by_class()
    issues = validate_events(events, capacities) + validate_legs(legs, capacities)

    write_issues(issues)
    write_report(events, legs, issues)

    print(f"events={len(events)}")
    print(f"legs={len(legs)}")
    print(f"issues={len(issues)}")
    print(f"issues_csv={ISSUES_CSV}")
    print(f"report_md={REPORT_MD}")


if __name__ == "__main__":
    main()
