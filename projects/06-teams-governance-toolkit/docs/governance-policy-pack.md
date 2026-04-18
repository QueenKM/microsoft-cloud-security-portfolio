# Governance Policy Pack

## Objective

Set a clear Microsoft Teams governance baseline for `Astera University` that protects collaboration spaces without making day-to-day teamwork dependent on ticket-driven admin bottlenecks.

## Policy Domains

| Domain | Baseline Control | Why It Exists | Admin Control Plane | Owner Responsibility |
| --- | --- | --- | --- | --- |
| Provisioning | New teams require a standard request payload with business purpose, data classification, owner pair, and expected external access pattern. | Prevent orphaned or duplicative teams and improve downstream lifecycle decisions. | Teams admin center, request workflow, approved templates | Submit accurate purpose and ownership data before launch. |
| Naming | Team names follow `BU-Workload-Topic` format with blocked words and reserved prefixes. | Keeps the tenant searchable and reduces misleading workspace names. | Microsoft 365 group naming policy | Use approved names and avoid side-channel renaming requests. |
| Ownership | Every team has at least two owners, one primary and one fallback. | Reduces abandoned teams and ownerless access decisions. | Teams membership and periodic reviews | Maintain owner coverage and respond to reviews. |
| Guest Access | Guest access is allowed only when there is a named business sponsor and a stated data-sharing purpose. | Limits ad hoc external access growth. | Teams guest access, Entra B2B, sensitivity labels | Review guests quarterly and remove unused guests promptly. |
| Shared Channels | Shared channels are preferred when collaboration can stay scoped to a single workstream rather than full team membership. | Reduces oversharing and avoids unnecessary guest account sprawl. | Teams channel policy, external collaboration settings | Use shared channels only for bounded partner collaboration. |
| Sensitivity And Privacy | Teams that handle sensitive academic, HR, finance, or regulated content must use an approved sensitivity label. | Enforces privacy, guest restrictions, and downstream compliance expectations. | Purview sensitivity labels | Select the correct label during team creation and request changes through governance. |
| Retention | Teams chat and channel retention expectations are documented up front and implemented centrally in Purview. | Keeps governance consistent with compliance requirements. | Purview retention policies | Understand that retention is centrally managed, not owner-managed. |
| Lifecycle | Teams are reviewed at least every 180 days and either renewed, archived, or queued for deletion. | Reduces stale collaboration spaces. | Group expiration, reports, archive/delete workflow | Confirm if the workspace is still needed and whether guests remain valid. |
| Exceptions | Exceptions must have a documented reason, expiry date, compensating controls, and approving authority. | Prevents permanent one-off exceptions. | Exception register and review process | Re-justify temporary deviations before expiry. |

## Baseline Decisions

## 1. Provisioning

- Allow controlled self-service instead of admin-only team creation.
- Capture a minimum metadata set at creation time:
  - business purpose
  - department or function
  - primary owner
  - backup owner
  - expected lifespan
  - guest or shared channel requirement
  - sensitivity expectation
- Use standard team templates for common scenarios such as:
  - department team
  - project team
  - vendor collaboration team
  - student services coordination team

## 2. Naming Convention

Recommended pattern:

```text
<Department>-<WorkspaceType>-<ShortPurpose>
```

Examples:

- `FIN-Project-Budget2027`
- `HR-Department-PeopleOps`
- `IT-Vendor-ServiceDesk`
- `REG-Academic-ExamBoard`

Rules:

- no personal names as the primary naming anchor
- no generic names such as `New Team`, `General`, or `Test`
- use approved department abbreviations
- reserve prefixes such as `SEC`, `HR`, `FIN`, and `IT` for managed use

## 3. Guest Access

Guest access is allowed only when all conditions are true:

- there is a legitimate business or academic need
- a named internal owner accepts responsibility
- the collaboration scope cannot be handled more safely through internal-only channels
- the expected data classification permits external sharing

Guest access is not approved for:

- broad department teams with no bounded external use case
- teams containing highly sensitive regulated content unless explicitly approved
- dormant teams that have already failed a lifecycle review

## 4. Shared Channels

Shared channels are the preferred pattern when:

- only one workstream must be shared externally
- the partner should not see the full team
- the team owner wants to reduce guest account sprawl

Shared channels are not the default when:

- the partner needs full team file and membership visibility
- ownership is unclear
- the collaboration boundary changes often and becomes difficult to review

## 5. Sensitivity And Classification

Use sensitivity labels to drive container-level protections for higher-risk teams.

Minimum label guidance:

| Label | Example Use | Governance Effect |
| --- | --- | --- |
| `General` | Broad internal collaboration | Standard internal defaults |
| `Confidential` | Department planning, student support, finance operations | Private team, tighter sharing review |
| `Highly Confidential` | HR investigations, regulated records, executive matters | Strongest restrictions, limited guest access or no guest access |

## 6. Retention

Retention is a central compliance decision, not a team-owner toggle.

Minimum policy expectations:

- define default retention objectives for chat and channel content
- document whether the team belongs to a business area with elevated retention needs
- separate retention from workspace deletion decisions
- make owners aware that archiving a team does not replace retention controls

## 7. Lifecycle

Lifecycle checkpoints:

- `Day 0`: create team and assign two owners
- `Day 90`: validate adoption for new project or vendor teams
- `Day 180`: mandatory ownership and guest review
- `End of business need`: archive first unless immediate deletion is justified

Expected lifecycle outcomes:

- renew
- archive
- delete
- escalate for exception

## 8. Exceptions

Allowed exception themes:

- short-term external exam board or accreditation work
- research collaboration with contractual controls
- legacy workspace requiring delayed cleanup for audit reasons

Required exception fields:

- requesting owner
- scope of deviation
- reason
- risks introduced
- compensating controls
- expiry date
- approving authority

## Implementation Notes

- Use Microsoft 365 group naming policy to enforce prefixes and blocked words.
- Use sensitivity labels to influence privacy and guest access decisions for teams.
- Use Microsoft 365 group expiration and review workflows to drive lifecycle cleanup.
- Use Teams channel policies to control who can create shared channels.
- Use Purview retention policies for chat and channel message retention requirements.

## Licensing Watch-Out

Specific governance features can depend on tenant licensing and service configuration. Validate the current licensing impact before rollout, especially for:

- sensitivity labels
- access reviews
- lifecycle automation
- advanced retention scenarios
