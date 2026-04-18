# Tenant And Subscription Boundaries

## Goal

Define a safe and realistic scope for the Azure sandbox so the lab stays affordable, easy to explain, and clearly separated from any real production activity.

## Scope Summary

| Layer | Decision | Rationale |
| --- | --- | --- |
| Entra tenant | use a dedicated sandbox or student tenant | keeps experiments away from real users and business identities |
| Azure subscription | use one dedicated lab subscription | simplifies billing, RBAC, and cleanup |
| Resource grouping | split monitoring, security operations, and demo workload | supports least privilege and cleaner ownership |
| Identity automation | mostly manual in the first phase | Entra configuration is central to the story and easier to explain step by step |
| Infrastructure automation | use `Bicep` for Azure resource baseline | Azure-native, recruiter-friendly, and easy to map to the architecture |

## In Scope

- one sandbox Entra tenant or equivalent isolated test tenant
- one Azure subscription dedicated to the lab
- monitoring and security resources such as `Log Analytics` and `Microsoft Sentinel`
- one small demo workload resource group
- RBAC for Azure resources and security operations
- safe attack simulation using lab-only accounts

## Out Of Scope

- production identities or real organizational users
- multi-subscription hub-and-spoke networking
- private endpoints and full enterprise network segmentation in phase one
- large-scale endpoint onboarding
- aggressive attack tooling or any activity outside the sandbox

## Tenant Boundary Rules

- do not reuse personal or production administrator accounts for daily lab operations
- keep at least one `break-glass` account documented and tightly controlled
- create dedicated lab personas for `student`, `faculty`, `it-admin`, and `security-analyst`
- avoid storing sensitive screenshots or identifiable tenant data in the public repository

## Subscription Boundary Rules

- subscription name: `sub-astera-security-sandbox`
- default region for the baseline: `westeurope`
- cost control approach: prefer low-cost services and one demo workload only
- cleanup approach: resources should be grouped so the lab can be removed cleanly

## Resource Group Ownership

| Resource Group | Primary Purpose | Primary Owner |
| --- | --- | --- |
| `rg-astera-sandbox-identity-monitoring` | shared monitoring foundation | IT admin |
| `rg-astera-sandbox-security-operations` | Sentinel and security workflows | security analyst and IT admin |
| `rg-astera-sandbox-demo-workload` | workload used for diagnostics and posture examples | IT admin |

## Naming Standard

- prefix: `astera`
- environment: `sandbox`
- resource groups: `rg-<workload>-<environment>-<purpose>`
- Log Analytics: `law-<workload>-<environment>-<suffix>`
- storage: `st<workload><environment><suffix>`

## What Is Managed Where

| Area | Managed In Project | Why |
| --- | --- | --- |
| subscription resource groups | `04-azure-iac` | reproducible infrastructure baseline |
| Log Analytics workspace | `04-azure-iac` | core platform resource that benefits from automation |
| storage baseline | `04-azure-iac` | good example of secure-by-default resource configuration |
| Conditional Access | `01-cloud-security-lab` | identity policy work is easier to demonstrate manually first |
| Sentinel connectors and analytic rules | `01-cloud-security-lab` | depends on tenant capabilities and log availability |

## Recommended Phase 1 Baseline

1. Create the three resource groups through `Bicep`.
2. Deploy the `Log Analytics workspace`.
3. Deploy a secure demo `Storage Account`.
4. Enable Sentinel manually on the workspace.
5. Add identity controls and detections in the cloud lab project.
