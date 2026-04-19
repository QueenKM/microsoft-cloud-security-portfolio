# Power BI Desktop Build Guide

## Goal

Turn the generated `Astera University` CSV dataset into a one-page Power BI dashboard with a clean semantic model and interview-ready visuals.

## Before You Start

1. Open [../data](../data).
2. Confirm these files exist:
   - `dim_date.csv`
   - `dim_department.csv`
   - `dim_workload.csv`
   - `fact_security_governance_daily.csv`
3. Open `Power BI Desktop`.

## Step 1: Import The CSV Files

1. Select `Get data`.
2. Choose `Text/CSV`.
3. Import all four CSV files from [../data](../data).
4. In the preview window, choose `Transform Data` instead of `Load`.

## Step 2: Apply Power Query Transformations

Use [power-query-transformations.md](power-query-transformations.md) as the source of truth.

### DimDate

- set `Date` to `Date`
- set year, quarter, month, and week columns to whole number
- set `IsWeekend` to true/false

### DimDepartment

- trim text columns
- confirm one row per department
- set `DepartmentKey` to whole number

### DimWorkload

- trim text columns
- set `WorkloadKey` to whole number

### FactSecurityGovernanceDaily

- set keys to whole number
- set metric columns to whole number except `ComplianceScore`
- set `ComplianceScore` to decimal number
- confirm the grain is still one row per `DateKey + DepartmentKey + WorkloadKey`

When done, select `Close & Apply`.

## Step 3: Create Relationships

Switch to `Model view` and create these single-direction relationships:

- `DimDate[DateKey]` -> `FactSecurityGovernanceDaily[DateKey]`
- `DimDepartment[DepartmentKey]` -> `FactSecurityGovernanceDaily[DepartmentKey]`
- `DimWorkload[WorkloadKey]` -> `FactSecurityGovernanceDaily[WorkloadKey]`

Keep the dimension tables on the outer edges and the fact table in the center. This gives you the best model-view screenshot later.

## Step 4: Add Measures

Copy the measures from [dax-measures.md](dax-measures.md) into a dedicated measure table or into `FactSecurityGovernanceDaily`.

Recommended order:

1. `Total Sign-In Failures`
2. `Total High Severity Incidents`
3. `Total Medium Severity Incidents`
4. `Total Privileged Role Changes`
5. `Total Data Loss Events`
6. `Active Guest Accounts`
7. `Teams Created`
8. `Teams Archived`
9. `Net Team Growth`
10. `Average Compliance Score`
11. `Average Risky Devices`
12. `Total Incidents`
13. `High Incident Rate`
14. `Privileged Change Rate`
15. `Guest Exposure Ratio`
16. `Incidents Per 100 Sign-In Failures`
17. `Compliance Score Delta Vs Previous Month`

## Step 5: Build The Report Page

Use [dashboard-design.md](dashboard-design.md) and [../artifacts/01-dashboard-wireframe.md](../artifacts/01-dashboard-wireframe.md).

### Top Row: KPI Cards

Add 6 cards:

- `Total Sign-In Failures`
- `Total Incidents`
- `Average Compliance Score`
- `Active Guest Accounts`
- `Net Team Growth`
- `Total Privileged Role Changes`

### Middle Row: Trend Visuals

#### Line chart: Sign-In Failures by Month

- Axis: `DimDate[MonthName]`
- Values: `Total Sign-In Failures`
- Sort by `DimDate[MonthNumber]`

#### Line and clustered column chart: Incidents vs Compliance

- Axis: `DimDate[MonthName]`
- Column values: `Total Incidents`
- Line values: `Average Compliance Score`

#### Stacked column chart: Incidents by Workload

- Axis: `DimWorkload[WorkloadName]`
- Column values:
  - `Total High Severity Incidents`
  - `Total Medium Severity Incidents`

### Bottom Row: Governance Visuals

#### Bar chart: Guest Accounts by Department

- Axis: `DimDepartment[DepartmentName]`
- Values: `Active Guest Accounts`

#### Clustered column chart: Teams Created vs Archived

- Axis: `DimDepartment[DepartmentName]`
- Values:
  - `Teams Created`
  - `Teams Archived`

#### Matrix: Department x Workload

- Rows: `DimDepartment[DepartmentName]`
- Columns: `DimWorkload[WorkloadName]`
- Values: `Total Incidents`
- Apply background color formatting to surface hot spots

## Step 6: Add Slicers

Add slicers for:

- `DimDate[MonthName]` or `DimDate[Date]`
- `DimDepartment[DepartmentName]`
- `DimWorkload[WorkloadName]`
- `DimDepartment[RiskTier]`

Place them vertically on the left or horizontally across the top.

## Step 7: Naming And Cleanup

- rename the report page to `Operations Overview`
- hide technical key columns from report view
- keep only business-friendly field names visible
- format compliance score as decimal or percentage-like presentation, depending on your style

## Screenshot Targets

When the report is ready, capture:

- model view screenshot
- Power Query screenshot
- final dashboard screenshot
- optional short GIF of slicer interaction

Use [screenshot-runbook.md](screenshot-runbook.md) for exact filenames.

## Strong Interview Narrative

1. The data model is simple on purpose so DAX stays clean.
2. The dashboard combines security signals and governance signals on one page.
3. The visuals move from executive KPI summary to operational drilldown.
4. The dataset connects back to the rest of the portfolio instead of being random analytics work.
