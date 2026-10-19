"""Public regional career-page probes. Never infer an active vacancy from HTTP 200."""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import requests
from bs4 import BeautifulSoup

ALLOWED = {"kariyer.mke.gov.tr", "rc.hku.edu.tr", "www.kayserikariyer.com", "kayserikariyer.com"}
USER_AGENT = "OsmanCareerResearch/0.2 (regional public-source verification)"

def inspect_page(entry, session):
    url = entry["url"]
    parsed = urlparse(url)
    result = {**entry, "checked_at": datetime.now(timezone.utc).isoformat(),
              "application_open_verified": False, "access_status": "unknown",
              "job_title": None, "date_evidence": None, "experience_evidence": None}
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED:
        result["access_status"] = "unapproved_domain"
        return result
    robots_url = parsed.scheme + "://" + parsed.hostname + "/robots.txt"
    robot = RobotFileParser()
    try:
        rr = session.get(robots_url, timeout=15)
        rr.raise_for_status()
        robot.parse(rr.text.splitlines())
        if not robot.can_fetch(USER_AGENT, url):
            result["access_status"] = "robots_disallowed"
            return result
        response = session.get(url, timeout=20, allow_redirects=True)
        final = urlparse(response.url)
        if final.hostname not in ALLOWED:
            result["access_status"] = "off_domain_redirect"
            return result
        result["access_status"] = "http_" + str(response.status_code)
        if response.status_code != 200:
            return result
        soup = BeautifulSoup(response.text, "html.parser")
        result["job_title"] = (soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else None)
        text = soup.get_text(" ", strip=True)
        dates = re.findall(r"\b\d{1,2}[./-]\d{1,2}[./-]20\d{2}\b", text)
        result["date_evidence"] = dates[:3]
        matches = re.findall(r"(?:yeni mezun|0\s*[-–]\s*2 yıl|en az \d+ yıl|\d+ yıl deneyim)", text, re.I)
        result["experience_evidence"] = matches[:3]
        # A live web page is insufficient to establish open applications.
        result["verification"] = "public_page_accessible_open_not_verified"
        return result
    except requests.RequestException as exc:
        result["access_status"] = "network_" + type(exc).__name__
        return result

def export(config_path, output):
    items = json.loads(config_path.read_text(encoding="utf-8"))["sources"]
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    rows = [inspect_page(item, session) for item in items]
    output.mkdir(parents=True, exist_ok=True)
    (output / "regional_source_candidates.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"regional_sources": len(rows), "verified_open": 0,
                      "access": {row["name"]: row["access_status"] for row in rows}}, ensure_ascii=False))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, default=Path("output/kariyernet"))
    p.add_argument("--config", type=Path, default=Path("tools/kariyernet/official_regional_sources.json"))
    args = p.parse_args()
    export(args.config, args.output)
