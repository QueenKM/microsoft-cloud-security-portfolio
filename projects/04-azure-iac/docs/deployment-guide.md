# Azure Baseline Deployment Guide

## Goal

Deploy the first reusable Azure baseline for the portfolio using `Bicep` at subscription scope.

## What Gets Deployed

- `rg-astera-sandbox-identity-monitoring`
- `rg-astera-sandbox-security-operations`
- `rg-astera-sandbox-demo-workload`
- one `Log Analytics workspace`
- one secure demo `Storage Account`

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

## Expected Outputs

- monitoring resource group name
- security operations resource group name
- demo workload resource group name
- Log Analytics workspace name
- storage account name

## Next Steps After Deployment

1. Enable `Microsoft Sentinel` on the created workspace.
2. Add Azure Activity and Entra connectors where available.
3. Capture resource screenshots for the portfolio.
4. Extend the baseline with networking, RBAC assignments, and a demo workload resource.

## Notes

- This workspace environment did not have `az` or `bicep` installed locally during authoring, so deployment commands were documented rather than executed here.
- Remote GitHub validation is included to compile the main Bicep template on push.
