# Azure Baseline Validation Checklist

## Template Checks

- [ ] `main.bicep` compiles successfully
- [ ] parameter file values match the target subscription and region
- [ ] naming stays within Azure length and character limits
- [ ] tags are applied to deployed resources

## Resource Checks

- [ ] all three resource groups are created
- [ ] `Log Analytics workspace` is deployed in the monitoring resource group
- [ ] `Storage Account` is deployed in the demo workload resource group
- [ ] storage blocks blob public access
- [ ] storage enforces HTTPS and `TLS 1.2`

## Operational Checks

- [ ] deployment outputs are recorded
- [ ] screenshots are captured for the repo
- [ ] workspace is ready for Sentinel enablement
- [ ] cost-impacting settings are understood before expanding the lab
