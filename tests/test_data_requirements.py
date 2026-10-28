
import unittest
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


class TestDataRequirements(unittest.TestCase):

    def test_campaign_count(self):
        campaigns = pd.read_csv(DATA_DIR / "campaigns.csv")
        self.assertEqual(len(campaigns), 500)

    def test_contact_count(self):
        contacts = pd.read_csv(DATA_DIR / "contacts.csv")
        self.assertEqual(len(contacts), 50_000)

    def test_touchpoint_count(self):
        touchpoints = pd.read_csv(DATA_DIR / "touchpoints.csv")
        self.assertEqual(len(touchpoints), 200_000)

    def test_attribution_models(self):
        attribution = pd.read_csv(DATA_DIR / "attribution_results.csv")
        expected_models = {"first_touch", "last_touch", "linear"}
        self.assertEqual(set(attribution["model_name"].unique()), expected_models)


if __name__ == "__main__":
    unittest.main()
