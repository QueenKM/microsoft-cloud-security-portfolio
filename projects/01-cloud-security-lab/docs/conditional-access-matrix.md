# Conditional Access Matrix

## Goal

Document a clear starting set of Conditional Access policies for the lab so the control story is easy to explain and reproduce.

## Policy Matrix

| Policy Name | Users And Roles | Apps Or Actions | Conditions | Controls | Notes |
| --- | --- | --- | --- | --- | --- |
| `CA01-Require-MFA-For-Admins` | all administrative roles | all cloud apps | any location, any device | require MFA | strongest baseline control for privileged identities |
| `CA02-Block-Legacy-Authentication` | all users | legacy auth clients | any location | block access | reduces password spray and basic auth risk |
| `CA03-Require-MFA-For-Security-Tools` | IT admins, security analysts | Azure management, security portals | any location | require MFA | protects admin access paths used in the lab |
| `CA04-Require-Trusted-Access-For-Admin-Work` | IT admins | admin portals | untrusted device or risky context | require compliant device or trusted access | optional if device compliance is in scope |
| `CA05-Report-Only-Risky-Sign-In-Policy` | selected test users | all cloud apps | risky sign-in, if available | report-only or require MFA | safe way to demonstrate policy evaluation |

## Exclusions

| Exclusion | Reason | Guardrail |
| --- | --- | --- |
| `break-glass-admin` | prevent total lockout in tenant recovery scenarios | unique credentials, monitored sign-ins, no daily use |
| pilot exception group, temporary only | safe rollout and troubleshooting | time-boxed removal plan |

## Rollout Order

1. Create the policies in `report-only` where risk is uncertain.
2. Enable the administrator MFA and legacy auth policies first.
3. Validate sign-in behavior with dedicated lab accounts.
4. Move stable policies to `On`.
5. Capture screenshots and sign-in logs for evidence.

## Demo Talking Points

- why privileged accounts get stricter controls than standard users
- why break-glass exists and why it must be tightly monitored
- how report-only mode reduces rollout risk
- how these policies support a Zero Trust identity posture
