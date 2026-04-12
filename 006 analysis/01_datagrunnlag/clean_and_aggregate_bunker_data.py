from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "004 data" / "Bunker Lifting List(Worksheet1) (1).csv"
OUT_DIR = Path(__file__).resolve().parent
CLEANED_CSV = OUT_DIR / "tab_bunker_cleaned.csv"
MONTHLY_CSV = OUT_DIR / "tab_bunker_monthly_by_port.csv"
SUMMARY_MD = OUT_DIR / "tab_bunker_summary.md"


def parse_number(value: str | None) -> float | None:
    if value is None:
        return None
    cleaned = value.strip().replace(" ", "").replace("\xa0", "").replace(",", ".")
    if cleaned == "":
        return None
    return float(cleaned)


def parse_date(value: str) -> datetime:
    return datetime.strptime(value.strip(), "%d.%m.%Y")


def read_rows() -> list[dict[str, str]]:
    with SOURCE.open(encoding="cp1252", newline="") as handle:
        lines = handle.read().splitlines()

    header_idx = next(
        i for i, line in enumerate(lines) if line.startswith("Purchase Status;Requirement ID;")
    )
    reader = csv.DictReader(lines[header_idx:], delimiter=";")

    rows: list[dict[str, str]] = []
    for row in reader:
        status = (row.get("Purchase Status") or "").strip()
        if status in {"", '"'}:
            continue
        rows.append(row)
    return rows


def clean_rows(rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], dict[str, int]]:
    cleaned: list[dict[str, object]] = []
    counters = defaultdict(int)

    for row in rows:
        delivery_date = parse_date(row["Delivery Date"])
        ordered_qty = parse_number(row["Ordered Qty"])
        invoiced_qty = parse_number(row["Invoiced Qty"])
        order_price = parse_number(row["Order Price"])
        invoice_price = parse_number(row["Invoice Price"])

        qty = invoiced_qty if invoiced_qty is not None else ordered_qty
        price = invoice_price if invoice_price is not None else order_price

        if invoiced_qty is None and ordered_qty is not None:
            counters["fallback_ordered_qty"] += 1
        if invoice_price is None and order_price is not None:
            counters["fallback_order_price"] += 1
        if qty is None or price is None:
            counters["dropped_missing_qty_or_price"] += 1
            continue
        if qty <= 0:
            counters["dropped_non_positive_qty"] += 1
            continue
        if price <= 0:
            counters["dropped_non_positive_price"] += 1
            continue

        cleaned.append(
            {
                "purchase_status": row["Purchase Status"].strip(),
                "requirement_id": row["Requirement ID"].strip(),
                "vessel": row["Vessel"].strip(),
                "voyage_no": row["Voyage No."].strip(),
                "port": row["Port"].strip(),
                "fuel_type": row["Fuel Type"].strip(),
                "delivery_date": delivery_date.date().isoformat(),
                "delivery_month": delivery_date.strftime("%Y-%m"),
                "delivery_year": delivery_date.strftime("%Y"),
                "vendor": (row.get("Vendor") or "").strip(),
                "supplier": (row.get("Supplier") or "").strip(),
                "ordered_qty": ordered_qty,
                "invoiced_qty": invoiced_qty,
                "effective_qty": qty,
                "order_price": order_price,
                "invoice_price": invoice_price,
                "effective_price": price,
                "cost_value": qty * price,
            }
        )

    return cleaned, dict(counters)


