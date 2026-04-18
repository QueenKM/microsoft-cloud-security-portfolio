# Title

Require device trust for sensitive and privileged access paths

## Date

`2026-04-18`

## Status

`Accepted`

## Context

Strong authentication alone does not reduce enough risk if privileged users can administer the environment from unknown or weakly protected endpoints. The architecture needs a simple rule that increases assurance for high-impact actions without blocking all productivity access.

## Options Considered

- allow privileged access from any device after MFA
- require trusted devices only for sensitive and privileged access
- require trusted devices for every user and every app from day one

## Decision

Require device trust for administrative portals, privileged sessions, and selected high-sensitivity applications. Standard collaboration can remain more flexible where business risk is lower.

## Consequences

- Positive outcome: compromised credentials alone are less useful for admin abuse.
- Positive outcome: the policy is strict where it matters most and easier to roll out.
- Tradeoff accepted: administrators need managed devices for some tasks.
- Follow-up required: define an exception path for emergency access and outages.
