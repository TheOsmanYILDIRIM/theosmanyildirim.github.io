import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from search_families import build_queries

class SearchFamiliesTests(unittest.TestCase):
    def test_bounded(self):
        queries=build_queries(limit=12)
        self.assertEqual(len(queries),12)
        self.assertEqual(len(queries),len(set(queries)))
        self.assertTrue(all("İstanbul" not in q for q in queries))
if __name__=="__main__":
    unittest.main()
