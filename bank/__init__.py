"""Problem bank loader. Every module in this package exposes PROBLEMS: list[dict]."""
from __future__ import annotations

import importlib
import pkgutil

PATTERN_ORDER = [
    "Arrays & Hashing",
    "Two Pointers",
    "Sliding Window",
    "Stack",
    "Binary Search",
    "Linked List",
    "Trees",
    "Tries",
    "Heap / Priority Queue",
    "Backtracking",
    "Graphs",
    "Advanced Graphs",
    "1-D Dynamic Programming",
    "2-D Dynamic Programming",
    "Greedy",
    "Intervals",
    "Math & Bit Manipulation",
    "Design",
    "Strings",
    "ML Coding",
]

REQUIRED = {"id", "title", "difficulty", "pattern", "tags", "companies", "description", "examples",
            "constraints", "hints", "tests", "solution", "approach", "complexity"}


def load_all() -> list[dict]:
    problems: list[dict] = []
    for mod in pkgutil.iter_modules(__path__):
        if mod.name.startswith("_"):
            continue
        module = importlib.import_module(f"{__name__}.{mod.name}")
        for p in getattr(module, "PROBLEMS", []):
            p = dict(p)
            p["_module"] = mod.name
            problems.append(p)
    order = {name: i for i, name in enumerate(PATTERN_ORDER)}
    diff = {"Easy": 0, "Medium": 1, "Hard": 2}
    problems.sort(key=lambda p: (order.get(p["pattern"], 99), diff.get(p["difficulty"], 9), p["title"]))
    for i, p in enumerate(problems, 1):
        p["number"] = i
    return problems


def starter_code(p: dict) -> str:
    if p.get("kind") == "design":
        return p["starter"]
    sig = p["signature"]
    return f"class Solution:\n    {sig}\n        pass\n"
