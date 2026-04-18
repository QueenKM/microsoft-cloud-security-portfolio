# Device Compliance Model

## Goal

Define how device trust influences access decisions for `Astera University` without forcing the same controls onto every user journey.

## Device Classes

| Device Class | Example | Trust Level | Typical Access |
| --- | --- | --- | --- |
| `Managed compliant device` | university-issued laptop | high | full access based on role |
| `Managed noncompliant device` | enrolled device missing controls | degraded | remediation only or reduced access |
| `Registered personal device` | faculty mobile device | medium | limited productivity access |
| `Unknown unmanaged device` | public or unregistered device | low | browser-only or blocked for sensitive apps |

## Compliance Signals

The model assumes device trust decisions are influenced by:

- device registration state
- compliance posture
- security baseline status
- disk encryption and endpoint protection state
- patch level and supported OS state

## Access Rules

### Standard Collaboration

Low-risk productivity tools can allow:

- managed compliant devices
- some registered personal devices

### Sensitive Academic Or HR Data

Require:

- compliant or strongly trusted devices
- MFA
- role-based access

### Administrative Access

Require:

- managed compliant device
- MFA
- dedicated admin identity or privileged role
- stronger session monitoring

## Design Rationale

- user identity alone is not enough for sensitive access
- unmanaged devices should not become a silent bypass for admin controls
- a small IT team needs coarse but enforceable device categories
- stricter device controls are focused on high-risk actions first

## Exceptions

Possible exceptions must be:

- time-bound
- approved
- documented
- reviewed after use

Examples:

- emergency access during a device outage
- temporary contractor support
- initial pilot rollout for a new control

## Evidence To Capture Later

- compliant device policy screenshot
- admin access policy showing device requirement
- exception handling note or sample approval flow

## Linked Decisions

- [Require Device Trust For Sensitive Access](../decision-logs/2026-04-18-require-device-trust-for-sensitive-access.md)
