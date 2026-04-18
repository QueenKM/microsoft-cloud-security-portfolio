# Zero Trust Reference Diagram

```mermaid
flowchart LR
    A["Users and Admin Personas"] --> B["Microsoft Entra ID\nIdentity Control Plane"]
    C["Managed and Personal Devices"] --> D["Device Trust Evaluation"]
    B --> E["Conditional Access and Session Policy"]
    D --> E
    E --> F["Microsoft 365 and SaaS Apps"]
    E --> G["Azure Admin and Security Portals"]
    E --> H["Academic and Business Data"]
    G --> I["Scoped Infrastructure Access"]
    F --> J["Collaboration and Productivity"]
    H --> K["Sensitivity and Sharing Controls"]
    B --> L["Sign-in and Audit Telemetry"]
    G --> L
    I --> L
    L --> M["Security Operations and Investigation"]
```

## Reading Guide

- identities and devices both feed access evaluation
- application and admin access paths are protected differently
- telemetry flows back into the security operations layer
- data protection sits behind identity, device, and app decisions
