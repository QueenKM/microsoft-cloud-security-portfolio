# Azure Baseline Validation Checklist

## Template Checks

- [ ] `main.bicep` compiles successfully
- [ ] parameter file values match the target subscription and region
- [ ] naming stays within Azure length and character limits
- [ ] tags are applied to deployed resources

## Resource Checks

- [ ] all three resource groups are created
- [ ] `Log Analytics workspace` is deployed in the monitoring resource group
- [ ] `Virtual Network` is deployed in the demo workload resource group
- [ ] management and workload subnets are created with the expected address ranges
- [ ] both subnets are associated with the expected `NSG`
- [ ] `NSG` diagnostic settings send supported logs to `Log Analytics`
- [ ] `Storage Account` is deployed in the demo workload resource group
- [ ] storage blocks blob public access
- [ ] storage enforces HTTPS and `TLS 1.2`
- [ ] storage blob service diagnostic settings send supported logs to `Log Analytics`
- [ ] optional Linux `VM` deploys successfully when enabled
- [ ] optional `VM` lands in the workload subnet
- [ ] optional `RBAC` assignments are created only when principal IDs are supplied

## Operational Checks

- [ ] deployment outputs are recorded
- [ ] screenshots are captured for the repo
- [ ] workspace is ready for Sentinel enablement
- [ ] cost-impacting settings are understood before expanding the lab
- [ ] temporary public IP access, if used, is removed after testing
