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

PRICE_CSV = MODEL_INPUT_DIR / "tab_model_v1_price_by_port_month.csv"
DEMAND_CSV = MODEL_INPUT_DIR / "tab_model_v1_demand_by_month.csv"
AVAILABILITY_CSV = MODEL_INPUT_DIR / "tab_model_v1_availability_by_port_month.csv"
PARAMETERS_JSON = MODEL_INPUT_DIR / "data_model_v1_parameters.json"
RESULT_CSV = ACTIVITY_DIR / "output" / "res_model_v1_solution_by_port_month.csv"
RESULT_JSON = ACTIVITY_DIR / "output" / "res_model_v1_summary.json"


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_price_data():
    """Load price parameter p[h,t]."""
    prices = {}
    for row in read_csv(PRICE_CSV):
        prices[(row["delivery_month"], row["port"])] = float(row["price_value"])
    return prices


def load_demand_data():
    """Load demand parameter D[t]."""
    return {
        row["delivery_month"]: float(row["demand_qty"])
        for row in read_csv(DEMAND_CSV)
    }


def load_availability_data():
    """Load availability parameter f[h,t]."""
    availability = {}
    for row in read_csv(AVAILABILITY_CSV):
        availability[(row["delivery_month"], row["port"])] = int(row["available_flag"])
    return availability


def load_monthly_data():
    """Load price and availability data grouped by month."""
    prices = load_price_data()
    availability = load_availability_data()
    parameters = load_parameters()
    monthly = {}
    for month in parameters["sets"]["months"]:
        for port in parameters["sets"]["ports"]:
            if availability.get((month, port), 0) != 1:
                continue
            monthly.setdefault(month, {})[port] = prices[(month, port)]
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
    demands = load_demand_data()
    
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
        
        demand = demands.get(month, 0.0)
        
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
        "validation_method": "solver-uavhengig simulering med behovsparameter fra tab_model_v1_demand_by_month.csv",
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
