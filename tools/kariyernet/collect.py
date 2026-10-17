"""Bounded, public-only Kariyer.net listing reader. No login, proxy, CAPTCHA bypass or browser spoofing."""
import argparse
import csv
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

ROOT = "https://www.kariyer.net"
CATEGORIES = [
    "/is-ilanlari/ankara-makine+muhendisi",
    "/is-ilanlari/ankara-uretim+muhendisi",
    "/is-ilanlari/ankara-kalite+muhendisi",
    "/is-ilanlari/kayseri-makine+muhendisi",
    "/is-ilanlari/kirikkale-makine+muhendisi",
]
USER_AGENT = "OsmanCareerResearch/0.1 (+public listing research; contact via repository)"
FIELDS = ("url", "title", "company", "location", "date_posted", "valid_through",
          "employment_type", "description", "source_category", "verification")


def extract_urls(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    urls = set()
    for a in soup.select("a[href]"):
        href = urldefrag(urljoin(base_url, a["href"]))[0]
        p = urlparse(href)
        if p.netloc.lower() not in ("kariyer.net", "www.kariyer.net"):
            continue
        if re.search(r"^/is-ilani/[^/?]+-\d+(?:/)?$", p.path):
            urls.add("https://www.kariyer.net" + p.path.rstrip("/"))
    return sorted(urls)


def iter_jsonld_jobs(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.select('script[type="application/ld+json"]'):
        try:
            raw = json.loads(tag.string or tag.get_text())
        except (ValueError, TypeError):
            continue
        stack = [raw]
        while stack:
            obj = stack.pop()
            if isinstance(obj, list):
                stack.extend(obj)
            elif isinstance(obj, dict):
                stack.extend(obj.get("@graph", []) if isinstance(obj.get("@graph"), list) else [])
                typ = obj.get("@type", "")
                types = typ if isinstance(typ, list) else [typ]
                if "JobPosting" in types:
                    yield obj


def normalize(job, url, category):
    org = job.get("hiringOrganization") or {}
    loc = job.get("jobLocation") or {}
    if isinstance(loc, list):
        loc = loc[0] if loc else {}
    address = loc.get("address", {}) if isinstance(loc, dict) else {}
    if isinstance(address, str):
        location = address
    else:
        location = ", ".join(str(address.get(k, "")) for k in ("addressLocality", "addressRegion") if address.get(k))
    text = BeautifulSoup(str(job.get("description") or ""), "html.parser").get_text(" ", strip=True)
    return dict(url=url, title=str(job.get("title") or ""), company=org.get("name", "") if isinstance(org, dict) else "",
                location=location, date_posted=str(job.get("datePosted") or ""),
                valid_through=str(job.get("validThrough") or ""), employment_type=str(job.get("employmentType") or ""),
                description=text[:12000], source_category=category, verification="public_jsonld_unverified_open")


def collect(output, max_details, delay):
    output.mkdir(parents=True, exist_ok=True)
    report = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "categories": {}, "errors": [],
              "fetched_detail_pages": 0, "extracted_jobpostings": 0, "note": "Listings are not verified as open; check official application page."}
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    robot = RobotFileParser()
    try:
        response = session.get(ROOT + "/robots.txt", timeout=20)
        response.raise_for_status()
        robot.parse(response.text.splitlines())
    except requests.RequestException as exc:
        report["errors"].append("robots_unavailable: " + type(exc).__name__)
        write(output, [], report)
        return

    discovered = {}
    def get(url):
        if not robot.can_fetch(USER_AGENT, url):
            report["errors"].append("robots_disallowed: " + url)
            return None
        try:
            res = session.get(url, timeout=25, allow_redirects=True)
            if urlparse(res.url).hostname not in ("kariyer.net", "www.kariyer.net"):
                report["errors"].append("redirect_outside_domain: " + url)
                return None
            if res.status_code in (403, 429):
                report["errors"].append("access_restricted_%d: %s" % (res.status_code, url))
                return None
            res.raise_for_status()
            return res.text
        except requests.RequestException as exc:
            report["errors"].append("fetch_error_%s: %s" % (type(exc).__name__, url))
            return None
        finally:
            time.sleep(delay)

    for category in CATEGORIES:
        html = get(ROOT + category)
        links = extract_urls(html, ROOT + category) if html else []
        report["categories"][category] = {"links": len(links), "accessible": html is not None}
        for link in links:
            discovered.setdefault(link, category)
    records = []
    for url, category in list(discovered.items())[:max_details]:
        html = get(url)
        if html is None:
            continue
        report["fetched_detail_pages"] += 1
        for job in iter_jsonld_jobs(html):
            records.append(normalize(job, url, category))
    report["discovered_unique_urls"] = len(discovered)
    report["extracted_jobpostings"] = len(records)
    write(output, records, report)


def write(output, records, report):
    (output / "jobs.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    with (output / "jobs.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(records)
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("output/kariyernet"))
    parser.add_argument("--max-details", type=int, default=80)
    parser.add_argument("--delay", type=float, default=3.0)
    args = parser.parse_args()
    collect(args.output, max(0, min(args.max_details, 100)), max(2.0, args.delay))
