from __future__ import annotations

import csv
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = ROOT / "004 data"
ACTIVITY_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ACTIVITY_DIR / "data"
METADATA_DIR = ACTIVITY_DIR / "metadata"

EVENTS_CSV = OUTPUT_DIR / "tab_voyage_events_2025.csv"
LEGS_CSV = OUTPUT_DIR / "tab_voyage_legs_2025.csv"
CAPACITY_CSV = OUTPUT_DIR / "tab_vessel_class_capacity.csv"
GUIDE_MD = METADATA_DIR / "tab_voyage_structure_guide.md"
PORT_MAPPING_CSV = OUTPUT_DIR / "tab_port_mapping_confidential.csv"

CAPACITY_M3 = {
    "C001": 2087.006,
    "C002": 2061.430,
    "C003": 1533.719,
    "C004": 1907.080,
    "C005": 1024.531,
}

FALLBACK_CONSUMPTION_COLUMNS = [
    "ME_Consumption_HFO",
    "ME_Consumption_LFO",
    "ME_Consumption_MGO",
    "AE_Consumption_HFO",
    "AE_Consumption_LFO",
    "AE_Consumption_MGO",
    "Boiler_Consumption_HFO",
    "Boiler_Consumption_LFO",
    "Boiler_Consumption_MGO",
    "Cargo_heating_Consumption_HFO",
    "Cargo_heating_Consumption_LFO",
    "Cargo_heating_Consumption_MGO",
    "Inert_gas_Consumption_MGO",
]


def parse_number(value: str | None) -> float | None:
    if value is None:
        return None
    cleaned = value.strip().replace(" ", "").replace("\xa0", "").replace(",", ".")
    if cleaned == "":
        return None
    return float(cleaned)


def parse_datetime(date_value: str, time_value: str) -> str:
    text = f"{date_value.strip()} {time_value.strip()}"
    parsed = datetime.strptime(text, "%Y-%m-%d %H:%M")
    return parsed.isoformat(timespec="minutes")


def country_from_unlocode(value: str) -> str:
    value = value.strip()
    if re.fullmatch(r"P\d{3}", value):
        return ""
    return value[:2] if len(value) >= 2 else ""


def vessel_ids_from_file(path: Path) -> tuple[str, str]:
    stem = path.stem.replace(" ", "")
    vessel_class = stem.split("-")[0]
    return vessel_class, stem


def is_raw_voyage_file(path: Path) -> bool:
    if not path.name.startswith("C") or path.suffix.lower() != ".csv":
        return False
    return "_train_80" not in path.stem and "_test_20" not in path.stem


def sum_existing(row: dict[str, str], columns: list[str]) -> float:
    total = 0.0
    for column in columns:
        value = parse_number(row.get(column))
        if value is not None:
            total += value
    return total


def row_consumption(row: dict[str, str]) -> tuple[float, float, float, float, float]:
    me = sum_existing(row, ["ME_Consumption", "ME_Consumption_BDN_2", "ME_Consumption_BDN_3"])
    ae = sum_existing(row, ["AE_Consumption", "AE_Consumption_BDN_2", "AE_Consumption_BDN_3"])
    boiler = sum_existing(
        row,
        ["Boiler_Consumption", "Boiler_Consumption_BDN_2", "Boiler_Consumption_BDN_3"],
    )
    other = sum_existing(
        row,
        [
            "Incinerator_Consumption",
            "Incinerator_Consumption_BDN_2",
            "Cargo_Heating_Consumption_BDN",
            "DPP_Cargo_Pump_Consumption_MDO",
        ],
    )

    total = me + ae + boiler + other
    if total == 0:
        total = sum_existing(row, FALLBACK_CONSUMPTION_COLUMNS)

    return (
        round(me, 4),
        round(ae, 4),
        round(boiler, 4),
        round(other, 4),
        round(total, 4),
    )


def contract_port_codes() -> set[str]:
    ports = {"NLRTM", "SGSIN", "P003", "P004"}
    if not PORT_MAPPING_CSV.exists():
        return ports

    with PORT_MAPPING_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            original = (row.get("original_port_code") or "").strip()
            anonymized = (row.get("anonymized_port_code") or "").strip()
            if original == "NLRTM" or original == "SGSIN" or original[:2] in {"SG", "KR"}:
                ports.add(original)
                if anonymized:
                    ports.add(anonymized)
    return ports


CONTRACT_PORT_CODES = contract_port_codes()


def contract_flag(*ports: str) -> str:
    for port in ports:
        port = port.strip()
        if port in CONTRACT_PORT_CODES or country_from_unlocode(port) in {"SG", "KR"}:
            return "1"
    return "0"


