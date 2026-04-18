# Portal Execution Checklist

## Goal

Provide a practical run order for the real Azure portal work so the lab is built consistently and the right evidence is captured along the way.

## Phase 1: Deploy The Baseline

1. Deploy the `Bicep` baseline from `04-azure-iac`.
2. Confirm the resource groups were created.
3. Confirm the `Log Analytics workspace`, `VNet`, `NSG`s, and storage account exist.
4. If needed, redeploy with:
   `deployDemoVirtualMachine=true`
   `demoVirtualMachineSshPublicKey=<your key>`
   `itAdminPrincipalId=<principal id>`
   `securityAnalystPrincipalId=<principal id>`
   `alertNotificationEmail=<your email>`

## Phase 2: Validate Monitoring Foundation

1. Open the `Log Analytics workspace`.
2. Confirm the workspace name matches the deployment outputs.
3. Open `Azure Monitor` -> `Alerts` -> `Alert rules`.
4. Confirm these rules exist:
   `RBAC Role Assignment Changes`
   `NSG Or Security Rule Changes`
   `Diagnostic Settings Changes`
5. If you provided an email address, confirm the action group exists and the email receiver is listed.

## Phase 3: Configure Identity Controls

1. Create or confirm the lab users:
   `student-user`
   `faculty-user`
   `it-admin`
   `security-analyst`
   `break-glass-admin`
2. Configure the first Conditional Access policies from the matrix:
   admin MFA
   block legacy authentication
   optional report-only risk policy
3. Capture the first Conditional Access screenshots before moving on.

## Phase 4: Enable Sentinel

1. Open the `Log Analytics workspace`.
2. Enable `Microsoft Sentinel`.
3. Open the `Data connectors` page.
4. Connect `Azure Activity`.
5. Connect Entra sign-in and audit sources if the tenant supports them.
6. If Defender for Cloud is available, connect it too.

## Phase 5: Validate Diagnostics

1. Open each `NSG` and confirm diagnostic settings are enabled.
2. Open the storage account `Blob service` diagnostic settings and confirm logs are enabled.
3. Run the `AzureActivity` and `SigninLogs` queries from the queries folder.
4. Capture screenshots of results once data appears.

## Phase 6: Trigger Safe Test Events

1. Perform repeated failed sign-ins with a dedicated test account.
2. Make one controlled RBAC role assignment change and revert it.
3. Make one harmless `NSG` rule edit and revert it.
4. If needed, create and remove one diagnostic settings change in the sandbox.

## Phase 7: Capture Evidence

1. Follow the [Screenshot Runbook](screenshot-runbook.md).
2. Save the screenshots into `artifacts/`.
3. Keep names aligned with the runbook.
4. Redact tenant IDs, emails, or anything sensitive before committing.

## Phase 8: Write The Story

1. Record what you triggered.
2. Record which rule or query detected it.
3. Record what the analyst would do next.
4. Add screenshots and short lessons learned to the repo.

## Done Criteria

- infrastructure exists
- at least three Conditional Access policies are visible
- Sentinel is enabled
- data connectors are configured as far as tenant licensing allows
- at least one alert or detection result is visible
- screenshots are saved with clean names
