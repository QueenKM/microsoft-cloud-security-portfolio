# Cyber Risk Tool Architecture

## Goal

Explain the design of the MVP so the project is easy to demo, extend, and discuss in interviews.

## Design Choices

- desktop-first UI using `PySide6`
- local `JSON` persistence for simplicity and portability
- multi-format reporting export so the register can move into meetings and reporting flows
- a small scoring engine separated from the UI so it can be tested independently

## Application Layers

### UI Layer

[app/main.py](../app/main.py) owns:

- the main window
- the risk register table
- the form for editing one risk
- the summary cards
- the live risk matrix

### Domain Layer

[app/models.py](../app/models.py) defines the `RiskItem` model used across the application.

[app/scoring.py](../app/scoring.py) defines:

- inherent score calculation
- residual score calculation
- risk-level classification
- summary metrics
- risk matrix aggregation

### Persistence Layer

[app/storage.py](../app/storage.py) handles:

- JSON load and save
- scenario-pack loading
- `CSV`, `XLSX`, and `PDF` export

## Scoring Model

The MVP uses a simple but interview-friendly approach:

- `inherent score = impact * likelihood`
- `residual score = inherent score * (1 - control effectiveness)`

This keeps the model understandable while still showing how mitigating controls influence risk.

## Extension Path

- replace JSON persistence with `SQLite`
- add risk treatment tracking and due dates
- add dashboard charts and filtering
- package the app for easier distribution
