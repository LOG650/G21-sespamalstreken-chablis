from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[4]
BASELINE_DIR = ROOT / "006 analysis" / "03_analyse" / "01_basiskjoring"
SENSITIVITY_DIR = ROOT / "006 analysis" / "03_analyse" / "02_sensitivitetsanalyse"

BASELINE_SUMMARY_JSON = BASELINE_DIR / "output" / "res_baseline_model_v1_summary.json"
BASELINE_BY_PORT_CSV = BASELINE_DIR / "output" / "res_baseline_model_v1_by_port.csv"
SENSITIVITY_SCENARIOS_CSV = SENSITIVITY_DIR / "output" / "res_sensitivity_model_scenarios.csv"

FIGURE_DIR = SENSITIVITY_DIR / "figures"
TABLE_DIR = SENSITIVITY_DIR / "output"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_markdown_table(path: Path, headers: list[str], rows: list[list[str]], caption: str) -> None:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    lines.extend(
        [
            "",
            f'<p align="center" style="font-size: 0.9em;"><small><i>{caption}</i></small></p>',
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def format_number(value: float, decimals: int = 2) -> str:
    formatted = f"{value:,.{decimals}f}"
    return formatted.replace(",", " ").replace(".", ",")


def load_inputs() -> tuple[dict[str, object], list[dict[str, str]], list[dict[str, str]]]:
    baseline_summary = json.loads(BASELINE_SUMMARY_JSON.read_text(encoding="utf-8"))
    baseline_by_port = read_csv(BASELINE_BY_PORT_CSV)
    scenarios = read_csv(SENSITIVITY_SCENARIOS_CSV)
    return baseline_summary, baseline_by_port, scenarios


def create_tables(
    baseline_summary: dict[str, object],
    baseline_by_port: list[dict[str, str]],
    scenarios: list[dict[str, str]],
) -> None:
    historical = float(baseline_summary["historical_total_cost"])
    model = float(baseline_summary["baseline_model_total_cost"])
    saving = float(baseline_summary["estimated_total_saving"])
    saving_pct = float(baseline_summary["estimated_total_saving_pct"])

    write_markdown_table(
        TABLE_DIR / "tab_result_baseline_vs_historical.md",
        ["Mål", "Verdi"],
        [
            ["Historisk kostnad", format_number(historical)],
            ["Modellkostnad", format_number(model)],
            ["Estimert besparelse", format_number(saving)],
            ["Besparelse i prosent", f"{format_number(saving_pct)} %"],
        ],
        "Tabell 8.1 Basiskjøring sammenlignet med historisk praksis.",
    )

    write_markdown_table(
        TABLE_DIR / "tab_result_baseline_by_port.md",
        ["Havn", "Antall måneder valgt", "Totalt volum", "Modellkostnad"],
        [
            [
                row["port"],
                row["selected_months"],
                format_number(float(row["solution_qty"])),
                format_number(float(row["solution_cost"])),
            ]
            for row in baseline_by_port
        ],
        "Tabell 8.2 Valgt havn, volum og kostnad i basiskjøringen.",
    )

    ranked = sorted(scenarios, key=lambda row: float(row["delta_vs_baseline"]))
    selected = ranked[:5] + ranked[-5:]
    selected = sorted(selected, key=lambda row: float(row["delta_vs_baseline"]))
    write_markdown_table(
        TABLE_DIR / "tab_result_sensitivity_top_effects.md",
        ["Scenario", "Total kostnad", "Endring mot basis", "Endring i prosent", "Besparelse mot historisk"],
        [
            [
                row["description"],
                format_number(float(row["total_cost"])),
                format_number(float(row["delta_vs_baseline"])),
                f"{format_number(float(row['delta_pct_vs_baseline']))} %",
                format_number(float(row["estimated_saving_vs_historical"])),
            ]
            for row in selected
        ],
        "Tabell 8.3 Scenarioene med størst utslag i sensitivitetsanalysen.",
    )


def save_bar_chart(path: Path, labels: list[str], values: list[float], ylabel: str, title: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.8))
    colors = ["#3A6EA5", "#4D908E", "#F4A261"]
    ax.bar(labels, values, color=colors[: len(labels)], width=0.62)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for index, value in enumerate(values):
        ax.text(index, value, format_number(value / 1_000_000, 1), ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def create_figures(
    baseline_summary: dict[str, object],
    baseline_by_port: list[dict[str, str]],
    scenarios: list[dict[str, str]],
) -> None:
    historical = float(baseline_summary["historical_total_cost"])
    model = float(baseline_summary["baseline_model_total_cost"])
    saving = float(baseline_summary["estimated_total_saving"])

    save_bar_chart(
        FIGURE_DIR / "fig_result_baseline_cost_comparison.png",
        ["Historisk", "Modell", "Besparelse"],
        [historical, model, saving],
        "Kostnad",
        "Historisk kostnad, modellkostnad og estimert besparelse",
    )

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ports = [row["port"] for row in baseline_by_port]
    selected_months = [int(row["selected_months"]) for row in baseline_by_port]
    ax.bar(ports, selected_months, color="#4D908E", width=0.62)
    ax.set_ylabel("Antall måneder")
    ax.set_title("Valgt havn i basiskjøringen")
    ax.grid(axis="y", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for index, value in enumerate(selected_months):
        ax.text(index, value, str(value), ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_result_baseline_selected_ports.png", dpi=180)
    plt.close(fig)

    tornado_rows = [
        row for row in scenarios if row["scenario_id"] != "baseline"
    ]
    tornado_rows = sorted(
        tornado_rows,
        key=lambda row: abs(float(row["delta_vs_baseline"])),
        reverse=True,
    )[:10]
    tornado_rows = sorted(tornado_rows, key=lambda row: float(row["delta_vs_baseline"]))

    labels = [row["description"] for row in tornado_rows]
    values = [float(row["delta_vs_baseline"]) / 1_000_000 for row in tornado_rows]
    colors = ["#4D908E" if value < 0 else "#D65F5F" for value in values]

    fig, ax = plt.subplots(figsize=(9, 5.6))
    ax.barh(labels, values, color=colors)
    ax.axvline(0, color="#333333", linewidth=0.8)
    ax.set_xlabel("Endring mot basis, mill. kostnadsenheter")
    ax.set_title("Største utslag i sensitivitetsanalysen")
    ax.grid(axis="x", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_result_sensitivity_tornado.png", dpi=180)
    plt.close(fig)


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    baseline_summary, baseline_by_port, scenarios = load_inputs()
    create_tables(baseline_summary, baseline_by_port, scenarios)
    create_figures(baseline_summary, baseline_by_port, scenarios)
    print("Tabeller og figurer er generert.")
    print(f"Figurer: {FIGURE_DIR}")
    print(f"Tabeller: {TABLE_DIR}")


if __name__ == "__main__":
    main()
