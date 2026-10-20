"""Evidence-aware seven-stage vacancy triage. Unknown requirements never pass as verified."""
import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

DIMENSIONS = {"profession":25,"requirements":25,"skills":20,"career":15,"location":10,"employer_evidence":5}
PRIMARY = ("kahramanmaras","gaziantep","osmaniye","adana","kayseri","malatya")
SECONDARY = ("mersin","ankara","adiyaman","hatay")
ROLES = ("makine muhendisi","mechanical engineer","uretim muhendisi","production engineer",
         "imalat muhendisi","manufacturing engineer","proses muhendisi","process engineer",
         "kalite muhendisi","quality engineer","mekanik tasarim","mechanical design",
         "mechanical maintenance","mekanik bakim","cad/cam","ar-ge","ur-ge")
SKILLS = ("solidworks","autocad","moldflow","technical drawing","teknik resim",
          "cnc","talaşlı","welding","kaynak","ndt","kalite kontrol","quality control","matlab")
FIELDS = ("source","source_id","url","company","title","location","status","score",
          "profession","requirements","skills","career","location_score","employer_evidence",
          "requirements_state","open_state","reasons","verification")

def normalize(text):
    s=unicodedata.normalize("NFKD",str(text or "").casefold()).replace("ı","i")
    return "".join(c for c in s if not unicodedata.combining(c))

def evaluate(job):
    title=normalize(job.get("title"))
    location=normalize(job.get("location"))
    description=normalize(job.get("description"))
    reasons=[]
    if "istanbul" in location:
        return _record(job,"excluded_location",0,[0]*6,"not_checked","not_verified",["İstanbul hariç tutuldu"])
    profession = 25 if any(x in title for x in ROLES) else (8 if ("engineer" in title or "muhendis" in title) else 0)
    if profession==0:
        reasons.append("Makine mühendisliği hedefiyle meslek uyumu kanıtlanmadı")
    elif profession==8:
        reasons.append("Mühendislik unvanı var ancak mekanik uzmanlık belirsiz")
    else:
        reasons.append("Hedef mühendislik rolüyle unvan eşleşmesi")
    location_points = 10 if any(c in location for c in PRIMARY) else 6 if any(c in location for c in SECONDARY) else 0
    if location_points==0:
        reasons.append("Konum hedef şehirler arasında doğrulanmadı")
    years=[int(n) for n in re.findall(r"(?:minimum|at least|en az)\s*(\d+)\s*(?:years?|yil)",description)]
    years.extend(int(n) for n in re.findall(r"(\d+)\s*\+\s*(?:years?|yil)",description))
    new_grad=bool(re.search(r"new grad|entry.level|yeni mezun|deneyimsiz|0\s*[-–]\s*2\s*(?:years?|yil)",description))
    senior=bool(re.search(r"senior|lead|manager|director|kidemli|yonetici|sef",title))
    english=bool(re.search(r"advanced english|fluent english|c1 english|ileri seviye ingilizce",description))
    wrong_degree=bool(re.search(r"only (electrical|chemical|civil) engineer|yalnizca (elektrik|kimya|insaat) muhendis",description))
    degree_uncertain=bool(re.search(r"(?:degree in|bachelor.s degree in|mezunu)\s*(?:industrial|electrical|chemical|civil|endustri|elektrik|kimya|insaat)",description))
    if wrong_degree:
        requirements=0
        reqstate="incompatible_degree"
        reasons.append("Zorunlu farklı mühendislik diploması")
    elif degree_uncertain:
        requirements=8
        reqstate="degree_requires_review"
        reasons.append("İstenen mühendislik bölümü makine diplomasıyla ayrıca karşılaştırılmalı")
    elif years and min(years)>2:
        requirements=2
        reqstate="experience_gap"
        reasons.append(f"En az {min(years)} yıl deneyim şartı")
    elif senior:
        requirements=4
        reqstate="senior_role"
        reasons.append("Kıdemli/yönetici unvanı")
    elif new_grad:
        requirements=25
        reqstate="new_graduate_explicit"
        reasons.append("Yeni mezun veya 0–2 yıl açıkça kabul ediliyor")
    else:
        requirements=12
        reqstate="unknown"
        reasons.append("Zorunlu deneyim ve bölüm şartı ayrıca doğrulanmalı")
    if english:
        requirements=max(0,requirements-8)
        reasons.append("İleri İngilizce şartı CV A2–B1 ile farklı")
    matched=[x for x in SKILLS if normalize(x) in description]
    skills=min(20, len(matched)*5)
    if matched: reasons.append("CV teknik eşleşmeleri: "+", ".join(matched[:5]))
    else: reasons.append("İlan metninden teknik beceri eşleşmesi kanıtlanamadı")
    career = 10 if profession==25 else 3
    if "training" in description or "egitim" in description or "mentorluk" in description: career=min(15,career+5)
    reasons.append("Kariyer puanı ilanın görevlerine dayanır, gerçek eğitim koşulları ayrıca araştırılmalı")
    employer=0
    reasons.append("Bağımsız işveren kanıtları henüz eklenmedi")
    dims=[profession,requirements,skills,career,location_points,employer]
    score=sum(dims)
    status="needs_detail_verification"
    if profession==0: status="low_profession_match"
    if location_points==0: status="location_unverified"
    if wrong_degree or (years and min(years)>2): status="requirement_gap"
    return _record(job,status,score,dims,reqstate,"not_verified",reasons)

