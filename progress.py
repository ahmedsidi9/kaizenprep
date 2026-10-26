"""Progress store with a light spaced-repetition schedule. Persists to data/progress.json."""
from __future__ import annotations

import json
import os
import threading
from datetime import date, datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PATH = os.path.join(DATA_DIR, "progress.json")
INTERVALS = [1, 3, 7, 14, 30, 60]  # days until next review after the n-th clean solve

_lock = threading.Lock()


def _load() -> dict:
    if not os.path.exists(PATH):
        return {"problems": {}, "submissions": []}
    with open(PATH, encoding="utf-8") as fh:
        try:
            return json.load(fh)
        except json.JSONDecodeError:
            return {"problems": {}, "submissions": []}


def _save(data: dict) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    tmp = PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1)
    os.replace(tmp, PATH)


def get_all() -> dict:
    with _lock:
        return _load()


def entry(pid: str) -> dict:
    with _lock:
        return _load()["problems"].get(pid, {})


def save_draft(pid: str, code: str) -> None:
    with _lock:
        data = _load()
        p = data["problems"].setdefault(pid, {})
        p["draft"] = code
        p["draft_at"] = datetime.now().isoformat(timespec="seconds")
        _save(data)


def save_note(pid: str, note: str) -> None:
    with _lock:
        data = _load()
        p = data["problems"].setdefault(pid, {})
        p["note"] = note
        _save(data)


def toggle_star(pid: str) -> bool:
    with _lock:
        data = _load()
        p = data["problems"].setdefault(pid, {})
        p["starred"] = not p.get("starred", False)
        _save(data)
        return p["starred"]


def record_submission(pid: str, code: str, result: dict) -> dict:
    """Record a submit. Accepted solves move the review schedule forward; failures reset it."""
    with _lock:
        data = _load()
        p = data["problems"].setdefault(pid, {})
        today = date.today()
        accepted = result["status"] == "Accepted"
        p["attempts"] = p.get("attempts", 0) + 1
        p["last_status"] = result["status"]
        p["last_at"] = datetime.now().isoformat(timespec="seconds")
        if accepted:
            level = p.get("level", 0)
            # if the review was overdue by a lot, or it took several attempts today, do not advance as far
            interval = INTERVALS[min(level, len(INTERVALS) - 1)]
            p["level"] = level + 1
            p["status"] = "solved"
            p["solved_at"] = p.get("solved_at") or today.isoformat()
            p["next_review"] = (today + timedelta(days=interval)).isoformat()
            p["accepted_code"] = code
        else:
            p["status"] = p.get("status") if p.get("status") == "solved" else "attempted"
            if p.get("status") == "solved":
                p["level"] = max(0, p.get("level", 1) - 1)
                p["next_review"] = (today + timedelta(days=1)).isoformat()
        p["draft"] = code
        data["submissions"].append({
            "id": pid, "status": result["status"], "passed": result["passed"], "total": result["total"],
            "ms": result.get("ms"), "at": p["last_at"], "code": code,
        })
        data["submissions"] = data["submissions"][-2000:]
        _save(data)
        return p


def rate_review(pid: str, rating: str) -> dict:
    """After a review solve, the user can say how it felt: 'again' resets, 'hard' keeps, 'easy' jumps."""
    with _lock:
        data = _load()
        p = data["problems"].setdefault(pid, {})
        today = date.today()
        level = p.get("level", 0)
        if rating == "again":
            level = 0
        elif rating == "hard":
            level = max(0, level - 1)
        elif rating == "easy":
            level = level + 1
        interval = INTERVALS[min(level, len(INTERVALS) - 1)]
        p["level"] = level
        p["next_review"] = (today + timedelta(days=interval)).isoformat()
        _save(data)
        return p


def due_reviews(problems: list[dict]) -> list[dict]:
    data = get_all()["problems"]
    today = date.today().isoformat()
    out = []
    for p in problems:
        e = data.get(p["id"])
        if e and e.get("status") == "solved" and e.get("next_review", "9999") <= today:
            out.append({"id": p["id"], "title": p["title"], "difficulty": p["difficulty"], "pattern": p["pattern"], "due": e["next_review"]})
    out.sort(key=lambda x: x["due"])
    return out


def submissions_for(pid: str) -> list[dict]:
    return [s for s in get_all()["submissions"] if s["id"] == pid][::-1]


def stats(problems: list[dict]) -> dict:
    data = get_all()["problems"]
    by_diff = {"Easy": [0, 0], "Medium": [0, 0], "Hard": [0, 0]}
    by_pattern: dict[str, list[int]] = {}
    solved = attempted = 0
    for p in problems:
        e = data.get(p["id"], {})
        by_diff[p["difficulty"]][1] += 1
        by_pattern.setdefault(p["pattern"], [0, 0])[1] += 1
        if e.get("status") == "solved":
            solved += 1
            by_diff[p["difficulty"]][0] += 1
            by_pattern[p["pattern"]][0] += 1
        elif e.get("status") == "attempted":
            attempted += 1
    # streak: consecutive days with at least one accepted submission
    days = {s["at"][:10] for s in get_all()["submissions"] if s["status"] == "Accepted"}
    streak = 0
    d = date.today()
    if d.isoformat() not in days:
        d -= timedelta(days=1)
    while d.isoformat() in days:
        streak += 1
        d -= timedelta(days=1)
    return {"solved": solved, "attempted": attempted, "total": len(problems), "by_difficulty": by_diff,
            "by_pattern": by_pattern, "streak": streak, "active_days": sorted(days)[-120:]}
