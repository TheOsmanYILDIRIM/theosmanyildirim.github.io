"""Deterministic CV-focused scoring. Never treats URL discovery as a verified vacancy."""
import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path

PRIMARY = ["kahramanmaras", "gaziantep", "osmaniye", "adana", "kayseri", "malatya"]
SECONDARY = ["mersin", "ankara"]
TARGETS = {"makine": 34, "mechanical": 34, "uretim": 31, "production": 31,
           "imalat": 31, "manufacturing": 31, "kalite": 28, "quality": 28,
           "tasarim": 27, "design engineer": 27, "proses": 29, "process engineer": 29,
           "ar-ge": 26, "r&d": 26, "cad": 26, "planning engineer": 23}
RELATED = ["solidworks", "autocad", "moldflow", "kaynak", "welding", "cnc",
           "ndt", "talaşlı", "machining", "lean manufacturing", "kalite kontrol",
           "quality control", "technical drawing", "teknik resim", "python", "matlab"]
FIELDS = ["score", "eligible_location", "company", "title", "location", "url",
          "source", "verification", "reason", "experience_signal", "language_signal"]

def fold(value):
    s = unicodedata.normalize("NFKD", str(value or "")).casefold()
    return "".join(ch for ch in s if not unicodedata.combining(ch)).replace("ı", "i")

def evaluate(job):
    title, location, desc = [fold(job.get(k)) for k in ("title", "location", "description")]
    reasons = []
    primary = any(c in location for c in PRIMARY)
    secondary = any(c in location for c in SECONDARY)
    excluded = "istanbul" in location
    # Missing or vague country-level location is not evidence of a local role.
    region_ok = (primary or secondary) and not excluded
    title_points = max((v for k, v in TARGETS.items() if k in title), default=0)
    if not title_points:
        title_points = 8 if ("engineer" in title or "muhendis" in title) else 0
    score = title_points
    if title_points >= 23:
        reasons.append("Makine/üretim/kalite/tasarım hedefiyle ilgili pozisyon")
    elif title_points:
        reasons.append("Mühendislik pozisyonu; uzmanlık uyumu belirsiz")
    else:
        reasons.append("Öncelikli makine mühendisliği alanı dışında")
    if primary:
        score += 35
        reasons.append("Birinci öncelikli şehir")
    elif secondary:
        score += 24
        reasons.append("İkinci öncelikli şehir")
    else:
        reasons.append("Hedef şehirler dışında veya konum belirsiz")
    if excluded:
        score = 0
        reasons.append("İstanbul kapsam dışı")
    years = [int(n) for n in re.findall(r"(?:minimum|at least|en az)\s*(\d+)\s*(?:years?|yıl)", desc)]
    years += [int(n) for n in re.findall(r"(\d+)\s*\+\s*(?:years?|yıl)", desc)]
    if re.search(r"new grad|entry.level|yeni mezun|deneyimsiz|0\s*[-–]\s*2\s*(?:years?|yıl)", desc):
        score += 20
        exp_signal = "new_graduate_or_0_2"
        reasons.append("Yeni mezun/0–2 yıl ifadesi")
    elif years and min(years) > 2:
        score -= 32
        exp_signal = f"minimum_{min(years)}_years"
        reasons.append(f"En az {min(years)} yıl tecrübe isteniyor")
    elif "senior" in title or "lead" in title or "manager" in title or "kidemli" in title:
        score -= 30
        exp_signal = "senior_title"
        reasons.append("Kıdemli pozisyon")
    else:
        exp_signal = "unknown"
        reasons.append("Deneyim koşulu doğrulanmalı")
    matches = [x for x in RELATED if fold(x) in desc]
    if matches:
        score += min(12, len(matches) * 3)
        reasons.append("CV beceri eşleşmesi: " + ", ".join(matches[:4]))
    lang = "advanced_english" if re.search(r"advanced english|fluent english|c1 english|ileri seviye ingilizce", desc) else "unspecified"
    if lang == "advanced_english":
        score -= 12
        reasons.append("İleri İngilizce şartı")
    return {"score": max(0, min(100, score)), "eligible_location": region_ok, "company": job.get("company", ""),
            "title": job.get("title", ""), "location": job.get("location", ""), "url": job.get("url", ""),
            "source": job.get("source", ""), "verification": job.get("verification", ""),
            "reason": "; ".join(reasons), "experience_signal": exp_signal, "language_signal": lang}

def main(folder):
    official = json.loads((folder / "official_jobs.json").read_text(encoding="utf-8"))
    evaluated = [evaluate(job) for job in official if job.get("verification") == "official_public_api"]
    evaluated.sort(key=lambda r: (not r["eligible_location"], -r["score"], r["company"], r["title"]))
    (folder / "cv_ranked.json").write_text(json.dumps(evaluated, ensure_ascii=False, indent=2), encoding="utf-8")
    with (folder / "cv_ranked.csv").open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(evaluated)
    info = {"total_official": len(official), "eligible_location_count": sum(x["eligible_location"] for x in evaluated),
            "top_eligible": sum(x["eligible_location"] and x["score"] >= 60 for x in evaluated),
            "note": "Score is a heuristic, not proof of qualification or open applications. Unverified Kariyer.net URLs excluded."}
    (folder / "cv_ranked_report.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(info, ensure_ascii=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("output/kariyernet"))
    main(parser.parse_args().output)
