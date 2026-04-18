# Zero Trust Implementation Roadmap

## Goal

Break the blueprint into realistic phases that a small university IT and security team can execute.

## Phase 1: Identity Foundation

- inventory privileged roles and admin accounts
- enforce MFA for admins
- block legacy authentication
- define break-glass handling
- centralize sign-in and audit logs

## Phase 2: Device Trust For Sensitive Paths

- define managed versus unmanaged device categories
- require trusted devices for administrative access
- apply stronger access policies to high-risk apps
- document exception handling

## Phase 3: Application And Data Guardrails

- classify critical applications
- move major apps under central SSO where possible
- align access to data sensitivity and sharing rules
- reduce uncontrolled guest exposure

## Phase 4: Visibility And Response

- centralize alerts and investigation queries
- tune alerts for privileged changes and risky access
- define incident ownership and response steps
- rehearse at least one privileged access scenario

## Phase 5: Continuous Improvement

- review standing privilege
- review policy exceptions
- expand automation for routine security decisions
- update threat model and decision records when architecture changes

## Milestones For This Repository

- [x] architecture narrative documented
- [x] first policy pack created
- [x] first decision records written
- [x] first STRIDE model written
- [x] diagram starter set created
- [ ] export polished diagram images into `artifacts/`
- [ ] add live tenant evidence when sandbox capacity returns
