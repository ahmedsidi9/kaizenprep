"""Export the bank, patterns and track data as JSON for the static (in-browser) build."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank, patterns, tracks, judge, apple_mle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static-build", "data")
os.makedirs(OUT, exist_ok=True)
problems = bank.load_all()
for p in problems:
    p["starter"] = bank.starter_code(p)
    p.pop("_module", None)
os.makedirs(os.path.join(OUT, "problems"), exist_ok=True)
SUMMARY = ("id", "number", "title", "difficulty", "pattern", "tags", "companies", "similar")
index = []
for p in problems:
    index.append({k: p.get(k, []) for k in SUMMARY})
    json.dump(p, open(os.path.join(OUT, "problems", p["id"] + ".json"), "w"), separators=(",", ":"))
json.dump({"problems": index, "patterns": bank.PATTERN_ORDER}, open(os.path.join(OUT, "index.json"), "w"), separators=(",", ":"))
json.dump(apple_mle.APPLE_MLE, open(os.path.join(OUT, "apple-mle.json"), "w"), separators=(",", ":"))
json.dump({"patterns": patterns.PATTERNS}, open(os.path.join(OUT, "patterns.json"), "w"), separators=(",", ":"))
json.dump({"guides": tracks.COMPANY_GUIDES, "weeks": tracks.WEEKS, "intervals": [1, 3, 7, 14, 30, 60]},
          open(os.path.join(OUT, "tracks.json"), "w"), separators=(",", ":"))
harness = judge.PRELUDE + '''

def _run_payload(payload_json):
    payload = json.loads(payload_json)
    spec, tests = payload["spec"], payload["tests"]
    out = _run_design(spec, tests) if spec.get("kind") == "design" else _run_function(spec, tests)
    return json.dumps(out)
'''
open(os.path.join(OUT, "harness.py"), "w").write(harness)
biggest = max(os.path.getsize(os.path.join(OUT, "problems", f)) for f in os.listdir(os.path.join(OUT, "problems")))
print(len(problems), "problems;", os.path.getsize(os.path.join(OUT, "index.json")) // 1024, "KB index; biggest problem file", biggest // 1024, "KB")
