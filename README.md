# Microsoft Cloud Security Portfolio

This repository is a structured portfolio workspace for six Microsoft and Azure focused projects. The goal is to build a strong, interview-ready body of work that demonstrates cloud security, architecture, governance, data analytics, and practical software delivery.

## Portfolio Goals

- Build one flagship Azure security lab with real detections and response flows.
- Show architectural thinking through Zero Trust documentation and threat modeling.
- Demonstrate analytics skills through a Power BI and Azure data pipeline project.
- Prove infrastructure automation skills with Bicep and Terraform.
- Stand out with a practical desktop cyber risk assessment tool.
- Add Microsoft 365 governance depth with a Teams governance toolkit.

## Recommended Storyline

Use one fictional organization across the whole portfolio so every project feels connected instead of random. This repo uses `Astera University` as the common scenario: a mid-sized institution with cloud identities, remote users, regulated data, student collaboration needs, and a small security team.

See [docs/portfolio-scenario.md](/Users/kris/Desktop/microsoft-cloud-security-portfolio/docs/portfolio-scenario.md) for the shared assumptions.

## Project Map

| Project | Focus | Main Skills | Cert Alignment |
| --- | --- | --- | --- |
| `01-cloud-security-lab` | Secure Azure sandbox | Entra ID, Sentinel, Defender for Cloud, KQL, alerts, RBAC | `SC-100`, `SC-200`, `SC-300` |
| `02-zero-trust-architecture-blueprint` | Security architecture repo | Zero Trust, diagrams, decision logs, STRIDE | `SC-100`, `AZ-305` |
| `03-power-bi-azure-data-pipeline` | Analytics project | Data modeling, ETL, DAX, dashboards | `PL-300` |
| `04-azure-iac` | Infrastructure automation | Terraform, Bicep, GitHub Actions | `AZ-104`, `AZ-305` |
| `05-cyber-risk-assessment-tool` | Practical security software | Python GUI, risk scoring, PDF/Excel export | Security + software portfolio |
| `06-teams-governance-toolkit` | M365 governance repo | Teams policies, retention, guest access | `MS-700` |

## Suggested Build Order

1. Start with the Azure foundation in `01-cloud-security-lab`.
2. Capture architecture decisions in `02-zero-trust-architecture-blueprint`.
3. Reuse logs and operational data in `03-power-bi-azure-data-pipeline`.
4. Automate baseline infrastructure in `04-azure-iac`.
5. Build the desktop app in `05-cyber-risk-assessment-tool`.
6. Finish with governance documentation in `06-teams-governance-toolkit`.

## Repo Structure

```text
microsoft-cloud-security-portfolio/
├── docs/
├── shared-assets/
└── projects/
    ├── 01-cloud-security-lab/
    ├── 02-zero-trust-architecture-blueprint/
    ├── 03-power-bi-azure-data-pipeline/
    ├── 04-azure-iac/
    ├── 05-cyber-risk-assessment-tool/
    └── 06-teams-governance-toolkit/
```

## What "Done" Looks Like

Each project should eventually contain:

- A clear `README` with purpose, architecture, and setup instructions.
- Screenshots, diagrams, or demo artifacts.
- Reproducible steps or infrastructure definitions.
- A short "business value" section for recruiters and interviewers.
- A short "lessons learned" section showing reflection.

## Planning Docs

- [docs/roadmap.md](/Users/kris/Desktop/microsoft-cloud-security-portfolio/docs/roadmap.md)
- [docs/project-tracker.md](/Users/kris/Desktop/microsoft-cloud-security-portfolio/docs/project-tracker.md)
- [docs/decision-log-template.md](/Users/kris/Desktop/microsoft-cloud-security-portfolio/docs/decision-log-template.md)
- [docs/threat-model-template.md](/Users/kris/Desktop/microsoft-cloud-security-portfolio/docs/threat-model-template.md)

## Next Move

The best first implementation step is to build the baseline of `01-cloud-security-lab` and let that project produce identities, logs, alerts, and security controls that can feed the rest of the portfolio.
