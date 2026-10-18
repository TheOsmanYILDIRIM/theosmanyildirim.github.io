import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cv_rank import evaluate

class CVRankingTests(unittest.TestCase):
    def test_target_city(self):
        r = evaluate({"title": "Üretim Mühendisi", "location": "Gaziantep", "description": "Yeni mezun, SolidWorks"})
        self.assertTrue(r["eligible_location"])
        self.assertGreaterEqual(r["score"], 70)
    def test_istanbul_excluded(self):
        r = evaluate({"title": "Makine Mühendisi", "location": "İstanbul", "description": "Yeni mezun"})
        self.assertFalse(r["eligible_location"])
        self.assertEqual(r["score"], 0)
    def test_senior_penalty(self):
        a = evaluate({"title": "Process Engineer", "location": "Kayseri", "description": "minimum 5 years experience"})
        b = evaluate({"title": "Process Engineer", "location": "Kayseri", "description": "new graduate"})
        self.assertLess(a["score"], b["score"])
    def test_unknown_location(self):
        self.assertFalse(evaluate({"title":"Mechanical Engineer","location":"Turkey"})["eligible_location"])
if __name__ == "__main__":
    unittest.main()
