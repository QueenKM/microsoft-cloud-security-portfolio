# Screenshot Runbook

## Goal

Capture consistent, recruiter-friendly evidence after the lab is deployed and configured.

## Naming Convention

Use filenames like these in [../artifacts](../artifacts/README.md):

- `01-ca-admin-mfa-policy.png`
- `02-log-analytics-workspace-overview.png`
- `03-azure-monitor-alert-rules-list.png`
- `04-role-assignment-alert-details.png`
- `05-nsg-diagnostics-settings.png`
- `06-storage-blob-diagnostics-settings.png`
- `07-sentinel-data-connectors.png`
- `08-sentinel-incident-overview.png`
- `09-kql-role-assignment-results.png`
- `10-kql-failed-signins-results.png`

## Must-Have Screenshots

### Identity And Access

1. `Conditional Access` policy list
2. admin MFA policy details
3. blocked legacy authentication policy details
4. RBAC role assignments at resource group scope

### Monitoring And Alerting

1. `Log Analytics workspace` overview
2. Azure Monitor alert rules list
3. one alert rule details page for role assignment changes
4. one alert rule details page for NSG or diagnostics changes
5. action group details, if configured

### Diagnostic Settings

1. NSG diagnostic settings targeting `Log Analytics`
2. storage blob service diagnostic settings targeting `Log Analytics`
3. Azure Activity or subscription diagnostics evidence, if configured

### Sentinel And Investigation

1. Sentinel overview page
2. data connectors page
3. one incident view after a safe simulation
4. KQL query results for failed sign-ins or Azure activity changes

## Capture Instructions

### Conditional Access

- go to `Entra ID` -> `Protection` -> `Conditional Access`
- capture the policy list
- open the admin MFA policy and capture assignments and access controls

### Log Analytics Workspace

- go to the created workspace
- capture the overview page showing workspace name and subscription
- capture query results after running one saved detection query

### Alert Rules

- go to `Azure Monitor` -> `Alerts` -> `Alert rules`
- capture the full list with rule names and states visible
- open the `RBAC Role Assignment Changes` rule
- capture the scope
- capture the query
- capture the evaluation frequency
- capture the severity
- capture the action group target, if present

### Diagnostics Capture

- go to each `NSG` -> `Monitoring` -> `Diagnostic settings`
- capture the categories and destination workspace
- go to the storage account `Blob service` diagnostic settings and capture enabled log categories

### Sentinel

- go to the `Microsoft Sentinel` workspace
- capture the overview, data connectors, and incidents list
- after a safe simulation, open one incident and capture the entities and timeline

## Presentation Tips

- crop tightly so the control being demonstrated is easy to read
- avoid screenshots with personal profile menus or irrelevant tabs open
- redact subscription IDs, tenant IDs, or emails when appropriate
- keep the portal theme consistent across screenshots if possible

## When To Take Screenshots

Take screenshots after these milestones:

1. `Bicep` baseline deployment completed
2. Conditional Access policies configured
3. diagnostic settings enabled
4. alert rules created or verified
5. Sentinel connected and receiving data
6. one safe simulation completed
