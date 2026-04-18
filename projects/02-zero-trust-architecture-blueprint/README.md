# Project 02: Zero Trust Architecture Blueprint

## Goal

Create an architecture-first blueprint for how `Astera University` applies Zero Trust across identity, devices, applications, data, infrastructure, and security operations.

## Why This Project Matters

This project is designed to show architect-level thinking, not only execution. It demonstrates that you can define trust boundaries, justify design choices, record tradeoffs, and model threats in a way that is useful to both engineers and leadership.

## Current Status

`In progress`

Core blueprint documentation, policy decisions, diagrams, and STRIDE artifacts are now in place. Live validation in Azure can be added later when sandbox subscription capacity is available.

## Architecture Story

`Astera University` is a mid-sized institution with:

- remote staff and faculty
- student collaboration in Microsoft 365
- regulated academic and personnel data
- a small IT team with limited operational capacity
- a need to reduce standing privilege and lateral movement risk

The blueprint assumes that every access request must be evaluated through the same policy logic:

- verify explicitly
- use least privilege
- assume breach

## Deliverables

- [Architecture Overview](docs/architecture-overview.md)
- [Device Compliance Model](docs/device-compliance-model.md)
- [Policy Pack](docs/policy-pack.md)
- [Implementation Roadmap](docs/implementation-roadmap.md)
- [Demo Checklist](docs/demo-checklist.md)
- [Reference Diagram](diagrams/zero-trust-reference.md)
- [Identity And Device Access Flow](diagrams/identity-device-access-flow.md)
- [Decision Log: Centralize Identity Control Plane](decision-logs/2026-04-18-centralize-identity-control-plane.md)
- [Decision Log: Require Device Trust For Sensitive Access](decision-logs/2026-04-18-require-device-trust-for-sensitive-access.md)
- [STRIDE Threat Model: Privileged Admin Access](threat-models/stride-privileged-admin-access.md)
- [Artifacts Folder](artifacts/README.md)

## Quick Links

- [Reference Diagram](diagrams/zero-trust-reference.md)
- [Identity And Device Access Flow](diagrams/identity-device-access-flow.md)
- [Policy Pack](docs/policy-pack.md)
- [Implementation Roadmap](docs/implementation-roadmap.md)
- [STRIDE Threat Model](threat-models/stride-privileged-admin-access.md)

## Blueprint Snapshot

| Layer | Core Decision |
| --- | --- |
| Identity | Centralize identity controls and reduce standing privilege |
| Devices | Require trust signals for sensitive access paths |
| Applications | Apply conditional access and app segmentation by risk |
| Data | Use classification and container-level protections |
| Operations | Route detections and triage through a common monitoring layer |

## Scope

### In Scope

- Zero Trust principles and trust boundaries
- identity and access design
- device trust and compliance model
- application access patterns
- data protection guardrails
- monitoring and response assumptions
- decision records and threat modeling

### Out Of Scope

- tenant-specific screenshots
- production deployment steps
- license procurement and billing operations
- detailed Intune configuration baselines
- low-level network firewall rule documentation

## Recruiter Value

This project is strong portfolio evidence for roles that expect:

- `SC-100` style architecture thinking
- cloud identity and governance design
- Zero Trust translation from principle to policy
- clear communication across business and technical audiences

## Suggested Demo Flow

1. Start with the reference diagram.
2. Explain the three Zero Trust principles and trust boundaries.
3. Walk through the identity and device access flow.
4. Show the policy pack and why sensitive access requires stronger controls.
5. Finish with the decision logs and STRIDE model to prove architectural depth.

## Sources Used

This blueprint is aligned with official Microsoft guidance:

- [Zero Trust security guidance](https://learn.microsoft.com/en-us/security/zero-trust/)
- [Identity, the first pillar of a Zero Trust security architecture](https://learn.microsoft.com/en-us/security/zero-trust/deploy/identity)
- [Secure endpoints with Zero Trust](https://learn.microsoft.com/en-us/security/zero-trust/deploy/endpoints)
- [Secure applications with Zero Trust](https://learn.microsoft.com/en-us/security/zero-trust/deploy/applications)
- [Microsoft Entra Conditional Access overview](https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview)

## Cert Alignment

`SC-100`, `AZ-305`
