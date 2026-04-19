# User Guide

## Start The App

```bash
python3 app/main.py
```

## Core Workflow

1. Create a new risk or load the sample ransomware scenario.
2. Enter the risk title, owner, category, and scenario details.
3. Score impact and likelihood from `1` to `5`.
4. Set `control effectiveness` to show how much existing controls reduce residual risk.
5. Save the risk and review the updated matrix and summary cards.
6. Export the current register to `CSV`, `Excel`, or `PDF` when needed.

## Suggested Demo

1. Launch the app.
2. Load the sample ransomware scenario.
3. Show the risk table and explain one high residual risk.
4. Update one risk with stronger controls and show the residual score drop.
5. Export the register to `CSV`, `Excel`, and `PDF`.

## Notes

- the register is saved locally to `data/risk_register.json`
- loading the sample scenario replaces the current register in the MVP
- exported workbooks and PDFs are generated locally from the current register

## Generate Demo Assets

```bash
python3 scripts/generate_demo_artifacts.py
```

This creates a dashboard screenshot plus sample `CSV`, `Excel`, and `PDF` exports in [artifacts](../artifacts/README.md).
