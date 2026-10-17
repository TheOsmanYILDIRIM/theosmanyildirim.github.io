import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from collect import extract_urls, iter_jsonld_jobs, normalize


class ExtractTests(unittest.TestCase):
    def test_links_are_deduplicated_and_only_kariyernet(self):
        html = '<a href="/is-ilani/ornek-muhendis-12345">a</a><a href="/is-ilani/ornek-muhendis-12345">b</a><a href="https://evil.example/is-ilani/test-22">x</a>'
        self.assertEqual(extract_urls(html, "https://www.kariyer.net/is-ilanlari/ankara"), ["https://www.kariyer.net/is-ilani/ornek-muhendis-12345"])

    def test_jsonld_job(self):
        html = '<script type="application/ld+json">{"@type":"JobPosting","title":"Üretim Mühendisi","hiringOrganization":{"name":"Örnek AŞ"},"description":"<p>Üretim planlama</p>"}</script>'
        jobs = list(iter_jsonld_jobs(html))
        self.assertEqual(len(jobs), 1)
        row = normalize(jobs[0], "https://www.kariyer.net/is-ilani/x-12", "/is-ilanlari/ankara")
        self.assertEqual(row["company"], "Örnek AŞ")
        self.assertEqual(row["description"], "Üretim planlama")


if __name__ == "__main__":
    unittest.main()
