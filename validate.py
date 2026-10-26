"""Validate the problem bank: schema checks and reference solutions must pass all tests.

Usage:
    python3 validate.py              # whole bank
    python3 validate.py arrays       # only bank/arrays.py
"""
from __future__ import annotations

import importlib
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bank  # noqa: E402
from judge import run_code  # noqa: E402

COMPANIES = {"google", "apple", "meta", "amazon", "microsoft"}


def check_schema(p: dict) -> list[str]:
    errs = []
    missing = bank.REQUIRED - set(p)
    if missing:
        errs.append(f"missing fields: {sorted(missing)}")
    if p.get("difficulty") not in ("Easy", "Medium", "Hard"):
        errs.append("difficulty must be Easy/Medium/Hard")
    if p.get("pattern") not in bank.PATTERN_ORDER:
        errs.append(f"unknown pattern {p.get('pattern')!r}")
    if p.get("kind") == "design":
        for f in ("class_name", "starter"):
            if f not in p:
                errs.append(f"design problem missing {f}")
    else:
        for f in ("function", "signature"):
            if f not in p:
                errs.append(f"missing {f}")
    if not isinstance(p.get("tests"), list) or len(p.get("tests", [])) < 4:
        errs.append("need at least 4 tests")
    for t in p.get("tests", []):
        if "input" not in t or "output" not in t:
            errs.append("each test needs input and output")
            break
    if not p.get("examples"):
        errs.append("need at least one example")
    comp = p.get("companies", {})
    if not isinstance(comp, dict) or not set(comp) <= COMPANIES:
        errs.append(f"companies must be a dict with keys from {sorted(COMPANIES)}")
    if len(p.get("hints", [])) < 2:
        errs.append("need at least 2 hints")
    if "time" not in p.get("complexity", {}) or "space" not in p.get("complexity", {}):
        errs.append("complexity needs time and space")
    return errs


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        modules = [importlib.import_module(f"bank.{argv[1]}")]
        problems = []
        for m in modules:
            for p in m.PROBLEMS:
                p = dict(p); p["_module"] = argv[1]; problems.append(p)
    else:
        problems = bank.load_all()
    ids = {}
    failures = 0
    for p in problems:
        pid = p.get("id", "?")
        if pid in ids:
            print(f"[DUP] {pid} in {p['_module']} and {ids[pid]}")
            failures += 1
        ids[pid] = p["_module"]
        errs = check_schema(p)
        if errs:
            failures += 1
            print(f"[SCHEMA] {p['_module']}/{pid}: " + "; ".join(errs))
            continue
        res = run_code(p["solution"], p, p["tests"])
        if res["status"] != "Accepted":
            failures += 1
            print(f"[FAIL] {p['_module']}/{pid}: {res['status']} ({res['passed']}/{res['total']})")
            for c in res["cases"]:
                if not c["ok"]:
                    print(f"    input={c['input']}\n    expected={c['expected']}\n    got={c.get('output')} {c.get('error') or ''}")
                    break
            if res.get("stderr"):
                print("    stderr:", res["stderr"][-500:])
        else:
            print(f"[ok]   {p['_module']}/{pid} ({res['total']} tests, {res['ms']} ms)")
    print(f"\n{len(problems)} problems, {failures} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
