# Starter KQL Detections

These are lab-friendly starter queries for detecting suspicious identity activity. Adjust thresholds for your tenant size and log volume.

## Query Files

The reusable query assets also exist as standalone files:

- [01-rbac-role-assignment-changes.kql](../queries/01-rbac-role-assignment-changes.kql)
- [02-nsg-security-rule-changes.kql](../queries/02-nsg-security-rule-changes.kql)
- [03-diagnostic-settings-changes.kql](../queries/03-diagnostic-settings-changes.kql)
- [04-failed-signins-by-user.kql](../queries/04-failed-signins-by-user.kql)
- [05-failed-signins-by-ip.kql](../queries/05-failed-signins-by-ip.kql)
- [06-high-failure-rate-followed-by-success.kql](../queries/06-high-failure-rate-followed-by-success.kql)

## Failed Sign-Ins By User

```kusto
SigninLogs
| where ResultType != 0
| summarize FailedAttempts = count() by UserPrincipalName, bin(TimeGenerated, 15m)
| where FailedAttempts >= 5
| order by FailedAttempts desc
```

## Failed Sign-Ins By IP Address

```kusto
SigninLogs
| where ResultType != 0
| summarize FailedAttempts = count(), UsersTargeted = dcount(UserPrincipalName) by IPAddress, bin(TimeGenerated, 15m)
| where FailedAttempts >= 10 or UsersTargeted >= 3
| order by FailedAttempts desc
```

## Role Assignment Changes In Azure Activity

```kusto
AzureActivity
| where OperationNameValue has "roleAssignments"
| project TimeGenerated, Caller, OperationNameValue, ActivityStatusValue, ResourceGroup, ResourceId
| order by TimeGenerated desc
```

## High Failure Rate Followed By Success

```kusto
let FailedWindow =
    SigninLogs
    | where ResultType != 0
    | summarize FailedAttempts = count() by UserPrincipalName, IPAddress, bin(TimeGenerated, 30m);
let SuccessWindow =
    SigninLogs
    | where ResultType == 0
    | summarize SuccessfulSignIns = count() by UserPrincipalName, IPAddress, bin(TimeGenerated, 30m);
FailedWindow
| join kind=inner SuccessWindow on UserPrincipalName, IPAddress, TimeGenerated
| where FailedAttempts >= 5 and SuccessfulSignIns >= 1
| project TimeGenerated, UserPrincipalName, IPAddress, FailedAttempts, SuccessfulSignIns
| order by TimeGenerated desc
```

## Notes

- `SigninLogs` availability depends on tenant licensing and connector configuration.
- Query field names can vary depending on log source and table version.
- Treat these as starter detections for a portfolio lab, then tune them after data starts flowing.
