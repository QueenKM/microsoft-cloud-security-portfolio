# Dashboard Wireframe

```mermaid
flowchart TB
    subgraph K["Top KPI Row"]
        K1["Total Sign-In Failures"]
        K2["Total Incidents"]
        K3["Average Compliance Score"]
        K4["Active Guest Accounts"]
        K5["Net Team Growth"]
        K6["Privileged Role Changes"]
    end

    subgraph T["Trend Row"]
        T1["Line chart: Sign-In Failures by Month"]
        T2["Combo chart: Incidents vs Compliance Score"]
        T3["Stacked columns: Incidents by Workload"]
    end

    subgraph G["Governance Row"]
        G1["Bar chart: Guest Accounts by Department"]
        G2["Columns: Teams Created vs Archived"]
        G3["Heat matrix: Department x Workload Risk"]
    end
```

## Reporting Story

The dashboard should quickly show whether operational noise is increasing faster than control maturity. If sign-in failures, high-severity incidents, and guest growth rise while compliance score stays flat, the university is becoming busier without becoming safer.
