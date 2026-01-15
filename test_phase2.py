import unittest
from fastapi.testclient import TestClient
from api import app
from logic import load_gazetted_tariffs
from analysis import run_differential_analysis

client = TestClient(app)

class TestPhase2(unittest.TestCase):
    def test_data_ingestion(self):
        """Ensure we can load data and it's not empty."""
        new_tariffs, old_tariffs = load_gazetted_tariffs()
        self.assertTrue(len(new_tariffs) > 0, "New tariffs should be loaded")
        self.assertTrue(len(old_tariffs) > 0, "Old tariffs should be loaded")

    def test_api_impact_summary(self):
        """Test the Day 4 Analysis Endpoint."""
        response = client.get("/impact/summary")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify statistical keys exist
        self.assertIn("net_financial_impact", data)
        self.assertIn("average_variance", data)
        self.assertIn("total_procedures_analyzed", data)

    def test_analysis_logic(self):
        """Verify the math in the Rate Analyzer."""
        df, stats = run_differential_analysis()
        # Check that variance is calculated correctly for the first item
        row = df.iloc[0]
        self.assertAlmostEqual(row["variance"], row["new_rate"] - row["old_rate"])

if __name__ == '__main__':
    unittest.main()