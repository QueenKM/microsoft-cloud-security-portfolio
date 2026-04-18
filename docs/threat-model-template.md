# STRIDE Threat Model Template

## System / Feature

Name the workload, process, or architecture area being reviewed.

## Scope

- In scope
- Out of scope
- Assumptions

## Assets

- Identity data
- Business data
- Infrastructure
- Logs and monitoring

## Entry Points

- User sign-in
- Admin portal actions
- API calls
- Device onboarding

## STRIDE Review

| Category | Example Threat | Existing Controls | Gaps | Mitigation |
| --- | --- | --- | --- | --- |
| Spoofing | Unauthorized use of stolen credentials | MFA, Conditional Access | Legacy auth exceptions | Block legacy auth |
| Tampering | Changes to logs or configs | RBAC, diagnostic settings | Broad admin access | Separate duties |
| Repudiation | User denies privileged action | Audit logs | Log retention not finalized | Enable retention policy |
| Information Disclosure | Sensitive data exposed to guests | Sensitivity labels, guest reviews | Manual reviews only | Add periodic access review |
| Denial of Service | Sign-in flooding or service abuse | Rate limits, alerting | Weak thresholds | Tune analytics |
| Elevation of Privilege | Excessive role assignments | PIM, least privilege | Some standing roles | Reduce privileged assignments |

## Highest Priority Actions

- Action 1
- Action 2
- Action 3
