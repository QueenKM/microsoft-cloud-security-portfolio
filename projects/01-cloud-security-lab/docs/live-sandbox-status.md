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
- [09-kql-nsg-change-results.png](../artifacts/screenshots/09-kql-nsg-change-results.png)
- [10-azure-monitor-nsg-alert-fired.png](../artifacts/screenshots/10-azure-monitor-nsg-alert-fired.png)

Supporting troubleshooting evidence:

- [06-subscription-activity-log-export-missing.png](../artifacts/screenshots/06-subscription-activity-log-export-missing.png)

## Validation Results

## NSG Change Detection

The live sandbox now has end-to-end validation for the `NSG Or Security Rule Changes` detection path.

Observed result:

- a temporary NSG rule was created and removed in the sandbox
- `AzureActivity` returned `securityRules/write` and `securityRules/delete` events for the target resource group
- the `NSG Or Security Rule Changes` scheduled query alert fired in `Azure Monitor`

Impact:

- the project now includes live proof of both telemetry ingestion and alert generation
- the remaining work is no longer about core monitoring validation

## Current Blockers

### Conditional Access

`Conditional Access` access in `Microsoft Entra` is blocked for the current user because the tenant does not grant sufficient administrative privilege for policy management.

Observed result:

- Conditional Access policies page returns `Insufficient privileges to complete the operation`

Impact:

- the project can document the intended Conditional Access design
- live Conditional Access screenshots are pending either higher privilege or a different tenant

## Next Validation Steps

1. Capture `Conditional Access` evidence if tenant privilege is later granted.
2. Optionally capture `08-subscription-activity-log-nsg-change.png` as extra portal evidence.
3. Optionally capture a Sentinel incident or additional alert timeline view.
4. Optionally add Defender for Cloud screenshots if the service is later enabled in the same sandbox.

## Interview Framing

This project already demonstrates:

- infrastructure automation in a real Azure subscription
- centralized logging and alerting
- diagnostic settings hygiene
- Sentinel onboarding
- practical troubleshooting of region policy restrictions, access blockers, and telemetry pipeline timing

The remaining work is focused on final detection proof, not on building the lab from scratch.
The main remaining gap is identity-policy evidence, not monitoring capability.
