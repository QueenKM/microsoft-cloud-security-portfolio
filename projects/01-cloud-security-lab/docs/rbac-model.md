# RBAC And Least Privilege Model

## Goal

Use a simple role model that demonstrates separation of duties without making the sandbox too complex to operate.

## Design Rules

- no daily work from highly privileged accounts
- assign permissions through groups where possible
- keep privileged assignments scoped to the smallest possible boundary
- document every exception, especially break-glass access

## Lab Personas

| Persona | Purpose | Privilege Level |
| --- | --- | --- |
| `student-user` | normal cloud and app access simulation | low |
| `faculty-user` | normal business access with slightly broader data exposure | low |
| `it-admin` | platform administration and configuration tasks | elevated |
| `security-analyst` | monitoring, triage, and investigation | elevated |
| `break-glass-admin` | emergency access only | highest, tightly controlled |

## Group-Based Access Model

| Group | Purpose | Example Members |
| --- | --- | --- |
| `grp-lab-subscription-readers` | read-only visibility into Azure resources | security analyst |
| `grp-lab-resource-admins` | manage demo workload resources | IT admin |
| `grp-lab-monitoring-contributors` | manage Log Analytics and alert rules | IT admin |
| `grp-lab-sentinel-analysts` | investigate Sentinel incidents | security analyst |
| `grp-lab-conditional-access-admins` | manage Conditional Access policies | IT admin |
| `grp-lab-break-glass` | emergency-only directory access | break-glass admin |

## Azure And Entra Role Matrix

| Scope | Role | Assigned To | Why |
| --- | --- | --- | --- |
| Entra tenant | `Global Administrator` | break-glass admin only | emergency recovery only |
| Entra tenant | `Conditional Access Administrator` | IT admin group | manage access policies without full tenant control |
| Entra tenant | `Security Reader` | security analyst group | inspect security data without making wide changes |
| Entra tenant | `Security Administrator` | IT admin, optional | manage security settings if required by the lab |
| Subscription | `Reader` | security analyst group | review Azure resources and configurations |
| Resource group | `Contributor` | IT admin group on `rg-demo-workload` only | operate the demo workload |
| Resource group | `Monitoring Contributor` | IT admin group on monitoring scope | manage alerts and diagnostics |
| Sentinel workspace | `Microsoft Sentinel Reader` or equivalent analyst role | security analyst group | investigate incidents |
| Sentinel workspace | `Microsoft Sentinel Contributor` | IT admin or security engineer role | create rules and content |

## Standing Access To Avoid

- permanent `Owner` on the whole subscription
- everyday use of `Global Administrator`
- broad `Contributor` rights across every resource group
- shared admin accounts

## Break-Glass Guidance

- keep at least one dedicated emergency admin account
- exclude it from normal Conditional Access enforcement only when required
- protect it with a long random password and offline storage process
- monitor every sign-in and treat access as an incident

## Evidence To Capture

- group membership screenshots
- scoped role assignments at resource group level
- a short explanation of why each privileged role exists
- any compensating controls for excluded emergency accounts
