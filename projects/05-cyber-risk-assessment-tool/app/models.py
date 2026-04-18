from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class RiskItem:
    title: str
    category: str
    asset: str
    scenario: str
    owner: str
    status: str
    impact: int
    likelihood: int
    control_effectiveness: int
    notes: str = ""
    existing_controls: str = ""
    identifier: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "title": self.title,
            "category": self.category,
            "asset": self.asset,
            "scenario": self.scenario,
            "owner": self.owner,
            "status": self.status,
            "impact": self.impact,
            "likelihood": self.likelihood,
            "control_effectiveness": self.control_effectiveness,
            "notes": self.notes,
            "existing_controls": self.existing_controls,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "RiskItem":
        return cls(
            identifier=payload.get("identifier") or str(uuid4()),
            title=str(payload.get("title", "")),
            category=str(payload.get("category", "Operational")),
            asset=str(payload.get("asset", "")),
            scenario=str(payload.get("scenario", "")),
            owner=str(payload.get("owner", "")),
            status=str(payload.get("status", "Open")),
            impact=int(payload.get("impact", 1)),
            likelihood=int(payload.get("likelihood", 1)),
            control_effectiveness=int(payload.get("control_effectiveness", 0)),
            notes=str(payload.get("notes", "")),
            existing_controls=str(payload.get("existing_controls", "")),
        )
