# Operating Model

## Objective

Turn Teams governance from a one-time admin setup into a repeatable operating model with clear ownership, review cadence, and escalation paths.

## Core Roles

| Role | Primary Responsibility | Typical Decisions |
| --- | --- | --- |
| Collaboration Service Owner | Owns the governance standard and target operating model. | Approves baseline policy changes, resolves process conflicts. |
| Teams Administrator | Implements tenant and policy settings. | Channel policy, guest access setting, template maintenance. |
| Security And Compliance Lead | Ensures governance aligns with risk and compliance obligations. | Sensitivity baseline, retention alignment, exception approval input. |
| Department Owner | Sponsors business use of a team. | Team purpose, owner assignment, renewal decision. |
| Team Owner | Runs the workspace day to day. | Membership, guest review, archive request. |
| Helpdesk Or Collaboration Support | Handles first-line support and intake. | Request triage, owner routing, simple configuration help. |

## Governance Principles

- centralize policy, decentralize routine ownership
- make high-risk changes explicit
- avoid permanent exceptions
- keep approvals lightweight for low-risk collaboration
- document lifecycle events so cleanup is auditable

## Suggested Cadence

## Weekly

- review new team requests
- review exception requests awaiting decision
- review failed provisioning or policy enforcement issues

## Monthly

- review teams without two owners
- review newly added guests and external collaboration spikes
- review dormant teams flagged by usage reporting

## Quarterly

- run team owner attestation
- review guest memberships for active teams
- review archived teams pending deletion
- review naming-policy or sensitivity-label exceptions

## Semiannual

- review policy pack against Microsoft roadmap changes
- confirm retention and lifecycle guidance still match institutional needs
- update templates and training notes

## Decision Rights

| Decision | Default Owner | Escalation Path |
| --- | --- | --- |
| Standard team creation | Department owner plus team owner | Collaboration service owner only if policy conflict exists |
| Guest access approval | Team owner for standard low-risk cases | Security lead for elevated-risk data |
| Shared channel approval | Team owner if policy allows | Teams admin if external sharing is involved |
| Sensitivity label deviation | Security and compliance lead | Collaboration service owner |
| Retention exception | Compliance lead | Governance board or equivalent authority |
| Lifecycle renewal dispute | Department owner | Service owner |

## Minimum Records To Maintain

- approved request record
- owner pair and sponsoring department
- guest access justification where relevant
- exception register with expiry dates
- archive or deletion decisions

## Success Measures

- percent of teams with two valid owners
- percent of teams renewed on time
- guest-heavy teams reviewed on schedule
- count of stale teams archived or deleted each quarter
- count of open governance exceptions past expiry
