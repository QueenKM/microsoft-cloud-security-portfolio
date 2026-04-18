# Title

Centralize access evaluation in a single identity control plane

## Date

`2026-04-18`

## Status

`Accepted`

## Context

`Astera University` needs a Zero Trust design that is explainable, monitorable, and practical for a small IT team. When sign-ins, application access, and admin access are spread across multiple inconsistent identity systems, policy quality drops and defenders lose visibility.

## Options Considered

- keep separate access paths for different application groups
- centralize user and admin access evaluation in `Microsoft Entra ID`
- defer identity centralization and focus only on endpoint controls

## Decision

Use `Microsoft Entra ID` as the primary identity control plane for user and admin access wherever practical. This creates one policy engine for Conditional Access, stronger sign-in telemetry, and a cleaner Zero Trust narrative.

## Consequences

- Positive outcome: access policies become easier to explain and audit.
- Positive outcome: sign-in and access telemetry becomes more consistent.
- Tradeoff accepted: legacy applications may need migration work or compensating controls.
- Follow-up required: identify applications that cannot be integrated immediately and document exceptions.
