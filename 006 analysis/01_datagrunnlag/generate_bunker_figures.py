from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = Path(__file__).resolve().parent
CLEANED_CSV = DATA_DIR / "tab_bunker_cleaned.csv"
MONTHLY_CSV = DATA_DIR / "tab_bunker_monthly_by_port.csv"
FIG_DIR = DATA_DIR / "figures"
FIG_GUIDE = DATA_DIR / "fig_bunker_guide.md"

PORT_COLORS = {
    "P001": "#0B3C5D",
    "P002": "#328CC1",
    "P003": "#D9B310",
    "P004": "#1D2731",
}


def parse_month(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def ensure_figure_dir() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)


def save_figure(filename: str) -> Path:
    path = FIG_DIR / filename
    plt.tight_layout()
    plt.savefig(path, dpi=220, bbox_inches="tight")
    plt.close()
    return path


def plot_total_volume_by_month(monthly_rows: list[dict[str, str]]) -> Path:
    totals = defaultdict(float)
    for row in monthly_rows:
        totals[row["delivery_month"]] += float(row["total_qty"])

    months = sorted(totals, key=parse_month)
    x_values = [parse_month(month) for month in months]
    y_values = [totals[month] for month in months]

    plt.figure(figsize=(12, 5))
    plt.plot(x_values, y_values, color="#0B3C5D", linewidth=2.4)
    plt.fill_between(x_values, y_values, color="#328CC1", alpha=0.18)
    plt.title("Samlet bunkret volum per måned")
    plt.xlabel("Måned")
    plt.ylabel("Volum")
    plt.grid(alpha=0.25, linestyle="--")
    return save_figure("fig_bunker_total_qty_by_month.png")


def plot_weighted_price_by_port(monthly_rows: list[dict[str, str]]) -> Path:
    rows_by_port: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in monthly_rows:
        rows_by_port[row["port"]].append(row)

    plt.figure(figsize=(12, 5.8))
    for port in sorted(rows_by_port):
        rows = sorted(rows_by_port[port], key=lambda row: parse_month(row["delivery_month"]))
        x_values = [parse_month(row["delivery_month"]) for row in rows]
        y_values = [float(row["weighted_avg_price"]) for row in rows]
        plt.plot(
            x_values,
            y_values,
            label=port,
            linewidth=2,
            color=PORT_COLORS.get(port),
        )

    plt.title("Vektet gjennomsnittspris per havn og måned")
    plt.xlabel("Måned")
    plt.ylabel("Pris")
    plt.grid(alpha=0.25, linestyle="--")
    plt.legend(title="Havn", ncols=4, frameon=False)
    return save_figure("fig_bunker_weighted_price_by_port_month.png")


def plot_season_profile(monthly_rows: list[dict[str, str]]) -> Path:
    month_names = ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Des"]
    volume_by_calendar_month: dict[int, list[float]] = defaultdict(list)
    price_sum_by_calendar_month = defaultdict(float)
    price_weight_by_calendar_month = defaultdict(float)

    for row in monthly_rows:
        calendar_month = parse_month(row["delivery_month"]).month
        qty = float(row["total_qty"])
        price = float(row["weighted_avg_price"])
        volume_by_calendar_month[calendar_month].append(qty)
        price_sum_by_calendar_month[calendar_month] += price * qty
        price_weight_by_calendar_month[calendar_month] += qty

    avg_volumes = []
    weighted_prices = []
    indices = list(range(1, 13))
    for month in indices:
        observations = volume_by_calendar_month.get(month, [])
        avg_volumes.append(sum(observations) / len(observations) if observations else 0.0)
        weight = price_weight_by_calendar_month.get(month, 0.0)
        weighted_prices.append(price_sum_by_calendar_month[month] / weight if weight else 0.0)

    fig, ax1 = plt.subplots(figsize=(12, 5.8))
    bars = ax1.bar(month_names, avg_volumes, color="#328CC1", alpha=0.85)
    ax1.set_title("Sesongprofil for volum og pris")
    ax1.set_xlabel("Kalendermåned")
    ax1.set_ylabel("Gjennomsnittlig volum")
    ax1.grid(axis="y", alpha=0.25, linestyle="--")

    ax2 = ax1.twinx()
    ax2.plot(month_names, weighted_prices, color="#D95F02", linewidth=2.2, marker="o")
    ax2.set_ylabel("Vektet gjennomsnittspris")

    ax1.bar_label(bars, fmt="%.0f", padding=2, fontsize=8)
    return save_figure("fig_bunker_season_profile.png")


def plot_price_distribution_by_port(cleaned_rows: list[dict[str, str]]) -> Path:
    prices_by_port: dict[str, list[float]] = defaultdict(list)
    for row in cleaned_rows:
        prices_by_port[row["port"]].append(float(row["effective_price"]))

    ports = sorted(prices_by_port)
    series = [prices_by_port[port] for port in ports]

    plt.figure(figsize=(9.5, 5.5))
    box = plt.boxplot(series, patch_artist=True, labels=ports, showfliers=False)
    for port, patch in zip(ports, box["boxes"], strict=True):
        patch.set_facecolor(PORT_COLORS.get(port, "#A7B6C2"))
        patch.set_alpha(0.75)

    plt.title("Prisfordeling per havn")
    plt.xlabel("Havn")
    plt.ylabel("Pris")
    plt.grid(axis="y", alpha=0.25, linestyle="--")
    return save_figure("fig_bunker_price_distribution_by_port.png")


def write_figure_guide(figure_paths: list[Path]) -> None:
    lines = [
        "# Figurguide for datagrunnlag",
        "",
        "Disse figurene er laget fra renset og aggregert bunkringsdata og kan brukes direkte i rapportens casekapittel og datakapittel.",
        "",
        "## Figurer",
        "",
        f"- `{figure_paths[0].name}`: viser total historisk bunkringsmengde per måned og egner seg i kapittel 4.2 om historisk utvikling.",
        f"- `{figure_paths[1].name}`: viser prisutvikling per havn over tid og egner seg til å forklare geografiske prisforskjeller i casekapitlet.",
        f"- `{figure_paths[2].name}`: viser sesongprofil for både volum og pris og egner seg i kapittel 4.3 om sesongmønster.",
        f"- `{figure_paths[3].name}`: viser prisfordeling per havn og gjør det enklere å diskutere variasjon og usikkerhet i datagrunnlaget i kapittel 5.2.",
        "",
        "## Kjøring",
        "",
        "Bruk denne kommandoen fra repo-roten:",
        "",
        "```powershell",
        "uv run --project \"006 analysis\" python \"006 analysis\\01_datagrunnlag\\generate_bunker_figures.py\"",
        "```",
        "",
        "Figurene skrives til `006 analysis/01_datagrunnlag/figures`.",
    ]
    FIG_GUIDE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ensure_figure_dir()
    cleaned_rows = read_csv(CLEANED_CSV)
    monthly_rows = read_csv(MONTHLY_CSV)

    figure_paths = [
        plot_total_volume_by_month(monthly_rows),
        plot_weighted_price_by_port(monthly_rows),
        plot_season_profile(monthly_rows),
        plot_price_distribution_by_port(cleaned_rows),
    ]
    write_figure_guide(figure_paths)

    for path in figure_paths:
        print(path.relative_to(ROOT).as_posix())
    print(FIG_GUIDE.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
