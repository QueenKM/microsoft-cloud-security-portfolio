import sys
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
