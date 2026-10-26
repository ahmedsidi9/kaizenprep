"""Company tracks and the 8-week study plan.

Company frequency scores come from the bank's `companies` field, which is a judgement
based on public interview reports (Glassdoor, Blind, interview-prep communities), not an
official or scraped tag. Treat the ordering as a strong prior, not a guarantee.
"""
from __future__ import annotations

from bank import PATTERN_ORDER

COMPANY_GUIDES = {
    "google": {
        "name": "Google",
        "summary": (
            "Google interviews are algorithm-heavy and ambiguity-heavy. Expect 45-minute rounds with one "
            "medium-to-hard problem, often with a twist or a follow-up that changes the constraints. "
            "Interviewers grade on four axes: coding, algorithms and data structures, communication, and "
            "problem navigation (how you handle hints, ambiguity, and scope)."
        ),
        "process": [
            "Recruiter screen, then one 45-minute phone/virtual coding screen (sometimes two).",
            "Onsite loop: typically 4 coding rounds plus 1 'Googleyness and Leadership' behavioural round. L5+ adds a system design round.",
            "Each round is written up independently; a hiring committee reads the packet. Consistency across rounds matters more than one brilliant round.",
            "You code in a shared Google Doc or a bare editor with no autocomplete or execution. Practice writing syntactically correct code without running it.",
        ],
        "focus": [
            "Graphs and grids (BFS/DFS, shortest paths, topological sort) appear more often than at any other large company.",
            "Dynamic programming, especially 2-D and interval DP, and problems where the naive recursion must be memoised and then space-optimised.",
            "Clarifying questions before coding. The prompt is often deliberately vague: ask about input size, duplicates, memory limits, streaming vs batch.",
            "Follow-ups: after you solve it, expect 'what if the input does not fit in memory', 'what if updates arrive online', or 'now do it in O(1) space'.",
            "Correctness over speed. Walk through your code on an example before saying you are done; interviewers note whether you find your own bugs.",
        ],
        "tips": [
            "Narrate your thinking continuously. Silence for more than 20 seconds reads as being stuck.",
            "State the brute force and its complexity in one sentence, then move on to the real approach.",
            "Write helper functions with clear names rather than one long block; graders read the code afterwards.",
            "For the behavioural round, prepare 6 STAR stories covering conflict, ambiguity, failure, leadership without authority, and impact.",
        ],
        "must_do": [
            "number-of-islands", "course-schedule", "word-ladder", "clone-graph", "pacific-atlantic-water-flow",
            "network-delay-time", "alien-dictionary", "longest-increasing-path-in-a-matrix", "minimum-window-substring",
            "merge-intervals", "meeting-rooms-ii", "trapping-rain-water", "median-of-two-sorted-arrays",
            "longest-increasing-subsequence", "edit-distance", "burst-balloons", "regular-expression-matching",
            "word-search-ii", "find-median-from-data-stream", "lru-cache", "design-hit-counter", "snapshot-array",
            "text-justification", "basic-calculator-ii", "n-queens", "kth-smallest-element-in-bst",
            "binary-tree-maximum-path-sum", "minimum-interval-to-include-each-query",
            "split-array-largest-sum", "swim-in-rising-water", "accounts-merge", "cheapest-flights-within-k-stops",
        ],
    },
    "apple": {
        "name": "Apple",
        "summary": (
            "Apple interviews are team-specific and practical. The loop is organised by the hiring team, so "
            "the mix depends on the role, but coding rounds lean toward clean implementation of data structures, "
            "string and array manipulation, linked lists, trees, and object-oriented design, with a strong emphasis "
            "on edge cases, memory, and production-quality code rather than exotic algorithms."
        ),
        "process": [
            "Recruiter call, then a technical phone screen with a team engineer (one or two medium problems).",
            "Onsite: 4-6 rounds over a day, each with a different team member. Coding, a design round, a round about past projects, and often a lunch or 'fit' conversation with the hiring manager.",
            "Expect at least one round that goes deep on something from your resume. Be ready to explain decisions and trade-offs in a project you own.",
            "Teams often favour the language of their stack (Swift/Objective-C, C++, Python). Ask which language is expected and be fluent in its idioms and memory model.",
        ],
        "focus": [
            "Arrays and strings: in-place manipulation, parsing, compression, two-pointer techniques.",
            "Linked lists and trees: reversal, cycle detection, merging, traversal order, BST properties. Expect to write these from scratch with no bugs.",
            "Design-style problems: LRU cache, rate limiter / hit counter, iterator classes, a data structure with O(1) operations. Clean class design is scored.",
            "Concurrency and memory basics for systems-adjacent roles: what happens with retain cycles, how you would make a cache thread safe.",
            "Practical system questions: design a photo library sync, a notification scheduler, an offline-first cache.",
        ],
        "tips": [
            "Write production-quality code: handle null/empty input, name things well, avoid clever one-liners.",
            "Test your code out loud with an edge case before declaring done. Apple interviewers care about this more than big-O polish.",
            "Prepare a 2-minute walkthrough of your best project, including what you would change now.",
            "Show enthusiasm for the product area of the team. Fit with the team is weighed heavily because the team makes the decision.",
        ],
        "must_do": [
            "two-sum", "reverse-linked-list", "merge-two-sorted-lists", "add-two-numbers", "palindrome-linked-list",
            "lru-cache", "min-stack", "implement-queue-using-stacks", "design-hit-counter", "insert-delete-getrandom-o1",
            "valid-anagram", "group-anagrams", "longest-substring-without-repeating-characters", "string-compression",
            "string-to-integer-atoi", "reverse-words-in-a-string", "valid-palindrome-ii", "longest-common-prefix",
            "merge-sorted-array", "move-zeroes", "rotate-array", "rotate-image", "spiral-matrix", "product-of-array-except-self",
            "maximum-depth-of-binary-tree", "validate-binary-search-tree", "binary-tree-level-order-traversal",
            "lowest-common-ancestor-of-bst", "kth-largest-element-in-an-array", "k-closest-points-to-origin",
            "merge-intervals", "best-time-to-buy-and-sell-stock", "coin-change", "number-of-islands", "find-the-duplicate-number",
        ],
    },
}

