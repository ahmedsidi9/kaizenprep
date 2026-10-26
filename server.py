"""KaizenPrep server: a local LeetCode-style practice platform. Standard library only.

    python3 server.py            # http://127.0.0.1:8000
    python3 server.py 9000       # custom port
"""
from __future__ import annotations

import json
import os
import random
import sys
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bank  # noqa: E402
import progress  # noqa: E402
import tracks  # noqa: E402
import patterns  # noqa: E402
import apple_mle  # noqa: E402
from judge import run_code  # noqa: E402

PROBLEMS = bank.load_all()
BY_ID = {p["id"]: p for p in PROBLEMS}
STATIC = os.path.join(HERE, "static")


def summary(p: dict, prog: dict) -> dict:
    e = prog.get(p["id"], {})
    return {
        "id": p["id"], "number": p["number"], "title": p["title"], "difficulty": p["difficulty"],
        "pattern": p["pattern"], "tags": p["tags"], "companies": p["companies"],
        "status": e.get("status"), "starred": e.get("starred", False), "next_review": e.get("next_review"),
        "attempts": e.get("attempts", 0),
    }


def problem_payload(p: dict) -> dict:
    visible = p["tests"][: max(2, min(3, len(p["examples"])))]
    e = progress.entry(p["id"])
    idx = p["number"] - 1
    prev_p = PROBLEMS[idx - 1] if idx > 0 else None
    next_p = PROBLEMS[idx + 1] if idx + 1 < len(PROBLEMS) else None
    return {
        "id": p["id"], "number": p["number"], "title": p["title"], "difficulty": p["difficulty"],
        "pattern": p["pattern"], "tags": p["tags"], "companies": p["companies"],
        "description": p["description"], "examples": p["examples"], "constraints": p["constraints"],
        "hints": p["hints"], "approach": p["approach"], "solution": p["solution"], "complexity": p["complexity"],
        "similar": [{"id": s, "title": BY_ID[s]["title"], "difficulty": BY_ID[s]["difficulty"]} for s in p.get("similar", []) if s in BY_ID],
        "followups": p.get("followups", []),
        "kind": p.get("kind", "function"),
        "starter": bank.starter_code(p),
        "draft": e.get("draft"),
        "note": e.get("note", ""),
        "starred": e.get("starred", False),
        "status": e.get("status"),
        "level": e.get("level", 0),
        "next_review": e.get("next_review"),
        "visible_tests": visible,
        "hidden_count": len(p["tests"]) - len(visible),
        "prev": {"id": prev_p["id"], "title": prev_p["title"]} if prev_p else None,
        "next": {"id": next_p["id"], "title": next_p["title"]} if next_p else None,
        "submissions": progress.submissions_for(p["id"])[:20],
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=STATIC, **kw)

    def log_message(self, fmt, *args):  # quieter log
        if "/api/" in (args[0] if args else ""):
            return
        super().log_message(fmt, *args)

    def _json(self, obj, status=HTTPStatus.OK):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n else b"{}"
        try:
            return json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return {}

    # ---- GET ----
    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        if path == "/":
            self.path = "/index.html"
            return super().do_GET()
        if not path.startswith("/api/"):
            return super().do_GET()
        prog = progress.get_all()["problems"]
        if path == "/api/problems":
            return self._json({"problems": [summary(p, prog) for p in PROBLEMS], "patterns": bank.PATTERN_ORDER})
        if path.startswith("/api/problem/"):
            pid = path.split("/", 3)[3].strip("/")
            if pid not in BY_ID:
                return self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)
            return self._json(problem_payload(BY_ID[pid]))
        if path == "/api/stats":
            return self._json({"stats": progress.stats(PROBLEMS), "reviews": progress.due_reviews(PROBLEMS)})
        if path == "/api/random":
            unsolved = [p for p in PROBLEMS if prog.get(p["id"], {}).get("status") != "solved"] or PROBLEMS
            return self._json({"id": random.choice(unsolved)["id"]})
        if path.startswith("/api/track/"):
            company = path.rsplit("/", 1)[1]
            if company not in tracks.COMPANY_GUIDES:
                return self._json({"error": "unknown company"}, HTTPStatus.NOT_FOUND)
            t = tracks.company_track(PROBLEMS, company)
            for key in ("must_do", "also", "all_by_frequency"):
                for item in t[key]:
                    item["status"] = prog.get(item["id"], {}).get("status")
            return self._json(t)
        if path == "/api/patterns":
            return self._json({"patterns": patterns.PATTERNS})
        if path == "/api/apple-mle":
            data = dict(apple_mle.APPLE_MLE)
            data["plan"] = [dict(w, problems=[{"id": i, "title": BY_ID[i]["title"], "difficulty": BY_ID[i]["difficulty"], "pattern": BY_ID[i]["pattern"], "status": prog.get(i, {}).get("status")} for i in w["problems"] if i in BY_ID]) for w in data["plan"]]
            data["coding"] = [summary(p, prog) for p in PROBLEMS if p["pattern"] == "ML Coding"]
            return self._json(data)
        if path == "/api/plan":
            return self._json(tracks.study_plan(PROBLEMS, prog))
        if path == "/api/mock":
            company = url.query.replace("company=", "") or "google"
            if company == "apple-mle":
                pool = [{"id": p["id"], "number": p["number"], "title": p["title"], "difficulty": p["difficulty"], "pattern": p["pattern"]} for p in PROBLEMS if p["pattern"] == "ML Coding"]
                pick = random.sample(pool, min(2, len(pool)))
                return self._json({"company": company, "problems": pick, "minutes": 45})
            t = tracks.company_track(PROBLEMS, company)
            pool = [i for i in t["must_do"] + t["also"] if i["difficulty"] != "Easy"] or t["all_by_frequency"]
            pick = random.sample(pool, min(2, len(pool)))
            return self._json({"company": company, "problems": pick, "minutes": 45})
        return self._json({"error": "unknown endpoint"}, HTTPStatus.NOT_FOUND)

    # ---- POST ----
    def do_POST(self):
        path = urlparse(self.path).path
        body = self._body()
        pid = body.get("id")
        if path in ("/api/run", "/api/submit"):
            p = BY_ID.get(pid)
            if not p:
                return self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)
            code = body.get("code", "")
            if path == "/api/run":
                tests = p["tests"][: max(2, min(3, len(p["examples"])))]
                custom = body.get("custom")
                if custom:
                    tests = tests + [{"input": c, "output": None} for c in custom]
                res = run_code(code, p, tests)
                progress.save_draft(pid, code)
                for c in res["cases"]:
                    if c["expected"] is None:
                        c["ok"] = c.get("error") is None
                        c["custom"] = True
                graded = [c for c in res["cases"] if not c.get("custom")]
                if res["cases"]:
                    if res["status"] in ("Wrong Answer", "Accepted"):
                        res["status"] = "Accepted" if all(c["ok"] for c in graded) else "Wrong Answer"
                    res["passed"] = sum(1 for c in graded if c["ok"]); res["total"] = len(graded)
                return self._json(res)
            res = run_code(code, p, p["tests"])
            entry = progress.record_submission(pid, code, res)
            res["entry"] = {k: entry.get(k) for k in ("status", "level", "next_review", "attempts")}
            return self._json(res)
        if path == "/api/draft":
            progress.save_draft(pid, body.get("code", ""))
            return self._json({"ok": True})
        if path == "/api/note":
            progress.save_note(pid, body.get("note", ""))
            return self._json({"ok": True})
        if path == "/api/star":
            return self._json({"starred": progress.toggle_star(pid)})
        if path == "/api/rate":
            return self._json(progress.rate_review(pid, body.get("rating", "hard")))
        return self._json({"error": "unknown endpoint"}, HTTPStatus.NOT_FOUND)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"KaizenPrep: {len(PROBLEMS)} problems loaded. Open http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
