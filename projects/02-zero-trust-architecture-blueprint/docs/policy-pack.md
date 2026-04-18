# Zero Trust Policy Pack

## Goal

Summarize the policy set that turns the blueprint into operational guardrails.

## Policy Set

| Policy ID | Policy Name | Intent | Primary Audience |
| --- | --- | --- | --- |
| `ZT-01` | Central Identity Control Plane | route sign-in and access evaluation through one identity policy engine | IT and architecture |
| `ZT-02` | Admin MFA Baseline | require MFA for privileged accounts and admin portals | admins |
| `ZT-03` | Block Legacy Authentication | prevent basic and legacy sign-in paths | all users |
| `ZT-04` | Sensitive Access Requires Trusted Device | require device trust for high-risk apps and admin work | admins, selected staff |
| `ZT-05` | Group-Based Least Privilege | assign access through groups and scoped roles | IT and IAM |
| `ZT-06` | Guest Access And External Sharing Guardrails | reduce accidental overexposure through collaboration | faculty, staff |
| `ZT-07` | Centralized Logging For Security Decisions | retain sign-in, audit, and privileged access telemetry | security operations |

## Policy Summaries

### `ZT-01` Central Identity Control Plane

All major user and admin access paths should be integrated with the primary identity provider to keep policy evaluation and telemetry consistent.

### `ZT-02` Admin MFA Baseline

Privileged accounts must use MFA, with stronger exclusions and monitoring for emergency access accounts only.

### `ZT-03` Block Legacy Authentication

Legacy authentication paths should be disabled because they bypass stronger modern access controls and increase password spray exposure.

### `ZT-04` Sensitive Access Requires Trusted Device

Administrative tasks and high-sensitivity applications should require a managed or compliant device, not only a valid password and MFA prompt.

### `ZT-05` Group-Based Least Privilege

Access should be granted through roles and groups that align to job function, with the narrowest practical scope.

### `ZT-06` Guest Access And External Sharing Guardrails

External collaboration should be allowed deliberately, with clear sharing limits, review expectations, and protections for sensitive information.

### `ZT-07` Centralized Logging For Security Decisions

Security-relevant actions must be logged centrally so the security team can investigate sign-ins, policy decisions, role changes, and anomalies.

## Rollout Priority

1. Centralize identity and sign-in telemetry.
2. Enforce admin MFA and block legacy authentication.
3. Introduce trusted-device requirements for sensitive access.
4. Reduce direct assignments and standing privilege.
5. Expand data and guest governance controls.

## Success Criteria

- privileged access always follows a stronger path than standard user access
- legacy sign-in paths are eliminated or documented as time-bound exceptions
- sensitive data access depends on both identity and device context
- analysts can explain who did what, from where, and under which policy

## References

- [Conditional Access overview](https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview)
- [Zero Trust security guidance](https://learn.microsoft.com/en-us/security/zero-trust/)
