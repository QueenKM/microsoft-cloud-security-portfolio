# Cloud Security Lab Artifacts

Store screenshots, exports, and demo evidence for the project in this folder.

## Suggested Contents

- Conditional Access screenshots
- Sentinel connector screenshots
- incident screenshots
- Azure Monitor alert rule screenshots
- action group screenshots
- KQL result screenshots
- architecture exports
- redacted response notes

Use clear names such as `ca-admin-mfa-policy.png` or `sentinel-failed-signins-incident.png`.

## Current Evidence Set

The following live screenshots were captured from the Azure for Students sandbox deployment and copied into [screenshots](screenshots):

- `02-log-analytics-workspace-overview.png`
- `03-azure-monitor-alert-rules-list.png`
- `04-role-assignment-alert-details.png`
- `05-nsg-diagnostics-settings.png`
- `06-storage-blob-diagnostics-settings.png`
- `06-subscription-activity-log-export.png`
- `07-sentinel-overview.png`
- `07-sentinel-data-connectors.png`

Repository copies are redacted or cropped where needed so public GitHub artifacts do not expose subscription-specific identifiers.

## Troubleshooting Evidence

These screenshots are useful to explain the build journey and blockers, but should usually be treated as appendix material instead of headline portfolio evidence:

- `06-subscription-activity-log-export-missing.png`

## Remaining Capture Goals

- `04-role-assignment-alert-configuration.png`
- `08-subscription-activity-log-nsg-change.png`
- `09-kql-nsg-change-results.png`
- `10-kql-failed-signins-results.png`, only if Entra sign-in telemetry becomes available
