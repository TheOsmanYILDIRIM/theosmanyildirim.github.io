"""Regionally relevant source registry; never silently converts candidates into open jobs."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

def export(config_path, output):
    items = json.loads(config_path.read_text(encoding="utf-8"))["sources"]
    accepted = []
    for entry in items:
        url = entry["url"]
        host = urlparse(url)
        if host.scheme != "https" or not host.netloc:
            raise ValueError("invalid source URL")
        accepted.append({**entry, "checked_at": datetime.now(timezone.utc).isoformat(),
                         "application_open_verified": False})
    output.mkdir(parents=True, exist_ok=True)
    (output / "regional_source_candidates.json").write_text(json.dumps(accepted, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"regional_sources={len(accepted)} verified_open=0")

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output", type=Path, default=Path("output/kariyernet"))
    p.add_argument("--config", type=Path, default=Path("tools/kariyernet/official_regional_sources.json"))
    a=p.parse_args()
    export(a.config,a.output)
