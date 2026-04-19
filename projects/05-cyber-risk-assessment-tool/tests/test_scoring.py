import sys
import unittest
from pathlib import Path
import subprocess
import tempfile
import zipfile
import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = PROJECT_ROOT / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from scoring import (  # noqa: E402
    calculate_inherent_score,
    calculate_residual_score,
    classify_risk,
)


class ScoringTests(unittest.TestCase):
    def test_inherent_score_uses_impact_times_likelihood(self) -> None:
        self.assertEqual(calculate_inherent_score(5, 4), 20)

    def test_residual_score_applies_control_effectiveness(self) -> None:
        self.assertEqual(calculate_residual_score(5, 4, 25), 15)

    def test_risk_classification_thresholds(self) -> None:
        self.assertEqual(classify_risk(4), "Low")
        self.assertEqual(classify_risk(8), "Medium")
        self.assertEqual(classify_risk(13), "High")
        self.assertEqual(classify_risk(20), "Critical")

    def test_cli_exports_csv_xlsx_and_pdf(self) -> None:
        app_entry = PROJECT_ROOT / "app" / "main.py"
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            csv_path = temp_path / "risk-register.csv"
            xlsx_path = temp_path / "risk-register.xlsx"
            pdf_path = temp_path / "risk-register.pdf"

            result = subprocess.run(
                [
                    sys.executable,
                    str(app_entry),
                    "--load-sample",
                    "--export-csv",
                    str(csv_path),
                    "--export-xlsx",
                    str(xlsx_path),
                    "--export-pdf",
                    str(pdf_path),
                    "--no-show",
                ],
                cwd=PROJECT_ROOT,
                env={**os.environ, "QT_QPA_PLATFORM": "offscreen"},
                capture_output=True,
                text=True,
                check=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertTrue(csv_path.exists())
            self.assertTrue(xlsx_path.exists())
            self.assertTrue(pdf_path.exists())

            with zipfile.ZipFile(xlsx_path) as workbook:
                names = set(workbook.namelist())
                self.assertIn("xl/workbook.xml", names)
                self.assertIn("xl/worksheets/sheet1.xml", names)
                self.assertIn("xl/worksheets/sheet2.xml", names)

            self.assertGreater(pdf_path.stat().st_size, 0)
            self.assertTrue(pdf_path.read_bytes().startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()
