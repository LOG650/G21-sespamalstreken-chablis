from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ACTIVITY_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = ACTIVITY_DIR / "input"
OUTPUT_DIR = ACTIVITY_DIR / "output"

PRICE_CSV = INPUT_DIR / "tab_model_v1_price_by_port_month.csv"
DEMAND_CSV = INPUT_DIR / "tab_model_v1_demand_by_month.csv"
AVAILABILITY_CSV = INPUT_DIR / "tab_model_v1_availability_by_port_month.csv"
PARAMETERS_JSON = INPUT_DIR / "data_model_v1_parameters.json"
RESULT_CSV = OUTPUT_DIR / "res_model_v1_solution_by_port_month.csv"
RESULT_JSON = OUTPUT_DIR / "res_model_v1_summary.json"


def load_price_data() -> dict[tuple[str, str], float]:
    with PRICE_CSV.open(encoding="utf-8", newline="") as handle:
        rows = csv.DictReader(handle)
        return {
            (row["port"], row["delivery_month"]): float(row["price_value"])
            for row in rows
        }


def load_demand_data() -> dict[str, float]:
    with DEMAND_CSV.open(encoding="utf-8", newline="") as handle:
        rows = csv.DictReader(handle)
        return {row["delivery_month"]: float(row["demand_qty"]) for row in rows}


def load_availability_data() -> dict[tuple[str, str], int]:
    with AVAILABILITY_CSV.open(encoding="utf-8", newline="") as handle:
        rows = csv.DictReader(handle)
        return {
            (row["port"], row["delivery_month"]): int(row["available_flag"])
            for row in rows
        }


def load_sets() -> tuple[list[str], list[str], dict[str, object]]:
    parameters = json.loads(PARAMETERS_JSON.read_text(encoding="utf-8"))
    ports = list(parameters["sets"]["ports"])
    months = list(parameters["sets"]["months"])
    return ports, months, parameters


def build_model():
    try:
        from pyomo.environ import (
            ConcreteModel,
            Constraint,
            NonNegativeReals,
            Objective,
            Param,
            Set,
            SolverFactory,
            Var,
            minimize,
            value,
        )
    except ImportError as exc:
        raise RuntimeError(
            "Pyomo er ikke installert i dette miljøet. Installer `pyomo` og en LP-solver "
            "som `glpk` eller `cbc` for å kjøre modellen."
        ) from exc

    ports, months, parameters = load_sets()
    prices = load_price_data()
    demand = load_demand_data()
    availability = load_availability_data()
    big_m = float(parameters.get("big_m_default", 1_000_000))

    model = ConcreteModel(name="bunker_model_v1")

    model.H = Set(initialize=ports, ordered=True)
    model.T = Set(initialize=months, ordered=True)

    model.p = Param(
        model.H,
        model.T,
        initialize={(h, t): prices[(h, t)] for h in ports for t in months},
    )
    model.D = Param(model.T, initialize={t: demand[t] for t in months})
    model.f = Param(
        model.H,
        model.T,
        initialize={(h, t): availability[(h, t)] for h in ports for t in months},
    )

    model.x = Var(model.H, model.T, domain=NonNegativeReals)

    def objective_rule(m):
        return sum(m.p[h, t] * m.x[h, t] for h in m.H for t in m.T)

    model.obj = Objective(rule=objective_rule, sense=minimize)

    def demand_rule(m, t):
        return sum(m.x[h, t] for h in m.H) >= m.D[t]

    model.demand_constraint = Constraint(model.T, rule=demand_rule)

    def port_rule(m, h, t):
        return m.x[h, t] <= big_m * m.f[h, t]

    model.port_constraint = Constraint(model.H, model.T, rule=port_rule)

    return model, SolverFactory, value, ports, months


def write_results(model, value, ports: list[str], months: list[str]) -> None:
    rows: list[dict[str, object]] = []
    total_cost = value(model.obj)
    monthly_cost: dict[str, float] = {}

    for t in months:
        monthly_cost[t] = 0.0
        for h in ports:
            qty = value(model.x[h, t])
            price = value(model.p[h, t])
            cost = qty * price
            monthly_cost[t] += cost
            rows.append(
                {
                    "delivery_month": t,
                    "port": h,
                    "solution_qty": round(qty, 6),
                    "price_value": round(price, 2),
                    "solution_cost": round(cost, 2),
                }
            )

    with RESULT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "model_version": "v1",
        "objective_total_cost": round(total_cost, 2),
        "months": months,
        "ports": ports,
        "result_file": str(RESULT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "monthly_total_cost": {month: round(cost, 2) for month, cost in monthly_cost.items()},
    }
    RESULT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Kjør modellversjon 1 i Pyomo.")
    parser.add_argument(
        "--solver",
        default="glpk",
        help="Navn på solver i Pyomo, for eksempel glpk eller cbc.",
    )
    args = parser.parse_args()

    model, SolverFactory, value, ports, months = build_model()
    solver = SolverFactory(args.solver)
    if solver is None or not solver.available(False):
        raise RuntimeError(
            f"Solver `{args.solver}` er ikke tilgjengelig. Installer en LP-solver som glpk eller cbc."
        )

    result = solver.solve(model, tee=False)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_results(model, value, ports, months)

    print("Løste modellversjon 1.")
    print(f"Solver status: {result.solver.status}")
    print(f"Resultatfil: {RESULT_CSV}")
    print(f"Oppsummering: {RESULT_JSON}")


if __name__ == "__main__":
    main()
