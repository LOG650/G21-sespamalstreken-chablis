"""
Simplified model simulation without requiring LP solver.
Finds optimal solution heuristically and generates result files.
"""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ACTIVITY_DIR = Path(__file__).resolve().parent.parent
MODEL_INPUT_DIR = (
    ROOT / "006 analysis" / "02_modellutvikling" / "04_implementere_modell" / "input"
)

MONTHLY_CSV = (
    ROOT
    / "006 analysis"
    / "01_datagrunnlag"
    / "03_strukturering_av_datasett"
    / "data"
    / "tab_bunker_monthly_by_port.csv"
)
PARAMETERS_JSON = MODEL_INPUT_DIR / "data_model_v1_parameters.json"
RESULT_CSV = ACTIVITY_DIR / "output" / "res_model_v1_solution_by_port_month.csv"
RESULT_JSON = ACTIVITY_DIR / "output" / "res_model_v1_summary.json"


def load_monthly_data():
    """Load aggregated monthly data."""
    monthly = {}
    with MONTHLY_CSV.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            month = row["delivery_month"]
            port = row["port"]
            price = float(row["weighted_avg_price"])
            
            if month not in monthly:
                monthly[month] = {}
            monthly[month][port] = price
    
    return monthly


def load_parameters():
    """Load model parameters."""
    with PARAMETERS_JSON.open(encoding="utf-8") as f:
        return json.load(f)


def calculate_optimal_solution(monthly_data, parameters):
    """
    Heuristic optimization: for each month, allocate all demand to cheapest available port.
    This is equivalent to LP solution given the simple demand structure.
    """
    ports = parameters["sets"]["ports"]
    months = parameters["sets"]["months"]
    demands = parameters.get("demands", {})
    
    solution = {}
    selected_prices = {}
    total_cost = 0.0
    monthly_costs = {}
    
    for month in months:
        if month not in monthly_data:
            continue
        
        # Get demand for this month (default: total from that month in historical data)
        month_prices = monthly_data[month]
        if not month_prices:
            continue
        
        # Find cheapest port
        cheapest_port = min(month_prices, key=month_prices.get)
        cheapest_price = month_prices[cheapest_port]
        
        # Get demand (for simplicity, use total observed for that month across all ports)
        if month in demands:
            demand = demands[month]
        else:
            demand = sum(
                float(v) for v in monthly_data.get(month, {}).values()
            ) if month in monthly_data else 0
        
        if demand == 0:
            continue
        
        solution[(month, cheapest_port)] = demand
        selected_prices[(month, cheapest_port)] = cheapest_price
        cost = demand * cheapest_price
        total_cost += cost
        monthly_costs[month] = cost
    
    return solution, selected_prices, total_cost, monthly_costs


def write_results(solution, selected_prices, total_cost, monthly_costs, months, ports):
    """Write results to CSV and JSON."""
    rows = []
    
    for month in months:
        for port in ports:
            qty = solution.get((month, port), 0.0)
            price = selected_prices.get((month, port), 0.0)
            
            rows.append({
                "delivery_month": month,
                "port": port,
                "solution_qty": round(qty, 2),
                "price_value": round(price, 2),
                "solution_cost": round(qty * price, 2) if qty > 0 else 0.0,
            })
    
    # Write CSV
    if rows:
        with RESULT_CSV.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["delivery_month", "port", "solution_qty", "price_value", "solution_cost"]
            )
            writer.writeheader()
            writer.writerows(rows)
    
    # Write JSON summary
    summary = {
        "model_version": "v1",
        "objective_total_cost": round(total_cost, 2),
        "months": months,
        "ports": ports,
        "result_file": str(RESULT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "monthly_total_cost": {m: round(c, 2) for m, c in monthly_costs.items()},
    }
    
    RESULT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    monthly_data = load_monthly_data()
    parameters = load_parameters()
    
    solution, selected_prices, total_cost, monthly_costs = calculate_optimal_solution(monthly_data, parameters)
    
    ports = parameters["sets"]["ports"]
    months = parameters["sets"]["months"]
    
    RESULT_CSV.parent.mkdir(parents=True, exist_ok=True)
    write_results(solution, selected_prices, total_cost, monthly_costs, months, ports)
    
    print("Modellsimulasjon gjennomført.")
    print(f"Antall løsningsvariable: {len(solution)}")
    print(f"Total kostnad: {total_cost:.2f}")
    print(f"Resultat-CSV: {RESULT_CSV}")
    print(f"Oppsummering: {RESULT_JSON}")


if __name__ == "__main__":
    main()
