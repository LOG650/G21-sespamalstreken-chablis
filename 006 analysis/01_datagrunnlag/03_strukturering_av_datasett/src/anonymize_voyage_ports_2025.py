from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = ROOT / "004 data"
ACTIVITY_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ACTIVITY_DIR / "data"
METADATA_DIR = ACTIVITY_DIR / "metadata"

EVENTS_CSV = OUTPUT_DIR / "tab_voyage_events_2025.csv"
LEGS_CSV = OUTPUT_DIR / "tab_voyage_legs_2025.csv"
PORT_MAPPING_CSV = OUTPUT_DIR / "tab_port_mapping_confidential.csv"
GUIDE_MD = METADATA_DIR / "tab_port_anonymization_guide.md"

FIXED_PORT_MAPPING = {
    "AEFJR": "P001",
    "USTSX": "P002",
    "NLRTM": "P003",
    "SGSIN": "P004",
}

PORT_PATTERN = re.compile(r"^P\d{3}$")
VOYAGE_PATTERN = re.compile(r"^VG\d{3,}$")


def is_anonymized_port(value: str | None) -> bool:
    return bool(value and PORT_PATTERN.match(value.strip()))


def is_anonymized_voyage(value: str | None) -> bool:
    return bool(value and VOYAGE_PATTERN.match(value.strip()))


def raw_voyage_files() -> list[Path]:
    return sorted(path for path in DATA_DIR.glob("C*.csv") if path.is_file())


def existing_port_mapping() -> dict[str, str]:
    if not PORT_MAPPING_CSV.exists():
        return {}

    with PORT_MAPPING_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return {
            row["original_port_code"].strip(): row["anonymized_port_code"].strip()
            for row in reader
            if row.get("original_port_code") and row.get("anonymized_port_code")
        }


def collect_ports_from_raw(paths: list[Path]) -> set[str]:
    ports: set[str] = set()
    for path in paths:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            for row in reader:
                for column in ["Voyage_From", "Voyage_To"]:
                    value = (row.get(column) or "").strip()
                    if value and not is_anonymized_port(value):
                        ports.add(value)
    return ports


def collect_ports_from_structured(paths: list[Path]) -> set[str]:
    ports: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                for column in [
                    "from_port_unlocode",
                    "to_port_unlocode",
                    "from_port_P00X",
                    "to_port_P00X",
                ]:
                    value = (row.get(column) or "").strip()
                    if value and not is_anonymized_port(value):
                        ports.add(value)
                available = (row.get("available_ports") or "").strip()
                if available:
                    for value in available.split("|"):
                        value = value.strip()
                        if value and not is_anonymized_port(value):
                            ports.add(value)
    return ports


def build_port_mapping(raw_paths: list[Path]) -> dict[str, str]:
    ports = collect_ports_from_raw(raw_paths)
    ports.update(collect_ports_from_structured([EVENTS_CSV, LEGS_CSV]))

    mapping = existing_port_mapping()
    mapping.update(FIXED_PORT_MAPPING)
    next_number = 5
    for port in sorted(ports):
        if port in mapping:
            continue
        while f"P{next_number:03d}" in mapping.values():
            next_number += 1
        mapping[port] = f"P{next_number:03d}"
        next_number += 1
    return mapping


def collect_voyages(raw_paths: list[Path]) -> list[str]:
    voyages: list[str] = []
    seen: set[str] = set()

    def add(value: str | None) -> None:
        value = (value or "").strip()
        if not value or is_anonymized_voyage(value) or value in seen:
            return
        seen.add(value)
        voyages.append(value)

    for path in raw_paths:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            for row in reader:
                add(row.get("Voyage_Number"))

    for path in [EVENTS_CSV, LEGS_CSV]:
        if not path.exists():
            continue
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                add(row.get("voyage_number"))

    return voyages


def build_voyage_mapping(raw_paths: list[Path]) -> dict[str, str]:
    return {voyage: f"VG{index:03d}" for index, voyage in enumerate(collect_voyages(raw_paths), start=1)}


def count_anonymized_voyages(raw_paths: list[Path]) -> int:
    voyages: set[str] = set()
    for path in raw_paths:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            for row in reader:
                value = (row.get("Voyage_Number") or "").strip()
                if is_anonymized_voyage(value):
                    voyages.add(value)

    for path in [EVENTS_CSV, LEGS_CSV]:
        if not path.exists():
            continue
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                value = (row.get("voyage_number") or "").strip()
                if is_anonymized_voyage(value):
                    voyages.add(value)
    return len(voyages)


def map_port(value: str | None, mapping: dict[str, str]) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    if is_anonymized_port(value):
        return value
    return mapping[value]


def map_voyage(value: str | None, mapping: dict[str, str]) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    if is_anonymized_voyage(value):
        return value
    return mapping[value]


def anonymize_raw_file(path: Path, port_mapping: dict[str, str], voyage_mapping: dict[str, str]) -> None:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    for row in rows:
        if "Voyage_From" in row:
            row["Voyage_From"] = map_port(row.get("Voyage_From"), port_mapping)
        if "Voyage_To" in row:
            row["Voyage_To"] = map_port(row.get("Voyage_To"), port_mapping)
        if "Voyage_Number" in row:
            row["Voyage_Number"] = map_voyage(row.get("Voyage_Number"), voyage_mapping)

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def anonymize_available_ports(value: str | None, port_mapping: dict[str, str]) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    return "|".join(map_port(port, port_mapping) for port in value.split("|") if port.strip())


