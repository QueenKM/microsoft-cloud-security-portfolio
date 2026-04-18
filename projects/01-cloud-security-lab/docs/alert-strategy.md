# Alert Strategy

## Goal

Define a practical first alerting layer for the lab that is realistic, easy to explain in interviews, and safe to deploy before the environment has full production-style telemetry.

## Detection Layers

### Layer 1: Platform Alerts Through IaC

These alerts are good first candidates for infrastructure-driven deployment because they rely on `AzureActivity`, which is stable and security-relevant.

- privileged or broad role assignment changes
- network security group or security rule changes
- diagnostic settings changes or removals

### Layer 2: Lab And Analyst Queries

These queries are useful for `Log Analytics` or `Sentinel` hunting, tuning, and demonstrations.

- failed sign-ins by user
- failed sign-ins by IP
- high failure rate followed by success
- resource activity review

## Why This Split Works

- `AzureActivity` based alerts support early detection even before the full lab matures.
- identity and workload detections often require data source onboarding, tuning, and realistic thresholds.
- this gives the portfolio both reproducible infrastructure and analyst-focused investigation content.

## Deployed Alert Candidates

| Alert | Data Source | Purpose | Deployment Style |
| --- | --- | --- | --- |
| `RBAC Role Assignment Changes` | `AzureActivity` | detect changes to role assignments | `Bicep` |
| `NSG Or Security Rule Changes` | `AzureActivity` | detect network control changes | `Bicep` |
| `Diagnostic Settings Changes` | `AzureActivity` | detect attempts to reduce visibility | `Bicep` |

## Query Assets

The lab query files live in [../queries](../queries/01-rbac-role-assignment-changes.kql).

Recommended first-use order:

1. `01-rbac-role-assignment-changes.kql`
2. `02-nsg-security-rule-changes.kql`
3. `03-diagnostic-settings-changes.kql`
4. `04-failed-signins-by-user.kql`
5. `05-failed-signins-by-ip.kql`
6. `06-high-failure-rate-followed-by-success.kql`

## Tuning Notes

- keep thresholds low enough for a small sandbox
- avoid noisy alerts that trigger on every normal action
- mark portal-created alerts separately from IaC-managed alerts if you temporarily experiment
- prefer activity-based alerts first, then grow into richer Sentinel analytics