def _record(job,status,score,dims,reqstate,open_state,reasons):
    return dict(zip(FIELDS,[
        job.get("source",""),str(job.get("source_id","")),job.get("url",""),
        job.get("company",""),job.get("title",""),job.get("location",""),
        status,score,*dims,reqstate,open_state,"; ".join(reasons),job.get("verification","")
    ]))

def run(folder, evidence_path=Path("tools/kariyernet/employer_evidence.json")):
    source=folder/"new_official_candidates.json"
    entries=json.loads(source.read_text(encoding="utf-8"))
    evidence = json.loads(evidence_path.read_text(encoding="utf-8")) if evidence_path.exists() else {"employers":[]}
    registry={(x["source"],str(x["employer_id"])):x for x in evidence.get("employers",[])
              if x.get("source") and x.get("employer_id")}
    ranked=[]
    for entry in entries:
        record=evaluate(entry)
        parsed=urlparse(entry.get("url", ""))
        board_id=parsed.path.strip("/").split("/")[0] if parsed.hostname=="jobs.lever.co" else ""
        key=(entry.get("source"),board_id)
        proof=registry.get(key)
        if proof:
            independent=[x for x in proof.get("sources",[]) if x.get("independent") is True
                         and str(x.get("url","")).startswith("https://") and x.get("fact")]
            record["employer_evidence"]=min(5,len(independent)*2)
            record["score"]=min(100,record["score"]+record["employer_evidence"])
            record["reasons"]+="; Bağımsız şirket kanıt sayısı: "+str(len(independent))
        ranked.append(record)
    ranked.sort(key=lambda x:-x["score"])
    (folder/"smart_ranked.json").write_text(json.dumps(ranked,ensure_ascii=False,indent=2),encoding="utf-8")
    with (folder/"smart_ranked.csv").open("w",newline="",encoding="utf-8") as out:
        writer=csv.DictWriter(out,fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(ranked)
    report={"candidates":len(ranked),"target_city_candidates":sum(x["location_score"]>0 for x in ranked),
            "explicit_new_graduate":sum(x["requirements_state"]=="new_graduate_explicit" for x in ranked),
            "verified_open":0,"source_note":"URL discovery and public API listing do not establish current application availability."}
    (folder/"smart_ranked_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,default=Path("output/kariyernet"))
    run(p.parse_args().output)
