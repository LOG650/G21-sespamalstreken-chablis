"""Valider modellresultater mot observerte ROB-baserte bunkringshendelser."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ACTIVITY_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ACTIVITY_DIR / "output"
METADATA_DIR = ACTIVITY_DIR / "metadata"

VOYAGE_LEGS_CSV = (
    ROOT
    / "006 analysis"
    / "01_datagrunnlag"
    / "03_strukturering_av_datasett"
    / "data"
    / "tab_voyage_legs_2025.csv"
)
MODEL_BY_LEG_CSV = (
    ROOT
    / "006 analysis"
    / "02_modellutvikling"
    / "04_implementere_modell"
    / "output"
    / "res_route_inventory_by_leg.csv"
)

VALIDATION_SUMMARY_JSON = OUTPUT_DIR / "res_operational_validation_summary.json"
VALIDATION_BY_VESSEL_CSV = OUTPUT_DIR / "res_operational_validation_by_vessel.csv"
VALIDATION_BY_LEG_CSV = OUTPUT_DIR / "res_operational_validation_by_leg.csv"
VALIDATION_MD = METADATA_DIR / "res_operational_validation_summary.md"

QTY_TOL = 1e-6


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"Kan ikke skrive tom tabell til `{relative(path)}`.")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def as_float(row: dict[str, str], column: str) -> float:
    value = row.get(column, "")
    return 0.0 if value == "" else float(value)


def as_int(row: dict[str, str], column: str) -> int:
    value = row.get(column, "")
    return 0 if value == "" else int(float(value))


def rounded(value: float, digits: int = 2) -> float:
    return round(value, digits)


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def format_number(value: float) -> str:
    return f"{value:,.2f}".replace(",", " ").replace(".", ",")


def format_percent(value: float | None) -> str:
    if value is None:
        return "ikke beregnet"
    return f"{value * 100:.2f}".replace(".", ",") + " %"


def safe_ratio(numerator: float, denominator: float) -> float | None:
    if abs(denominator) <= QTY_TOL:
        return None
    return numerator / denominator


def build_leg_rows() -> list[dict[str, object]]:
    voyage_rows = read_csv(VOYAGE_LEGS_CSV)
    model_rows = read_csv(MODEL_BY_LEG_CSV)
    model_by_key = {
        (row["vessel_file_id"], int(row["leg_sequence"])): row for row in model_rows
    }

    validation_rows: list[dict[str, object]] = []
    missing_model_keys: list[tuple[str, int]] = []

    for voyage in voyage_rows:
        key = (voyage["vessel_file_id"], int(voyage["leg_sequence"]))
        model = model_by_key.get(key)
        if model is None:
            missing_model_keys.append(key)
            continue

        consumption = as_float(voyage, "fuel_consumption_total")
        rob_start = as_float(voyage, "rob_start")
        rob_end = as_float(voyage, "rob_end")
        observed_bunker_event = as_int(voyage, "bunkering_inferred") == 1
        inferred_bunker_qty = (
            max(0.0, rob_end - rob_start + consumption) if observed_bunker_event else 0.0
        )

        model_purchase_qty = as_float(model, "model_purchase_qty")
        model_external_qty = as_float(model, "model_external_qty")
        model_total_bunker_qty = model_purchase_qty + model_external_qty
        model_bunker_event = model_total_bunker_qty > QTY_TOL
        model_priced_event = model_purchase_qty > QTY_TOL
        available_priced_event = model.get("available_priced_ports", "") != ""

        validation_rows.append(
            {
                "vessel_file_id": voyage["vessel_file_id"],
                "vessel_class": voyage["vessel_class"],
                "leg_sequence": int(voyage["leg_sequence"]),
                "period_month": voyage["period_month"],
                "voyage_number": voyage["voyage_number"],
                "from_port": voyage["from_port_P00X"],
                "to_port": voyage["to_port_P00X"],
                "available_priced_ports": model.get("available_priced_ports", ""),
                "observed_bunker_event": int(observed_bunker_event),
                "observed_bunker_qty_estimate": rounded(inferred_bunker_qty),
                "model_bunker_event": int(model_bunker_event),
                "model_priced_event": int(model_priced_event),
                "available_priced_event": int(available_priced_event),
                "model_purchase_qty": rounded(model_purchase_qty),
                "model_external_qty": rounded(model_external_qty),
                "model_total_bunker_qty": rounded(model_total_bunker_qty),
                "qty_difference_model_minus_observed": rounded(
                    model_total_bunker_qty - inferred_bunker_qty
                ),
                "absolute_qty_difference": rounded(
                    abs(model_total_bunker_qty - inferred_bunker_qty)
                ),
                "model_inventory_end": rounded(as_float(model, "model_inventory_end")),
                "observed_rob_end": rounded(rob_end),
                "inventory_end_minus_observed": rounded(
                    as_float(model, "inventory_end_minus_observed")
                ),
            }
        )

    if missing_model_keys:
        raise ValueError(f"Mangler modellrader for {len(missing_model_keys)} voyage-etapper.")
    return validation_rows


def aggregate_by_vessel(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    aggregates: dict[str, dict[str, float | str]] = {}
    for row in rows:
        vessel = str(row["vessel_file_id"])
        values = aggregates.setdefault(
            vessel,
            {
                "vessel_file_id": vessel,
                "vessel_class": str(row["vessel_class"]),
                "leg_count": 0.0,
                "observed_bunker_events": 0.0,
                "model_bunker_events": 0.0,
                "overlap_bunker_events": 0.0,
                "observed_bunker_qty_estimate": 0.0,
                "model_total_bunker_qty": 0.0,
                "model_purchase_qty": 0.0,
                "model_external_qty": 0.0,
                "absolute_qty_difference": 0.0,
                "absolute_inventory_end_difference": 0.0,
                "priced_legs_with_observed_bunkering": 0.0,
                "priced_legs_with_model_purchase": 0.0,
            },
        )
        observed_event = float(row["observed_bunker_event"])
        model_event = float(row["model_bunker_event"])
        values["leg_count"] = float(values["leg_count"]) + 1
        values["observed_bunker_events"] = (
            float(values["observed_bunker_events"]) + observed_event
        )
        values["model_bunker_events"] = float(values["model_bunker_events"]) + model_event
        values["overlap_bunker_events"] = (
            float(values["overlap_bunker_events"])
            + (1.0 if observed_event and model_event else 0.0)
        )
        values["observed_bunker_qty_estimate"] = float(
            values["observed_bunker_qty_estimate"]
        ) + float(row["observed_bunker_qty_estimate"])
        values["model_total_bunker_qty"] = float(values["model_total_bunker_qty"]) + float(
            row["model_total_bunker_qty"]
        )
        values["model_purchase_qty"] = float(values["model_purchase_qty"]) + float(
            row["model_purchase_qty"]
        )
        values["model_external_qty"] = float(values["model_external_qty"]) + float(
            row["model_external_qty"]
        )
        values["absolute_qty_difference"] = float(values["absolute_qty_difference"]) + float(
            row["absolute_qty_difference"]
        )
        values["absolute_inventory_end_difference"] = float(
            values["absolute_inventory_end_difference"]
        ) + abs(float(row["inventory_end_minus_observed"]))
        values["priced_legs_with_observed_bunkering"] = float(
            values["priced_legs_with_observed_bunkering"]
        ) + (
            1.0
            if float(row["available_priced_event"]) and observed_event
            else 0.0
        )
        values["priced_legs_with_model_purchase"] = float(
            values["priced_legs_with_model_purchase"]
        ) + (
            1.0 if float(row["available_priced_event"]) and float(row["model_priced_event"]) else 0.0
        )

    output_rows: list[dict[str, object]] = []
    for values in aggregates.values():
        observed_events = float(values["observed_bunker_events"])
        model_events = float(values["model_bunker_events"])
        overlap_events = float(values["overlap_bunker_events"])
        leg_count = float(values["leg_count"])
        observed_qty = float(values["observed_bunker_qty_estimate"])
        model_qty = float(values["model_total_bunker_qty"])
        output_rows.append(
            {
                "vessel_file_id": values["vessel_file_id"],
                "vessel_class": values["vessel_class"],
                "leg_count": int(leg_count),
                "observed_bunker_events": int(observed_events),
                "model_bunker_events": int(model_events),
                "overlap_bunker_events": int(overlap_events),
                "event_precision": rounded(safe_ratio(overlap_events, model_events) or 0.0, 4),
                "event_recall": rounded(safe_ratio(overlap_events, observed_events) or 0.0, 4),
                "observed_bunker_qty_estimate": rounded(observed_qty),
                "model_total_bunker_qty": rounded(model_qty),
                "model_purchase_qty": rounded(float(values["model_purchase_qty"])),
                "model_external_qty": rounded(float(values["model_external_qty"])),
                "model_qty_to_observed_qty_ratio": rounded(
                    safe_ratio(model_qty, observed_qty) or 0.0, 4
                ),
                "sum_absolute_qty_difference": rounded(float(values["absolute_qty_difference"])),
                "mean_absolute_inventory_end_difference": rounded(
                    float(values["absolute_inventory_end_difference"]) / leg_count
                ),
                "priced_legs_with_observed_bunkering": int(
                    float(values["priced_legs_with_observed_bunkering"])
                ),
                "priced_legs_with_model_purchase": int(
                    float(values["priced_legs_with_model_purchase"])
                ),
            }
        )
    return sorted(output_rows, key=lambda row: str(row["vessel_file_id"]))


def build_summary(rows: list[dict[str, object]], by_vessel: list[dict[str, object]]) -> dict[str, object]:
    observed_events = sum(int(row["observed_bunker_event"]) for row in rows)
    model_events = sum(int(row["model_bunker_event"]) for row in rows)
    overlap_events = sum(
        1
        for row in rows
        if int(row["observed_bunker_event"]) == 1 and int(row["model_bunker_event"]) == 1
    )
    observed_qty = sum(float(row["observed_bunker_qty_estimate"]) for row in rows)
    model_qty = sum(float(row["model_total_bunker_qty"]) for row in rows)
    model_purchase_qty = sum(float(row["model_purchase_qty"]) for row in rows)
    model_external_qty = sum(float(row["model_external_qty"]) for row in rows)
    priced_observed_events = sum(
        1
        for row in rows
        if int(row["available_priced_event"]) == 1 and int(row["observed_bunker_event"]) == 1
    )
    priced_model_events = sum(
        1
        for row in rows
        if int(row["available_priced_event"]) == 1 and int(row["model_priced_event"]) == 1
    )
    inventory_mae = sum(abs(float(row["inventory_end_minus_observed"])) for row in rows) / len(
        rows
    )
    top_observed_vessel = max(
        by_vessel, key=lambda row: float(row["observed_bunker_qty_estimate"])
    )
    top_model_vessel = max(by_vessel, key=lambda row: float(row["model_total_bunker_qty"]))

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "analysis_name": "operational_validation_against_observed_bunkering",
        "source_files": {
            "voyage_legs": relative(VOYAGE_LEGS_CSV),
            "model_by_leg": relative(MODEL_BY_LEG_CSV),
        },
        "output_files": {
            "summary": relative(VALIDATION_SUMMARY_JSON),
            "by_vessel": relative(VALIDATION_BY_VESSEL_CSV),
            "by_leg": relative(VALIDATION_BY_LEG_CSV),
            "metadata": relative(VALIDATION_MD),
        },
        "leg_count": len(rows),
        "vessel_file_count": len(by_vessel),
        "observed_bunker_events": observed_events,
        "model_bunker_events": model_events,
        "overlap_bunker_events": overlap_events,
        "event_precision": safe_ratio(overlap_events, model_events),
        "event_recall": safe_ratio(overlap_events, observed_events),
        "observed_bunker_qty_estimate": observed_qty,
        "model_total_bunker_qty": model_qty,
        "model_purchase_qty": model_purchase_qty,
        "model_external_qty": model_external_qty,
        "model_qty_to_observed_qty_ratio": safe_ratio(model_qty, observed_qty),
        "priced_legs_with_observed_bunkering": priced_observed_events,
        "priced_legs_with_model_purchase": priced_model_events,
        "mean_absolute_inventory_end_difference": inventory_mae,
        "top_observed_bunker_vessel": top_observed_vessel["vessel_file_id"],
        "top_model_bunker_vessel": top_model_vessel["vessel_file_id"],
        "method_note": (
            "Observerte bunkringsmengder er estimert fra ROB-endring + forbruk per etappe. "
            "Dette er en operativ kontroll av timing og volum, ikke en økonomisk backtest av faktisk innkjøpskostnad."
        ),
    }


def write_markdown(summary: dict[str, object], by_vessel: list[dict[str, object]]) -> None:
    lines = [
        "# Operativ validering mot observerte bunkringshendelser",
        "",
        "Denne analysen sammenligner modellens bunkringsbeslutninger med observerte ROB-baserte bunkringshendelser i de strukturerte voyage-dataene for 2025.",
        "",
        "Observert bunkringshendelse hentes fra `bunkering_inferred` i de strukturerte voyage-dataene. For slike hendelser estimeres observert bunkringsmengde som positiv økning i beholdning etter justering for forbruk på etappen: `max(0, ROB_slutt - ROB_start + forbruk)`. Dette gir en praktisk kontroll av modellens timing og volum, men ikke en full økonomisk backtest mot faktiske innkjøpspriser.",
        "",
        "## Hovedtall",
        "",
        f"- Voyage-etapper: {summary['leg_count']}",
        f"- Observerte bunkringshendelser: {summary['observed_bunker_events']}",
        f"- Modellhendelser med bunkring: {summary['model_bunker_events']}",
        f"- Overlappende hendelser: {summary['overlap_bunker_events']}",
        f"- Event precision: {format_percent(summary['event_precision'])}",
        f"- Event recall: {format_percent(summary['event_recall'])}",
        f"- Estimert observert bunkringsmengde: {format_number(summary['observed_bunker_qty_estimate'])}",
        f"- Modellert total bunkringsmengde: {format_number(summary['model_total_bunker_qty'])}",
        f"- Modellert mengde som andel av observert estimat: {format_percent(summary['model_qty_to_observed_qty_ratio'])}",
        f"- Gjennomsnittlig absolutt avvik mellom modellert sluttbeholdning og observert ROB-slutt: {format_number(summary['mean_absolute_inventory_end_difference'])}",
        "",
        "## Tolkning",
        "",
        "Modellen treffer ikke nødvendigvis de samme bunkringstidspunktene som observert praksis, fordi den er formulert som en kostnadsminimerende beslutningsmodell og ikke som en modell for å gjenskape historiske beslutninger. Avvik mellom observerte og modellerte hendelser er derfor forventet.",
        "",
        "Valideringen er likevel nyttig fordi den viser om modellens samlede bunkringsmengde og beholdningsutvikling ligger i en operativt rimelig størrelsesorden. Dersom modellen hadde gitt svært få hendelser, ekstremt høye mengder eller systematiske brudd mot observert beholdningsnivå, ville det indikert svakere operativ relevans.",
        "",
        "## Resultat per fartøyfil",
        "",
        "| Fartøyfil | Observerte hendelser | Modellhendelser | Overlapp | Observert mengde | Modellert mengde | Modell/observert | Beholdningsavvik MAE |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in by_vessel:
        lines.append(
            "| {vessel_file_id} | {observed_bunker_events} | {model_bunker_events} | {overlap_bunker_events} | {observed_qty} | {model_qty} | {ratio} | {mae} |".format(
                vessel_file_id=row["vessel_file_id"],
                observed_bunker_events=row["observed_bunker_events"],
                model_bunker_events=row["model_bunker_events"],
                overlap_bunker_events=row["overlap_bunker_events"],
                observed_qty=format_number(float(row["observed_bunker_qty_estimate"])),
                model_qty=format_number(float(row["model_total_bunker_qty"])),
                ratio=format_percent(float(row["model_qty_to_observed_qty_ratio"])),
                mae=format_number(float(row["mean_absolute_inventory_end_difference"])),
            )
        )
    lines.extend(
        [
            "",
            "<p align=\"center\" style=\"font-size: 0.9em;\"><small><i>Tabell V.1 Operativ validering av modellert bunkring mot observerte ROB-baserte bunkringshendelser.</i></small></p>",
        ]
    )
    VALIDATION_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    leg_rows = build_leg_rows()
    by_vessel = aggregate_by_vessel(leg_rows)
    summary = build_summary(leg_rows, by_vessel)

    write_csv(VALIDATION_BY_LEG_CSV, leg_rows)
    write_csv(VALIDATION_BY_VESSEL_CSV, by_vessel)
    VALIDATION_SUMMARY_JSON.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_markdown(summary, by_vessel)

    print("Operativ validering er generert.")
    print(f"Etapper: {summary['leg_count']}")
    print(f"Observerte hendelser: {summary['observed_bunker_events']}")
    print(f"Modellhendelser: {summary['model_bunker_events']}")
    print(f"Modell/observert mengderatio: {summary['model_qty_to_observed_qty_ratio']:.4f}")


if __name__ == "__main__":
    main()
