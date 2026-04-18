# Exception Process

## Purpose

Allow limited deviations from the governance baseline without turning exceptions into a permanent shadow policy.

## Acceptable Exception Categories

- temporary guest access for a restricted high-value collaboration
- delayed deletion due to audit or legal hold preparation
- short-term naming deviation required by an external accreditation or vendor program
- temporary shared channel usage outside the default pattern with documented controls

## Information Required

- requester name and role
- team name or planned team name
- business reason
- exact policy rule requiring exception
- data classification involved
- external parties involved
- risk introduced
- compensating controls
- requested start date
- requested expiry date

## Decision Criteria

Approve only if:

- the business need is specific and time-bounded
- the policy conflict is real, not just inconvenient
- compensating controls are clear
- a review date is set
- the exception owner accepts accountability

## Review Workflow

1. request submitted by team owner or sponsor
2. collaboration service owner reviews for completeness
3. security or compliance reviews if the exception affects data exposure, retention, or privacy
4. decision recorded as approve, reject, or approve with conditions
5. exception reviewed again before expiry

## Default SLAs

- standard exception: 5 business days
- elevated-risk exception: 10 business days
- urgent operational exception: same day with retrospective review

## Exception Outcomes

- approved with expiry date
- approved with conditions
- rejected
- redirected to standard provisioning because no exception is actually needed

## Exit Rule

Every exception must end in one of these states:

- returned to standard governance baseline
- replaced by a newly approved standard policy
- retired because the team was archived or deleted