def data_quality_flag(row: dict[str, object], capacity: float | None) -> str:
    flags: list[str] = []
    if row["voyage_number"] == "":
        flags.append("missing_voyage")
    if row["from_port_P00X"] == "" or row["to_port_P00X"] == "":
        flags.append("missing_port")
    if row["rob_fuel_total"] in {"", None}:
        flags.append("missing_rob")
    elif capacity is not None and float(row["rob_fuel_total"]) > capacity:
        flags.append("rob_above_capacity")
    if float(row["total_consumption"]) < 0:
        flags.append("negative_consumption")
    return "ok" if not flags else "|".join(flags)


def read_voyage_events() -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    for source in sorted(path for path in DATA_DIR.glob("C*.csv") if is_raw_voyage_file(path)):
        vessel_class, vessel_file_id = vessel_ids_from_file(source)
        capacity = CAPACITY_M3.get(vessel_class)
        with source.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            for row in reader:
                me, ae, boiler, other, total = row_consumption(row)
                event = {
                    "vessel_class": vessel_class,
                    "vessel_file_id": vessel_file_id,
                    "event_datetime_utc": parse_datetime(row["Date_UTC"], row["Time_UTC"]),
                    "event_date_utc": row["Date_UTC"].strip(),
                    "event_time_utc": row["Time_UTC"].strip(),
                    "event_type": row.get("Event", "").strip(),
                    "voyage_number": row.get("Voyage_Number", "").strip(),
                    "from_port_P00X": row.get("Voyage_From", "").strip(),
                    "to_port_P00X": row.get("Voyage_To", "").strip(),
                    "from_country": country_from_unlocode(row.get("Voyage_From", "")),
                    "to_country": country_from_unlocode(row.get("Voyage_To", "")),
                    "hours_since_previous_report": round(
                        parse_number(row.get("Time_Since_Previous_Report")) or 0.0,
                        4,
                    ),
                    "distance_nm": round(parse_number(row.get("Distance")) or 0.0, 4),
                    "me_consumption": me,
                    "ae_consumption": ae,
                    "boiler_consumption": boiler,
                    "other_consumption": other,
                    "total_consumption": total,
                    "rob_fuel_total": parse_number(row.get("ROB_Fuel_Total")),
                    "contract_port_flag": contract_flag(
                        row.get("Voyage_From", ""), row.get("Voyage_To", "")
                    ),
                    "source_file": source.name,
                    "source_system": row.get("Source_System", "").strip(),
                    "last_updated": row.get("Last_Updated", "").strip(),
                }
                event["data_quality_flag"] = data_quality_flag(event, capacity)
                events.append(event)

    events.sort(key=lambda item: (item["vessel_file_id"], item["event_datetime_utc"]))
    return events


def aggregate_legs(events: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str, str], list[dict[str, object]]] = defaultdict(list)
    for event in events:
        key = (
            str(event["vessel_file_id"]),
            str(event["voyage_number"]),
            str(event["from_port_P00X"]),
            str(event["to_port_P00X"]),
        )
        grouped[key].append(event)

    by_file: dict[str, list[tuple[tuple[str, str, str, str], list[dict[str, object]]]]] = defaultdict(list)
    for key, rows in grouped.items():
        rows.sort(key=lambda item: str(item["event_datetime_utc"]))
        by_file[key[0]].append((key, rows))

    legs: list[dict[str, object]] = []
    for vessel_file_id in sorted(by_file):
        file_groups = sorted(
            by_file[vessel_file_id],
            key=lambda pair: str(pair[1][0]["event_datetime_utc"]),
        )
        for sequence, (key, rows) in enumerate(file_groups, start=1):
            first = rows[0]
            last = rows[-1]
            rob_values = [
                float(row["rob_fuel_total"])
                for row in rows
                if row["rob_fuel_total"] not in {"", None}
            ]
            capacity = CAPACITY_M3.get(str(first["vessel_class"]))
            quality_flags = sorted(
                {
                    flag
                    for row in rows
                    for flag in str(row["data_quality_flag"]).split("|")
                    if flag and flag != "ok"
                }
            )
            if capacity is not None and rob_values and max(rob_values) > capacity:
                quality_flags.append("rob_above_capacity")

            bunkering_inferred = "0"
            for previous, current in zip(rob_values, rob_values[1:]):
                if current > previous:
                    bunkering_inferred = "1"
                    break

            ports = sorted(
                {
                    str(row["from_port_P00X"])
                    for row in rows
                    if str(row["from_port_P00X"]).strip()
                }
                | {
                    str(row["to_port_P00X"])
                    for row in rows
                    if str(row["to_port_P00X"]).strip()
                }
            )

            legs.append(
                {
                    "vessel_class": first["vessel_class"],
                    "vessel_file_id": vessel_file_id,
                    "voyage_number": key[1],
                    "leg_sequence": sequence,
                    "from_port_P00X": key[2],
                    "to_port_P00X": key[3],
                    "departure_datetime_utc": first["event_datetime_utc"],
                    "arrival_datetime_utc": last["event_datetime_utc"],
                    "period_month": str(first["event_datetime_utc"])[:7],
                    "distance_nm_total": round(sum(float(row["distance_nm"]) for row in rows), 4),
                    "duration_hours_total": round(
                        sum(float(row["hours_since_previous_report"]) for row in rows), 4
                    ),
                    "fuel_consumption_total": round(
                        sum(float(row["total_consumption"]) for row in rows), 4
                    ),
                    "rob_start": "" if not rob_values else rob_values[0],
                    "rob_end": "" if not rob_values else rob_values[-1],
                    "bunkering_inferred": bunkering_inferred,
                    "available_ports_P00X": "|".join(ports),
                    "contract_port_flag": contract_flag(*ports),
                    "data_quality_flag": "ok"
                    if not quality_flags
                    else "|".join(sorted(set(quality_flags))),
                }
            )
    return legs


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_capacity_csv() -> None:
    rows = [
        {
            "vessel_class": vessel_class,
            "bunker_capacity_m3": capacity,
            "capacity_source": "verifiserte 2025-tall fra dataleverandør",
            "capacity_note": "Ikke avklart om tallet er total eller operativ kapasitet.",
        }
        for vessel_class, capacity in sorted(CAPACITY_M3.items())
    ]
    write_csv(
        CAPACITY_CSV,
        rows,
        ["vessel_class", "bunker_capacity_m3", "capacity_source", "capacity_note"],
    )


