#!/usr/bin/env python3
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
import random


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


@dataclass(frozen=True)
class Department:
    key: int
    name: str
    risk_tier: str
    executive_owner: str


@dataclass(frozen=True)
class Workload:
    key: int
    name: str
    platform_domain: str
    primary_persona: str


DEPARTMENTS = [
    Department(1, "IT", "High", "CIO"),
    Department(2, "Finance", "High", "CFO"),
    Department(3, "HR", "High", "HR Director"),
    Department(4, "Student Services", "Medium", "Student Services Director"),
    Department(5, "Research Office", "High", "VP Research"),
]

WORKLOADS = [
    Workload(1, "Entra ID", "Identity", "IT Administrator"),
    Workload(2, "Sentinel", "Security Operations", "Security Analyst"),
    Workload(3, "Microsoft Teams", "Collaboration", "Department Owner"),
    Workload(4, "Azure", "Cloud Infrastructure", "IT Administrator"),
    Workload(5, "Endpoints", "Device Security", "Security Analyst"),
]


def daterange(start: date, end: date) -> list[date]:
    current = start
    values: list[date] = []
    while current <= end:
        values.append(current)
        current += timedelta(days=1)
    return values


def compliance_baseline(department_key: int, workload_key: int) -> float:
    return 63 + department_key * 2 + workload_key * 1.5


def safe_int(value: float) -> int:
    return max(0, int(round(value)))


def build_rows() -> list[dict[str, object]]:
    random.seed(42)
    rows: list[dict[str, object]] = []
    start = date(2026, 1, 1)
    end = date(2026, 3, 31)

    for current_date in daterange(start, end):
        day_index = (current_date - start).days
        month_boost = (current_date.month - 1) * 1.8
        weekday_factor = 1.15 if current_date.weekday() < 5 else 0.7

        for department in DEPARTMENTS:
            dept_factor = 0.85 + department.key * 0.18

            for workload in WORKLOADS:
                workload_factor = 0.9 + workload.key * 0.14
                incident_pressure = dept_factor * workload_factor * weekday_factor

                sign_in_failures = safe_int(
                    18
                    + day_index * 0.12
                    + month_boost
                    + department.key * 3.6
                    + workload.key * 2.8
                    + random.uniform(-4, 7)
                )
                high_incidents = safe_int(
                    random.uniform(0, 1.6) + (incident_pressure - 0.8) * 0.7
                )
                medium_incidents = safe_int(
                    1
                    + random.uniform(0, 2.5)
                    + incident_pressure * 1.1
                )
                privileged_changes = safe_int(
                    random.uniform(0, 1.2) + department.key * 0.15 + workload.key * 0.2
                )
                guest_accounts = safe_int(
                    2
                    + department.key * 1.6
                    + (3.5 if workload.name == "Microsoft Teams" else 0.5)
                    + month_boost
                    + random.uniform(-2, 2)
                )
                teams_created = safe_int(
                    random.uniform(0, 1.8)
                    + (2.2 if workload.name == "Microsoft Teams" else 0.0)
                    + (0.5 if current_date.day <= 7 else 0.0)
                )
                teams_archived = safe_int(
                    random.uniform(0, 1.2)
                    + (1.1 if workload.name == "Microsoft Teams" and current_date.day >= 20 else 0.0)
                )
                compliance_score = round(
                    min(
                        96.0,
                        max(
                            52.0,
                            compliance_baseline(department.key, workload.key)
                            + day_index * 0.08
                            - high_incidents * 0.9
                            - medium_incidents * 0.35
                            - privileged_changes * 0.25
                            + random.uniform(-1.8, 1.8),
                        ),
                    ),
                    2,
                )
                risky_devices = safe_int(
                    random.uniform(0, 2.8)
                    + department.key * 0.7
                    + (2.6 if workload.name == "Endpoints" else 0.8)
                    + high_incidents * 0.6
                )
                data_loss_events = safe_int(
                    random.uniform(0, 0.9)
                    + (0.8 if workload.name in {"Microsoft Teams", "Entra ID"} else 0.2)
                    + (0.5 if department.name in {"Finance", "Research Office"} else 0.1)
                )

                rows.append(
                    {
                        "DateKey": int(current_date.strftime("%Y%m%d")),
                        "DepartmentKey": department.key,
                        "WorkloadKey": workload.key,
                        "SignInFailures": sign_in_failures,
                        "HighSeverityIncidents": high_incidents,
                        "MediumSeverityIncidents": medium_incidents,
                        "PrivilegedRoleChanges": privileged_changes,
                        "GuestAccountsActive": guest_accounts,
                        "TeamsCreated": teams_created,
                        "TeamsArchived": teams_archived,
                        "ComplianceScore": compliance_score,
                        "RiskyDevices": risky_devices,
                        "DataLossEvents": data_loss_events,
                    }
                )
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    dates = []
    for current_date in daterange(date(2026, 1, 1), date(2026, 3, 31)):
        dates.append(
            {
                "DateKey": int(current_date.strftime("%Y%m%d")),
                "Date": current_date.isoformat(),
                "Year": current_date.year,
                "Quarter": f"Q{((current_date.month - 1) // 3) + 1}",
                "MonthNumber": current_date.month,
                "MonthName": current_date.strftime("%B"),
                "WeekNumber": int(current_date.strftime("%V")),
                "DayOfMonth": current_date.day,
                "DayOfWeek": current_date.strftime("%A"),
                "IsWeekend": current_date.weekday() >= 5,
            }
        )

    departments = [
        {
            "DepartmentKey": item.key,
            "DepartmentName": item.name,
            "RiskTier": item.risk_tier,
            "ExecutiveOwner": item.executive_owner,
        }
        for item in DEPARTMENTS
    ]

    workloads = [
        {
            "WorkloadKey": item.key,
            "WorkloadName": item.name,
            "PlatformDomain": item.platform_domain,
            "PrimaryPersona": item.primary_persona,
        }
        for item in WORKLOADS
    ]

    facts = build_rows()

    write_csv(
        DATA_DIR / "dim_date.csv",
        [
            "DateKey",
            "Date",
            "Year",
            "Quarter",
            "MonthNumber",
            "MonthName",
            "WeekNumber",
            "DayOfMonth",
            "DayOfWeek",
            "IsWeekend",
        ],
        dates,
    )
    write_csv(
        DATA_DIR / "dim_department.csv",
        ["DepartmentKey", "DepartmentName", "RiskTier", "ExecutiveOwner"],
        departments,
    )
    write_csv(
        DATA_DIR / "dim_workload.csv",
        ["WorkloadKey", "WorkloadName", "PlatformDomain", "PrimaryPersona"],
        workloads,
    )
    write_csv(
        DATA_DIR / "fact_security_governance_daily.csv",
        [
            "DateKey",
            "DepartmentKey",
            "WorkloadKey",
            "SignInFailures",
            "HighSeverityIncidents",
            "MediumSeverityIncidents",
            "PrivilegedRoleChanges",
            "GuestAccountsActive",
            "TeamsCreated",
            "TeamsArchived",
            "ComplianceScore",
            "RiskyDevices",
            "DataLossEvents",
        ],
        facts,
    )

    print("Generated dataset in", DATA_DIR)
    print("Rows in fact table:", len(facts))


if __name__ == "__main__":
    main()
