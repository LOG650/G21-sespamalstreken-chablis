from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[4]
BASELINE_MONTH_CSV = (
    ROOT
    / "006 analysis"
    / "03_analyse"
    / "01_basiskjoring"
    / "output"
    / "res_baseline_model_v1_by_month.csv"
)
FIGURE_DIR = ROOT / "006 analysis" / "03_analyse" / "03_resultattolkning" / "figures"
FIGURE_PATH = FIGURE_DIR / "fig_result_monthly_saving.png"


def read_rows() -> list[dict[str, str]]:
    with BASELINE_MONTH_CSV.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def format_million(value: float) -> str:
    return f"{value / 1_000_000:.1f}".replace(".", ",")


def main() -> None:
    rows = read_rows()
    months = [row["delivery_month"] for row in rows]
    savings = [float(row["estimated_saving"]) for row in rows]
    colors = ["#3A6EA5" if value >= 0 else "#C44E52" for value in savings]

    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.bar(months, [value / 1_000_000 for value in savings], color=colors, width=0.82)
    ax.axhline(0, color="#333333", linewidth=0.8)
    ax.set_ylabel("Estimert besparelse, mill.")
    ax.set_xlabel("Måned")
    ax.set_title("Månedlig estimert besparelse i basiskjøringen")
    ax.grid(axis="y", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    tick_step = 4
    ax.set_xticks(range(0, len(months), tick_step))
    ax.set_xticklabels(months[::tick_step], rotation=45, ha="right")

    total_saving = sum(savings)
    ax.text(
        0.01,
        0.96,
        f"Total estimert besparelse: {format_million(total_saving)} mill.",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#dddddd"},
    )

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(FIGURE_PATH, dpi=180)
    plt.close(fig)
    print(FIGURE_PATH)


if __name__ == "__main__":
    main()
