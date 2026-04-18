# Power Query Transformations

## Import Strategy

Import all four CSV files from the `data` folder and apply these baseline transformations.

## DimDate

- set `Date` to `Date` type
- set numeric columns to whole number
- set `IsWeekend` to true/false
- sort by `Date`

## DimDepartment

- trim text fields
- keep one row per department
- set `DepartmentKey` to whole number

## DimWorkload

- trim text fields
- set `WorkloadKey` to whole number
- use `WorkloadName` for slicers and legend values

## FactSecurityGovernanceDaily

- set keys to whole number
- set metric columns to whole number except `ComplianceScore`
- set `ComplianceScore` to decimal number
- validate that there are no null keys
- confirm one row per `DateKey + DepartmentKey + WorkloadKey`

## Suggested Validation Steps

- count rows in the fact table before and after transformations
- confirm every fact row joins to all three dimensions
- confirm no negative values exist in the generated metrics
- confirm `ComplianceScore` stays in the expected range

## Optional Modeling Enhancements

- create a date table in DAX only if you do not want to use `DimDate`
- add a `MonthStartDate` column for cleaner monthly visuals
- create a department grouping table if you want a faculty versus operations split
