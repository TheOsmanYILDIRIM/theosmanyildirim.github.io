"""Create recommendation queue after collection; preserve raw daily archives.
Reviewed listing IDs are scoped to provider. Employer bans match exact source identifiers only.
"""
import argparse
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

def reviewed_keys(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    return {(x["provider"], str(x["listing_id"])) for x in data["listings"]}

def banned_company_keys(profile_path):
    return set(re.findall(r"^- company_key:\s*(\S+)\s*$", profile_path.read_text(encoding="utf-8"), re.M))

def listing_key(url):
    p = urlparse(url)
    if p.hostname not in ("kariyer.net", "www.kariyer.net"):
        return None
    m = re.fullmatch(r"/is-ilani/[^/?]+-(\d+)/?", p.path)
    return ("kariyer.net", m.group(1)) if m else None

def is_banned(entry, banned):
    # No substring company-name ban. Only an exact, explicitly recorded issuer identifier.
    url = entry.get("url", "")
    p = urlparse(url)
    if p.hostname not in ("kariyer.net", "www.kariyer.net"):
        return False
    slug = p.path.removeprefix("/is-ilani/")
    for key in banned:
        provider, _, employer_slug = key.partition("/")
        if provider == "kariyer.net" and employer_slug:
            if slug.startswith(employer_slug + "-") and re.fullmatch(r"[^/?]+-\d+", slug):
                return True
    return False

def extract_source_evidence(detail):
    """Conservative, source-backed fields. Never infer from keyword or URL slug."""
    description = str(detail.get("description") or "")
    title = str(detail.get("title") or "")
    location = str(detail.get("location") or "")
    normalized = description.casefold()
    years = re.findall(r"(?:en az|minimum|at least)\\s*(\\d+)\\s*(?:yıl|years?)", normalized)
    grad = bool(re.search(r"yeni mezun|new graduates?|entry.level|deneyimsiz", normalized))
    degree = bool(re.search(r"makine mühendisli(?:ği|ği)|mechanical engineering", normalized))
    expiry = str(detail.get("valid_through") or "").strip()
    closed = False
    if expiry:
        try:
            closed = date.fromisoformat(expiry[:10]) < date.today()
        except ValueError:
            pass
    return {
        "city_evidence": location,
        "profession_evidence": title,
        "experience_min_years": min(map(int, years)) if years else None,
        "new_graduate_evidence": grad,
        "mechanical_degree_mentioned": degree,
        "requirements_state": "source_text_requires_review" if description else "unknown",
        "open_state": "expired_date" if closed else "not_verified",
        "open_evidence": "validThrough expired" if closed else None,
    }


def build(folder, reviewed_path, profile_path):
    folder.mkdir(parents=True, exist_ok=True)
    keys = reviewed_keys(reviewed_path)
    banned = banned_company_keys(profile_path)
    discovered = json.loads((folder / "discovered_urls.json").read_text(encoding="utf-8"))
    official = json.loads((folder / "official_jobs.json").read_text(encoding="utf-8"))
    # Join only publicly extracted JobPosting metadata. URL/keyword are not proof.
    details = {}
    detail_path = folder / "jobs.json"
    if detail_path.exists():
        for item in json.loads(detail_path.read_text(encoding="utf-8")):
            url = item.get("url", "")
            if listing_key(url) and item.get("verification") == "public_jsonld_unverified_open":
                details.setdefault(url, item)
    new_urls, excluded, seen = [], [], set()
    for entry in discovered:
        key = listing_key(entry["url"])
        if not key or key in seen:
            continue
        seen.add(key)
        reason = "banned_employer" if is_banned(entry,banned) else "reviewed_listing" if key in keys else None
        if reason:
            excluded.append({"url": entry["url"], "reason": reason, "listing_id":key[1]})
        else:
            detail = details.get(entry["url"], {})
            title = str(detail.get("title") or "")
            location = str(detail.get("location") or "")
            new_urls.append({
                **entry, "listing_id": key[1],
                "verification": "public_jsonld_unverified_open" if detail else "url_only_not_verified_open",
                "title": title, "company": str(detail.get("company") or ""),
                "location": location, "date_posted": str(detail.get("date_posted") or ""),
                "valid_through": str(detail.get("valid_through") or ""),
                "description": str(detail.get("description") or ""),
                "employment_type": str(detail.get("employment_type") or ""),
                "city_state": "source_metadata_unverified" if location else "unknown",
                "profession_state": "source_metadata_unverified" if title else "unknown",
                **extract_source_evidence(detail),
            })
    new_official = []
    for row in official:
        key=(row.get("source"),str(row.get("source_id", "")))
        # no cross-provider inference; ids must be explicitly reviewed under their own provider
        if key in keys:
            excluded.append({"url":row.get("url"),"reason":"reviewed_listing","listing_id":key[1]})
        else:
            new_official.append(row)
    report={"discovered_total":len(discovered),"new_kariyernet_urls":len(new_urls),
            "new_official_records":len(new_official),"excluded":len(excluded),
            "reviewed_key_count":len(keys),"banned_employer_keys":sorted(banned),
            "structured_metadata_candidates":sum(x["verification"]=="public_jsonld_unverified_open" for x in new_urls),
            "verified_open_kariyernet":0,
            "expired_by_source_date":sum(x["open_state"]=="expired_date" for x in new_urls),
            "note":"Source-extracted metadata is not independent verification of location, profession, requirements, or open application. Full raw archive retained."}
    for name, data in (("new_kariyernet_candidates.json",new_urls),
                       ("new_official_candidates.json",new_official),
                       ("excluded_candidates.json",excluded),
                       ("candidate_filter_report.json",report)):
        (folder/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,default=Path("output/kariyernet"))
    p.add_argument("--reviewed",type=Path,default=Path("tools/kariyernet/reviewed_listings.json"))
    p.add_argument("--profile",type=Path,default=Path("tools/kariyernet/OSMAN_JOB_PROFILE.md"))
    a=p.parse_args()
    build(a.output,a.reviewed,a.profile)
