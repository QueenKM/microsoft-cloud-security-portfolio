# DAX Measures

## Core Volume Measures

```DAX
Total Sign-In Failures =
SUM ( FactSecurityGovernanceDaily[SignInFailures] )
```

```DAX
Total High Severity Incidents =
SUM ( FactSecurityGovernanceDaily[HighSeverityIncidents] )
```

```DAX
Total Medium Severity Incidents =
SUM ( FactSecurityGovernanceDaily[MediumSeverityIncidents] )
```

```DAX
Total Privileged Role Changes =
SUM ( FactSecurityGovernanceDaily[PrivilegedRoleChanges] )
```

```DAX
Total Data Loss Events =
SUM ( FactSecurityGovernanceDaily[DataLossEvents] )
```

## Governance Measures

```DAX
Active Guest Accounts =
SUM ( FactSecurityGovernanceDaily[GuestAccountsActive] )
```

```DAX
Teams Created =
SUM ( FactSecurityGovernanceDaily[TeamsCreated] )
```

```DAX
Teams Archived =
SUM ( FactSecurityGovernanceDaily[TeamsArchived] )
```

```DAX
Net Team Growth =
[Teams Created] - [Teams Archived]
```

## Posture Measures

```DAX
Average Compliance Score =
AVERAGE ( FactSecurityGovernanceDaily[ComplianceScore] )
```

```DAX
Average Risky Devices =
AVERAGE ( FactSecurityGovernanceDaily[RiskyDevices] )
```

## Derived Insight Measures

```DAX
Total Incidents =
[Total High Severity Incidents] + [Total Medium Severity Incidents]
```

```DAX
High Incident Rate =
DIVIDE ( [Total High Severity Incidents], [Total Incidents] )
```

```DAX
Privileged Change Rate =
DIVIDE ( [Total Privileged Role Changes], [Total Incidents] )
```

```DAX
Guest Exposure Ratio =
DIVIDE ( [Active Guest Accounts], [Teams Created] + 1 )
```

```DAX
Incidents Per 100 Sign-In Failures =
DIVIDE ( [Total Incidents] * 100, [Total Sign-In Failures] )
```

```DAX
Compliance Score Delta Vs Previous Month =
VAR CurrentMonthScore =
    [Average Compliance Score]
VAR PreviousMonthScore =
    CALCULATE (
        [Average Compliance Score],
        DATEADD ( DimDate[Date], -1, MONTH )
    )
RETURN
    CurrentMonthScore - PreviousMonthScore
```

## Suggested KPI Cards

- `Total Sign-In Failures`
- `Total Incidents`
- `Average Compliance Score`
- `Active Guest Accounts`
- `Net Team Growth`
- `Compliance Score Delta Vs Previous Month`
