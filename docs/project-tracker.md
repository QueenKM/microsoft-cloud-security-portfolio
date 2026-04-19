# Project Tracker

## Overall Status

- `01-cloud-security-lab`: Live Azure sandbox deployed, validated in `AzureActivity`, and backed by fired alert evidence
- `02-zero-trust-architecture-blueprint`: Blueprint docs, diagrams, decisions, and STRIDE model complete for portfolio use
- `03-power-bi-azure-data-pipeline`: Sample dataset, semantic model, DAX catalogue, and dashboard preview complete
- `04-azure-iac`: Bicep baseline, network, workload, RBAC, alert layer, and visible overview artifact complete
- `05-cyber-risk-assessment-tool`: PySide6 MVP complete with scoring, persistence, and `CSV`/`XLSX`/`PDF` export
- `06-teams-governance-toolkit`: Governance policy pack, operating model, templates, and visible artifact complete

## Immediate Backlog

- [x] Define Azure tenant and subscription boundaries for the sandbox.
- [x] Create the first version of the cloud security lab architecture diagram.
- [x] List the exact Entra ID and Sentinel components to configure.
- [x] Build the first Bicep baseline for the sandbox subscription.
- [x] Extend the baseline with networking and diagnostic settings.
- [x] Add an optional demo workload and initial Azure RBAC pattern.
- [x] Add initial Azure Monitor alerting assets and screenshot instructions.
- [x] Add operator-facing portal and incident walkthrough guides.
- [x] Build the first Zero Trust architecture narrative and policy pack.
- [x] Add initial Zero Trust diagrams, decision logs, and STRIDE model.
- [x] Deploy the Cloud Security Lab baseline into an Azure for Students subscription.
- [x] Capture the first live monitoring, alerting, diagnostics, and Sentinel screenshots.
- [x] Wait for subscription activity log export ingestion, then capture NSG change evidence in `AzureActivity`.
- [x] Capture a Conditional Access blocker note or live policy evidence, depending on future Entra privileges.
- [x] Choose the first dataset for the Power BI pipeline.
- [x] Build the first sample dataset, star schema, and DAX design pack.
- [x] Decide whether the desktop risk tool will use `PySide6` or another GUI stack.
- [x] Build the first Cyber Risk Assessment Tool MVP with local scoring and CSV export.
- [x] Generate the first Cyber Risk Assessment Tool screenshot and sample export artifacts.
- [x] Draft the first Teams governance policy pack.
- [x] Add the first Teams governance operating model, templates, and visible artifact.

## Quality Bar

- [x] Every project has a strong README.
- [x] Every project has at least one visible artifact.
- [x] Every project has a recruiter-focused value statement.
- [x] Every project has a demo checklist.
- [x] Every project is polished enough to discuss in an interview.

## External Blockers

- `01-cloud-security-lab`: `Conditional Access` validation is documented but still blocked by student-tenant `Microsoft Entra` privileges.