def write_cleaned_csv(rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with CLEANED_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def aggregate_monthly(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], dict[str, object]] = {}

    for row in rows:
        key = (str(row["delivery_month"]), str(row["port"]))
        if key not in grouped:
            grouped[key] = {
                "delivery_month": row["delivery_month"],
                "port": row["port"],
                "transaction_count": 0,
                "total_qty": 0.0,
                "total_cost_proxy": 0.0,
                "price_sum": 0.0,
                "min_price": float(row["effective_price"]),
                "max_price": float(row["effective_price"]),
                "unique_vessels": set(),
                "unique_suppliers": set(),
            }

        bucket = grouped[key]
        price = float(row["effective_price"])
        qty = float(row["effective_qty"])
        bucket["transaction_count"] += 1
        bucket["total_qty"] += qty
        bucket["total_cost_proxy"] += qty * price
        bucket["price_sum"] += price
        bucket["min_price"] = min(float(bucket["min_price"]), price)
        bucket["max_price"] = max(float(bucket["max_price"]), price)
        bucket["unique_vessels"].add(str(row["vessel"]))
        supplier = str(row["supplier"]).strip()
        if supplier:
            bucket["unique_suppliers"].add(supplier)

    aggregated: list[dict[str, object]] = []
    for key in sorted(grouped):
        bucket = grouped[key]
        total_qty = float(bucket["total_qty"])
        transaction_count = int(bucket["transaction_count"])
        aggregated.append(
            {
                "delivery_month": bucket["delivery_month"],
                "port": bucket["port"],
                "transaction_count": transaction_count,
                "total_qty": round(total_qty, 2),
                "weighted_avg_price": round(float(bucket["total_cost_proxy"]) / total_qty, 2),
                "simple_avg_price": round(float(bucket["price_sum"]) / transaction_count, 2),
                "min_price": round(float(bucket["min_price"]), 2),
                "max_price": round(float(bucket["max_price"]), 2),
                "unique_vessels": len(bucket["unique_vessels"]),
                "unique_suppliers": len(bucket["unique_suppliers"]),
            }
        )
    return aggregated


def write_monthly_csv(rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with MONTHLY_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_summary_md(
    raw_rows: list[dict[str, str]],
    cleaned_rows: list[dict[str, object]],
    monthly_rows: list[dict[str, object]],
    counters: dict[str, int],
) -> None:
    ports = sorted({str(row["port"]) for row in cleaned_rows})
    months = sorted({str(row["delivery_month"]) for row in cleaned_rows})
    by_port: dict[str, dict[str, float]] = defaultdict(lambda: {"n": 0, "qty": 0.0, "cost": 0.0})
    for row in cleaned_rows:
        port = str(row["port"])
        qty = float(row["effective_qty"])
        price = float(row["effective_price"])
        by_port[port]["n"] += 1
        by_port[port]["qty"] += qty
        by_port[port]["cost"] += qty * price

    lines = [
        "# Oppsummering av renset bunkringsdata",
        "",
        f"- Rå observasjoner lest inn: {len(raw_rows)}",
        f"- Rensede observasjoner beholdt: {len(cleaned_rows)}",
        f"- Månedlige aggregater opprettet: {len(monthly_rows)}",
        f"- Antall havner: {len(ports)} ({', '.join(ports)})",
        f"- Antall måneder i aggregatet: {len(months)}",
        "",
        "## Rensevalg",
        "",
        f"- `Invoiced Qty` brukes som hovedvolum, med fallback til `Ordered Qty`: {counters.get('fallback_ordered_qty', 0)} observasjoner",
        f"- `Invoice Price` brukes som hovedpris, med fallback til `Order Price`: {counters.get('fallback_order_price', 0)} observasjoner",
        f"- Forkastet på grunn av manglende pris eller volum etter fallback: {counters.get('dropped_missing_qty_or_price', 0)} observasjoner",
        f"- Forkastet på grunn av ikke-positivt volum: {counters.get('dropped_non_positive_qty', 0)} observasjoner",
        f"- Forkastet på grunn av ikke-positiv pris: {counters.get('dropped_non_positive_price', 0)} observasjoner",
        "",
        "## Aggregert oversikt per havn",
        "",
        "| Havn | Observasjoner | Total mengde | Vektet snittpris |",
        "| --- | --- | --- | --- |",
    ]

    for port in sorted(by_port):
        stats = by_port[port]
        weighted = stats["cost"] / stats["qty"]
        lines.append(
            f"| {port} | {int(stats['n'])} | {stats['qty']:.2f} | {weighted:.2f} |"
        )

    lines.extend(
        [
            "",
            "## Filer",
            "",
            f"- `tab_bunker_cleaned.csv`: renset transaksjonsnivå",
            f"- `tab_bunker_monthly_by_port.csv`: aggregert per havn og måned",
        ]
    )

    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    raw_rows = read_rows()
    cleaned_rows, counters = clean_rows(raw_rows)
    monthly_rows = aggregate_monthly(cleaned_rows)
    write_cleaned_csv(cleaned_rows)
    write_monthly_csv(monthly_rows)
    write_summary_md(raw_rows, cleaned_rows, monthly_rows, counters)
    print(f"cleaned_rows={len(cleaned_rows)}")
    print(f"monthly_rows={len(monthly_rows)}")
    print(f"cleaned_csv={CLEANED_CSV}")
    print(f"monthly_csv={MONTHLY_CSV}")


if __name__ == "__main__":
    main()
