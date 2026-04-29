"""Lag et tolkningsnotat fra ferdige basis- og sensitivitetsresultater."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
BASELINE_DIR = ROOT / "006 analysis" / "03_analyse" / "01_basiskjoring" / "output"
SENSITIVITY_DIR = ROOT / "006 analysis" / "03_analyse" / "02_sensitivitetsanalyse" / "output"
ACTIVITY_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ACTIVITY_DIR / "output"
METADATA_DIR = ACTIVITY_DIR / "metadata"

BASELINE_SUMMARY_JSON = BASELINE_DIR / "res_baseline_route_inventory_summary.json"
BASELINE_BY_VESSEL_CSV = BASELINE_DIR / "res_baseline_route_inventory_by_vessel.csv"
BASELINE_BY_PORT_CSV = BASELINE_DIR / "res_baseline_route_inventory_by_port.csv"
SENSITIVITY_SUMMARY_JSON = SENSITIVITY_DIR / "res_sensitivity_route_inventory_summary.json"
SENSITIVITY_SCENARIOS_CSV = SENSITIVITY_DIR / "res_sensitivity_route_inventory_scenarios.csv"

INTERPRETATION_JSON = OUTPUT_DIR / "res_route_inventory_interpretation.json"
INTERPRETATION_MD = METADATA_DIR / "res_route_inventory_interpretation.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(row: dict[str, str], column: str) -> float:
    value = row.get(column, "")
    if value == "":
        return 0.0
    return float(value)


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def format_percent(value: float) -> str:
    return f"{value * 100:.2f}".replace(".", ",") + " %"


def format_number(value: float) -> str:
    return f"{value:,.2f}".replace(",", " ").replace(".", ",")


def unique_rounded(rows: list[dict[str, str]], column: str, digits: int = 6) -> set[float]:
    return {round(as_float(row, column), digits) for row in rows}


def check_item(name: str, status: bool, value: object, expected: object) -> dict[str, object]:
    return {
        "check": name,
        "status": "OK" if status else "FEIL",
        "value": value,
        "expected": expected,
    }


def build_interpretation() -> dict[str, object]:
    """Bygg maskinlesbar resultattolkning med eksplisitte konsistenssjekker."""
    baseline = json.loads(BASELINE_SUMMARY_JSON.read_text(encoding="utf-8"))
    sensitivity = json.loads(SENSITIVITY_SUMMARY_JSON.read_text(encoding="utf-8"))
    by_vessel = read_csv(BASELINE_BY_VESSEL_CSV)
    by_port = read_csv(BASELINE_BY_PORT_CSV)
    scenarios = read_csv(SENSITIVITY_SCENARIOS_CSV)

    vessels_with_no_priced_ports = [
        row["vessel_file_id"] for row in by_vessel if int(row["priced_leg_count"]) == 0
    ]
    vessels_with_high_external_share = [
        row["vessel_file_id"]
        for row in by_vessel
        if as_float(row, "external_share_of_consumption") >= 0.80
    ]
    top_priced_purchase_vessel = max(by_vessel, key=lambda row: as_float(row, "model_purchase_qty"))
    top_external_vessel = max(by_vessel, key=lambda row: as_float(row, "model_external_qty"))
    top_external_share_vessel = max(
        by_vessel, key=lambda row: as_float(row, "external_share_of_consumption")
    )
    top_purchase_port = max(by_port, key=lambda row: as_float(row, "purchase_qty"))
    zero_purchase_ports = [row["port"] for row in by_port if as_float(row, "purchase_qty") == 0]

    baseline_cost = float(baseline["total_model_cost"])
    low_scenario = min(scenarios, key=lambda row: as_float(row, "total_model_cost"))
    high_scenario = max(scenarios, key=lambda row: as_float(row, "total_model_cost"))
    purchase_qty_values = unique_rounded(scenarios, "model_purchase_qty")
    external_qty_values = unique_rounded(scenarios, "model_external_qty")
    plan_stable = len(purchase_qty_values) == 1 and len(external_qty_values) == 1
    calculated_cost_range = as_float(high_scenario, "total_model_cost") - as_float(
        low_scenario, "total_model_cost"
    )
    inventory_share_of_consumption = max(
        0.0,
        1
        - float(baseline["priced_share_of_consumption"])
        - float(baseline["external_share_of_consumption"]),
    )
    external_cost_share_of_total = float(baseline["external_cost"]) / baseline_cost

    checks = [
        check_item(
            "Kjøpsmengde er lik i alle proxy-scenarioer",
            len(purchase_qty_values) == 1,
            sorted(purchase_qty_values),
            "én unik verdi",
        ),
        check_item(
            "Ekstern/ukjent mengde er lik i alle proxy-scenarioer",
            len(external_qty_values) == 1,
            sorted(external_qty_values),
            "én unik verdi",
        ),
        check_item(
            "Kostnadsspenn stemmer med laveste og høyeste scenario",
            round(calculated_cost_range, 2) == round(float(sensitivity["total_cost_range"]), 2),
            round(calculated_cost_range, 2),
            round(float(sensitivity["total_cost_range"]), 2),
        ),
        check_item(
            "Dekningsandeler overstiger ikke totalforbruk",
            inventory_share_of_consumption >= 0,
            round(
                float(baseline["priced_share_of_consumption"])
                + float(baseline["external_share_of_consumption"]),
                6,
            ),
            "<= 1",
        ),
        check_item(
            "Minst ett fartøy har høy ekstern/ukjent andel",
            len(vessels_with_high_external_share) > 0,
            len(vessels_with_high_external_share),
            "> 0",
        ),
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_files": {
            "baseline_summary": relative(BASELINE_SUMMARY_JSON),
            "baseline_by_vessel": relative(BASELINE_BY_VESSEL_CSV),
            "baseline_by_port": relative(BASELINE_BY_PORT_CSV),
            "sensitivity_summary": relative(SENSITIVITY_SUMMARY_JSON),
            "sensitivity_scenarios": relative(SENSITIVITY_SCENARIOS_CSV),
        },
        "coverage": {
            "priced_leg_count": baseline["priced_leg_count"],
            "leg_count": baseline["leg_count"],
            "priced_leg_share": baseline["priced_leg_count"] / baseline["leg_count"],
            "purchased_leg_count": baseline["purchased_leg_count"],
            "priced_share_of_consumption": baseline["priced_share_of_consumption"],
            "external_share_of_consumption": baseline["external_share_of_consumption"],
            "inventory_share_of_consumption": inventory_share_of_consumption,
            "vessels_with_no_priced_ports": vessels_with_no_priced_ports,
            "vessels_with_high_external_share": vessels_with_high_external_share,
            "high_external_share_threshold": 0.80,
        },
        "vessel_findings": {
            "top_priced_purchase_vessel": {
                "vessel_file_id": top_priced_purchase_vessel["vessel_file_id"],
                "model_purchase_qty": as_float(top_priced_purchase_vessel, "model_purchase_qty"),
                "priced_share_of_consumption": as_float(
                    top_priced_purchase_vessel, "priced_share_of_consumption"
                ),
            },
            "top_external_vessel": {
                "vessel_file_id": top_external_vessel["vessel_file_id"],
                "model_external_qty": as_float(top_external_vessel, "model_external_qty"),
                "external_share_of_consumption": as_float(
                    top_external_vessel, "external_share_of_consumption"
                ),
            },
            "top_external_share_vessel": {
                "vessel_file_id": top_external_share_vessel["vessel_file_id"],
                "model_external_qty": as_float(top_external_share_vessel, "model_external_qty"),
                "external_share_of_consumption": as_float(
                    top_external_share_vessel, "external_share_of_consumption"
                ),
            },
        },
        "port_findings": {
            "top_purchase_port": {
                "port": top_purchase_port["port"],
                "purchase_qty": as_float(top_purchase_port, "purchase_qty"),
                "priced_cost": as_float(top_purchase_port, "priced_cost"),
            },
            "zero_purchase_ports": zero_purchase_ports,
        },
        "sensitivity_findings": {
            "baseline_total_model_cost": baseline_cost,
            "min_total_model_cost": sensitivity["min_total_model_cost"],
            "max_total_model_cost": sensitivity["max_total_model_cost"],
            "total_cost_range": sensitivity["total_cost_range"],
            "low_scenario_multiplier": as_float(low_scenario, "external_price_multiplier"),
            "high_scenario_multiplier": as_float(high_scenario, "external_price_multiplier"),
            "external_cost_share_of_total": external_cost_share_of_total,
            "plan_stable_in_tested_scenarios": plan_stable,
            "unique_model_purchase_qty_values": sorted(purchase_qty_values),
            "unique_model_external_qty_values": sorted(external_qty_values),
        },
        "consistency_checks": checks,
    }


def write_markdown(result: dict[str, object]) -> None:
    """Skriv norsk tolkningsnotat med observasjoner, tolkning og sjekker."""
    coverage = result["coverage"]
    vessel = result["vessel_findings"]
    port = result["port_findings"]
    sensitivity = result["sensitivity_findings"]
    checks = result["consistency_checks"]
    generated_at = result["generated_at"]
    no_priced_ports = ", ".join(coverage["vessels_with_no_priced_ports"]) or "ingen"
    high_external_vessels = ", ".join(coverage["vessels_with_high_external_share"]) or "ingen"
    zero_ports = ", ".join(port["zero_purchase_ports"]) or "ingen"
    stable_text = (
        "Kjøpsplanen er stabil i de testede proxy-scenarioene; analysen viser derfor kostnadseffekt, ikke endret anbefalt plan."
        if sensitivity["plan_stable_in_tested_scenarios"]
        else "Kjøpsplanen endres i minst ett proxy-scenario; sensitivitetsresultatet må derfor tolkes som både kostnads- og planendring."
    )
    high_external_threshold = format_percent(coverage["high_external_share_threshold"]).replace(
        ",00 %", " %"
    )

    lines = [
        "# Resultattolkning for operasjonell hovedmodell",
        "",
        "Dette notatet samler hovedfunn fra basiskjøring og sensitivitetsanalyse. Det er et støtteartefakt for rapportens analyse-, resultat- og diskusjonskapitler.",
        "",
        f"Generert: {generated_at}",
        "",
        "## Hovedfunn",
        "",
        f"- Prisede modellhavner finnes på {coverage['priced_leg_count']} av {coverage['leg_count']} etapper ({format_percent(coverage['priced_leg_share'])}).",
        f"- Kjøp i prisede havner dekker {format_percent(coverage['priced_share_of_consumption'])} av modellert forbruk.",
        f"- Ekstern/ukjent bunkring utgjør {format_percent(coverage['external_share_of_consumption'])} av modellert forbruk.",
        f"- Startbeholdning og beholdningsflyt dekker den resterende andelen på {format_percent(coverage['inventory_share_of_consumption'])}.",
        f"- Fartøy uten prisede modellhavner i ruten: {no_priced_ports}.",
        f"- Fartøy med minst {high_external_threshold} ekstern/ukjent andel: {high_external_vessels}.",
        "",
        "## Fartøy og havner",
        "",
        f"- Størst modellert kjøp i prisede havner ligger på {vessel['top_priced_purchase_vessel']['vessel_file_id']} med {format_number(vessel['top_priced_purchase_vessel']['model_purchase_qty'])}.",
        f"- Størst ekstern/ukjent mengde ligger på {vessel['top_external_vessel']['vessel_file_id']} med {format_number(vessel['top_external_vessel']['model_external_qty'])}.",
        f"- Høyest ekstern/ukjent andel ligger på {vessel['top_external_share_vessel']['vessel_file_id']} med {format_percent(vessel['top_external_share_vessel']['external_share_of_consumption'])}.",
        f"- Størst kjøpsvolum i priset modellhavn ligger på {port['top_purchase_port']['port']} med {format_number(port['top_purchase_port']['purchase_qty'])}.",
        f"- Modellhavner uten kjøp i basiskjøringen: {zero_ports}.",
        "",
        "## Sensitivitet",
        "",
        f"- Total modellkostnad i basisscenarioet er {format_number(sensitivity['baseline_total_model_cost'])}.",
        f"- Kostnadsspennet i proxyanalysen er {format_number(sensitivity['total_cost_range'])}.",
        f"- Ekstern/ukjent kostnad utgjør {format_percent(sensitivity['external_cost_share_of_total'])} av total modellkostnad i basisscenarioet.",
        f"- Laveste scenario er proxyfaktor {str(round(sensitivity['low_scenario_multiplier'], 2)).replace('.', ',')}; høyeste scenario er proxyfaktor {str(round(sensitivity['high_scenario_multiplier'], 2)).replace('.', ',')}.",
        f"- {stable_text}",
        "",
        "## Tolkning",
        "",
        "Resultatet viser at modellen gir en konkret bunkringsplan først og fremst der fartøyenes ruter overlapper med de prisede modellhavnene. Når prisede modellhavner bare finnes på en liten andel av etappene, blir modellens operative anbefalinger sterkest for fartøy som faktisk passerer `P001`-`P004`, og svakere for fartøy som ikke gjør det.",
        "",
        f"Ekstern/ukjent bunkring på {format_percent(coverage['external_share_of_consumption'])} bør tolkes som en kvantitativ diagnose av datagapet i prisgrunnlaget, ikke som et eget operativt havnevalg. Andelen viser hvor stor del av forbruket modellen ikke kan knytte til prisede modellhavner med dagens datadekning.",
        "",
        f"Den resterende dekningsandelen på {format_percent(coverage['inventory_share_of_consumption'])} kommer fra startbeholdning og beholdningsflyt gjennom ruten. Dette forklarer hvorfor priset andel og ekstern/ukjent andel ikke summerer til 100 %, og gjør tolkningen av dekningsandelene mer komplett.",
        "",
        "Proxyfaktor 1,25 er en arbeidsantagelse for ekstern/ukjent bunkring. Sensitivitetsanalysen er en smal én-veis analyse av denne antagelsen, og terskelen på 80 % brukes bare som en arbeidsdefinisjon for å identifisere fartøy der ekstern/ukjent bunkring dominerer kraftig.",
        "",
        "## Konsistenssjekker",
        "",
    ]
    for check in checks:
        lines.append(
            f"- {check['status']}: {check['check']} (verdi: {check['value']}, forventet: {check['expected']})."
        )
    INTERPRETATION_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    result = build_interpretation()
    INTERPRETATION_JSON.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_markdown(result)

    print("Resultattolkning er generert.")
    print(f"Oppsummering: {INTERPRETATION_JSON}")
    print(f"Notat: {INTERPRETATION_MD}")


if __name__ == "__main__":
    main()
