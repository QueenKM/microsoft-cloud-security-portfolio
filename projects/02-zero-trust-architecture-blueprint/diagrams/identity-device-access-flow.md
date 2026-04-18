# Identity And Device Access Flow

```mermaid
sequenceDiagram
    actor Admin as IT Admin
    participant Device as Managed Device
    participant Entra as Microsoft Entra ID
    participant Policy as Conditional Access
    participant App as Azure Admin Portal
    participant Logs as Audit and Sign-in Logs

    Admin->>Device: Start privileged session
    Device->>Entra: Present device and user context
    Entra->>Policy: Evaluate identity, role, device, and risk
    Policy-->>Admin: Require MFA and trusted device
    Admin->>Entra: Complete MFA
    Entra->>App: Issue access token with approved context
    App-->>Admin: Allow scoped administrative action
    Entra->>Logs: Record sign-in details
    App->>Logs: Record privileged activity
```

## Reading Guide

- the user does not reach the admin portal directly
- policy evaluation happens before sensitive access is granted
- privileged sessions generate both identity and activity evidence
