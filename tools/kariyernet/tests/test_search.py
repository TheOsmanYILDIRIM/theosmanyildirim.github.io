import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from search import parse_keywords, build_search_url

class SearchTests(unittest.TestCase):
    def test_keywords(self):
        self.assertEqual(parse_keywords("CNC;makine mühendisi;CNC"), ["CNC", "makine mühendisi"])
    def test_five_page_url(self):
        self.assertEqual(build_search_url("makine mühendisi", 5),
                         "https://www.kariyer.net/is-ilanlari?kw=makine+m%C3%BChendisi&cp=5")
if __name__ == "__main__":
    unittest.main()
