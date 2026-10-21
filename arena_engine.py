"""Pure functions for PIVOT's Phase 3 competitive classroom layer."""
from typing import Iterable, Mapping, Any

METRICS = ("cash", "service", "trust", "morale", "risk")
BASELINE = {"cash": 70.0, "service": 78.0, "trust": 70.0, "morale": 72.0, "risk": 25.0}
MARKET_PULSES = (
    ("DEMAND SIGNAL", "Customers are comparing value more closely. Teams must balance price, service quality, and trust."),
    ("SUPPLY SHOCK", "A key input or delivery constraint may disrupt execution. Teams should consider capacity and contingency plans."),
    ("COMPETITIVE RESPONSE", "Rivals are reacting to market moves. A decision that worked last round may now be easier to copy or counter."),
    ("BOARD REVIEW", "Stakeholders want evidence of results. Teams should show what worked, what failed, and what they will change next."),
)


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, float(value)))


def market_pulse(round_no: int) -> tuple[str, str]:
    """Return the shared external condition for a 0-based round index."""
    return MARKET_PULSES[min(max(int(round_no), 0), len(MARKET_PULSES) - 1)]


def apply_effects(effects_by_round: Iterable[Mapping[str, Any]]) -> dict[str, float]:
    """Compute bounded company health from the baseline and saved round effects."""
    values = dict(BASELINE)
    for effects in effects_by_round:
        for key in METRICS:
            try:
                delta = float(effects.get(key, 0))
            except (TypeError, ValueError):
                delta = 0.0
            values[key] = clamp(values[key] + delta)
    return {key: round(value, 1) for key, value in values.items()}


def health_score(metrics: Mapping[str, Any]) -> float:
    """Equal-weight health index; risk is reversed so lower risk is better."""
    vals = {key: clamp(metrics.get(key, BASELINE[key])) for key in METRICS}
    return round((vals["cash"] + vals["service"] + vals["trust"] + vals["morale"] + (100 - vals["risk"])) / 5, 1)


def rank_standings(teams: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Rank teams by progress first, then health score; input records are not mutated."""
    result = [dict(team) for team in teams]
    result.sort(key=lambda team: (int(team.get("rounds", 0)), float(team.get("score", 0))), reverse=True)
    for rank, team in enumerate(result, 1):
        team["rank"] = rank
    return result
