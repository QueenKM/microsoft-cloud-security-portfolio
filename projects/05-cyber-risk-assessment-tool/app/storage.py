from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from models import RiskItem
from scoring import risk_row


def load_risks(path: Path) -> list[RiskItem]:
    if not path.exists():
        return []

    payload = json.loads(path.read_text(encoding="utf-8"))
    return [RiskItem.from_dict(item) for item in payload]


def save_risks(path: Path, risks: Iterable[RiskItem]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = [risk.to_dict() for risk in risks]
    path.write_text(json.dumps(serialized, indent=2), encoding="utf-8")


def load_scenario(path: Path) -> list[RiskItem]:
    return load_risks(path)


def export_csv(path: Path, risks: Iterable[RiskItem]) -> None:
    rows = [risk_row(risk) for risk in risks]
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "identifier",
                "title",
                "category",
                "asset",
                "scenario",
                "owner",
                "status",
                "impact",
                "likelihood",
                "control_effectiveness",
                "inherent_score",
                "residual_score",
                "risk_level",
                "existing_controls",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