WEEKS = [
    ("Foundations: arrays, hashing, two pointers", ["Arrays & Hashing", "Two Pointers"]),
    ("Windows, stacks, binary search", ["Sliding Window", "Stack", "Binary Search"]),
    ("Linked lists and trees", ["Linked List", "Trees"]),
    ("Tries, heaps, backtracking", ["Tries", "Heap / Priority Queue", "Backtracking"]),
    ("Graphs", ["Graphs", "Advanced Graphs"]),
    ("Dynamic programming", ["1-D Dynamic Programming", "2-D Dynamic Programming"]),
    ("Greedy, intervals, math and bits", ["Greedy", "Intervals", "Math & Bit Manipulation"]),
    ("Design, strings, and mock interviews", ["Design", "Strings"]),
]


def company_track(problems: list[dict], company: str) -> dict:
    guide = COMPANY_GUIDES[company]
    by_id = {p["id"]: p for p in problems}
    must = [by_id[i] for i in guide["must_do"] if i in by_id]
    must_ids = {p["id"] for p in must}
    diff = {"Easy": 0, "Medium": 1, "Hard": 2}
    rest = [p for p in problems if p["companies"].get(company, 0) >= 3 and p["id"] not in must_ids]
    rest.sort(key=lambda p: (-p["companies"].get(company, 0), diff[p["difficulty"]], p["number"]))
    freq = [p for p in problems if p["companies"].get(company, 0) >= 1]
    freq.sort(key=lambda p: (-p["companies"].get(company, 0), p["number"]))

    def brief(p):
        return {"id": p["id"], "number": p["number"], "title": p["title"], "difficulty": p["difficulty"],
                "pattern": p["pattern"], "score": p["companies"].get(company, 0)}

    return {
        "company": company,
        "name": guide["name"],
        "summary": guide["summary"],
        "process": guide["process"],
        "focus": guide["focus"],
        "tips": guide["tips"],
        "must_do": [brief(p) for p in must],
        "also": [brief(p) for p in rest],
        "all_by_frequency": [brief(p) for p in freq],
        "pattern_mix": _pattern_mix(freq, company),
    }


def _pattern_mix(problems: list[dict], company: str) -> list[dict]:
    weight: dict[str, int] = {}
    for p in problems:
        weight[p["pattern"]] = weight.get(p["pattern"], 0) + p["companies"].get(company, 0)
    total = sum(weight.values()) or 1
    out = [{"pattern": k, "share": round(100 * v / total)} for k, v in weight.items()]
    out.sort(key=lambda x: -x["share"])
    return out


def study_plan(problems: list[dict], progress: dict) -> dict:
    """8 weeks, 6 study days each. Problems are spread across days within the week's patterns."""
    diff = {"Easy": 0, "Medium": 1, "Hard": 2}
    weeks = []
    for wi, (title, patterns) in enumerate(WEEKS, 1):
        pool = [p for p in problems if p["pattern"] in patterns]
        pool.sort(key=lambda p: (patterns.index(p["pattern"]), diff[p["difficulty"]], p["number"]))
        days = [[] for _ in range(6)]
        for i, p in enumerate(pool):
            days[i % 6].append({"id": p["id"], "number": p["number"], "title": p["title"], "difficulty": p["difficulty"],
                                "pattern": p["pattern"], "status": progress.get(p["id"], {}).get("status")})
        extras = []
        if wi == 8:
            extras = ["Two full mock interviews (use the Mock tab): one Google-style, one Apple-style.",
                      "Re-solve every problem marked 'again' or 'hard' in reviews.",
                      "Write out your 6 behavioural STAR stories and rehearse them aloud."]
        elif wi == 5:
            extras = ["Mid-point mock interview: one graph problem, 45 minutes, no hints."]
        weeks.append({"week": wi, "title": title, "patterns": patterns, "days": days, "extras": extras,
                      "done": sum(1 for d in days for p in d if p["status"] == "solved"), "total": len(pool)})
    return {"weeks": weeks, "daily_routine": [
        "Warm-up (10 min): one review-due problem from the Reviews list, from memory.",
        "New problems (60-90 min): the day's list. Spend at most 25 minutes before opening a hint, 40 before the editorial.",
        "After each problem: read the editorial even if you passed, and write one line in Notes about the key idea.",
        "Wrap-up (5 min): re-explain today's hardest problem out loud as if to an interviewer.",
    ]}
