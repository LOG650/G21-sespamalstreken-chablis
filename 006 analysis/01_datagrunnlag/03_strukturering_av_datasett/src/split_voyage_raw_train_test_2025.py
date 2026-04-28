from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = ROOT / "004 data"
ACTIVITY_DIR = Path(__file__).resolve().parent.parent
METADATA_DIR = ACTIVITY_DIR / "metadata"
SUMMARY_MD = METADATA_DIR / "tab_voyage_raw_train_test_split_2025.md"


def is_raw_voyage_file(path: Path) -> bool:
    if not path.name.startswith("C") or path.suffix.lower() != ".csv":
        return False
    return "_train_80" not in path.stem and "_test_20" not in path.stem


def parse_datetime(row: dict[str, str]) -> datetime:
    return datetime.strptime(
        f"{row['Date_UTC'].strip()} {row['Time_UTC'].strip()}",
        "%Y-%m-%d %H:%M",
    )


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    rows.sort(key=parse_datetime)
    return fieldnames, rows


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def row_range(rows: list[dict[str, str]]) -> tuple[str, str]:
    if not rows:
        return "", ""
    first = parse_datetime(rows[0]).isoformat(timespec="minutes")
    last = parse_datetime(rows[-1]).isoformat(timespec="minutes")
    return first, last


def split_file(path: Path) -> dict[str, object]:
    fieldnames, rows = read_rows(path)
    split_index = int(len(rows) * 0.8)
    train_rows = rows[:split_index]
    test_rows = rows[split_index:]

    train_path = path.with_name(f"{path.stem}_train_80{path.suffix}")
    test_path = path.with_name(f"{path.stem}_test_20{path.suffix}")

    write_rows(train_path, fieldnames, train_rows)
    write_rows(test_path, fieldnames, test_rows)

    train_start, train_end = row_range(train_rows)
    test_start, test_end = row_range(test_rows)

    return {
        "source_file": path.name,
        "train_file": train_path.name,
        "test_file": test_path.name,
        "source_rows": len(rows),
        "train_rows": len(train_rows),
        "test_rows": len(test_rows),
        "train_start": train_start,
        "train_end": train_end,
        "test_start": test_start,
        "test_end": test_end,
        "source_unchanged": "ja",
    }


def write_summary(results: list[dict[str, object]]) -> None:
    total_source = sum(int(row["source_rows"]) for row in results)
    total_train = sum(int(row["train_rows"]) for row in results)
    total_test = sum(int(row["test_rows"]) for row in results)

    lines = [
        "# Train/test-splitt av voyage-rådata 2025",
        "",
        "Denne filen dokumenterer kronologisk 80/20-splitt av de åtte anonymiserte voyage-råfilene i `004 data`.",
        "",
        "Splitten er laget på råfilnivå som grunnlag for eventuell separat train/test-rensing og -strukturering. Originalfilene er beholdt urørt, og nye filer er skrevet med suffiksene `_train_80.csv` og `_test_20.csv`.",
        "",
        "## Metode",
        "",
        "- Hver råfil er splittet separat.",
        "- Radene er sortert etter kombinert `Date_UTC` og `Time_UTC`.",
        "- De tidligste 80 % av radene er lagt i train.",
        "- De siste 20 % av radene er lagt i test.",
        "- Split-indeks er beregnet som `int(antall_rader * 0.8)`.",
        "",
        "## Oppsummering",
        "",
        f"- Råfiler splittet: {len(results)}",
        f"- Totalt antall rå rader: {total_source}",
        f"- Totalt antall train-rader: {total_train}",
        f"- Totalt antall test-rader: {total_test}",
        "",
        "## Splitt per fil",
        "",
        "| Kilde | Rå rader | Train-fil | Train-rader | Train-periode | Test-fil | Test-rader | Test-periode | Original urørt |",
        "| --- | ---: | --- | ---: | --- | --- | ---: | --- | --- |",
    ]

    for row in results:
        train_period = f"{row['train_start']} til {row['train_end']}"
        test_period = f"{row['test_start']} til {row['test_end']}"
        lines.append(
            f"| `{row['source_file']}` | {row['source_rows']} | `{row['train_file']}` | "
            f"{row['train_rows']} | {train_period} | `{row['test_file']}` | "
            f"{row['test_rows']} | {test_period} | {row['source_unchanged']} |"
        )

    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    sources = sorted(path for path in DATA_DIR.glob("C*.csv") if is_raw_voyage_file(path))
    results = [split_file(path) for path in sources]
    write_summary(results)

    print(f"source_files={len(results)}")
    print(f"train_files={len(results)}")
    print(f"test_files={len(results)}")
    print(f"summary_md={SUMMARY_MD}")


if __name__ == "__main__":
    main()
