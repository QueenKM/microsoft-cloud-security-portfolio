# Cyber Risk Tool Artifacts

Store generated screenshots and export samples for the desktop tool in this folder.

## Expected Artifacts

- `01-main-dashboard.png`
- `01-risk-register-export.csv`

## Current Artifacts

- [01-main-dashboard.png](01-main-dashboard.png)
- [01-risk-register-export.csv](01-risk-register-export.csv)

## Generation

Run:

```bash
python3 scripts/generate_demo_artifacts.py
```

This loads the sample ransomware scenario, exports the current register to CSV, and captures the main dashboard in offscreen mode.
