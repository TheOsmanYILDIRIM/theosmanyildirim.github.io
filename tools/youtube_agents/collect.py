#!/usr/bin/env python3
"""Collect relevant public YouTube captions; keep every failure visible."""
import argparse
import html
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

CHANNELS = {
    "forn-ai": "https://www.youtube.com/@fornyapayzeka",
    "avenox": "https://www.youtube.com/@avenoxai",
}
DIRECT = re.compile(
    r"(?i)(?:alt[ -]?ajan|sub[ -]?agent|multi[ -]?agent|agentic|agents?\b|"
    r"ajan(?:lar|ları|lara|larla|ın|ı)?\b|orkestrasyon|orchestrat|fleet|"
    r"delegat|paralel ajan|parallel agents?|yapay zek[aâ] ekib|ai team|"
    r"yapay zek[aâ]yı işe ald|ai workforce)"
)
CONTEXT = re.compile(r"(?i)(?:context|bağlam|hafıza|memory|beyin|workflow|codex|claude code|jev|skill|görev|task|prompt|worktree|harness|otonom)")
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
TIME_LINE = re.compile(r"^\d\d:\d\d:\d\d[.,]\d{3}\s*-->")
TAG = re.compile(r"<[^>]+>")


def run_ytdlp(args, timeout):
    cmd = [sys.executable, "-m", "yt_dlp", "--no-warnings", *args]
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    if done.returncode != 0:
        return None, "yt-dlp exit status " + str(done.returncode)
    return done.stdout, None


def parse_json(raw):
    try:
        return json.loads(raw) if raw else None
    except json.JSONDecodeError:
        return None


def simplify_vtt(text):
    lines, previous = [], ""
    for raw in text.splitlines():
        line = raw.strip().lstrip("\ufeff")
        if not line or line.startswith(("WEBVTT", "NOTE", "STYLE", "REGION", "Kind:", "Language:")):
            continue
        if TIME_LINE.match(line) or line.isdecimal():
            continue
        line = html.unescape(TAG.sub("", line)).strip()
        if not line or line == previous:
            continue
        if previous and line.startswith(previous) and len(previous) >= 12:
            lines[-1] = line
        elif previous and previous.startswith(line):
            continue
        else:
            lines.append(line)
        previous = line
    return "\n".join(lines).strip()


def classify(title, description=""):
    title, description = title or "", description or ""
    if DIRECT.search(title):
        return "direct"
    if DIRECT.search(description) and CONTEXT.search(title + " " + description):
        return "direct_description"
    if CONTEXT.search(title) and re.search(r"(?i)(?:codex|claude code|yapay zek[aâ]|ai |model|agent|ajan)", title):
        return "supporting"
    return None


def base_video(row):
    if not isinstance(row, dict):
        return None
    video_id = row.get("id") or row.get("url")
    if not isinstance(video_id, str) or not VIDEO_ID.fullmatch(video_id):
        return None
    return {
        "id": video_id,
        "title": str(row.get("title") or ""),
        "url": "https://www.youtube.com/watch?v=" + video_id,
        "duration": row.get("duration"),
        "upload_date": row.get("upload_date"),
    }


def discover(channel, timeout, max_videos):
    found, failures = {}, []
    for suffix in ("videos", "streams"):
        raw, error = run_ytdlp(
            ["--flat-playlist", "--dump-single-json", "--ignore-errors", f"{CHANNELS[channel]}/{suffix}"],
            timeout,
        )
        obj = parse_json(raw)
        if error or not isinstance(obj, dict) or not isinstance(obj.get("entries"), list):
            failures.append({"surface": suffix, "error": error or "invalid or missing catalog"})
            continue
        for item in obj["entries"]:
            record = base_video(item)
            if record:
                found.setdefault(record["id"], record)
                if max_videos and len(found) >= max_videos:
                    break
        if max_videos and len(found) >= max_videos:
            break
    return list(found.values()), failures


