import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from layout_engine import ALPHABET,BASELINES,F29_START,validate_rows,parse_stats,arrays_for_layout,run


def test_corpus_wide_sampling():
    data=parse_stats(ROOT/'data/corpus_stats.json')
    assert data['train']['words']>=10_000
    assert data['test']['words']>=2_000
    assert data['train']['bi_counts'].shape==(29,29)
    assert data['test']['bi_counts'].sum()>0
    # Per-word pair conservation for strings of >=2 characters.
    assert data['train']['uni_counts'].sum() > data['train']['bi_counts'].sum()


def test_layout_all_letters_unique():
    for layout in BASELINES.values(): validate_rows(layout,strict_29=False)
    validate_rows(F29_START)
    found=json.loads((ROOT/'report/results.json').read_text('utf-8'))
    for name,item in found['layout'].items():
        validate_rows(item['rows'],strict_29=name not in BASELINES)
        assert 0<=item['holdout']['alternation_pct']<=100
        assert abs(item['holdout']['left_pct']+item['holdout']['right_pct']-100)<.002


def test_deterministic_search(tmp_path):
    a=run(ROOT/'data/corpus_stats.json',tmp_path/'a.json',iterations=35,restarts=1)
    b=run(ROOT/'data/corpus_stats.json',tmp_path/'b.json',iterations=35,restarts=1)
    assert a==b


def test_held_out_improvement_is_model_only():
    data=json.loads((ROOT/'report/results.json').read_text('utf-8'))
    q=data['layout']['Q32']['holdout']
    v=data['layout']['V29']['holdout']
    s=data['layout']['S29']['holdout']
    assert v['motion_index']<q['motion_index']
    assert s['glide_distance']<q['glide_distance']
    assert 'not observed' in data['metadata']['limitations']


def test_key_area_consistent():
    for name,rows in BASELINES.items():
        reach,width,fit,switch,dist=arrays_for_layout(rows)
        assert len(reach)==len(ALPHABET)
        assert (width>0).all()
        assert (fit>=0).all()
        assert (dist==dist.T).all()
