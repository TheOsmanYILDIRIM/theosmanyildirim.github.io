import sys
import json
import csv
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from smart_rank import run

class EmployerEvidenceTests(unittest.TestCase):
    def test_only_independent_exact_board(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            jobs=[
                {"source":"lever","source_id":"1","url":"https://jobs.lever.co/getmidas/1","company":"Midas","title":"Mechanical Engineer","location":"Ankara","description":""},
                {"source":"lever","source_id":"2","url":"https://jobs.lever.co/notmidas/2","company":"Midas","title":"Mechanical Engineer","location":"Ankara","description":""}
            ]
            (folder/"new_official_candidates.json").write_text(json.dumps(jobs))
            evidence={"employers":[{"source":"lever","employer_id":"getmidas","sources":[
                {"url":"https://example.org/report","independent":True,"fact":"Research report"},
                {"url":"https://example.org/self","independent":False,"fact":"Self claim"}]}]}
            path=folder/"evidence.json"
            path.write_text(json.dumps(evidence))
            run(folder,path)
            result=json.loads((folder/"smart_ranked.json").read_text())
            by_id={x["source_id"]:x for x in result}
            self.assertEqual(by_id["1"]["employer_evidence"],2)
            self.assertEqual(by_id["2"]["employer_evidence"],0)
            with (folder/"smart_ranked.csv").open() as f:
                self.assertEqual(len(list(csv.DictReader(f))),2)
if __name__=="__main__":
    unittest.main()
