# Zero Trust Architecture Overview

## Goal

Describe the target-state Zero Trust architecture for `Astera University` in a way that is easy to explain, review, and extend later into a live tenant deployment.

## Design Drivers

- remote and hybrid users must access resources from unmanaged networks
- privileged actions need stronger controls than everyday access
- the university stores data with different sensitivity levels
- the security team is small, so controls must be repeatable and observable
- the environment should reduce blast radius if one identity, device, or workload is compromised

## Core Principles

### Verify Explicitly

Every access request is evaluated using available signals such as:

- user identity
- group membership
- role assignment
- device state
- application sensitivity
- session context
- risk signals and abnormal behavior

### Use Least Privilege

Access is scoped by:

- role
- task
- resource boundary
- data sensitivity
- time and approval path for privileged work

### Assume Breach

The architecture treats internal networks, user devices, and application sessions as potentially hostile until they are continuously validated. Controls are chosen to reduce lateral movement, overprivileged access, and silent persistence.

## Architectural Layers

### Identity Control Plane

`Microsoft Entra ID` is the primary policy decision point for user and admin access. This gives the environment one place to evaluate identities, enforce Conditional Access, and centralize authentication telemetry.

Key controls:

- modern authentication only
- MFA for all admins and sensitive app access
- break-glass exclusions with monitoring
- group-based access instead of direct assignment where possible
- privileged access separated from normal user personas

### Device Trust Layer

Devices are not trusted by default. Sensitive actions require device trust, not only successful sign-in.

Key controls:

- device registration and inventory
- compliance checks for managed endpoints
- stronger requirements for administrator sessions
- limited access paths for unmanaged or unknown devices

### Application Access Layer

Applications are categorized and protected according to business criticality and protocol maturity.

Key controls:

- SSO through the central identity plane
- adaptive access policies for sensitive applications
- stronger controls for admin portals and academic records systems
- visibility into sign-ins, risky access patterns, and app usage

### Data Protection Layer

Data access decisions depend on identity, device trust, and workload sensitivity.

Key controls:

- role-based access to high-value datasets
- sensitivity-based handling expectations
- collaboration guardrails for guests and external sharing
- logging for access, sharing, and privileged changes

### Infrastructure And Workload Layer

Infrastructure is segmented to limit blast radius and simplify monitoring.

Key controls:

- separate management and workload boundaries
- scoped admin rights
- central logging and alerting
- infrastructure changes treated as security-relevant events

### Visibility And Response Layer

Zero Trust only works if decisions and exceptions are visible to defenders.

Key controls:

- centralized sign-in and audit telemetry
- alerts on privileged changes
- investigation queries and analyst runbooks
- clear ownership for triage and escalation

## Trust Boundaries

The blueprint uses five high-level trust boundaries:

1. `External user and device boundary`
2. `Identity and policy decision boundary`
3. `Managed endpoint boundary`
4. `Application and data boundary`
5. `Security operations boundary`

The design intent is that crossing each boundary requires evaluation, not assumption.

## Personas

| Persona | Primary Goal | Access Pattern | Control Expectations |
| --- | --- | --- | --- |
| `student-user` | learning and collaboration | browser and SaaS access | low privilege, standard policy |
| `faculty-user` | teaching and content access | Microsoft 365, files, apps | moderate data exposure, standard policy |
| `it-admin` | administer cloud platforms | admin portals and infrastructure | MFA, trusted device, scoped rights |
| `security-analyst` | investigate incidents | logs, alerts, cases, hunting | read-heavy, monitored privileged access |
| `break-glass-admin` | emergency recovery only | exceptional use | excluded from normal policies, heavily monitored |

## Target Outcomes

- access decisions are based on identity plus context, not network location alone
- privileged actions are more difficult than standard collaboration work
- the same control plane is visible to both administrators and defenders
- architecture decisions are documented and reviewable
- the environment remains explainable in interviews and architecture reviews

## Related Artifacts

- [Device Compliance Model](device-compliance-model.md)
- [Policy Pack](policy-pack.md)
- [Implementation Roadmap](implementation-roadmap.md)
- [Reference Diagram](../diagrams/zero-trust-reference.md)
