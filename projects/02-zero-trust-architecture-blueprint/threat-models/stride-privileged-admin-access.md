# STRIDE Threat Model: Privileged Admin Access

## System / Feature

Privileged administrator access to cloud administration portals and security tooling.

## Scope

- In scope: admin sign-in, device trust checks, role-based authorization, privileged operations, and logging
- Out of scope: detailed network firewall rule sets, vendor-specific endpoint hardening baselines, and SOC escalation tooling
- Assumptions: a central identity provider exists, audit logging is enabled, and at least one emergency admin account is maintained

## Assets

- administrator credentials
- privileged role assignments
- infrastructure and security settings
- sign-in and audit logs

## Entry Points

- admin sign-in flow
- cloud management portals
- privileged role activation or assignment
- emergency admin access path

## STRIDE Review

| Category | Example Threat | Existing Controls | Gaps | Mitigation |
| --- | --- | --- | --- | --- |
| Spoofing | Attacker uses stolen admin credentials | MFA, central identity provider | MFA alone may not prove device trust | Require trusted device for sensitive access |
| Tampering | Malicious admin changes logging or security settings | scoped RBAC, change alerts | some admin roles still broad | reduce standing access and monitor changes |
| Repudiation | Admin denies making a privileged change | audit logs, sign-in logs | inconsistent app integration can weaken traceability | centralize admin access and preserve logs |
| Information Disclosure | Admin or attacker accesses sensitive records beyond need | least privilege design, scoped roles | manual access reviews may lag | add periodic access reviews and tighter scoping |
| Denial of Service | Sign-in abuse or account lockout affects real admins | emergency admin process, monitoring | break-glass path may be under-tested | rehearse emergency access and document runbook |
| Elevation of Privilege | User gains excessive rights through misassignment | role separation, approval expectations | standing privilege remains in some scenarios | adopt JIT where possible and alert on changes |

## Highest Priority Actions

- require trusted devices for privileged access
- centralize and review high-risk role assignments
- alert on role assignment and logging changes
