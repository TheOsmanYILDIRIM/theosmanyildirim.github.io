"""Configurable direct Kariyer.net keyword/page collection, respecting robots and access limits."""
import argparse
import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlparse
from urllib.robotparser import RobotFileParser

import requests
from collect import ROOT, USER_AGENT, FIELDS, extract_urls, iter_jsonld_jobs, normalize


def parse_keywords(raw):
    words = [x.strip() for x in raw.replace("\n", ";").split(";") if x.strip()]
    return list(dict.fromkeys(words))[:20]


def build_search_url(keyword, page):
    return ROOT + "/is-ilanlari?" + urlencode({"kw": keyword, "cp": page})


def run(output, keywords, pages, max_details, delay):
    output.mkdir(parents=True, exist_ok=True)
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "source": "kariyer.net",
              "keywords": keywords, "pages_requested_per_keyword": pages, "pages": [],
              "errors": [], "discovered_unique_urls": 0, "detail_pages_fetched": 0,
              "jobposting_records": 0, "note": "Not evidence of an open application; verify with source."}
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "text/html"})
    robot = RobotFileParser()
    try:
        resp = session.get(ROOT + "/robots.txt", timeout=20)
        resp.raise_for_status()
        robot.parse(resp.text.splitlines())
    except requests.RequestException as exc:
        report["errors"].append("robots_unavailable:" + type(exc).__name__)
        save(output, [], report)
        return

    def fetch(url):
        if not robot.can_fetch(USER_AGENT, url):
            return None, "robots_disallowed"
        try:
            response = session.get(url, timeout=25, allow_redirects=True)
            if urlparse(response.url).hostname not in ("kariyer.net", "www.kariyer.net"):
                return None, "outside_domain_redirect"
            if response.status_code in (403, 429):
                return None, "restricted_" + str(response.status_code)
            response.raise_for_status()
            return response.text, "ok"
        except requests.RequestException as exc:
            return None, "request_error_" + type(exc).__name__
        finally:
            time.sleep(delay)

    discovered = {}
    for keyword in keywords:
        for page in range(1, pages + 1):
            url = build_search_url(keyword, page)
            html, status = fetch(url)
            links = extract_urls(html, url) if html else []
            report["pages"].append({"keyword": keyword, "page": page, "url": url,
                                    "status": status, "found_links": len(links)})
            if status != "ok":
                report["errors"].append({"url": url, "status": status})
            for link in links:
                discovered.setdefault(link, {"keyword": keyword, "page": page})

    # Preserve every discovered URL even when detail pages deny access.
    (output / "discovered_urls.json").write_text(
        json.dumps([{"url": url, **source} for url, source in discovered.items()],
                   ensure_ascii=False, indent=2), encoding="utf-8")
    # Page success is not evidence that pagination advanced. Identify identical URL sets.
    report["note"] = "HTTP 200 or extracted URLs do not prove pagination, open status or metadata."
    records = []
    blocked_details = False
    for url, source in list(discovered.items())[:max_details]:
        if blocked_details:
            break
        html, status = fetch(url)
        if status != "ok":
            report["errors"].append({"url": url, "status": status})
            if status in ("restricted_403", "restricted_429"):
                blocked_details = True
                report["errors"].append({"status": "detail_crawl_halted_after_access_restriction"})
            continue
        report["detail_pages_fetched"] += 1
        extracted = False
        for job in iter_jsonld_jobs(html):
            records.append(normalize(job, url, source["keyword"]))
            extracted = True
        if not extracted:
            records.append({**dict.fromkeys(FIELDS, ""), "url": url,
                            "source_category": source["keyword"],
                            "verification": "url_discovered_metadata_missing"})
    report["discovered_unique_urls"] = len(discovered)
    report["jobposting_records"] = len(records)
    report["metadata_complete_records"] = sum(bool(x.get("title")) and bool(x.get("company")) for x in records)
    save(output, records, report)


def save(folder, records, report):
    (folder / "jobs.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    with (folder / "jobs.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)
    (folder / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--keywords", default="makine mühendisi;üretim mühendisi;kalite mühendisi;CNC;teknik ressam")
    p.add_argument("--pages", type=int, default=5)
    p.add_argument("--max-details", type=int, default=150)
    p.add_argument("--delay", type=float, default=3)
    p.add_argument("--output", type=Path, default=Path("output/kariyernet"))
    a = p.parse_args()
    run(a.output, parse_keywords(a.keywords), min(10, max(5, a.pages)),
        min(200, max(0, a.max_details)), max(2.5, a.delay))
