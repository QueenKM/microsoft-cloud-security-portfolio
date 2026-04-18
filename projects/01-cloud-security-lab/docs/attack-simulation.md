# Safe Attack Simulation Plan

## Goal

Generate safe, controlled events in the sandbox so the lab shows a full detection and response story.

## Scenario 1: Repeated Failed Sign-Ins

Use a dedicated test account and intentionally sign in with the wrong password several times from your own device.

Expected result:

- failed sign-in entries in Entra ID logs
- matching results in `SigninLogs`
- alert or analytic rule firing if thresholds are met

## Scenario 2: Password Spray Style Pattern In Miniature

Use several dedicated test accounts that you control and perform a very small number of bad sign-in attempts against each one. Keep this limited and fully contained to the lab.

Expected result:

- multiple failures from the same IP
- multiple targeted users in a short time window
- useful demonstration for an IP-based or multi-user detection

## Scenario 3: Privileged Change Monitoring

Make a controlled role assignment change in the lab and then revert it.

Expected result:

- Azure activity log records
- evidence for RBAC change monitoring
- a chance to demonstrate governance and least privilege review

## Response Walkthrough

When the alert appears:

1. Open the incident or alert.
2. Validate which user, IP, and time window are involved.
3. Check whether the target account is privileged.
4. Contain by disabling the dedicated test account or forcing a password reset in the sandbox story.
5. Document the incident in the repo with screenshots and lessons learned.

## Safety Rules

- only use accounts you created for the lab
- keep all tests low volume and manual
- do not run tests against real users or production tenants
- record exactly what you triggered so the evidence is easy to explain later
