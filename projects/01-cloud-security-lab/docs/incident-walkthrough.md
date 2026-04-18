# Incident Walkthrough

## Goal

Provide one clean incident story that ties together infrastructure, alerts, portal evidence, and analyst decision-making.

## Recommended Scenario

Use `controlled RBAC role assignment change` as the first fully documented incident.

Why this scenario works well:

- it is safe to perform in a sandbox
- it maps directly to least privilege and governance
- it triggers activity-based monitoring without needing complex workload behavior
- it is easy to explain to interviewers

## Scenario Summary

An administrator account makes a role assignment change in the sandbox. The platform alerting layer detects the change, and the analyst validates whether the action was expected or risky.

## Preconditions

- `Bicep` baseline deployed
- `Log Analytics workspace` exists
- Azure Monitor alert rules exist
- `Azure Activity` data is flowing to the workspace
- at least one admin-capable test account exists

## Trigger Steps

1. Sign in with the dedicated admin test account.
2. Assign a role such as `Reader` or `Contributor` at the resource group scope in the sandbox.
3. Wait for Azure Activity records and alert evaluation.
4. Revert the assignment after the evidence is captured.

## Expected Detection Evidence

- `AzureActivity` contains `Microsoft.Authorization/roleAssignments/write`
- the `RBAC Role Assignment Changes` alert rule shows a fired evaluation or matching results
- optional action group notification appears if email notifications were enabled

## Analyst Walkthrough

1. Open the alert or matching query results.
2. Identify the caller, scope, and affected role.
3. Confirm whether the target principal should have received that access.
4. Decide whether the action was approved, mistaken, or suspicious.
5. Revert or contain if the assignment was not intended.
6. Record the incident and the improvement action.

## Suggested Screenshot Set

1. alert rules list
2. role assignment alert details
3. Azure Activity query results
4. resource group role assignments before or after revert
5. short incident notes or timeline

## Example Lessons Learned

- role assignment changes are easy to miss without activity monitoring
- least privilege depends on both design and continuous review
- low-volume sandbox alerts must use tight, simple conditions
- screenshots and timelines make the project much stronger for interviews

## Follow-Up Improvements

- add stricter approval flow for privileged changes
- add Sentinel analytics or incidents for privileged actions
- add alert enrichment through an action group or playbook
- reduce standing access for admin personas where possible
