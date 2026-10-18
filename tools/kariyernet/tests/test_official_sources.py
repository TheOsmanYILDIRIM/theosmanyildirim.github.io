import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from official_sources import normalize_greenhouse, normalize_lever, allowed_board

class OfficialSourcesTests(unittest.TestCase):
    def test_greenhouse(self):
        data = {"id": 123, "title": "Mechanical Engineer", "absolute_url": "https://boards.greenhouse.io/example/jobs/123", "location": {"name": "Ankara"}, "content": "<p>Production</p>"}
        row = normalize_greenhouse(data, "Test Employer", "2026-10-18")
        self.assertEqual((row["title"], row["location"], row["description"]), ("Mechanical Engineer", "Ankara", "Production"))
    def test_lever(self):
        data = {"id": "abc", "text": "Process Engineer", "hostedUrl": "https://jobs.lever.co/example/abc", "categories": {"location": "Kayseri"}, "descriptionPlain": "Process optimization"}
        row = normalize_lever(data, "Test Employer", "2026-10-18")
        self.assertEqual((row["title"], row["location"], row["description"]), ("Process Engineer", "Kayseri", "Process optimization"))
    def test_config_rejects_unsafe_token(self):
        self.assertFalse(allowed_board({"provider":"greenhouse","board":"../../abc"}))
        self.assertTrue(allowed_board({"provider":"lever","board":"example"}))
if __name__ == "__main__":
    unittest.main()
