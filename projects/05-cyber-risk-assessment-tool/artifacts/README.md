# Cyber Risk Tool Artifacts

Store generated screenshots and export samples for the desktop tool in this folder.

## Expected Artifacts

- `01-main-dashboard.png`
- `01-risk-register-export.csv`
- `01-risk-register-export.xlsx`
- `01-risk-register-export.pdf`

## Current Artifacts

- [01-main-dashboard.png](01-main-dashboard.png)
- [01-risk-register-export.csv](01-risk-register-export.csv)
- [01-risk-register-export.xlsx](01-risk-register-export.xlsx)
- [01-risk-register-export.pdf](01-risk-register-export.pdf)

## Generation

Run:

```bash
python3 scripts/generate_demo_artifacts.py
```

This loads the sample ransomware scenario, exports the current register to `CSV`, `Excel`, and `PDF`, and captures the main dashboard in offscreen mode.
