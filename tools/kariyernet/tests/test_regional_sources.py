import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from regional_sources import inspect_page

class FakeSession:
    def get(self, url, timeout=15, allow_redirects=False):
        class Response:
            status_code = 200
            text = "<html><h1>Yalın Üretim Mühendisi</h1><p>Yeni mezun 08.06.2026</p></html>"
            def raise_for_status(self): pass
        response = Response()
        response.url = url
        if url.endswith("robots.txt"):
            response.text = "User-agent: *\nAllow: /"
        return response

class RegionalTests(unittest.TestCase):
    def test_public_page_is_not_proof_of_open_application(self):
        entry = {"name":"Example","url":"https://rc.hku.edu.tr/kariyer/sample","city":"Gaziantep"}
        row = inspect_page(entry, FakeSession())
        self.assertEqual(row["access_status"], "http_200")
        self.assertFalse(row["application_open_verified"])
        self.assertEqual(row["job_title"], "Yalın Üretim Mühendisi")
        self.assertEqual(row["requirements_state"], "source_text_requires_review")
        self.assertEqual(row["open_state"], "not_verified")
        self.assertIsNone(row["source_city_evidence"])
    def test_explicit_closed_not_open(self):
        class ClosedSession(FakeSession):
            def get(self, url, timeout=15, allow_redirects=False):
                response = super().get(url, timeout, allow_redirects)
                if not url.endswith("robots.txt"):
                    response.text = "<h1>Makine Mühendisi</h1><p>Gaziantep. Başvuru süresi doldu.</p>"
                return response
        entry = {"name":"Closed","url":"https://rc.hku.edu.tr/kariyer/sample","city":"Gaziantep"}
        row = inspect_page(entry, ClosedSession())
        self.assertEqual(row["open_state"], "source_says_closed")
        self.assertEqual(row["source_city_evidence"], "Gaziantep")
        self.assertFalse(row["application_open_verified"])

    def test_unknown_domain_rejected(self):
        row = inspect_page({"name":"Nope","url":"https://example.com/jobs"}, FakeSession())
        self.assertEqual(row["access_status"], "unapproved_domain")

if __name__ == "__main__":
    unittest.main()
