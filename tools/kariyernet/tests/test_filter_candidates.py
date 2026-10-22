import sys
import tempfile
import unittest
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from filter_candidates import listing_key, is_banned, build, extract_source_evidence

class CandidateFilterTests(unittest.TestCase):
    def test_exact_id(self):
        self.assertEqual(listing_key("https://www.kariyer.net/is-ilani/example-4569311"), ("kariyer.net","4569311"))
    def test_company_similarity_not_enough(self):
        ban={"kariyer.net/isisan-isi-sanayi-a-s"}
        self.assertTrue(is_banned({"url":"https://www.kariyer.net/is-ilani/isisan-isi-sanayi-a-s-imalat-muhendisi-4576522"},ban))
        self.assertFalse(is_banned({"url":"https://www.kariyer.net/is-ilani/isisan-makina-baska-firma-muhendisi-4561234"},ban))
        self.assertFalse(is_banned({"url":"https://www.kariyer.net/is-ilani/baska-firma-isisan-isi-sanayi-a-s-9876543"},ban))
    def test_ban_reason_precedes_reviewed_status(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            url="https://www.kariyer.net/is-ilani/isisan-isi-sanayi-a-s-imalat-102"
            (root/"discovered_urls.json").write_text(json.dumps([{"url":url}]))
            (root/"official_jobs.json").write_text("[]")
            review=root/"review.json"
            review.write_text(json.dumps({"listings":[{"provider":"kariyer.net","listing_id":"102"}]}))
            profile=root/"profile.md"
            profile.write_text("- company_key: kariyer.net/isisan-isi-sanayi-a-s\n")
            build(root,review,profile)
            excluded=json.loads((root/"excluded_candidates.json").read_text())
            self.assertEqual(excluded[0]["reason"],"banned_employer")

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
    def test_structured_evidence_not_open_proof(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            url = "https://www.kariyer.net/is-ilani/ornek-makine-muhendisi-555"
            (root/"discovered_urls.json").write_text(json.dumps([{"url": url, "keyword": "Ankara"}]))
            (root/"official_jobs.json").write_text("[]")
            (root/"jobs.json").write_text(json.dumps([{"url":url, "title":"Makine Mühendisi",
                "location":"Gaziantep", "company":"Örnek", "description":"Yeni mezun",
                "verification":"public_jsonld_unverified_open"}]))
            review = root/"review.json"
            review.write_text('{"listings":[]}')
            profile = root/"profile.md"
            profile.write_text("- company_key: kariyer.net/isisan-isi-sanayi-a-s\\n")
            build(root, review, profile)
            candidates = json.loads((root/"new_kariyernet_candidates.json").read_text())
            self.assertEqual(len(candidates), 1)
            self.assertEqual(candidates[0]["location"], "Gaziantep")
            self.assertEqual(candidates[0]["title"], "Makine Mühendisi")
            self.assertEqual(candidates[0]["open_state"], "not_verified")
            self.assertEqual(candidates[0]["requirements_state"], "source_text_requires_review")
            report = json.loads((root/"candidate_filter_report.json").read_text())
            self.assertEqual(report["structured_metadata_candidates"], 1)
            self.assertEqual(report["verified_open_kariyernet"], 0)

    def test_requirement_evidence_does_not_imply_open(self):
        source = {"title":"Makine Mühendisi", "location":"Gaziantep",
                  "description":"Yeni mezun makine mühendisliği mezunu veya en az 2 yıl deneyim"}
        result = extract_source_evidence(source)
        self.assertEqual(result["city_evidence"], "Gaziantep")
        self.assertEqual(result["experience_min_years"], 2)
        self.assertTrue(result["new_graduate_evidence"])
        self.assertTrue(result["mechanical_degree_mentioned"])
        self.assertEqual(result["open_state"], "not_verified")

    def test_expired_source_date_cannot_be_open(self):
        result = extract_source_evidence({"valid_through":"2020-01-01"})
        self.assertEqual(result["open_state"], "expired_date")

if __name__=="__main__":
    unittest.main()