def captions_for(video, dest, timeout):
    dest.mkdir(parents=True, exist_ok=True)
    output = str(dest / (video["id"] + ".%(ext)s"))
    _, error = run_ytdlp(
        ["--no-playlist", "--skip-download", "--write-subs", "--write-auto-subs",
         "--sub-langs", "tr.*,en.*", "--sub-format", "vtt/best",
         "--retries", "2", "--fragment-retries", "2", "--socket-timeout", "15",
         "--output", output, video["url"]],
        timeout,
    )
    captions = []
    for path in sorted(dest.glob(video["id"] + ".*.vtt")):
        lang = path.name[len(video["id"]) + 1:-4]
        if not re.fullmatch(r"(?:tr|en)(?:[-_][A-Za-z0-9-]+)?", lang):
            continue
        normalized = simplify_vtt(path.read_text(encoding="utf-8", errors="replace"))
        if normalized:
            text_path = dest / (video["id"] + "." + lang + ".txt")
            text_path.write_text(normalized + "\n", encoding="utf-8")
            captions.append({"language": lang, "text_file": text_path.name,
                             "characters": len(normalized)})
        path.unlink()
    return captions, error


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="output/youtube-agents")
    p.add_argument("--max-videos", type=int, default=0)
    p.add_argument("--max-captions", type=int, default=0)
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--metadata-timeout", type=int, default=50)
    p.add_argument("--scan-descriptions", action="store_true")
    args = p.parse_args(argv)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    summary = {"created_utc": datetime.now(timezone.utc).isoformat(), "tool": "yt-dlp",
               "channels": CHANNELS, "videos": [], "channel_failures": [], "totals": {}}
    candidates = []
    for channel in CHANNELS:
        videos, failures = discover(channel, args.timeout * 3, args.max_videos)
        for failure in failures:
            summary["channel_failures"].append({"channel": channel, **failure})
        for item in videos:
            item["channel"] = channel
            category = classify(item["title"])
            if args.scan_descriptions or category:
                raw, error = run_ytdlp(
                    ["--skip-download", "--dump-single-json", "--no-playlist", item["url"]],
                    args.metadata_timeout,
                )
                obj = parse_json(raw)
                if isinstance(obj, dict):
                    item["title"] = str(obj.get("title") or item["title"])
                    item["duration"] = obj.get("duration")
                    item["upload_date"] = obj.get("upload_date")
                    category = classify(item["title"], obj.get("description"))
                elif category:
                    item["metadata_warning"] = error or "metadata invalid"
            item["category"] = category
            item["captions"] = []
            item["status"] = "not_relevant" if category is None else "pending"
            summary["videos"].append(item)
            if category:
                candidates.append(item)
    if args.max_captions:
        candidates.sort(key=lambda x: (x["category"] == "supporting", x["channel"], x["id"]))
        for item in candidates[args.max_captions:]:
            item["status"] = "skipped_limit"
        candidates = candidates[:args.max_captions]
    for item in candidates:
        item["captions"], error = captions_for(
            item, out / "transcripts" / item["channel"], args.timeout
        )
        item["status"] = "downloaded" if item["captions"] else "missing_or_blocked"
        if error:
            item["caption_error"] = error
    statuses = Counter(item["status"] for item in summary["videos"])
    summary["totals"] = {
        "discovered": len(summary["videos"]),
        "direct": sum(x["category"] in ("direct", "direct_description") for x in summary["videos"]),
        "supporting": sum(x["category"] == "supporting" for x in summary["videos"]),
        "captions_downloaded": statuses["downloaded"],
        "missing_or_blocked": statuses["missing_or_blocked"],
        "skipped_limit": statuses["skipped_limit"],
    }
    (out / "manifest.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    with (out / "selected.md").open("w", encoding="utf-8") as f:
        f.write("# Alt ajan video keşfi\n\n")
        for x in summary["videos"]:
            if x["category"]:
                name = x["title"].replace("[", "(").replace("]", ")")
                f.write(f"- [{name}]({x['url']}) — {x['channel']} / {x['category']} / {x['status']}\n")
    print(json.dumps(summary["totals"], ensure_ascii=False))
    if not summary["videos"]:
        print("ERROR: catalog empty; cannot claim coverage", file=sys.stderr)
        return 2
    if not summary["totals"]["direct"]:
        print("ERROR: no relevant agent videos", file=sys.stderr)
        return 3
    if not summary["totals"]["captions_downloaded"]:
        print("ERROR: captions unavailable", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
