"""Deterministic multi-company market simulation for PIVOT Phase 4.

All monetary values are abstract currency units. This is an educational model,
not a forecast. The model is deterministic for identical inputs.
"""
from __future__ import annotations
from typing import Any, Mapping
import math

ROUNDS = 6
INITIAL_DEMAND = 10_000
INITIAL_STATE = {
    "cash": 500_000.0, "price": 100.0, "quality": 65.0,
    "brand": 50.0, "capacity": 2_500, "inventory": 0,
    "cumulative_profit": 0.0, "market_share": 0.0,
    "customers": 0, "satisfaction": 65.0,
}
PULSES = [
    {"name":"Value-conscious customers", "demand_factor":0.98, "cost_factor":1.00, "note":"Customers compare price and value more closely."},
    {"name":"Supplier cost shock", "demand_factor":1.00, "cost_factor":1.12, "note":"Input costs rise this round; protect margins and supply reliability."},
    {"name":"Category buzz", "demand_factor":1.12, "cost_factor":1.00, "note":"Category demand expands, but firms may not have enough capacity."},
    {"name":"Trust under scrutiny", "demand_factor":0.96, "cost_factor":1.03, "note":"Customers pay more attention to quality and brand credibility."},
    {"name":"Aggressive rival offers", "demand_factor":1.00, "cost_factor":1.00, "note":"Price competition intensifies across the market."},
    {"name":"Board review", "demand_factor":1.04, "cost_factor":1.02, "note":"The market rewards firms that balance growth and durable economics."},
]

def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, float(v)))

def initial_company(name: str) -> dict[str, Any]:
    return {**INITIAL_STATE, "name": name}

def validate_decision(d: Mapping[str, Any]) -> dict[str, float]:
    """Normalize and bound the five decisions accepted for a round."""
    return {
        "price": round(clamp(float(d.get("price", 100)), 60, 160), 2),
        "marketing": round(clamp(float(d.get("marketing", 20_000)), 0, 100_000), 2),
        "quality_investment": round(clamp(float(d.get("quality_investment", 10_000)), 0, 60_000), 2),
        "capacity": int(clamp(float(d.get("capacity", 2500)), 500, 6000)),
        "people_investment": round(clamp(float(d.get("people_investment", 5_000)), 0, 30_000), 2),
    }

def _attractiveness(company: Mapping[str, Any], decision: Mapping[str, Any]) -> float:
    # Bounded, interpretable demand score: value, quality, brand and marketing.
    price = float(decision["price"])
    quality = clamp(float(company.get("quality", 65)) + float(decision["quality_investment"]) / 6000, 25, 100)
    brand = clamp(float(company.get("brand", 50)) + float(decision["marketing"]) / 10000, 10, 100)
    value = clamp(120 / price, 0.55, 1.8)
    return max(0.05, (0.42 * value + 0.30 * quality / 75 + 0.28 * brand / 60))

def settle_round(companies: Mapping[str, Mapping[str, Any]], decisions: Mapping[str, Mapping[str, Any]], round_no: int, market_demand: int = INITIAL_DEMAND) -> dict[str, Any]:
    """Resolve one simultaneous round for all companies and return new states/results.

    Decisions are evaluated together. Market demand is split proportionally to
    attractiveness, then constrained by capacity. Unserved demand is not silently
    reassigned, which keeps the model transparent and easy to teach.
    """
    if not companies or set(companies) != set(decisions):
        raise ValueError("Every participating company must submit exactly one decision before settlement.")
    pulse = PULSES[min(max(int(round_no), 0), len(PULSES)-1)]
    normalized = {n: validate_decision(d) for n, d in decisions.items()}
    attraction = {n: _attractiveness(companies[n], normalized[n]) for n in companies}
    total = sum(attraction.values()) or 1.0
    demand_total = max(1, int(market_demand * pulse["demand_factor"]))
    results: dict[str, Any] = {}
    new_states: dict[str, Any] = {}
    for name, prev in companies.items():
        d = normalized[name]
        demand = int(round(demand_total * attraction[name] / total))
        units = min(demand, d["capacity"])
        price = d["price"]
        marketing = d["marketing"]
        qinv = d["quality_investment"]
        people = d["people_investment"]
        # Explicit unit-cost and fixed-cost assumptions for a teaching model.
        unit_cost = (42 + max(0, d["capacity"] - 2500) * 0.002) * pulse["cost_factor"]
        revenue = units * price
        production_cost = units * unit_cost
        fixed_cost = 24_000 + d["capacity"] * 4.0
        total_cost = production_cost + marketing + qinv + people + fixed_cost
        profit = revenue - total_cost
        cash = float(prev.get("cash", INITIAL_STATE["cash"])) + profit
        quality = clamp(float(prev.get("quality", 65)) + qinv / 12000 - 1.0, 25, 100)
        brand = clamp(float(prev.get("brand", 50)) + marketing / 25000 - 1.5, 10, 100)
        satisfaction = clamp(0.55 * quality + 0.25 * (100 - abs(price - 95) * 0.6) + 0.20 * clamp(float(prev.get("satisfaction", 65)) + people / 10000 - 1, 0, 100), 0, 100)
        state = {"name":name,"cash":round(cash,2),"price":price,"quality":round(quality,2),"brand":round(brand,2),"capacity":d["capacity"],"inventory":0,"cumulative_profit":round(float(prev.get("cumulative_profit",0))+profit,2),"market_share":round(units/demand_total*100,2),"customers":units,"satisfaction":round(satisfaction,2)}
        new_states[name] = state
        results[name] = {"round":int(round_no)+1,"demand":demand,"units_sold":units,"revenue":round(revenue,2),"production_cost":round(production_cost,2),"marketing":marketing,"quality_investment":qinv,"people_investment":people,"fixed_cost":round(fixed_cost,2),"total_cost":round(total_cost,2),"profit":round(profit,2),"cash":round(cash,2),"market_share":state["market_share"],"satisfaction":state["satisfaction"],"quality":state["quality"],"brand":state["brand"],"capacity_utilization":round(units/d["capacity"]*100,1),"pulse":pulse["name"]}
    return {"round":int(round_no)+1,"pulse":pulse,"market_demand":demand_total,"states":new_states,"results":results,"decisions":normalized}

def company_score(state: Mapping[str, Any]) -> float:
    # Performance score rewards profit, satisfaction, share and solvency; bounded.
    profit_component = clamp(50 + float(state.get("cumulative_profit", 0)) / 50000, 0, 100)
    cash_component = clamp(float(state.get("cash", 0)) / 10000, 0, 100)
    return round(0.40 * profit_component + 0.25 * clamp(state.get("satisfaction",65),0,100) + 0.20 * clamp(state.get("market_share",0)*5,0,100) + 0.15 * cash_component, 2)
