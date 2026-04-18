# Shared Portfolio Scenario

## Organization

`Astera University` is a fictional mid-sized university with:

- 4,500 students
- 350 faculty and staff
- a hybrid work model
- Microsoft 365 and Azure adoption in progress
- a small IT and security team

## Business Drivers

- Protect student and staff identities.
- Reduce phishing, credential theft, and lateral movement risk.
- Improve visibility with centralized logging and monitoring.
- Standardize cloud deployments and governance.
- Enable collaboration without losing control over guest access and retention.

## Primary Personas

- `Student`: frequent SaaS user, low privilege, mobile-first.
- `Faculty`: sensitive academic and research data access.
- `IT Administrator`: elevated privilege, break-glass and just-in-time access concerns.
- `Security Analyst`: triages incidents in Sentinel and Defender.
- `Department Owner`: needs Teams spaces and simple risk reporting.

## High-Value Assets

- Entra ID identities and privileged roles
- student records and academic systems
- Teams collaboration spaces
- Azure subscriptions and workloads
- endpoint compliance data
- security logs and incident records

## Threat Assumptions

- Password spraying and failed logon bursts
- MFA fatigue and account compromise attempts
- overly broad RBAC permissions
- unmanaged guest access in Teams
- insecure cloud configurations
- ransomware impact on business operations

## Reuse Across Projects

- `01-cloud-security-lab`: secure the tenant and detect suspicious activity.
- `02-zero-trust-architecture-blueprint`: document the security model for the university.
- `03-power-bi-azure-data-pipeline`: analyze security and operations data.
- `04-azure-iac`: automate the landing zone and workload baseline.
- `05-cyber-risk-assessment-tool`: assess scenarios such as ransomware against university services.
- `06-teams-governance-toolkit`: define collaboration guardrails for departments and guests.
