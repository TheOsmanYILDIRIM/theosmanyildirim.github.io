"""Official public job-board feeds. Only configured, identified employer boards."""
import argparse
import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

FIELDS = ("source", "source_id", "url", "title", "company", "location",
          "date_posted", "description", "verification", "retrieved_at")
HEADERS = {"User-Agent": "OsmanCareerResearch/0.2 (public-job-board-reader)", "Accept": "application/json"}

def plain(value):
    return BeautifulSoup(str(value or ""), "html.parser").get_text(" ", strip=True)[:12000]

def normalize_greenhouse(data, company, stamp):
    return {
        "source": "greenhouse", "source_id": str(data.get("id", "")),
        "url": data.get("absolute_url", ""), "title": data.get("title", ""),
        "company": company, "location": (data.get("location") or {}).get("name", ""),
        "date_posted": data.get("updated_at", ""),
        "description": plain(data.get("content")), "verification": "official_public_api",
        "retrieved_at": stamp
    }

def normalize_lever(data, company, stamp):
    categories = data.get("categories") or {}
    description = data.get("descriptionPlain") or data.get("description", "")
    return {
        "source": "lever", "source_id": str(data.get("id", "")),
        "url": data.get("hostedUrl") or data.get("applyUrl") or "",
        "title": data.get("text", ""), "company": company,
        "location": categories.get("location", ""),
        "date_posted": str(data.get("createdAt") or ""),
        "description": plain(description), "verification": "official_public_api",
        "retrieved_at": stamp
    }

def allowed_board(board):
    kind = board.get("provider")
    token = board.get("board", "")
    return kind in ("greenhouse", "lever") and bool(token) and all(c.isalnum() or c in "-_" for c in token)

def collect(config_path, output):
    output.mkdir(parents=True, exist_ok=True)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    boards = config.get("boards", [])
    timestamp = datetime.now(timezone.utc).isoformat()
    report = {"timestamp_utc": timestamp, "feeds": [], "valid_records": 0, "errors": []}
    records = []
    session = requests.Session()
    session.headers.update(HEADERS)
    for board in boards[:25]:
        if not allowed_board(board):
            report["errors"].append({"board": str(board.get("company", "")), "reason": "invalid_board_config"})
            continue
        kind, token = board["provider"], board["board"]
        url = (f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true"
               if kind == "greenhouse" else f"https://api.lever.co/v0/postings/{token}?mode=json")
        status = {"company": board.get("company", ""), "provider": kind, "status": "unavailable", "count": 0}
        try:
            response = session.get(url, timeout=20)
            response.raise_for_status()
            payload = response.json()
            jobs = payload.get("jobs", []) if kind == "greenhouse" else payload
            if not isinstance(jobs, list):
                raise ValueError("unexpected_json_shape")
            for job in jobs[:2000]:
                row = normalize_greenhouse(job, board.get("company", token), timestamp) if kind == "greenhouse" else normalize_lever(job, board.get("company", token), timestamp)
                if row["url"] and row["title"] and row["company"] and urlparse(row["url"]).scheme == "https":
                    records.append(row)
                    status["count"] += 1
            status["status"] = "ok"
        except (requests.RequestException, ValueError, TypeError, KeyError) as exc:
            status["status"] = "error"
            report["errors"].append({"board": board.get("company", token), "reason": type(exc).__name__})
        report["feeds"].append(status)
    records = list({(r["source"], r["source_id"], r["url"]): r for r in records}.values())
    report["valid_records"] = len(records)
    (output / "official_jobs.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "official_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    with (output / "official_jobs.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(records)
    print(json.dumps({"official_records": len(records), "feeds": len(report["feeds"])}))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("tools/kariyernet/official_boards.json"))
    parser.add_argument("--output", type=Path, default=Path("output/kariyernet"))
    args = parser.parse_args()
    collect(args.config, args.output)
