from __future__ import annotations

from dataclasses import asdict
from statistics import mean
from typing import Iterable

from models import RiskItem


def clamp_score(value: int, minimum: int = 1, maximum: int = 5) -> int:
    return max(minimum, min(maximum, int(value)))


def clamp_percentage(value: int, minimum: int = 0, maximum: int = 90) -> int:
    return max(minimum, min(maximum, int(value)))


def calculate_inherent_score(impact: int, likelihood: int) -> int:
    return clamp_score(impact) * clamp_score(likelihood)


def calculate_residual_score(impact: int, likelihood: int, control_effectiveness: int) -> int:
    inherent = calculate_inherent_score(impact, likelihood)
    weighted = round(inherent * (1 - (clamp_percentage(control_effectiveness) / 100)))
    return max(1, weighted)


def classify_risk(score: int) -> str:
    if score <= 5:
        return "Low"
    if score <= 10:
        return "Medium"
    if score <= 15:
        return "High"
    return "Critical"


def matrix_counts(risks: Iterable[RiskItem]) -> dict[tuple[int, int], int]:
    counts: dict[tuple[int, int], int] = {}
    for risk in risks:
        key = (clamp_score(risk.impact), clamp_score(risk.likelihood))
        counts[key] = counts.get(key, 0) + 1
    return counts


def summarize_risks(risks: Iterable[RiskItem]) -> dict[str, float | int]:
    risk_list = list(risks)
    if not risk_list:
        return {
            "total": 0,
            "critical": 0,
            "high": 0,
            "average_residual_score": 0.0,
        }

    residual_scores = [
        calculate_residual_score(risk.impact, risk.likelihood, risk.control_effectiveness)
        for risk in risk_list
    ]
    levels = [classify_risk(score) for score in residual_scores]
    return {
        "total": len(risk_list),
        "critical": levels.count("Critical"),
        "high": levels.count("High"),
        "average_residual_score": round(mean(residual_scores), 2),
    }


def risk_row(risk: RiskItem) -> dict[str, str | int]:
    inherent_score = calculate_inherent_score(risk.impact, risk.likelihood)
    residual_score = calculate_residual_score(
        risk.impact, risk.likelihood, risk.control_effectiveness
    )
    return {
        **asdict(risk),
        "inherent_score": inherent_score,
        "residual_score": residual_score,
        "risk_level": classify_risk(residual_score),
    }
