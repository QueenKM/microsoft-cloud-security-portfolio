# Cloud Security Lab Implementation Plan

## Objective

Create a secure Azure sandbox for `Astera University` that demonstrates:

- identity hardening
- centralized logging
- security posture monitoring
- basic detections
- incident triage and response

## Suggested Azure Layout

## Subscription Structure

- `mg-astera-security-lab` management group, optional
- `sub-astera-security-sandbox` subscription
- `rg-identity-monitoring`
- `rg-security-operations`
- `rg-demo-workload`

## Core Services

- Microsoft Entra ID
- Log Analytics workspace
- Microsoft Sentinel
- Defender for Cloud
- Azure Monitor alerting
- one demo workload such as a VM or App Service

## Identity Baseline

- create separate test users for `student`, `faculty`, `it-admin`, and `security-analyst`
- create at least one break-glass account with very strong protection and offline storage guidance
- disable legacy authentication where possible
- enforce MFA for admins and high-risk access paths
- use least privilege role assignments

## Conditional Access Starter Policies

- require MFA for administrators
- block legacy authentication
- require MFA for risky sign-ins, if available in the tenant
- require compliant or trusted access for admin portals, if supported by the lab scope
- exclude break-glass account from standard sign-in disruption policies with strong compensating controls

## Monitoring Baseline

- deploy one Log Analytics workspace
- enable Microsoft Sentinel on that workspace
- onboard Azure activity logs and Entra ID logs where available
- connect Defender for Cloud
- enable diagnostic settings on the demo workload and key Azure resources

## Minimum Detection Set

- repeated failed sign-ins by account
- repeated failed sign-ins by IP address
- privileged role assignment changes
- disabled or modified security controls
- impossible or unusual admin sign-in patterns, if enough data exists

## Response Workflow

1. Alert triggers in Sentinel or Azure Monitor.
2. Analyst opens the incident and validates the evidence.
3. Analyst checks related sign-in activity and account context.
4. Analyst contains the issue by disabling the test account or revoking access in the sandbox.
5. Analyst documents findings, root cause, and follow-up improvements.

## Deliverables For GitHub

- architecture diagram
- policy list
- screenshots of Conditional Access and Sentinel
- KQL queries
- attack simulation notes
- incident response walkthrough

## Definition Of Done

- at least three identity policies configured
- Defender for Cloud onboarded
- Sentinel enabled and receiving data
- at least two alerting or analytic rules documented
- one safe attack simulation completed
- one incident story documented with screenshots
