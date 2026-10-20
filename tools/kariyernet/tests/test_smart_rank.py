import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from smart_rank import evaluate,DIMENSIONS
class SmartRankTests(unittest.TestCase):
    def test_weights(self):
        self.assertEqual(sum(DIMENSIONS.values()),100)
    def test_no_false_open(self):
        x=evaluate({"title":"Makine Mühendisi","location":"Gaziantep","description":"Yeni mezun"})
        self.assertEqual(x["open_state"],"not_verified")
        self.assertEqual(x["requirements_state"],"new_graduate_explicit")
        self.assertEqual(x["requirements"],25)
    def test_senior_gap(self):
        x=evaluate({"title":"Senior Mechanical Engineer","location":"Kayseri","description":"minimum 5 years"})
        self.assertEqual(x["status"],"requirement_gap")
    def test_no_city_inference(self):
        x=evaluate({"title":"Production Engineer","location":"Turkey","description":""})
        self.assertEqual(x["location_score"],0)
    def test_degree_other_discipline_needs_review(self):
        x=evaluate({"title":"Production Engineer","location":"Gaziantep",
                    "description":"Bachelor's degree in industrial engineering"})
        self.assertEqual(x["requirements_state"],"degree_requires_review")
    def test_experience_gap_has_priority(self):
        x=evaluate({"title":"Production Engineer","location":"Gaziantep",
                    "description":"Bachelor's degree in industrial engineering. Minimum 5 years"})
        self.assertEqual(x["requirements_state"],"experience_gap")
    def test_explicit_incompatible_degree(self):
        x=evaluate({"title":"Quality Engineer","location":"Kayseri",
                    "description":"only electrical engineer"})
        self.assertEqual(x["requirements_state"],"incompatible_degree")
    def test_istanbul_excluded(self):
        x=evaluate({"title":"Mechanical Engineer","location":"İstanbul","description":"new grad"})
        self.assertEqual(x["score"],0)
if __name__=="__main__":
    unittest.main()
