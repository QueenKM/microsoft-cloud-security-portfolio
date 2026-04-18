# Live Sandbox Status

## Goal

Record the current state of the real Azure deployment so the repository clearly separates completed evidence from pending validation work.

## Deployment Snapshot

- Deployment date: `2026-04-18`
- Subscription type: `Azure for Students`
- Region: `Sweden Central`
- Deployment scope: subscription
- Deployment status: `Succeeded`

## Live Resources Confirmed

- `rg-astera-sandbox-identity-monitoring`
- `rg-astera-sandbox-security-operations`
- `rg-astera-sandbox-demo-workload`
- `law-astera-sandbox-b6izcc`
- `vnet-astera-sandbox-core`
- `nsg-astera-sandbox-management`
- `nsg-astera-sandbox-workload`
- `stasterasandboxb6izcc`
- Azure Monitor action group and scheduled query alerts
- `Microsoft Sentinel` enabled on the Log Analytics workspace

## Evidence Captured

Headline evidence already collected:

- [02-log-analytics-workspace-overview.png](../artifacts/screenshots/02-log-analytics-workspace-overview.png)
- [03-azure-monitor-alert-rules-list.png](../artifacts/screenshots/03-azure-monitor-alert-rules-list.png)
- [04-role-assignment-alert-details.png](../artifacts/screenshots/04-role-assignment-alert-details.png)
- [05-nsg-diagnostics-settings.png](../artifacts/screenshots/05-nsg-diagnostics-settings.png)
- [06-storage-blob-diagnostics-settings.png](../artifacts/screenshots/06-storage-blob-diagnostics-settings.png)
- [06-subscription-activity-log-export.png](../artifacts/screenshots/06-subscription-activity-log-export.png)
- [07-sentinel-overview.png](../artifacts/screenshots/07-sentinel-overview.png)
- [07-sentinel-data-connectors.png](../artifacts/screenshots/07-sentinel-data-connectors.png)

Supporting troubleshooting evidence:

- [06-subscription-activity-log-export-missing.png](../artifacts/screenshots/06-subscription-activity-log-export-missing.png)

## Current Blockers

### Conditional Access

`Conditional Access` access in `Microsoft Entra` is blocked for the current user because the tenant does not grant sufficient administrative privilege for policy management.

Observed result:

- Conditional Access policies page returns `Insufficient privileges to complete the operation`

Impact:

- the project can document the intended Conditional Access design
- live Conditional Access screenshots are pending either higher privilege or a different tenant

### AzureActivity Validation Window

The subscription activity log export was initially missing and was created later on `2026-04-18`.

Observed state:

- `AzureActivity` queries returned no rows before the subscription activity log diagnostic setting was created
- the export path now points to `law-astera-sandbox-b6izcc`

Impact:

- platform detections should be validated only after the expected ingestion window
- a fresh NSG change test should be generated after the export has had time to populate the workspace

## Next Validation Steps

1. Wait for the subscription activity log export ingestion window to pass.
2. Create and remove one temporary NSG rule in the sandbox.
3. Query `AzureActivity` for the NSG write and delete operations.
4. Capture:
   - `08-subscription-activity-log-nsg-change.png`
   - `09-kql-nsg-change-results.png`
5. Check whether the `NSG Or Security Rule Changes` alert fires and capture one alert or incident view if available.

## Interview Framing

This project already demonstrates:

- infrastructure automation in a real Azure subscription
- centralized logging and alerting
- diagnostic settings hygiene
- Sentinel onboarding
- practical troubleshooting of region policy restrictions, access blockers, and telemetry pipeline timing

The remaining work is focused on final detection proof, not on building the lab from scratch.