def write_guide(events: list[dict[str, object]], legs: list[dict[str, object]]) -> None:
    quality_counts: dict[str, int] = defaultdict(int)
    for row in events:
        quality_counts[str(row["data_quality_flag"])] += 1
    leg_quality_counts: dict[str, int] = defaultdict(int)
    for row in legs:
        leg_quality_counts[str(row["data_quality_flag"])] += 1

    lines = [
        "# Struktur for voyage-data 2025",
        "",
        "Denne filen dokumenterer modellklare tabeller generert fra de anonymiserte voyage-filene i `004 data`.",
        "",
        "## Genererte tabeller",
        "",
        "| Fil | Nivå | Bruk |",
        "| --- | --- | --- |",
        "| `tab_voyage_events_2025.csv` | Rapporteringshendelse | Detaljert sporbarhet, kontroll og eventuell videre aggregering |",
        "| `tab_voyage_legs_2025.csv` | Voyage-etappe | Hovedtabell for fartøy- og rutebasert optimeringsmodell |",
        "| `tab_vessel_class_capacity.csv` | Fartøyklasse | Kapasitetsparameter $K_v$ |",
        "",
        "## Kolonner i `tab_voyage_events_2025.csv`",
        "",
        "| Kolonne | Forklaring |",
        "| --- | --- |",
        "| `vessel_class` | Anonymisert fartøyklasse, hentet fra filnavn |",
        "| `vessel_file_id` | Anonym fil-ID, f.eks. `C001-1` |",
        "| `event_datetime_utc` | Kombinert dato og tid i UTC |",
        "| `event_type` | Rapportert hendelsestype |",
        "| `voyage_number` | Voyage-identifikator |",
        "| `from_port_P00X`, `to_port_P00X` | Anonymisert start- og slutthavn |",
        "| `from_country`, `to_country` | Landprefiks fra opprinnelig UN/Locode når tabellen genereres fra ikke-pseudonymiserte rådata; tomt ved P-koder |",
        "| `hours_since_previous_report` | Timer siden forrige rapport |",
        "| `distance_nm` | Rapportert distanse, antatt nautiske mil |",
        "| `me_consumption`, `ae_consumption`, `boiler_consumption`, `other_consumption` | Forbruk gruppert etter maskin-/forbrukstype |",
        "| `total_consumption` | Sum modellrelevant forbruk for raden |",
        "| `rob_fuel_total` | Total remaining on board etter rapportering |",
        "| `contract_port_flag` | 1 dersom raden berører kontraktsrelevant havn basert på intern portmapping |",
        "| `data_quality_flag` | Enkel kvalitetsmarkør for manglende voyage, port, ROB eller kapasitetsavvik |",
        "",
        "## Kolonner i `tab_voyage_legs_2025.csv`",
        "",
        "| Kolonne | Forklaring |",
        "| --- | --- |",
        "| `vessel_class`, `vessel_file_id`, `voyage_number` | Identifikasjon av anonymisert fartøy og voyage |",
        "| `leg_sequence` | Kronologisk løpenummer innen fartøyfil |",
        "| `from_port_P00X`, `to_port_P00X` | Etappens anonymiserte start- og slutthavn |",
        "| `departure_datetime_utc`, `arrival_datetime_utc` | Første og siste tidspunkt i etappen |",
        "| `period_month` | Måned brukt for kobling mot prisdata |",
        "| `distance_nm_total`, `duration_hours_total` | Aggregert distanse og varighet |",
        "| `fuel_consumption_total` | Aggregert forbruk, kandidat for $d_{v,t}$ |",
        "| `rob_start`, `rob_end` | Første og siste observerte ROB i etappen |",
        "| `bunkering_inferred` | 1 dersom ROB øker innen etappen |",
        "| `available_ports_P00X` | Observerte anonymiserte havner i etappen, separert med `|` |",
        "| `contract_port_flag` | 1 dersom en observert havn er kontraktsrelevant basert på intern portmapping |",
        "| `data_quality_flag` | Oppsummerte kvalitetsflagg fra rapporteringsradene |",
        "",
        "## Omfang og kontroller",
        "",
        f"- Rapporteringsrader strukturert: {len(events)}",
        f"- Voyage-etapper aggregert: {len(legs)}",
        f"- Fartøyklasser med kapasitet: {len(CAPACITY_M3)}",
        "",
        "### Kvalitetsflagg på rapporteringsnivå",
        "",
        "| Flagg | Antall |",
        "| --- | ---: |",
    ]
    for flag, count in sorted(quality_counts.items()):
        lines.append(f"| `{flag}` | {count} |")

    lines.extend(
        [
            "",
            "### Kvalitetsflagg på etappenivå",
            "",
            "| Flagg | Antall |",
            "| --- | ---: |",
        ]
    )
    for flag, count in sorted(leg_quality_counts.items()):
        lines.append(f"| `{flag}` | {count} |")

    lines.extend(
        [
            "",
            "## Modellkobling",
            "",
            "- $K_v$ hentes fra `tab_vessel_class_capacity.csv`.",
            "- $d_{v,t}$ kan hentes fra `fuel_consumption_total` i `tab_voyage_legs_2025.csv`.",
            "- $I_{v,t}$ kan initialiseres eller kontrolleres med `rob_start` og `rob_end`.",
            "- Reell havnetilgjengelighet kan avledes fra `from_port_P00X`, `to_port_P00X` og `available_ports_P00X`.",
            "- Intern kobling mellom opprinnelige havnekoder og P-koder ligger i `data/tab_port_mapping_confidential.csv` og skal ikke publiseres som rapportvedlegg.",
            "- `contract_port_flag` er et første teknisk flagg og må valideres mot faktisk kontraktsomfang før det brukes som hard restriksjon.",
        ]
    )
    GUIDE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    events = read_voyage_events()
    legs = aggregate_legs(events)

    event_fields = [
        "vessel_class",
        "vessel_file_id",
        "event_datetime_utc",
        "event_date_utc",
        "event_time_utc",
        "event_type",
        "voyage_number",
        "from_port_P00X",
        "to_port_P00X",
        "from_country",
        "to_country",
        "hours_since_previous_report",
        "distance_nm",
        "me_consumption",
        "ae_consumption",
        "boiler_consumption",
        "other_consumption",
        "total_consumption",
        "rob_fuel_total",
        "contract_port_flag",
        "data_quality_flag",
        "source_file",
        "source_system",
        "last_updated",
    ]
    leg_fields = [
        "vessel_class",
        "vessel_file_id",
        "voyage_number",
        "leg_sequence",
        "from_port_P00X",
        "to_port_P00X",
        "departure_datetime_utc",
        "arrival_datetime_utc",
        "period_month",
        "distance_nm_total",
        "duration_hours_total",
        "fuel_consumption_total",
        "rob_start",
        "rob_end",
        "bunkering_inferred",
        "available_ports_P00X",
        "contract_port_flag",
        "data_quality_flag",
    ]

    write_csv(EVENTS_CSV, events, event_fields)
    write_csv(LEGS_CSV, legs, leg_fields)
    write_capacity_csv()
    write_guide(events, legs)

    print(f"events={len(events)}")
    print(f"legs={len(legs)}")
    print(f"events_csv={EVENTS_CSV}")
    print(f"legs_csv={LEGS_CSV}")
    print(f"capacity_csv={CAPACITY_CSV}")
    print(f"guide_md={GUIDE_MD}")


if __name__ == "__main__":
    main()
