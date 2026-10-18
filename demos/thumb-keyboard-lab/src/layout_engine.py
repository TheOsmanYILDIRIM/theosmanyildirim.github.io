"""Reproducible, assumption-driven Turkish touchscreen keyboard layout search.

Scores are dimensionless proxy costs, never real WPM or clinical comfort claims.
Digits contain frequency-aggregated Turkish OpenSubtitles wordforms.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np

ALPHABET = "abcçdefgğhıijklmnoöprsştuüvyz"
BASELINES = {
    "Q32": ["qwertyuıopğü", "asdfghjklşi", "zxcvbnmöç"],
    "F32": ["fgğıodrnhpqw", "uieaütkmlyş", "xjövcçzsb"],
}
F29_START = ["fgğıodrnhp", "uieaütkmly", "şjövcçzsb"]
TR_COUNTS = (10, 10, 9)


def validate_rows(rows: list[str], *, strict_29: bool = True) -> None:
    chars = "".join(rows)
    expected = set(ALPHABET) if strict_29 else (set(ALPHABET) | set("qwx"))
    if len(rows) != 3 or len(chars) != len(set(chars)) or set(chars) != expected:
        raise ValueError(f"Invalid layout: {rows}; missing={expected-set(chars)}, unexpected={set(chars)-expected}")


def make_positions(row_sizes: tuple[int, ...] | list[int]) -> np.ndarray:
    return np.array([[ (column+.5)/n, (r+.5)/3, 1/n, float(n)]
                     for r,n in enumerate(row_sizes) for column in range(n)], dtype=np.float64)


def scan_layout(rows: list[str]) -> np.ndarray:
    mapping = {letter: index for index, letter in enumerate("".join(rows))}
    return np.array([mapping[c] for c in ALPHABET], dtype=np.int32)


def parse_stats(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data["alphabet"] != ALPHABET:
        raise ValueError("Wrong alphabet or corpus format")
    count = len(ALPHABET)
    for partition in ("train", "test"):
        item = data[partition]
        uni = [int(k, 36) for k in item["uni"].split(".")]
        bi = [int(k, 36) for k in item["bi"].split(".")]
        if len(uni) != count or len(bi) != count*count or any(x<0 for x in uni+bi):
            raise ValueError(f"Malformed {partition} aggregate")
        item["uni_counts"] = np.array(uni, dtype=np.float64)
        item["bi_counts"] = np.array(bi, dtype=np.float64).reshape(count,count)
    return data


def arrays_for_layout(rows: list[str]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    slots = make_positions(tuple(map(len, rows)))
    p = slots[scan_layout(rows)]
    x,y,w,n = p.T
    left = x < .5
    handed = left.astype(np.int8)
    ideal_x = np.where(left,.22,.78)
    # Hypothetical thumb-zone priors; personalized measurements replace this prior.
    reach = np.sqrt(((x-ideal_x)/.48)**2 + ((y-.72)/.68)**2)
    reach += np.where((y>.80) & ((x<.15)|(x>.85)), .16, 0)
    width_penalty = (n/10.0)**1.7
    distance = np.sqrt((x[:,None]-x[None,:])**2+(y[:,None]-y[None,:])**2)
    target_width = np.minimum(w[:,None],w[None,:])
    fitts = np.log2(1.0+distance/target_width)
    switches = handed[:,None]!=handed[None,:]
    return reach, width_penalty, fitts, switches, distance


def evaluate(rows: list[str], stats: dict, partition: str, *, switch_scale: float = .34) -> dict:
    validate_rows(rows,strict_29=len("".join(rows))==29)
    uni = stats[partition]["uni_counts"]
    bi = stats[partition]["bi_counts"]
    reach,width_pen,fitts,switches,distance = arrays_for_layout(rows)
    total = float(uni.sum())
    pairs = float(bi.sum())
    if total<=0 or pairs<=0: raise ValueError("Empty sample")
    motion = float((bi * fitts * np.where(switches,switch_scale,1)).sum()/pairs)
    comfort = float((uni*reach).sum()/total)
    precision = float((uni*width_pen).sum()/total)
    glide = float((bi*distance).sum()/pairs)
    alternation = float((bi*switches).sum()/pairs)
    left_positions = (scan_layout(rows) < len(rows[0])) # replaced with actual handed assignment
    positions = make_positions(list(map(len,rows)))[scan_layout(rows)]
    left_share = float(uni[positions[:,0]<.5].sum()/total)
    return {"motion_index":round(motion,6),"reach_index":round(comfort,6),
            "width_index":round(precision,6),"glide_distance":round(glide,6),
            "alternation_pct":round(100*alternation,3),"left_pct":round(100*left_share,3),
            "right_pct":round(100*(1-left_share),3),"keys":len("".join(rows)),
            "vowel_left_pct":round(100*sum(1 for c in "aeıioöuü" if positions[ALPHABET.index(c),0]<.5)/8,1)}


def proxy_score(metrics: dict, goal: str) -> float:
    if goal == "balance":return .64*metrics["motion_index"]+.27*metrics["reach_index"]+.09*metrics["width_index"]
    if goal == "comfort":return .34*metrics["motion_index"]+.55*metrics["reach_index"]+.11*metrics["width_index"]
    if goal == "swipe":return .84*metrics["glide_distance"]+.13*metrics["reach_index"]+.03*metrics["width_index"]
    raise ValueError(goal)


def score_layout(rows: list[str], stats: dict, partition: str, goal: str, *, switch_scale: float=.34) -> float:
    # Unrounded math to ensure search uses consistent comparison.
    uni,bi=stats[partition]["uni_counts"],stats[partition]["bi_counts"]
    reach,width_pen,fitts,switches,distance=arrays_for_layout(rows)
    mot=np.sum(bi*fitts*np.where(switches,switch_scale,1))/bi.sum()
    com=np.sum(uni*reach)/uni.sum()
    wid=np.sum(uni*width_pen)/uni.sum()
    gli=np.sum(bi*distance)/bi.sum()
    return float((.64*mot+.27*com+.09*wid) if goal=="balance" else
                 (.34*mot+.55*com+.11*wid) if goal=="comfort" else
                 (.84*gli+.13*com+.03*wid))


def optimize(stats: dict, goal: str, seed: int, iterations: int, restarts: int) -> tuple[list[str],float]:
    # Anneal on 29-key geometry; swap letters, never duplicate or drop a letter.
    rng=random.Random(seed)
    template=list(map(list,F29_START))
    def asrows(flat:list[str])->list[str]:
        return ["".join(flat[:10]),"".join(flat[10:20]),"".join(flat[20:])]
    f=list("".join(F29_START))
    best_rows=asrows(f); best=score_layout(best_rows,stats,"train",goal)
    for run in range(restarts):
        current=f.copy()
        if run: rng.shuffle(current)
        current_rows=asrows(current)
        cur=score_layout(current_rows,stats,"train",goal)
        for i in range(iterations):
            a,b=rng.sample(range(29),2)
            current[a],current[b]=current[b],current[a]
            new=score_layout(asrows(current),stats,"train",goal)
            t=max(0.00035,(.16*(.00035/.16)**(i/max(1,iterations-1))))
            if new<cur or rng.random()<math.exp(min(0,(cur-new)/t)):
                cur=new
                if cur<best:
                    best=cur;best_rows=asrows(current)
            else:current[a],current[b]=current[b],current[a]
    validate_rows(best_rows)
    return best_rows, best


def run(stats_path:Path, output:Path, *, iterations:int=3500,restarts:int=3) -> dict:
    stats=parse_stats(stats_path)
    data={"metadata":{"corpus":stats["source"],"source_blob_sha":stats["source_blob_sha"],
            "alphabet":ALPHABET,"train_words":stats["train"]["words"],
            "test_words":stats["test"]["words"],"weighting":stats["weighting"],
            "limitations":"Model-only scores: not observed typing times, fatigue, or WPM. Word-internal transitions; no space, punctuation, swipes, learning, autocorrect."},
          "layout":{},"assumptions":{"switch_scale":.34,"thumb_priors":"left (.22,.72), right (.78,.72) normalized; hypothetical","geometry":"rows of 12/11/9 for original Q/F, 10/10/9 for alternatives"}}
    for id,rows in BASELINES.items():
        validate_rows(rows,strict_29=False)
        data["layout"][id]={"title": id=="Q32" and "Türkçe Q (32 tuş)" or "Türkçe F (32 tuş)","rows":rows,"optimized_for":"baseline"}
    label={"balance":("V29","Dengeli Çift Başparmak"),"comfort":("K29","Erişim Öncelikli"),"swipe":("S29","Kaydırma Öncelikli")}
    for j,goal in enumerate(("balance","comfort","swipe")):
        rows,best=optimize(stats,goal,20261018+j*1000,iterations,restarts)
        id,title=label[goal]; data["layout"][id]={"title":title,"rows":rows,"optimized_for":goal,"train_objective":round(best,6)}
    for id,item in data["layout"].items():
        rows=item["rows"]
        item["train"]=evaluate(rows,stats,"train")
        item["holdout"]=evaluate(rows,stats,"test")
        item["sensitivity"]={str(s):evaluate(rows,stats,"test",switch_scale=s)["motion_index"] for s in (.25,.34,.65,1.)}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return data


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--stats",default="data/corpus_stats.json")
    parser.add_argument("--out",default="report/results.json")
    parser.add_argument("--iterations",type=int,default=3500)
    parser.add_argument("--restarts",type=int,default=3)
    args=parser.parse_args()
    out=run(Path(args.stats),Path(args.out),iterations=args.iterations,restarts=args.restarts)
    for id,v in out["layout"].items():
        print(id," ".join(v["rows"]),"motion",v["holdout"]["motion_index"],
              "reach",v["holdout"]["reach_index"],"glide",v["holdout"]["glide_distance"])

if __name__=="__main__":main()
