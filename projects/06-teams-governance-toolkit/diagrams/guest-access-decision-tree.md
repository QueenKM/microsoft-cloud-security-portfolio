# Guest Access Decision Tree

```mermaid
flowchart TD
    A["Need to collaborate with people outside Astera University?"] -->|No| B["Create or use an internal Team"]
    A -->|Yes| C["Does the partner need access to the full Team workspace?"]
    C -->|Yes| D["Use guest access"]
    C -->|No| E["Can the work stay inside one bounded workstream?"]
    E -->|Yes| F["Use a shared channel"]
    E -->|No| G["Escalate for governance review"]
    D --> H["Check sensitivity, owner accountability, and lifecycle plan"]
    F --> H
    G --> I["Approve exception or redesign collaboration pattern"]
```

## Reading The Diagram

- choose `guest access` when the external user needs broad participation in the team
- choose `shared channel` when the collaboration should stay inside one scoped lane
- choose `governance review` when neither option cleanly matches the policy baseline
