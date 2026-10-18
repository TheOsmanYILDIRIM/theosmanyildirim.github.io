"""Dependency-free deterministic ES Module -> single-file deployable HTML bundler."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]

def build():
    html=(ROOT/'web/index.template.html').read_text('utf-8')
    css=(ROOT/'web/app.css').read_text('utf-8')
    js=(ROOT/'web/app.js').read_text('utf-8')
    model=json.loads((ROOT/'report/results.json').read_text('utf-8'))
    model["corpus_aggregates"]=json.loads((ROOT/'data/corpus_stats.json').read_text('utf-8'))
    source=html.replace('/*__APP_CSS__*/',css)
    source=source.replace('/*__EXPERIMENT_DATA__*/',json.dumps(model,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
    source=source.replace('/*__APP_JS__*/',js.replace('</script','<\\/script'))
    output=ROOT/'index.html'
    output.write_text(source,'utf-8')
    return output
if __name__ == '__main__':
    out=build();print(out,out.stat().st_size,'bytes')
