"""Interval problems. See SCHEMA.md for the dict format."""

PROBLEMS = [
    {
        "id": "insert-interval",
        "title": "Insert Interval",
        "difficulty": "Medium",
        "pattern": "Intervals",
        "tags": ["Array", "Intervals"],
        "companies": {"google": 3, "apple": 1, "meta": 2, "amazon": 2, "microsoft": 1},
        "description": (
            "You are given `intervals`, a list of closed intervals `[start, end]` that are **sorted by start and pairwise "
            "non-overlapping**, plus one extra interval `newInterval`.\n\n"
            "Insert `newInterval` so that the list stays sorted and non-overlapping, merging it with any intervals it touches or "
            "overlaps. Return the resulting list. Do not assume you may mutate the input."
        ),
        "examples": [
            {"input": "intervals = [[1,3],[6,9]], newInterval = [2,5]", "output": "[[1,5],[6,9]]",
             "explanation": "[2,5] overlaps [1,3]; they merge into [1,5]."},
            {"input": "intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]", "output": "[[1,2],[3,10],[12,16]]",
             "explanation": "[4,8] overlaps [3,5], [6,7] and [8,10]; all four merge into [3,10]."},
            {"input": "intervals = [], newInterval = [5,7]", "output": "[[5,7]]"},
        ],
        "constraints": ["0 <= intervals.length <= 10^4", "0 <= start <= end <= 10^5", "intervals is sorted by start and non-overlapping."],
        "hints": [
            "Because the input is sorted, the intervals fall into three groups: entirely before the new one, overlapping it, entirely after it.",
            "Copy the 'before' group unchanged, absorb the overlapping group into newInterval by taking min(start) and max(end), then copy the 'after' group.",
            "An interval [a,b] is entirely before if b < newStart; entirely after if a > newEnd; otherwise it overlaps. Three short loops, one pass, no sorting needed.",
        ],
        "function": "insert",
        "signature": "def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:",
        "arg_types": {"intervals": "List[List[int]]", "newInterval": "List[int]"},
        "return_type": "List[List[int]]",
        "compare": "exact",
        "tests": [
            {"input": {"intervals": [[1, 3], [6, 9]], "newInterval": [2, 5]}, "output": [[1, 5], [6, 9]]},
            {"input": {"intervals": [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], "newInterval": [4, 8]}, "output": [[1, 2], [3, 10], [12, 16]]},
            {"input": {"intervals": [], "newInterval": [5, 7]}, "output": [[5, 7]]},
            {"input": {"intervals": [[1, 5]], "newInterval": [2, 3]}, "output": [[1, 5]]},
            {"input": {"intervals": [[1, 5]], "newInterval": [6, 8]}, "output": [[1, 5], [6, 8]]},
            {"input": {"intervals": [[3, 5]], "newInterval": [1, 2]}, "output": [[1, 2], [3, 5]]},
            {"input": {"intervals": [[1, 5]], "newInterval": [5, 7]}, "output": [[1, 7]]},
            {"input": {"intervals": [[2 * i, 2 * i + 1] for i in range(5000)], "newInterval": [1, 9998]}, "output": [[0, 9999]]},
            {"input": {"intervals": [[2 * i, 2 * i + 1] for i in range(5000)], "newInterval": [20000, 20001]},
             "output": [[2 * i, 2 * i + 1] for i in range(5000)] + [[20000, 20001]]},
        ],
        "solution": (
            "class Solution:\n"
            "    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:\n"
            "        start, end = newInterval\n"
            "        out = []\n"
            "        i, n = 0, len(intervals)\n"
            "        # 1. intervals that end before the new one starts\n"
            "        while i < n and intervals[i][1] < start:\n"
            "            out.append(intervals[i])\n"
            "            i += 1\n"
            "        # 2. intervals that overlap: absorb them\n"
            "        while i < n and intervals[i][0] <= end:\n"
            "            start = min(start, intervals[i][0])\n"
            "            end = max(end, intervals[i][1])\n"
            "            i += 1\n"
            "        out.append([start, end])\n"
            "        # 3. the rest\n"
            "        out.extend(intervals[i:])\n"
            "        return out\n"
        ),
        "approach": (
            "**Key insight: the input is already sorted and disjoint, so the intervals that overlap the new one form one contiguous block "
            "in the list. Everything before that block is untouched, everything after is untouched.**\n\n"
            "Walk the list once in three phases. Phase 1 copies intervals whose `end < newStart`. Phase 2 absorbs intervals whose "
            "`start <= newEnd` by widening `newInterval` to `[min(starts), max(ends)]`. Phase 3 appends the merged interval and copies "
            "the remainder.\n\n"
            "**Why it is correct:** two closed intervals `[a,b]` and `[c,d]` overlap exactly when `a <= d and c <= b`. In a sorted disjoint "
            "list, the set of intervals satisfying this against a fixed `[c,d]` is contiguous, so once we leave phase 2 nothing later can "
            "overlap, and the widened interval covers precisely the union of the block plus the new interval.\n\n"
            "**Common mistakes:** using `<=` versus `<` inconsistently so that touching intervals (`[1,5]` and `[5,7]`) are not merged; "
            "sorting and running a general merge, which is correct but `O(n log n)` and misses the point; mutating `newInterval` in "
            "place when the caller may still need it.\n\n"
            "**Interview follow-ups:** (1) Many insertions in a row: keep a balanced BST / sorted structure keyed by start, or batch and "
            "run Merge Intervals once. (2) Remove an interval instead of inserting (split any interval it cuts into up to two pieces). "
            "(3) Half-open intervals `[start, end)` change the touching rule: `[1,5)` and `[5,7)` do not merge."
        ),
        "complexity": {"time": "O(n)", "space": "O(n) for the output"},
        "similar": ["merge-intervals", "non-overlapping-intervals", "remove-interval"],
    },
    {
        "id": "merge-intervals",
        "title": "Merge Intervals",
        "difficulty": "Medium",
        "pattern": "Intervals",
        "tags": ["Array", "Sorting", "Intervals"],
        "companies": {"google": 4, "apple": 3, "meta": 5, "amazon": 4, "microsoft": 3},
        "description": (
            "Given a list of closed intervals `[start, end]` in arbitrary order, merge every group of overlapping intervals into a single "
            "interval and return the resulting list, sorted by start.\n\n"
            "Intervals that merely touch (one ends where the next begins) count as overlapping."
        ),
        "examples": [
            {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]",
             "explanation": "[1,3] and [2,6] overlap and become [1,6]."},
            {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]", "explanation": "Touching at 4 counts as overlapping."},
            {"input": "intervals = [[5,6],[1,2]]", "output": "[[1,2],[5,6]]", "explanation": "Nothing merges, but the output must be sorted."},
        ],
        "constraints": ["1 <= intervals.length <= 10^4", "0 <= start <= end <= 10^4"],
        "hints": [
            "If you sort by start, every interval that can merge with the current one appears right after it.",
            "Keep the last interval of the output. If the next interval starts at or before its end, extend the end; otherwise start a new output interval.",
            "Extend with max(end, next_end), not just next_end: [1,10] followed by [2,3] must stay [1,10].",
        ],
        "function": "merge",
        "signature": "def merge(self, intervals: List[List[int]]) -> List[List[int]]:",
        "arg_types": {"intervals": "List[List[int]]"},
        "return_type": "List[List[int]]",
        "compare": "exact",
        "tests": [
            {"input": {"intervals": [[1, 3], [2, 6], [8, 10], [15, 18]]}, "output": [[1, 6], [8, 10], [15, 18]]},
            {"input": {"intervals": [[1, 4], [4, 5]]}, "output": [[1, 5]]},
            {"input": {"intervals": [[5, 6], [1, 2]]}, "output": [[1, 2], [5, 6]]},
            {"input": {"intervals": [[1, 4]]}, "output": [[1, 4]]},
            {"input": {"intervals": [[1, 4], [0, 4]]}, "output": [[0, 4]]},
            {"input": {"intervals": [[1, 10], [2, 3], [4, 5]]}, "output": [[1, 10]]},
            {"input": {"intervals": [[2, 2], [1, 1], [3, 3]]}, "output": [[1, 1], [2, 2], [3, 3]]},
            {"input": {"intervals": [[i, i + 1] for i in range(5000, -1, -1)]}, "output": [[0, 5001]]},
            {"input": {"intervals": [[3 * i, 3 * i + 1] for i in range(2999, -1, -1)]}, "output": [[3 * i, 3 * i + 1] for i in range(3000)]},
        ],
        "solution": (
            "class Solution:\n"
            "    def merge(self, intervals: List[List[int]]) -> List[List[int]]:\n"
            "        intervals.sort(key=lambda iv: iv[0])\n"
            "        out = []\n"
            "        for start, end in intervals:\n"
            "            if out and start <= out[-1][1]:\n"
            "                out[-1][1] = max(out[-1][1], end)   # overlaps the last merged interval\n"
            "            else:\n"
            "                out.append([start, end])\n"
            "        return out\n"
        ),
        "approach": (
            "**Key insight: after sorting by start, an interval can only overlap the most recently merged interval; if it does not, "
            "nothing earlier can overlap it either.**\n\n"
            "Sort by start. Keep an output list; for each interval, if its start is `<=` the end of the last output interval, extend that "
            "end to `max(end, current end)`; otherwise push the interval as a new group.\n\n"
            "**Why it is correct (invariant):** after processing the first `k` sorted intervals, the output is exactly the merged form of "
            "those `k`. The next interval has a start at least as large as every previous start, so the only output interval it can "
            "intersect is the last one (all earlier ones ended before the last one started). Taking the `max` of ends handles an interval "
            "that is fully contained in the current group.\n\n"
            "**Common mistakes:** writing `out[-1][1] = end` instead of `max(...)` (breaks on `[1,10],[2,3]`); using `<` instead of `<=` "
            "so touching intervals do not merge; forgetting to sort; mutating the caller's input without mentioning it.\n\n"
            "**Interview follow-ups:** (1) Streaming input where intervals arrive one at a time (see Insert Interval, or maintain a sorted "
            "container). (2) Return the total covered length, or the gaps between merged intervals (Employee Free Time). "
            "(3) Can you avoid sorting? Only if the coordinate range is small (bucket by start) or the input is already sorted."
        ),
        "complexity": {"time": "O(n log n)", "space": "O(n)"},
        "similar": ["insert-interval", "meeting-rooms", "non-overlapping-intervals"],
    },
    {
        "id": "non-overlapping-intervals",
        "title": "Non-overlapping Intervals",
        "difficulty": "Medium",
        "pattern": "Intervals",
        "tags": ["Array", "Greedy", "Sorting", "Intervals"],
        "companies": {"google": 2, "amazon": 2, "microsoft": 1},
        "description": (
            "Given a list of intervals `[start, end]`, return the **minimum number of intervals to remove** so that the remaining ones do "
            "not overlap.\n\n"
            "Intervals that only touch at an endpoint, such as `[1,2]` and `[2,3]`, are considered non-overlapping."
        ),
        "examples": [
            {"input": "intervals = [[1,2],[2,3],[3,4],[1,3]]", "output": "1", "explanation": "Remove [1,3]; the other three only touch."},
            {"input": "intervals = [[1,2],[1,2],[1,2]]", "output": "2", "explanation": "Only one copy can stay."},
            {"input": "intervals = [[1,2],[2,3]]", "output": "0"},
        ],
        "constraints": ["1 <= intervals.length <= 10^5", "-5 * 10^4 <= start < end <= 5 * 10^4"],
        "hints": [
            "Removing the minimum number of intervals is the same as keeping the maximum number of non-overlapping ones. That is the classic activity-selection problem.",
            "Sort by END time. Always keep the interval that finishes earliest; it leaves the most room for the ones that follow.",
            "Track the end of the last kept interval. For each interval in end order, keep it if its start >= that end, otherwise count it as removed.",
        ],
        "function": "eraseOverlapIntervals",
        "signature": "def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:",
        "arg_types": {"intervals": "List[List[int]]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"intervals": [[1, 2], [2, 3], [3, 4], [1, 3]]}, "output": 1},
            {"input": {"intervals": [[1, 2], [1, 2], [1, 2]]}, "output": 2},
            {"input": {"intervals": [[1, 2], [2, 3]]}, "output": 0},
            {"input": {"intervals": [[1, 2]]}, "output": 0},
            {"input": {"intervals": [[1, 100], [2, 3], [4, 5]]}, "output": 1},
            {"input": {"intervals": [[-5, 2], [0, 10], [3, 4], [5, 6]]}, "output": 1},
            {"input": {"intervals": [[1, 5], [2, 3], [3, 4]]}, "output": 1},
            {"input": {"intervals": [[i, i + 2] for i in range(5000)]}, "output": 2500},
            {"input": {"intervals": [[i, i + 1] for i in range(3000)] + [[0, 3000]]}, "output": 1},
        ],
        "solution": (
            "class Solution:\n"
            "    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:\n"
            "        intervals.sort(key=lambda iv: iv[1])   # earliest finishing first\n"
            "        removed = 0\n"
            "        last_end = float('-inf')\n"
            "        for start, end in intervals:\n"
            "            if start >= last_end:\n"
            "                last_end = end       # keep it\n"
            "            else:\n"
            "                removed += 1         # overlaps the kept one that ends earliest\n"
            "        return removed\n"
        ),
        "approach": (
            "**Key insight: minimising removals equals maximising the number of kept, pairwise disjoint intervals. Greedily keeping the "
            "interval that ends earliest is optimal.**\n\n"
            "Sort by end. Scan in that order, remembering `last_end` of the most recently kept interval. If the current start is "
            "`>= last_end`, keep it and update `last_end`; otherwise it collides with a kept interval and is removed.\n\n"
            "**Why it is correct (exchange argument):** suppose an optimal set of kept intervals does not include the earliest-ending "
            "interval `e`. Replace the first interval of that optimal set with `e`: it ends no later, so it cannot collide with the rest. "
            "The set is still valid and the same size, so some optimal solution starts with `e`. Apply the same argument to the "
            "remaining intervals that start after `e` ends.\n\n"
            "**Common mistakes:** sorting by start instead of end (then you must keep the one with the smaller end when two overlap, "
            "which also works but is easier to get wrong); using `>` rather than `>=` so touching intervals count as overlapping; "
            "counting kept intervals and forgetting to subtract from `n`.\n\n"
            "**Interview follow-ups:** (1) Return the kept intervals themselves. (2) Weighted version where each interval has a value "
            "and you maximise total value (sort by end, DP with binary search, `O(n log n)`). (3) Minimum Number of Arrows to Burst "
            "Balloons is the same greedy with the complementary question: how many groups of mutually overlapping intervals exist."
        ),
        "complexity": {"time": "O(n log n)", "space": "O(1) beyond sorting"},
        "similar": ["minimum-number-of-arrows-to-burst-balloons", "merge-intervals", "meeting-rooms"],
    },
    {
        "id": "meeting-rooms",
        "title": "Meeting Rooms",
        "difficulty": "Easy",
        "pattern": "Intervals",
        "tags": ["Array", "Sorting", "Intervals"],
        "companies": {"google": 2, "apple": 1, "meta": 3, "amazon": 2, "microsoft": 1},
        "description": (
            "You are given a list of meeting time intervals `[start, end]`. Determine whether **one person** could attend every "
            "meeting, that is, whether no two meetings overlap.\n\n"
            "A meeting that starts exactly when another ends does not conflict with it. Return `true` if all meetings can be attended, "
            "otherwise `false`."
        ),
        "examples": [
            {"input": "intervals = [[0,30],[5,10],[15,20]]", "output": "false", "explanation": "[5,10] starts while [0,30] is still running."},
            {"input": "intervals = [[7,10],[2,4]]", "output": "true"},
            {"input": "intervals = [[1,5],[5,10]]", "output": "true", "explanation": "Back-to-back meetings are fine."},
        ],
        "constraints": ["0 <= intervals.length <= 10^4", "0 <= start < end <= 10^6"],
        "hints": [
            "If two meetings overlap, after sorting by start they will be adjacent (or there will be an adjacent overlapping pair somewhere).",
            "Sort by start and check every consecutive pair: a conflict exists when the next meeting starts before the current one ends.",
        ],
        "function": "canAttendMeetings",
        "signature": "def canAttendMeetings(self, intervals: List[List[int]]) -> bool:",
        "arg_types": {"intervals": "List[List[int]]"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"intervals": [[0, 30], [5, 10], [15, 20]]}, "output": False},
            {"input": {"intervals": [[7, 10], [2, 4]]}, "output": True},
            {"input": {"intervals": [[1, 5], [5, 10]]}, "output": True},
            {"input": {"intervals": []}, "output": True},
            {"input": {"intervals": [[1, 5]]}, "output": True},
            {"input": {"intervals": [[1, 5], [4, 10]]}, "output": False},
            {"input": {"intervals": [[6, 7], [2, 4], [8, 12]]}, "output": True},
            {"input": {"intervals": [[i, i + 1] for i in range(10000, -1, -1)]}, "output": True},
            {"input": {"intervals": [[i, i + 1] for i in range(10000, -1, -1)] + [[500, 502]]}, "output": False},
        ],
        "solution": (
            "class Solution:\n"
            "    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:\n"
            "        intervals.sort(key=lambda iv: iv[0])\n"
            "        for i in range(1, len(intervals)):\n"
            "            if intervals[i][0] < intervals[i - 1][1]:\n"
            "                return False\n"
            "        return True\n"
        ),
        "approach": (
            "**Key insight: once meetings are sorted by start time, any conflict shows up between two consecutive meetings.**\n\n"
            "Sort by start, then scan adjacent pairs. If `intervals[i].start < intervals[i-1].end`, two meetings overlap and the answer is "
            "false. If the scan finishes, every meeting begins at or after the previous one ends.\n\n"
            "**Why it is correct:** suppose some pair `(a, b)` with `a` before `b` in sorted order overlaps, i.e. `b.start < a.end`. Every "
            "meeting `c` between them in sorted order has `c.start <= b.start < a.end`, so `a` overlaps its immediate successor as well. "
            "Thus checking neighbours is sufficient; it is obviously necessary.\n\n"
            "**Common mistakes:** using `<=` and rejecting back-to-back meetings; comparing with the maximum end seen so far is actually "
            "unnecessary here because in a valid schedule ends are also increasing, but it does no harm.\n\n"
            "**Interview follow-ups:** (1) How many rooms are needed when conflicts exist (Meeting Rooms II). (2) Find a free slot of a "
            "given length for a new meeting (scan the gaps). (3) Intervals arrive as a stream: keep them in a sorted structure and check "
            "the two neighbours of each insertion point."
        ),
        "complexity": {"time": "O(n log n)", "space": "O(1) beyond sorting"},
        "similar": ["meeting-rooms-ii", "merge-intervals", "non-overlapping-intervals"],
    },
    {
        "id": "meeting-rooms-ii",
        "title": "Meeting Rooms II",
        "difficulty": "Medium",
        "pattern": "Intervals",
        "tags": ["Array", "Sorting", "Heap / Priority Queue", "Intervals"],
        "companies": {"google": 4, "apple": 2, "meta": 4, "amazon": 4, "microsoft": 3},
        "description": (
            "You are given a list of meeting time intervals `[start, end]`. Return the **minimum number of conference rooms** needed so "
            "that no two meetings share a room while they overlap.\n\n"
            "A meeting that starts exactly when another ends may reuse that room."
        ),
        "examples": [
            {"input": "intervals = [[0,30],[5,10],[15,20]]", "output": "2",
             "explanation": "[0,30] occupies one room the whole time; [5,10] and [15,20] can share a second room."},
            {"input": "intervals = [[7,10],[2,4]]", "output": "1"},
            {"input": "intervals = [[1,10],[2,9],[3,8],[4,7]]", "output": "4", "explanation": "All four are running at time 5."},
        ],
        "constraints": ["0 <= intervals.length <= 10^4", "0 <= start < end <= 10^6"],
        "hints": [
            "The answer is the maximum number of meetings that are in progress at the same instant.",
            "Sort by start. Keep a min-heap of end times of meetings currently using a room. When a new meeting starts, if the earliest-ending meeting has already finished, pop it (reuse the room). Push the new end. The heap size at its largest is the answer.",
            "Alternative: sort starts and ends separately and sweep with two pointers, incrementing on a start and decrementing on an end (process an end first when it equals a start).",
        ],
        "function": "minMeetingRooms",
        "signature": "def minMeetingRooms(self, intervals: List[List[int]]) -> int:",
        "arg_types": {"intervals": "List[List[int]]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"intervals": [[0, 30], [5, 10], [15, 20]]}, "output": 2},
            {"input": {"intervals": [[7, 10], [2, 4]]}, "output": 1},
            {"input": {"intervals": [[1, 10], [2, 9], [3, 8], [4, 7]]}, "output": 4},
            {"input": {"intervals": []}, "output": 0},
            {"input": {"intervals": [[1, 2]]}, "output": 1},
            {"input": {"intervals": [[1, 5], [5, 10]]}, "output": 1},
            {"input": {"intervals": [[1, 5], [2, 6], [8, 9], [8, 9]]}, "output": 2},
            {"input": {"intervals": [[i, i + 100] for i in range(5000)]}, "output": 100},
            {"input": {"intervals": [[i % 50, i % 50 + 60] for i in range(2000)]}, "output": 2000},
            {"input": {"intervals": [[2 * i, 2 * i + 1] for i in range(5000)]}, "output": 1},
        ],
        "solution": (
            "class Solution:\n"
            "    def minMeetingRooms(self, intervals: List[List[int]]) -> int:\n"
            "        intervals.sort(key=lambda iv: iv[0])\n"
            "        busy_until = []   # min-heap of end times of meetings occupying a room\n"
            "        rooms = 0\n"
            "        for start, end in intervals:\n"
            "            if busy_until and busy_until[0] <= start:\n"
            "                heapq.heapreplace(busy_until, end)   # reuse the room that frees up earliest\n"
            "            else:\n"
            "                heapq.heappush(busy_until, end)      # need a new room\n"
            "            rooms = max(rooms, len(busy_until))\n"
            "        return rooms\n"
        ),
        "approach": (
            "**Key insight: the number of rooms needed equals the maximum number of meetings overlapping at any single moment. "
            "Processing meetings by start time with a min-heap of end times tracks exactly that.**\n\n"
            "Sort by start. The heap holds the end times of meetings that currently hold a room; its minimum is the room that frees up "
            "first. For each meeting, if that earliest end is `<= start`, the room is free and we replace its end time with ours; "
            "otherwise every room is busy and we push a new end. The largest heap size seen is the answer.\n\n"
            "**Why it is correct:** at the moment a meeting starts, the heap contains precisely the meetings that started earlier and have "
            "not yet ended (plus possibly some that ended but were not popped because a free room was not needed; they only make the "
            "heap larger than necessary at that instant, and the maximum is still attained at some start time where all expired "
            "entries are reused first). Reusing the earliest-freed room never hurts because any free room is interchangeable.\n\n"
            "**Alternative: two sorted arrays.** Sort starts and ends separately. Sweep: at each start, if the smallest unmatched end is "
            "`<= start`, a meeting finished and a room is released (advance the end pointer); otherwise allocate a room. This is the same "
            "idea without a heap and is a nice thing to mention.\n\n"
            "**Common mistakes:** using `<` instead of `<=` for room reuse (back-to-back meetings should share a room); popping only one "
            "finished meeting per start is correct for the maximum, but students sometimes pop all and then compute size incorrectly; "
            "returning the final heap size instead of its maximum.\n\n"
            "**Interview follow-ups:** (1) Which room does each meeting get (Meeting Rooms III: assign the lowest-indexed free room). "
            "(2) Report the time interval during which the most rooms are in use. (3) Rooms have capacities or meetings have attendee "
            "counts (sweep line with weights)."
        ),
        "complexity": {"time": "O(n log n)", "space": "O(n)"},
        "similar": ["meeting-rooms", "merge-intervals", "car-pooling"],
    },
    {
        "id": "minimum-interval-to-include-each-query",
        "title": "Minimum Interval to Include Each Query",
        "difficulty": "Hard",
        "pattern": "Intervals",
        "tags": ["Array", "Sorting", "Heap / Priority Queue", "Intervals", "Offline Queries"],
        "companies": {"google": 1, "amazon": 1},
        "description": (
            "You are given `intervals`, a list of closed integer intervals `[left, right]`, and a list of integer `queries`. The "
            "**size** of an interval is `right - left + 1`.\n\n"
            "For each query `q`, find the smallest size among all intervals that contain `q` (`left <= q <= right`). If no interval "
            "contains `q`, the answer for that query is `-1`.\n\n"
            "Return the answers in the same order as `queries`."
        ),
        "examples": [
            {"input": "intervals = [[1,4],[2,4],[3,6],[4,4]], queries = [2,3,4,5]", "output": "[3,3,1,4]",
             "explanation": "Query 2 is inside [1,4] (size 4) and [2,4] (size 3); the smallest is 3. Query 4 is inside [4,4] of size 1. Query 5 is only inside [3,6]."},
            {"input": "intervals = [[2,3],[2,5],[1,8],[20,25]], queries = [2,19,5,22]", "output": "[2,-1,4,6]",
             "explanation": "Nothing contains 19."},
            {"input": "intervals = [[1,1]], queries = [1,2]", "output": "[1,-1]"},
        ],
        "constraints": ["1 <= intervals.length, queries.length <= 10^5", "1 <= left <= right <= 10^7", "1 <= queries[i] <= 10^7"],
        "hints": [
            "Checking every interval for every query is O(n * q). The queries are independent, so you may answer them in any order and reorder the results at the end.",
            "Sort the queries and the intervals by left endpoint. As the query value grows, intervals become 'active' once their left <= q; an interval stops being useful once its right < q.",
            "Keep a min-heap of (size, right) for active intervals. For each query in sorted order, push all intervals whose left <= q, then pop while the top's right < q. The top is the answer. Record it against the query's original index.",
        ],
        "function": "minInterval",
        "signature": "def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:",
        "arg_types": {"intervals": "List[List[int]]", "queries": "List[int]"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"intervals": [[1, 4], [2, 4], [3, 6], [4, 4]], "queries": [2, 3, 4, 5]}, "output": [3, 3, 1, 4]},
            {"input": {"intervals": [[2, 3], [2, 5], [1, 8], [20, 25]], "queries": [2, 19, 5, 22]}, "output": [2, -1, 4, 6]},
            {"input": {"intervals": [[1, 1]], "queries": [1, 2]}, "output": [1, -1]},
            {"input": {"intervals": [[1, 10]], "queries": [5, 10, 1, 11, 0]}, "output": [10, 10, 10, -1, -1]},
            {"input": {"intervals": [[5, 6], [1, 9]], "queries": [7, 7, 5]}, "output": [9, 9, 2]},
            {"input": {"intervals": [[1, 4], [2, 4], [3, 6], [4, 4]], "queries": []}, "output": []},
            {"input": {"intervals": [[0, 10000]] + [[i, i] for i in range(5000)], "queries": list(range(10000))},
             "output": [1] * 5000 + [10001] * 5000},
            {"input": {"intervals": [[i, 9999 - i] for i in range(5000)], "queries": list(range(9999, -1, -1))},
             "output": [10000 - 2 * min(q, 9999 - q) for q in range(9999, -1, -1)]},
        ],
        "solution": (
            "class Solution:\n"
            "    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:\n"
            "        intervals.sort()                                   # by left endpoint\n"
            "        order = sorted(range(len(queries)), key=lambda k: queries[k])\n"
            "        ans = [-1] * len(queries)\n"
            "        active = []   # min-heap of (size, right) for intervals with left <= current query\n"
            "        i = 0\n"
            "        for k in order:\n"
            "            q = queries[k]\n"
            "            while i < len(intervals) and intervals[i][0] <= q:\n"
            "                left, right = intervals[i]\n"
            "                heapq.heappush(active, (right - left + 1, right))\n"
            "                i += 1\n"
            "            while active and active[0][1] < q:   # ended before q; useless for all later queries too\n"
            "                heapq.heappop(active)\n"
            "            if active:\n"
            "                ans[k] = active[0][0]\n"
            "        return ans\n"
        ),
        "approach": (
            "**Key insight: answer the queries offline in increasing order. Then intervals enter the candidate set when the query reaches "
            "their left endpoint and leave for good once the query passes their right endpoint, so a sweep with a heap works.**\n\n"
            "Sort intervals by `left` and sort the queries (remembering their original indices). Maintain a min-heap keyed by interval "
            "size. For each query `q` in increasing order: push every not-yet-pushed interval with `left <= q`; then pop from the heap "
            "while the smallest interval's `right < q` (it has expired); the heap top, if any, is the answer for `q`.\n\n"
            "**Why it is correct:** when we read the heap for query `q`, every interval with `left <= q` has been pushed (sorted order plus "
            "monotone queries), and every interval on top of the heap has `right >= q`, so it contains `q`. Expired intervals deeper in "
            "the heap do not matter because we only read the top; they are removed lazily if they ever surface. Because queries only "
            "increase, an expired interval can never become valid again, so lazy deletion is safe.\n\n"
            "**Common mistakes:** forgetting to map answers back to the original query order; popping expired intervals before pushing "
            "new ones (fine) versus never popping (returns stale answers); keying the heap on `right` instead of size.\n\n"
            "**Interview follow-ups:** (1) Online queries that cannot be reordered: build a segment tree over coordinates storing the "
            "minimum size, or use a persistent structure. (2) Return the interval itself, not just its size. (3) Count how many "
            "intervals contain each query instead of the minimum size (prefix sums over sorted endpoints, no heap needed)."
        ),
        "complexity": {"time": "O((n + q) log(n + q))", "space": "O(n + q)"},
        "similar": ["meeting-rooms-ii", "merge-intervals", "the-skyline-problem"],
    },
    {
        "id": "minimum-number-of-arrows-to-burst-balloons",
        "title": "Minimum Number of Arrows to Burst Balloons",
        "difficulty": "Medium",
        "pattern": "Intervals",
        "tags": ["Array", "Greedy", "Sorting", "Intervals"],
        "companies": {"google": 1, "amazon": 2, "microsoft": 1},
        "description": (
            "Balloons are taped to a wall; balloon `i` spans the horizontal range `[xstart, xend]`. An arrow shot straight up at "
            "coordinate `x` bursts every balloon whose range includes `x` (endpoints inclusive), and keeps flying.\n\n"
            "Return the minimum number of arrows needed to burst all the balloons."
        ),
        "examples": [
            {"input": "points = [[10,16],[2,8],[1,6],[7,12]]", "output": "2",
             "explanation": "An arrow at x = 6 bursts [2,8] and [1,6]; an arrow at x = 11 bursts [10,16] and [7,12]."},
            {"input": "points = [[1,2],[3,4],[5,6],[7,8]]", "output": "4", "explanation": "No two balloons share a coordinate."},
            {"input": "points = [[1,2],[2,3],[3,4],[4,5]]", "output": "2", "explanation": "Arrows at x = 2 and x = 4."},
        ],
        "constraints": ["1 <= points.length <= 10^5", "-2^31 <= xstart < xend <= 2^31 - 1"],
        "hints": [
            "Each arrow should burst a group of balloons that all share a common point. How do you form the fewest such groups?",
            "Sort by right endpoint. Shoot the first arrow at the smallest right endpoint: that balloon has to be burst, and shooting any further left cannot hit more balloons.",
            "Every balloon whose start is <= the arrow position is hit. The first balloon that starts after it needs a new arrow at ITS right endpoint. Count arrows.",
        ],
        "function": "findMinArrowShots",
        "signature": "def findMinArrowShots(self, points: List[List[int]]) -> int:",
        "arg_types": {"points": "List[List[int]]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"points": [[10, 16], [2, 8], [1, 6], [7, 12]]}, "output": 2},
            {"input": {"points": [[1, 2], [3, 4], [5, 6], [7, 8]]}, "output": 4},
            {"input": {"points": [[1, 2], [2, 3], [3, 4], [4, 5]]}, "output": 2},
            {"input": {"points": [[1, 2]]}, "output": 1},
            {"input": {"points": [[1, 10], [2, 3], [4, 5]]}, "output": 2},
            {"input": {"points": [[-2147483646, -2147483645], [2147483646, 2147483647]]}, "output": 2},
            {"input": {"points": [[3, 9], [7, 12], [3, 8], [6, 8], [9, 10], [2, 9], [0, 9], [3, 9], [0, 6], [2, 8]]}, "output": 2},
            {"input": {"points": [[i, i + 1] for i in range(0, 10000, 2)]}, "output": 5000},
            {"input": {"points": [[i, i + 10] for i in range(4999, -1, -1)]}, "output": 455},
        ],
        "solution": (
            "class Solution:\n"
            "    def findMinArrowShots(self, points: List[List[int]]) -> int:\n"
            "        points.sort(key=lambda p: p[1])   # by right endpoint\n"
            "        arrows = 0\n"
            "        arrow_x = float('-inf')\n"
            "        for start, end in points:\n"
            "            if start > arrow_x:        # current arrow misses this balloon\n"
            "                arrows += 1\n"
            "                arrow_x = end          # shoot at its right edge\n"
            "        return arrows\n"
        ),
        "approach": (
            "**Key insight: among the unburst balloons, the one with the smallest right endpoint must be hit by some arrow, and the best "
            "place for that arrow is exactly that right endpoint: any position further right misses this balloon, any position further "
            "left hits a subset of what the endpoint hits.**\n\n"
            "Sort by `xend`. Shoot the first arrow at `points[0].xend`. Walk the list: a balloon whose `xstart <= arrow_x` is already "
            "burst (its `xend >= arrow_x` because of the sort order); the first balloon with `xstart > arrow_x` needs a new arrow, placed "
            "at its own `xend`. The number of arrows shot is the answer.\n\n"
            "**Why it is correct (exchange argument):** take any optimal solution. Its leftmost arrow must hit the balloon with the smallest "
            "right endpoint `r`; moving that arrow to `r` still hits every balloon it hit before (they all contain `r` since they start "
            "`<= arrow <= r` and end `>= r`). Repeating on the remaining balloons shows the greedy never needs more arrows than optimal.\n\n"
            "**Common mistakes:** sorting by start and trying to extend a running intersection without shrinking its right edge; "
            "using `>=` instead of `>` so that a balloon starting exactly at the arrow is treated as missed; integer overflow in "
            "languages with fixed-width ints when initialising `arrow_x` (use the first balloon's end instead of a sentinel).\n\n"
            "**Interview follow-ups:** (1) This is the dual of Non-overlapping Intervals: arrows = size of the maximum set of pairwise "
            "disjoint balloons. (2) Each arrow has a width `w` (hits `[x, x+w]`): the same greedy with `arrow_x = end + w`. "
            "(3) Return the arrow coordinates, not just the count."
        ),
        "complexity": {"time": "O(n log n)", "space": "O(1) beyond sorting"},
        "similar": ["non-overlapping-intervals", "merge-intervals", "meeting-rooms"],
    },
]
