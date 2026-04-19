from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_ENTRY = PROJECT_ROOT / "app" / "main.py"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
SCREENSHOT_PATH = ARTIFACTS_DIR / "01-main-dashboard.png"
CSV_PATH = ARTIFACTS_DIR / "01-risk-register-export.csv"
XLSX_PATH = ARTIFACTS_DIR / "01-risk-register-export.xlsx"
PDF_PATH = ARTIFACTS_DIR / "01-risk-register-export.pdf"


def run() -> int:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        str(APP_ENTRY),
        "--load-sample",
        "--capture",
        str(SCREENSHOT_PATH),
        "--export-csv",
        str(CSV_PATH),
        "--export-xlsx",
        str(XLSX_PATH),
        "--export-pdf",
        str(PDF_PATH),
        "--no-show",
    ]
    environment = os.environ.copy()
    environment["QT_QPA_PLATFORM"] = "offscreen"
    return subprocess.call(command, env=environment)


if __name__ == "__main__":
    raise SystemExit(run())
