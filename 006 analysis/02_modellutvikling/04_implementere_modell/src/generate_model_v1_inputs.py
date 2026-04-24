from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SOURCE = (
    ROOT
    / "006 analysis"
    / "01_datagrunnlag"
    / "03_strukturering_av_datasett"
    / "data"
    / "tab_bunker_monthly_by_port.csv"
)
ACTIVITY_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = ACTIVITY_DIR / "input"

PRICE_CSV = INPUT_DIR / "tab_model_v1_price_by_port_month.csv"
DEMAND_CSV = INPUT_DIR / "tab_model_v1_demand_by_month.csv"
AVAILABILITY_CSV = INPUT_DIR / "tab_model_v1_availability_by_port_month.csv"
PARAMETERS_JSON = INPUT_DIR / "data_model_v1_parameters.json"
README_MD = ACTIVITY_DIR / "README_model_v1.md"


def read_monthly_rows() -> list[dict[str, str]]:
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_outputs(rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    months = sorted({row["delivery_month"] for row in rows})
    ports = sorted({row["port"] for row in rows})

    observed = {(row["delivery_month"], row["port"]): row for row in rows}

    port_price_sum = defaultdict(float)
    port_qty_sum = defaultdict(float)
    for row in rows:
        port = row["port"]
        price = float(row["weighted_avg_price"])
        qty = float(row["total_qty"])
        port_price_sum[port] += price * qty
        port_qty_sum[port] += qty

    port_fallback_price = {
        port: round(port_price_sum[port] / port_qty_sum[port], 2) for port in ports
    }

    demand_rows: list[dict[str, object]] = []
    availability_rows: list[dict[str, object]] = []
    price_rows: list[dict[str, object]] = []

    for month in months:
        month_total_qty = 0.0
        observed_ports = 0
        for port in ports:
            key = (month, port)
            row = observed.get(key)
            available = 1 if row else 0
            availability_rows.append(
                {
                    "delivery_month": month,
                    "port": port,
                    "available_flag": available,
                }
            )

            if row:
                price = round(float(row["weighted_avg_price"]), 2)
                source = "observed"
                month_total_qty += float(row["total_qty"])
                observed_ports += 1
            else:
                price = port_fallback_price[port]
                source = "imputed_port_average"

            price_rows.append(
                {
                    "delivery_month": month,
                    "port": port,
                    "price_value": price,
                    "price_source": source,
                }
            )

        demand_rows.append(
            {
                "delivery_month": month,
                "demand_qty": round(month_total_qty, 2),
                "observed_port_count": observed_ports,
            }
        )

    parameters = {
        "model_version": "v1",
        "description": "Forenklet kostnadsminimeringsmodell basert på havn og måned.",
        "source_file": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "sets": {
            "ports": ports,
            "months": months,
        },
        "parameter_files": {
            "prices": str(PRICE_CSV.relative_to(ROOT)).replace("\\", "/"),
            "demand": str(DEMAND_CSV.relative_to(ROOT)).replace("\\", "/"),
            "availability": str(AVAILABILITY_CSV.relative_to(ROOT)).replace("\\", "/"),
        },
        "price_fallback_rule": "Hvis en havn mangler observasjon i en måned, brukes havnens vektede gjennomsnittspris over hele analyseperioden.",
        "demand_rule": "Månedlig behov settes lik samlet observert bunkret mengde på tvers av de fire havnene i perioden.",
        "availability_rule": "available_flag = 1 hvis havnen har observert transaksjon i måneden, ellers 0.",
        "big_m_default": 1000000,
        "port_fallback_price": port_fallback_price,
    }

    return price_rows, demand_rows, availability_rows, parameters


def write_json(path: Path, data: dict[str, object]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_readme(parameters: dict[str, object]) -> None:
    ports = ", ".join(parameters["sets"]["ports"])
    months = parameters["sets"]["months"]
    content = "\n".join(
        [
            "# Modellinput for modellversjon 1",
            "",
            "Denne mappen inneholder modellparametere som hører til den forenklede modellversjon 1 beskrevet i `005 report/Kaylee_rapport.md`.",
            "",
            "## Filer",
            "",
            "- `tab_model_v1_price_by_port_month.csv`: prisparameter `p[h,t]`",
            "- `tab_model_v1_demand_by_month.csv`: behovsparameter `D[t]`",
            "- `tab_model_v1_availability_by_port_month.csv`: tilgjengelighetsparameter `f[h,t]`",
            "- `data_model_v1_parameters.json`: samlet metadata og parameterbeskrivelse",
            "",
            "## Definisjon",
            "",
            f"- Havner: {ports}",
            f"- Perioder: {months[0]} til {months[-1]}",
            f"- Prisregel ved manglende observasjon: {parameters['price_fallback_rule']}",
            f"- Behovsregel: {parameters['demand_rule']}",
            f"- Tilgjengelighetsregel: {parameters['availability_rule']}",
            "",
            "Filnavnene starter med `tab_model_v1_` eller `data_model_v1_` for å gjøre det enkelt å se at de tilhører modellversjon 1.",
            "",
        ]
    )
    README_MD.write_text(content, encoding="utf-8")


def main() -> None:
    rows = read_monthly_rows()
    price_rows, demand_rows, availability_rows, parameters = build_outputs(rows)

    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(PRICE_CSV, price_rows)
    write_csv(DEMAND_CSV, demand_rows)
    write_csv(AVAILABILITY_CSV, availability_rows)
    write_json(PARAMETERS_JSON, parameters)
    write_readme(parameters)

    print(f"prices={PRICE_CSV}")
    print(f"demand={DEMAND_CSV}")
    print(f"availability={AVAILABILITY_CSV}")
    print(f"json={PARAMETERS_JSON}")


if __name__ == "__main__":
    main()