def anonymize_structured_file(
    path: Path,
    port_mapping: dict[str, str],
    voyage_mapping: dict[str, str],
) -> None:
    if not path.exists():
        return

    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        original_fieldnames = reader.fieldnames or []
        rows = list(reader)

    output_fieldnames: list[str] = []
    for field in original_fieldnames:
        if field in {"from_port_unlocode", "from_port_P00X"}:
            if "from_port_P00X" not in output_fieldnames:
                output_fieldnames.append("from_port_P00X")
        elif field in {"to_port_unlocode", "to_port_P00X"}:
            if "to_port_P00X" not in output_fieldnames:
                output_fieldnames.append("to_port_P00X")
        elif field in {"available_ports", "available_ports_P00X"}:
            if "available_ports_P00X" not in output_fieldnames:
                output_fieldnames.append("available_ports_P00X")
        elif field not in output_fieldnames:
            output_fieldnames.append(field)

    output_rows: list[dict[str, str]] = []
    for row in rows:
        output_row: dict[str, str] = {}
        for field in output_fieldnames:
            if field == "from_port_P00X":
                output_row[field] = map_port(
                    row.get("from_port_unlocode") or row.get("from_port_P00X"),
                    port_mapping,
                )
            elif field == "to_port_P00X":
                output_row[field] = map_port(
                    row.get("to_port_unlocode") or row.get("to_port_P00X"),
                    port_mapping,
                )
            elif field == "available_ports_P00X":
                output_row[field] = anonymize_available_ports(
                    row.get("available_ports") or row.get("available_ports_P00X"),
                    port_mapping,
                )
            elif field == "voyage_number":
                output_row[field] = map_voyage(row.get("voyage_number"), voyage_mapping)
            else:
                output_row[field] = row.get(field, "")
        output_rows.append(output_row)

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def write_port_mapping(mapping: dict[str, str]) -> None:
    rows = [
        {
            "original_port_code": original,
            "anonymized_port_code": anonymized,
            "mapping_note": "modellhavn"
            if original in FIXED_PORT_MAPPING
            else "supplerende voyage-havn",
        }
        for original, anonymized in sorted(mapping.items(), key=lambda item: item[1])
    ]
    with PORT_MAPPING_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["original_port_code", "anonymized_port_code", "mapping_note"],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_guide(
    port_mapping: dict[str, str],
    voyage_mapping: dict[str, str],
    raw_paths: list[Path],
) -> None:
    voyage_count = len(voyage_mapping) or count_anonymized_voyages(raw_paths)
    lines = [
        "# Port- og voyage-anonymisering 2025",
        "",
        "Eksisterende voyage-filer i repoet er anonymisert på plass. Rådata med opprinnelige koder forutsettes oppbevart utenfor repoet.",
        "",
        "## Regler",
        "",
        "- `Voyage_From` og `Voyage_To` i `004 data/C*.csv` er erstattet med anonymiserte `Pxxx`-koder.",
        "- `Voyage_Number` i `004 data/C*.csv` er erstattet med anonymiserte `VGxxx`-koder.",
        "- `from_port_unlocode` er erstattet av `from_port_P00X` i strukturerte voyage-tabeller.",
        "- `to_port_unlocode` er erstattet av `to_port_P00X` i strukturerte voyage-tabeller.",
        "- `available_ports` er erstattet av `available_ports_P00X` i strukturerte voyage-etapper.",
        "- `P001` til `P004` følger eksisterende modellhavner, mens `P005+` er øvrige voyage-havner.",
        "",
        "## Omfang",
        "",
        f"- Rå-/splitfiler anonymisert i `004 data`: {len(raw_paths)}",
        f"- Portkoder i konfidensiell mapping: {len(port_mapping)}",
        f"- Voyage-koder anonymisert: {voyage_count}",
        "",
        "## Konfidensiell mapping",
        "",
        "`data/tab_port_mapping_confidential.csv` inneholder kobling mellom opprinnelig havnekode og anonym portkode. Filen skal brukes internt og ikke legges som publisert rapportvedlegg.",
    ]
    GUIDE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_paths = raw_voyage_files()
    port_mapping = build_port_mapping(raw_paths)
    voyage_mapping = build_voyage_mapping(raw_paths)

    for path in raw_paths:
        anonymize_raw_file(path, port_mapping, voyage_mapping)

    anonymize_structured_file(EVENTS_CSV, port_mapping, voyage_mapping)
    anonymize_structured_file(LEGS_CSV, port_mapping, voyage_mapping)
    write_port_mapping(port_mapping)
    write_guide(port_mapping, voyage_mapping, raw_paths)

    print(f"raw_files={len(raw_paths)}")
    print(f"port_mappings={len(port_mapping)}")
    print(f"voyage_mappings={len(voyage_mapping)}")
    print(f"mapping_csv={PORT_MAPPING_CSV}")
    print(f"guide_md={GUIDE_MD}")


if __name__ == "__main__":
    main()
