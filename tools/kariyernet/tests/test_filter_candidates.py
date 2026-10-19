import sys
import tempfile
import unittest
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from filter_candidates import listing_key, is_banned, build

class CandidateFilterTests(unittest.TestCase):
    def test_exact_id(self):
        self.assertEqual(listing_key("https://www.kariyer.net/is-ilani/example-4569311"), ("kariyer.net","4569311"))
    def test_company_similarity_not_enough(self):
        ban={"kariyer.net/isisan-isi-sanayi-a-s"}
        self.assertTrue(is_banned({"url":"https://www.kariyer.net/is-ilani/isisan-isi-sanayi-a-s-imalat-muhendisi-4576522"},ban))
        self.assertFalse(is_banned({"url":"https://www.kariyer.net/is-ilani/isisan-makina-baska-firma-muhendisi-4561234"},ban))
        self.assertFalse(is_banned({"url":"https://www.kariyer.net/is-ilani/baska-firma-isisan-isi-sanayi-a-s-9876543"},ban))
    def test_review_applies_only_to_listing(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"discovered_urls.json").write_text(json.dumps([
                {"url":"https://www.kariyer.net/is-ilani/ornek-makine-muhendisi-100"},
                {"url":"https://www.kariyer.net/is-ilani/ornek-uretim-muhendisi-101"},
                {"url":"https://www.kariyer.net/is-ilani/isisan-isi-sanayi-a-s-imalat-102"}]))
            (root/"official_jobs.json").write_text("[]")
            review=root/"review.json";review.write_text(json.dumps({"listings":[{"provider":"kariyer.net","listing_id":"100"}]}))
            profile=root/"profile.md";profile.write_text("- company_key: kariyer.net/isisan-isi-sanayi-a-s\n")
            build(root,review,profile)
            result=json.loads((root/"new_kariyernet_candidates.json").read_text())
            self.assertEqual([x["listing_id"] for x in result],["101"])
            self.assertEqual(len(json.loads((root/"excluded_candidates.json").read_text())),2)
if __name__=="__main__":
    unittest.main()
