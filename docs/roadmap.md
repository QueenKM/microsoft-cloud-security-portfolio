# Portfolio Roadmap

## Phase 0: Foundation

- Finalize the shared scenario and scope boundaries.
- Decide naming conventions for repos, diagrams, screenshots, and exports.
- Keep every project in English for stronger GitHub and recruiter readability.

## Phase 1: Flagship Security Lab

Build `01-cloud-security-lab` first because it creates the strongest interview story and produces artifacts that can feed other projects.

Target outputs:

- Azure subscription layout
- Entra ID hardening baseline
- Conditional Access policies
- Defender for Cloud onboarding
- Sentinel workspace, connectors, analytic rules
- Log Analytics queries and alert rules
- attack simulation and incident walkthrough

## Phase 2: Architecture Layer

Build `02-zero-trust-architecture-blueprint` in parallel with the lab once the first controls exist.

Target outputs:

- Zero Trust diagrams
- identity, device, app, and data flows
- security policy pack
- decision log entries
- STRIDE threat model

## Phase 3: Automation and Analytics

Use project outputs as inputs for the next two builds.

`03-power-bi-azure-data-pipeline`

- ingest CSV, SQL, or exported security data
- model a star schema
- create DAX measures and KPIs
- build a clean dashboard

`04-azure-iac`

- recreate the Azure baseline with Bicep or Terraform
- add security defaults and diagnostics
- add CI validation

## Phase 4: Software and Governance

`05-cyber-risk-assessment-tool`

- build a desktop app for risk scoring
- use ransomware as the first scenario pack
- add PDF and Excel export

`06-teams-governance-toolkit`

- define naming, retention, guest access, and lifecycle controls
- package templates and review checklists

## Suggested Delivery Rhythm

- Week 1: Cloud security lab foundation
- Week 2: Sentinel detections and attack simulation
- Week 3: Zero Trust diagrams and threat model
- Week 4: IaC baseline
- Week 5: Data pipeline and dashboard
- Week 6: Cyber risk assessment tool MVP
- Week 7: Teams governance toolkit
- Week 8: Polish, screenshots, README cleanup, demo videos

## Demo Strategy

Every project should end with:

- 3 to 6 screenshots
- one architecture or workflow diagram
- one short demo script
- one lessons learned section
- one recruiter-friendly summary paragraph
