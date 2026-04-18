# Project 01: Cloud Security Lab

## Goal

Build an end-to-end Azure security lab in a sandbox subscription that demonstrates identity protection, monitoring, detection, and response.

## Why This Project Matters

This is the flagship project in the portfolio. It shows hands-on execution with Microsoft security tooling and creates the strongest interview story for cloud security roles.

## Core Scope

- Entra ID tenant hardening
- Conditional Access baseline
- RBAC and least privilege design
- Defender for Cloud onboarding
- Sentinel SIEM deployment
- Log Analytics workspace and alerts
- simulated attack activity such as failed sign-ins or password spraying
- detection and response workflow

## Recommended Tech

- Azure subscription sandbox
- Microsoft Entra ID
- Azure Monitor and Log Analytics
- Microsoft Defender for Cloud
- Microsoft Sentinel
- KQL
- optional Logic Apps playbook for response automation

## Deliverables

- architecture diagram
- security baseline document
- KQL queries and analytic rules
- alert and incident screenshots
- attack simulation walkthrough
- incident response playbook

## Starter Docs

- [Implementation Plan](docs/implementation-plan.md)
- [Architecture Overview](docs/architecture.md)
- [Tenant And Subscription Boundaries](docs/tenant-subscription-boundaries.md)
- [RBAC Model](docs/rbac-model.md)
- [Conditional Access Matrix](docs/conditional-access-matrix.md)
- [Sentinel Onboarding Checklist](docs/sentinel-onboarding-checklist.md)
- [Starter KQL Detections](docs/kql-detections.md)
- [Safe Attack Simulation Plan](docs/attack-simulation.md)

## Build Phases

1. Create the sandbox structure and define admin roles.
2. Configure identity protections and Conditional Access.
3. Onboard Defender for Cloud, Sentinel, and logging.
4. Simulate suspicious activity and document detections.
5. Polish the repo with screenshots, lessons learned, and business value.

## Evidence To Capture

- Conditional Access policy screens
- Defender secure score or recommendations
- Sentinel incident queue
- Log Analytics query results
- RBAC assignment model
- attack timeline from event to response

## Cert Alignment

`SC-100`, `SC-200`, `SC-300`
