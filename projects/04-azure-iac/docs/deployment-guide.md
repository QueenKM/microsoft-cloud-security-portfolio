# Azure Baseline Deployment Guide

## Goal

Deploy the first reusable Azure baseline for the portfolio using `Bicep` at subscription scope.

## What Gets Deployed

- `rg-astera-sandbox-identity-monitoring`
- `rg-astera-sandbox-security-operations`
- `rg-astera-sandbox-demo-workload`
- one `Log Analytics workspace`
- one `Virtual Network`
- two subnets: management and workload
- two `Network Security Groups`
- one secure demo `Storage Account`
- diagnostic settings for supported `NSG` and storage blob logs
- one optional Linux `VM` workload
- optional `RBAC` assignments for IT admin and security analyst principals

## Prerequisites

- Azure subscription with permission to deploy at subscription scope
- Azure CLI with Bicep support
- authenticated session with `az login`
- a region that supports the selected resources

## Files

- main template: [bicep/main.bicep](../bicep/main.bicep)
- default parameters: [bicep/parameters/sandbox.parameters.json](../bicep/parameters/sandbox.parameters.json)

## Validate With What-If

```bash
az deployment sub what-if \
  --name astera-sandbox-baseline-whatif \
  --location westeurope \
  --template-file ./projects/04-azure-iac/bicep/main.bicep \
  --parameters @./projects/04-azure-iac/bicep/parameters/sandbox.parameters.json
```

## Deploy

```bash
az deployment sub create \
  --name astera-sandbox-baseline \
  --location westeurope \
  --template-file ./projects/04-azure-iac/bicep/main.bicep \
  --parameters @./projects/04-azure-iac/bicep/parameters/sandbox.parameters.json
```

## Optional Parameters To Override

Before enabling the demo workload or RBAC:

- set `deployDemoVirtualMachine=true`
- provide `demoVirtualMachineSshPublicKey`
- optionally set `demoVirtualMachinePublicIpEnabled=true` for temporary admin access
- provide `itAdminPrincipalId` and `securityAnalystPrincipalId` to create Azure RBAC assignments
- change `itAdminPrincipalType` or `securityAnalystPrincipalType` if you use users or service principals instead of groups

## Expected Outputs

- monitoring resource group name
- security operations resource group name
- demo workload resource group name
- Log Analytics workspace name
- virtual network name
- storage account name
- optional demo virtual machine name

## Next Steps After Deployment

1. Enable `Microsoft Sentinel` on the created workspace.
2. Add Azure Activity and Entra connectors where available.
3. Capture resource screenshots for the portfolio.
4. If needed, redeploy with the optional demo VM and RBAC principal IDs enabled.

## Notes

- This workspace environment did not have `az` or `bicep` installed locally during authoring, so deployment commands were documented rather than executed here.
- Remote GitHub validation is included to compile the main Bicep template on push.
