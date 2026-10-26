"""Backtracking problems: subsets, combinations, permutations, grid search, constraint placement."""

import itertools


def _queens_brute(n):
    """Independent brute-force oracle for N-Queens: filter permutations by diagonal clashes."""
    out = []
    for cols in itertools.permutations(range(n)):
        if len({c + r for r, c in enumerate(cols)}) == n and len({c - r for r, c in enumerate(cols)}) == n:
            out.append(["." * c + "Q" + "." * (n - c - 1) for c in cols])
    return out


def _balanced(n):
    """Independent oracle for balanced parentheses via the decomposition '(' A ')' B."""
    if n == 0:
        return [""]
    return [f"({a}){b}" for i in range(n) for a in _balanced(i) for b in _balanced(n - 1 - i)]


PROBLEMS = [
    # ------------------------------------------------------------------ subsets
    {
        "id": "subsets",
        "title": "Subsets",
        "difficulty": "Medium",
        "pattern": "Backtracking",
        "tags": ["Array", "Backtracking", "Bit Manipulation"],
        "companies": {"google": 3, "apple": 2, "meta": 3, "amazon": 3, "microsoft": 2},
        "description": (
            "You are given an array `nums` whose elements are all **distinct**. Produce every possible subset "
            "(the power set), including the empty subset and the full array.\n\n"
            "No subset may appear twice. Both the order of the subsets and the order of elements inside a "
            "subset are up to you."
        ),
        "examples": [
            {"input": "nums = [1,2,3]", "output": "[[],[1],[2],[3],[1,2],[1,3],[2,3],[1,2,3]]",
             "explanation": "Three elements give 2^3 = 8 subsets."},
            {"input": "nums = [0]", "output": "[[],[0]]"},
        ],
        "constraints": ["0 <= nums.length <= 12", "-10 <= nums[i] <= 10", "All values in nums are distinct."],
        "hints": [
            "Every element is either in a subset or not. How many subsets does that give for n elements?",
            "Build subsets incrementally: at index i, decide to include nums[i] or skip it, then recurse on i + 1.",
            "Equivalent formulation: iterate i from a start index, append nums[i], recurse with start = i + 1, pop. Record the current path at every call, not only at the leaves.",
        ],
        "function": "subsets",
        "signature": "def subsets(self, nums: List[int]) -> List[List[int]]:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "List[List[int]]",
        "compare": "unordered_nested",
        "tests": [
            {"input": {"nums": [1, 2, 3]}, "output": [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]},
            {"input": {"nums": [0]}, "output": [[], [0]]},
            {"input": {"nums": []}, "output": [[]]},
            {"input": {"nums": [-1, 5]}, "output": [[], [-1], [5], [-1, 5]]},
            {"input": {"nums": [4, 1, 9, 7]},
             "output": [[], [4], [1], [9], [7], [4, 1], [4, 9], [4, 7], [1, 9], [1, 7], [9, 7],
                        [4, 1, 9], [4, 1, 7], [4, 9, 7], [1, 9, 7], [4, 1, 9, 7]]},
            {"input": {"nums": list(range(1, 13))},
             "output": [[i for i in range(1, 13) if (m >> (i - 1)) & 1] for m in range(1 << 12)]},
        ],
        "solution": '''class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        path = []

        def backtrack(start: int) -> None:
            res.append(path[:])
            for i in range(start, len(nums)):
                path.append(nums[i])
                backtrack(i + 1)
                path.pop()

        backtrack(0)
        return res
''',
        "approach": (
            "**Key insight: every subset is a sequence of include/exclude decisions, one per element.** "
            "Enumerating those decisions as a tree visits each of the 2^n subsets exactly once.\n\n"
            "**Algorithm.** Keep a `path` list. `backtrack(start)` first records a copy of `path` (every "
            "node of the recursion tree is a valid subset), then for each `i >= start` appends `nums[i]`, "
            "recurses with `start = i + 1`, and pops. Forcing indices to increase is what prevents the same "
            "subset from being generated in two different orders.\n\n"
            "**Why it works.** The call with a given `start` enumerates exactly the subsets of "
            "`nums[start:]` prefixed by the current `path`. By induction every subset appears once.\n\n"
            "**Common mistakes:** appending `path` itself instead of a copy (all entries then alias the "
            "same mutable list, which ends up empty); recording only at the leaves (misses subsets that "
            "stop early); forgetting to pop.\n\n"
            "**Alternatives worth mentioning:** iterate masks `0..2^n-1` and take bit `i` as membership "
            "(very compact, O(n * 2^n)); or the iterative doubling trick where each new element is appended "
            "to a copy of every subset built so far.\n\n"
            "**Interview follow-ups:** What changes if `nums` contains duplicates? (sort, then skip a value "
            "equal to its predecessor at the same depth; see Subsets II.) Can you return subsets of a fixed "
            "size k only? (stop recursing when `len(path) == k`.) How would you stream the subsets without "
            "holding all 2^n in memory? (turn the recursion into a generator.)"
        ),
        "complexity": {"time": "O(n * 2^n)", "space": "O(n) recursion depth, excluding the output"},
        "similar": ["subsets-ii", "combination-sum", "permutations"],
    },
    # ------------------------------------------------------------ combination-sum
    {
        "id": "combination-sum",
        "title": "Combination Sum",
        "difficulty": "Medium",
        "pattern": "Backtracking",
        "tags": ["Array", "Backtracking"],
        "companies": {"google": 3, "apple": 2, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "Given an array of **distinct** positive integers `candidates` and a positive integer `target`, "
            "list every combination of candidates whose values add up to `target`.\n\n"
            "A candidate may be used **any number of times**. Two combinations are considered the same if they "
            "use the same multiset of values, regardless of order, so each distinct multiset must appear exactly "
            "once. Return the combinations in any order."
        ),
        "examples": [
            {"input": "candidates = [2,3,6,7], target = 7", "output": "[[2,2,3],[7]]",
             "explanation": "2 + 2 + 3 = 7 and 7 = 7. Nothing else works: 6 leaves 1, which no candidate covers."},
            {"input": "candidates = [2,3,5], target = 8", "output": "[[2,2,2,2],[2,3,3],[3,5]]"},
            {"input": "candidates = [2], target = 1", "output": "[]"},
        ],
        "constraints": [
            "1 <= candidates.length <= 30",
            "2 <= candidates[i] <= 40, all distinct",
            "1 <= target <= 40",
            "The number of valid combinations is below 150.",
        ],
        "hints": [
            "Think of it as choosing how many copies of each candidate to take, in a fixed candidate order, so a multiset is never produced twice.",
            "Recurse with a `start` index and a `remaining` amount. Pick candidate i >= start, subtract it, and recurse with the *same* start (reuse allowed).",
            "Sort the candidates first; then as soon as candidates[i] > remaining you can `break` out of the loop instead of just `continue`.",
        ],
        "function": "combinationSum",
        "signature": "def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:",
        "arg_types": {"candidates": "List[int]", "target": "int"},
        "return_type": "List[List[int]]",
        "compare": "unordered_nested",
        "tests": [
            {"input": {"candidates": [2, 3, 6, 7], "target": 7}, "output": [[2, 2, 3], [7]]},
            {"input": {"candidates": [2, 3, 5], "target": 8}, "output": [[2, 2, 2, 2], [2, 3, 3], [3, 5]]},
            {"input": {"candidates": [2], "target": 1}, "output": []},
            {"input": {"candidates": [1], "target": 2}, "output": [[1, 1]]},
            {"input": {"candidates": [5, 10], "target": 3}, "output": []},
            {"input": {"candidates": [7, 3], "target": 10}, "output": [[3, 7]]},
            {"input": {"candidates": [1, 2], "target": 40},
             "output": [[1] * (40 - 2 * k) + [2] * k for k in range(21)]},
            {"input": {"candidates": [2, 3], "target": 60},
             "output": [[2] * ((60 - 3 * b) // 2) + [3] * b for b in range(0, 21, 2)]},
        ],
        "solution": '''class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        res = []
        path = []

        def backtrack(start: int, remaining: int) -> None:
            if remaining == 0:
                res.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break
                path.append(candidates[i])
                backtrack(i, remaining - candidates[i])
                path.pop()

        backtrack(0, target)
        return res
''',
        "approach": (
            "**Key insight: generate combinations in non-decreasing candidate order so each multiset has "
            "exactly one representation.** Allowing reuse just means the recursive call keeps the same "
            "`start` index instead of moving to `i + 1`.\n\n"
            "**Algorithm.** Sort `candidates`. `backtrack(start, remaining)`: if `remaining == 0`, record "
            "the path. Otherwise loop `i` from `start`; if `candidates[i] > remaining` break (everything after "
            "is larger too); else push `candidates[i]`, recurse with `(i, remaining - candidates[i])`, pop.\n\n"
            "**Why it works.** Each path is a sorted multiset summing to target, and a sorted multiset "
            "corresponds to exactly one sequence of index choices. The `break` is safe only because the "
            "array is sorted, which is why sorting is not optional.\n\n"
            "**Common mistakes:** recursing with `start + 1` or `0` instead of `i` (the former forbids reuse, "
            "the latter produces permutations of the same multiset); using `continue` where `break` would prune "
            "the whole rest of the loop; not copying `path` when recording.\n\n"
            "**Interview follow-ups:** Only count the combinations instead of listing them? (that is coin-change "
            "DP in O(n * target).) Candidates with duplicates and each used once? (Combination Sum II: sort, "
            "skip equal neighbours, recurse with `i + 1`.) Can you bound the recursion depth? (at most "
            "`target / min(candidates)`.)"
        ),
        "complexity": {"time": "O(n^(T/m)) worst case, where T = target and m = smallest candidate", "space": "O(T/m) recursion depth"},
        "similar": ["combination-sum-ii", "subsets", "coin-change"],
    },
    # --------------------------------------------------------------- permutations
    {
        "id": "permutations",
        "title": "Permutations",
        "difficulty": "Medium",
        "pattern": "Backtracking",
        "tags": ["Array", "Backtracking"],
        "companies": {"google": 3, "apple": 3, "meta": 3, "amazon": 3, "microsoft": 3},
        "description": (
            "Given an array `nums` of **distinct** integers, return every ordering of its elements. "
            "The permutations themselves may be listed in any order."
        ),
        "examples": [
            {"input": "nums = [1,2,3]", "output": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]",
             "explanation": "3! = 6 orderings."},
            {"input": "nums = [0,1]", "output": "[[0,1],[1,0]]"},
            {"input": "nums = [1]", "output": "[[1]]"},
        ],
        "constraints": ["0 <= nums.length <= 7", "-10 <= nums[i] <= 10", "All values are distinct."],
        "hints": [
            "Fix the first element, then permute the rest. How do you keep track of which elements are still available?",
            "Carry a `used` boolean array (or a set). At each depth, try every unused element, mark it, recurse, unmark it.",
            "Space-saving variant: swap nums[i] into position `depth`, recurse on depth + 1, then swap back. No extra `used` array.",
        ],
        "function": "permute",
        "signature": "def permute(self, nums: List[int]) -> List[List[int]]:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "List[List[int]]",
        "compare": "unordered",
        "tests": [
            {"input": {"nums": [1, 2, 3]}, "output": [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]},
            {"input": {"nums": [0, 1]}, "output": [[0, 1], [1, 0]]},
            {"input": {"nums": [1]}, "output": [[1]]},
            {"input": {"nums": []}, "output": [[]]},
            {"input": {"nums": [-2, 0, 9]}, "output": [[-2, 0, 9], [-2, 9, 0], [0, -2, 9], [0, 9, -2], [9, -2, 0], [9, 0, -2]]},
            {"input": {"nums": [1, 2, 3, 4, 5, 6, 7]},
             "output": [list(p) for p in itertools.permutations([1, 2, 3, 4, 5, 6, 7])]},
        ],
        "solution": '''class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []
        path = []
        used = [False] * len(nums)

        def backtrack() -> None:
            if len(path) == len(nums):
                res.append(path[:])
                return
            for i, x in enumerate(nums):
                if used[i]:
                    continue
                used[i] = True
                path.append(x)
                backtrack()
                path.pop()
                used[i] = False

        backtrack()
        return res
''',
        "approach": (
            "**Key insight: a permutation is built position by position, and at each position any element "
            "not yet placed is a legal choice.** That is a depth-n search tree with n! leaves.\n\n"
            "**Algorithm.** Keep `path` and a parallel `used` array. At each call, if `path` is full record a "
            "copy; otherwise for every index `i` with `used[i]` false: mark it, append `nums[i]`, recurse, then "
            "undo both. The undo step is what makes it backtracking rather than a copy-everything approach.\n\n"
            "**Why it works.** Each leaf corresponds to one injective assignment of elements to positions, "
            "i.e. one permutation, and the `used` array guarantees injectivity.\n\n"
            "**Common mistakes:** forgetting to reset `used[i]`; appending `path` without copying; using "
            "`x in path` for the membership test (O(n) per check and wrong if values could repeat).\n\n"
            "**Interview follow-ups:** Duplicates in the input? (sort, and skip `nums[i]` when it equals "
            "`nums[i-1]` and `used[i-1]` is false.) Generate the k-th permutation directly? (factorial number "
            "system, O(n^2).) Produce the next permutation in place in O(n)? (find the rightmost ascent, swap, "
            "reverse the suffix.)"
        ),
        "complexity": {"time": "O(n * n!)", "space": "O(n) for recursion and the used array, excluding output"},
        "similar": ["permutations-ii", "subsets", "next-permutation"],
    },
    # ----------------------------------------------------------------- subsets-ii
    {
        "id": "subsets-ii",
        "title": "Subsets II",
        "difficulty": "Medium",
        "pattern": "Backtracking",
        "tags": ["Array", "Backtracking", "Sorting"],
        "companies": {"google": 2, "meta": 2, "amazon": 2, "microsoft": 1},
        "description": (
            "Given an integer array `nums` that **may contain duplicates**, return every distinct subset "
            "(the power set without repeats).\n\n"
            "Two subsets are the same if they contain the same values with the same multiplicities, so "
            "`[1,2]` and `[2,1]` count as one. Return the subsets in any order."
        ),
        "examples": [
            {"input": "nums = [1,2,2]", "output": "[[],[1],[1,2],[1,2,2],[2],[2,2]]",
             "explanation": "Picking the first 2 alone or the second 2 alone gives the same subset [2], so it appears once."},
            {"input": "nums = [0]", "output": "[[],[0]]"},
        ],
        "constraints": ["0 <= nums.length <= 14", "-10 <= nums[i] <= 10"],
        "hints": [
            "Start from the Subsets solution and think about exactly which branch creates a duplicate.",
            "Sort first. At a given recursion depth, choosing nums[i] when nums[i] == nums[i-1] and i > start repeats a subset you already built from nums[i-1].",
            "So inside the loop: `if i > start and nums[i] == nums[i-1]: continue`. Equal values are still allowed at *different* depths, which is how [2,2] is produced.",
        ],
        "function": "subsetsWithDup",
        "signature": "def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "List[List[int]]",
        "compare": "unordered_nested",
        "tests": [
            {"input": {"nums": [1, 2, 2]}, "output": [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]},
            {"input": {"nums": [0]}, "output": [[], [0]]},
            {"input": {"nums": []}, "output": [[]]},
            {"input": {"nums": [2, 2, 2]}, "output": [[], [2], [2, 2], [2, 2, 2]]},
            {"input": {"nums": [4, 4, 1, 4]},
             "output": [[], [1], [1, 4], [1, 4, 4], [1, 4, 4, 4], [4], [4, 4], [4, 4, 4]]},
            {"input": {"nums": [1, 2, 1, 3]},
             "output": [[], [1], [1, 1], [1, 1, 2], [1, 1, 2, 3], [1, 1, 3], [1, 2], [1, 2, 3], [1, 3],
                        [2], [2, 3], [3]]},
            {"input": {"nums": [7, 1, 6, 2, 5, 3, 4, 4, 3, 5, 2, 6, 1, 7]},
             "output": [sum(([v] * c for v, c in zip(range(1, 8), counts)), [])
                        for counts in itertools.product(range(3), repeat=7)]},
        ],
        "solution": '''class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = []
        path = []

        def backtrack(start: int) -> None:
            res.append(path[:])
            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i - 1]:
                    continue
                path.append(nums[i])
                backtrack(i + 1)
                path.pop()

        backtrack(0)
        return res
''',
        "approach": (
            "**Key insight: after sorting, duplicates sit next to each other, and a repeated subset arises "
            "only when two equal values are chosen as alternatives at the same depth.** Allowing the first "
            "copy and skipping the later ones at that depth removes every duplicate without a hash set.\n\n"
            "**Algorithm.** Sort. Same recursion as Subsets, but inside the loop skip index `i` when "
            "`i > start and nums[i] == nums[i-1]`. The `i > start` condition matters: when `i == start` the "
            "equal value is being chosen at a deeper level (e.g. the second 2 in `[2,2]`), which is legitimate.\n\n"
            "**Why it works.** For any multiset subset, the canonical path takes its copies of each value from "
            "the leftmost positions. Any other path would at some depth pick a copy whose left neighbour is equal "
            "and unpicked, and the skip rule kills exactly those paths.\n\n"
            "**Common mistakes:** dropping the `i > start` guard (then `[2,2]` is never generated); forgetting to "
            "sort; deduplicating with `set(tuple(...))` at the end, which works but is O(2^n) extra and signals "
            "you did not see the structure.\n\n"
            "**Interview follow-ups:** Count distinct subsets without generating them? (product of "
            "`(count_v + 1)` over distinct values.) Same trick for Permutations II and Combination Sum II? "
            "(yes, that is the point of learning it.) Iterative version? (track how many subsets were added in "
            "the previous round and only extend those when the value repeats.)"
        ),
        "complexity": {"time": "O(n * 2^n)", "space": "O(n) excluding output"},
        "similar": ["subsets", "combination-sum-ii", "permutations-ii"],
    },
    # --------------------------------------------------------- combination-sum-ii
    {
        "id": "combination-sum-ii",
        "title": "Combination Sum II",
        "difficulty": "Medium",
        "pattern": "Backtracking",
        "tags": ["Array", "Backtracking", "Sorting"],
        "companies": {"google": 2, "meta": 1, "amazon": 2, "microsoft": 1},
        "description": (
            "You are given a list `candidates` of positive integers, possibly with repeated values, and a "
            "target sum `target`. Find every unique combination of candidates adding up to `target`, where "
            "**each position in the list can be used at most once**.\n\n"
            "Two combinations that contain the same values (as a multiset) are duplicates and only one of them "
            "may be returned. Order of the output does not matter."
        ),
        "examples": [
            {"input": "candidates = [10,1,2,7,6,1,5], target = 8", "output": "[[1,1,6],[1,2,5],[1,7],[2,6]]",
             "explanation": "There are two 1s in the input, so [1,1,6] is valid, but [1,7] must appear only once even though either 1 could be used."},
            {"input": "candidates = [2,5,2,1,2], target = 5", "output": "[[1,2,2],[5]]"},
        ],
        "constraints": ["1 <= candidates.length <= 100", "1 <= candidates[i] <= 50", "1 <= target <= 30"],
        "hints": [
            "Sort the candidates so that equal values are adjacent and you can prune once a value exceeds the remaining sum.",
            "Recurse with start = i + 1 (each position once). To avoid duplicate multisets, skip candidates[i] if it equals candidates[i-1] and i > start.",
            "Use `break` rather than `continue` when candidates[i] > remaining: the list is sorted, so nothing after it fits either.",
        ],
        "function": "combinationSum2",
        "signature": "def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:",
        "arg_types": {"candidates": "List[int]", "target": "int"},
        "return_type": "List[List[int]]",
        "compare": "unordered_nested",
        "tests": [
            {"input": {"candidates": [10, 1, 2, 7, 6, 1, 5], "target": 8}, "output": [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]},
            {"input": {"candidates": [2, 5, 2, 1, 2], "target": 5}, "output": [[1, 2, 2], [5]]},
            {"input": {"candidates": [1], "target": 2}, "output": []},
            {"input": {"candidates": [3, 3, 3], "target": 9}, "output": [[3, 3, 3]]},
            {"input": {"candidates": [1, 1, 1, 1], "target": 2}, "output": [[1, 1]]},
            {"input": {"candidates": [4, 4, 2, 2, 6], "target": 8}, "output": [[2, 2, 4], [2, 6], [4, 4]]},
            {"input": {"candidates": [1] * 20 + [2] * 20, "target": 30},
             "output": [[1] * (30 - 2 * k) + [2] * k for k in range(5, 16)]},
        ],
        "solution": '''class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        res = []
        path = []

        def backtrack(start: int, remaining: int) -> None:
            if remaining == 0:
                res.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                path.append(candidates[i])
                backtrack(i + 1, remaining - candidates[i])
                path.pop()

        backtrack(0, target)
        return res
''',
        "approach": (
            "**Key insight: combine the two standard tricks, sorted-break pruning from Combination Sum and "
            "same-depth duplicate skipping from Subsets II.** Each position is used once, so the recursive call "
            "advances to `i + 1`.\n\n"
            "**Algorithm.** Sort. `backtrack(start, remaining)`: record on `remaining == 0`. Loop `i` from "
            "`start`; `break` if `candidates[i] > remaining`; `continue` if `i > start` and "
            "`candidates[i] == candidates[i-1]`; otherwise push, recurse on `(i + 1, remaining - candidates[i])`, "
            "pop.\n\n"
            "**Why it works.** Sorting makes the break valid and makes duplicates adjacent. The skip rule ensures "
            "that among equal values, the combination always takes a prefix of the run, so each multiset has one "
            "canonical path.\n\n"
            "**Common mistakes:** checking the skip rule before the break (still correct but order the cheap "
            "prune first); writing `i > 0` instead of `i > start`, which wrongly forbids using two equal values in "
            "the same combination; forgetting that the input `[1]*20 + [2]*20` explodes without dedup.\n\n"
            "**Interview follow-ups:** Why is the `[1]*20 + [2]*20` style input the real test of your "
            "solution? (without the skip rule you explore 2^40 branches.) How does the complexity compare to "
            "Combination Sum? (depth bounded by n here, by target/min there.) Could a counting approach (value -> "
            "frequency) be cleaner? (yes: iterate distinct values and choose how many copies to take, 0..freq.)"
        ),
        "complexity": {"time": "O(2^n) worst case", "space": "O(n) excluding output"},
        "similar": ["combination-sum", "subsets-ii"],
    },
    # ---------------------------------------------------------------- word-search
    {
        "id": "word-search",
        "title": "Word Search",
        "difficulty": "Medium",
        "pattern": "Backtracking",
        "tags": ["Array", "Backtracking", "Matrix", "DFS"],
        "companies": {"google": 3, "apple": 3, "meta": 4, "amazon": 4, "microsoft": 4},
        "description": (
            "You are given an `m x n` grid of lowercase or uppercase letters `board` and a string `word`. "
            "Decide whether `word` can be traced in the grid by starting at any cell and repeatedly stepping to "
            "a **horizontally or vertically adjacent** cell, spelling the word letter by letter.\n\n"
            "A cell may be used at most once within a single trace. Return `True` if such a path exists."
        ),
        "examples": [
            {"input": "board = [[\"c\",\"a\",\"t\"],[\"o\",\"d\",\"s\"],[\"g\",\"o\",\"d\"]], word = \"cats\"",
             "output": "true", "explanation": "c(0,0) -> a(0,1) -> t(0,2) -> s(1,2)."},
            {"input": "board = [[\"c\",\"a\",\"t\"],[\"o\",\"d\",\"s\"],[\"g\",\"o\",\"d\"]], word = \"dog\"",
             "output": "true", "explanation": "d(1,1) -> o(2,1) -> g(2,0)."},
            {"input": "board = [[\"c\",\"a\",\"t\"],[\"o\",\"d\",\"s\"],[\"g\",\"o\",\"d\"]], word = \"catso\"",
             "output": "false", "explanation": "After reaching s at (1,2) no unused neighbour holds an o."},
        ],
        "constraints": ["1 <= m, n <= 50", "1 <= word.length <= 30", "board and word contain only letters"],
        "hints": [
            "Try every cell as a starting point and run a depth-first search that matches one character per step.",
            "Mark the current cell as visited before exploring its neighbours, and restore it afterwards. Overwriting the cell with a sentinel like '#' avoids a separate visited set.",
            "Return True as soon as the index reaches len(word). Check bounds and the character match at the top of the recursive call so the four neighbour calls stay symmetrical.",
        ],
        "function": "exist",
        "signature": "def exist(self, board: List[List[str]], word: str) -> bool:",
        "arg_types": {"board": "List[List[str]]", "word": "str"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"board": [["c", "a", "t"], ["o", "d", "s"], ["g", "o", "d"]], "word": "cats"}, "output": True},
            {"input": {"board": [["c", "a", "t"], ["o", "d", "s"], ["g", "o", "d"]], "word": "dog"}, "output": True},
            {"input": {"board": [["c", "a", "t"], ["o", "d", "s"], ["g", "o", "d"]], "word": "catso"}, "output": False},
            {"input": {"board": [["a"]], "word": "a"}, "output": True},
            {"input": {"board": [["a"]], "word": "aa"}, "output": False},
            {"input": {"board": [["a", "a"]], "word": "aaa"}, "output": False},
            {"input": {"board": [["a", "b"], ["c", "d"]], "word": "abdc"}, "output": True},
            {"input": {"board": [["a", "b"], ["c", "d"]], "word": "acd"}, "output": True},
            {"input": {"board": [["a", "b"], ["c", "d"]], "word": "ad"}, "output": False},
            {"input": {"board": [[chr(97 + (r + c) % 26) for c in range(40)] for r in range(40)],
                       "word": "abcdefghijklmnopqrstuvwxyza"}, "output": True},
            {"input": {"board": [[chr(97 + (r + c) % 26) for c in range(40)] for r in range(40)],
                       "word": "zzz"}, "output": False},
        ],
        "solution": '''class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])

        def dfs(r: int, c: int, k: int) -> bool:
            if k == len(word):
                return True
            if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[k]:
                return False
            saved = board[r][c]
            board[r][c] = "#"
            found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1)
                     or dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))
            board[r][c] = saved
            return found

        return any(dfs(r, c, 0) for r in range(m) for c in range(n))
''',
        "approach": (
            "**Key insight: a path spelling the word is a depth-first search where the next character is "
            "the constraint, and the cell must be temporarily marked so the path never revisits it.**\n\n"
            "**Algorithm.** For every cell, call `dfs(r, c, 0)`. `dfs` succeeds when `k == len(word)`; fails "
            "when out of bounds or `board[r][c] != word[k]`; otherwise overwrites the cell with `#`, tries the "
            "four neighbours with `k + 1`, restores the letter, and returns whether any neighbour succeeded.\n\n"
            "**Why it works.** Every path of length `len(word)` that spells the word with distinct cells is "
            "explored by some sequence of recursive calls, and the sentinel prevents cycles. Restoring the cell is "
            "what allows a later start or a sibling branch to reuse it.\n\n"
            "**Common mistakes:** forgetting to restore the cell (later searches see `#`); checking the match "
            "after marking (then the mark is applied to non-matching cells); not short-circuiting with `or` so all "
            "four branches run even after success.\n\n"
            "**Interview follow-ups:** Many words on one board? (Word Search II: build a trie of the words and "
            "walk the board once per cell, pruning trie branches as words are found.) Cheap pre-checks? (compare "
            "letter frequencies of the word with the board; search from the rarer end of the word.) Worst-case "
            "board? (all identical letters with a word that fails at the last character is exponential, "
            "O(m * n * 3^L).)"
        ),
        "complexity": {"time": "O(m * n * 3^L), L = len(word)", "space": "O(L) recursion"},
        "similar": ["word-search-ii", "number-of-islands", "palindrome-partitioning"],
    },
    # ------------------------------------------------------ palindrome-partitioning
    {
        "id": "palindrome-partitioning",
        "title": "Palindrome Partitioning",
        "difficulty": "Medium",
        "pattern": "Backtracking",
        "tags": ["String", "Backtracking", "Dynamic Programming"],
        "companies": {"google": 2, "meta": 2, "amazon": 2, "microsoft": 1},
        "description": (
            "Split the string `s` into consecutive pieces so that **every piece reads the same forwards and "
            "backwards**. Return all such partitions.\n\n"
            "Each partition is a list of substrings that concatenate back to `s`. The partitions may be "
            "returned in any order, but the pieces inside a partition must stay in their original order."
        ),
        "examples": [
            {"input": "s = \"aab\"", "output": "[[\"a\",\"a\",\"b\"],[\"aa\",\"b\"]]",
             "explanation": "\"aab\" itself is not a palindrome, so it cannot be a single piece."},
            {"input": "s = \"a\"", "output": "[[\"a\"]]"},
            {"input": "s = \"aba\"", "output": "[[\"a\",\"b\",\"a\"],[\"aba\"]]"},
        ],
        "constraints": ["1 <= s.length <= 16", "s consists of lowercase English letters"],
        "hints": [
            "Choose where the first piece ends. If s[start:end] is a palindrome, recurse on the remainder.",
            "Recurse with a `start` index; for each `end` > start, check the palindrome, push the piece, recurse from `end`, pop.",
            "Palindrome checks are O(L) each; precomputing a 2-D `is_pal[i][j]` table in O(n^2) makes each check O(1), though for n <= 16 the direct check is fine.",
        ],
        "function": "partition",
        "signature": "def partition(self, s: str) -> List[List[str]]:",
        "arg_types": {"s": "str"},
        "return_type": "List[List[str]]",
        "compare": "unordered",
        "tests": [
            {"input": {"s": "aab"}, "output": [["a", "a", "b"], ["aa", "b"]]},
            {"input": {"s": "a"}, "output": [["a"]]},
            {"input": {"s": "aba"}, "output": [["a", "b", "a"], ["aba"]]},
            {"input": {"s": "abc"}, "output": [["a", "b", "c"]]},
            {"input": {"s": "aaa"}, "output": [["a", "a", "a"], ["a", "aa"], ["aa", "a"], ["aaa"]]},
            {"input": {"s": "abba"}, "output": [["a", "b", "b", "a"], ["a", "bb", "a"], ["abba"]]},
            {"input": {"s": "a" * 14},
             "output": [["a" * (b - a) for a, b in zip((0,) + cuts, cuts + (14,))]
                        for k in range(14) for cuts in itertools.combinations(range(1, 14), k)]},
        ],
        "solution": '''class Solution:
    def partition(self, s: str) -> List[List[str]]:
        n = len(s)
        res = []
        path = []

        def is_pal(i: int, j: int) -> bool:
            while i < j:
                if s[i] != s[j]:
                    return False
                i += 1
                j -= 1
            return True

        def backtrack(start: int) -> None:
            if start == n:
                res.append(path[:])
                return
            for end in range(start, n):
                if is_pal(start, end):
                    path.append(s[start:end + 1])
                    backtrack(end + 1)
                    path.pop()

        backtrack(0)
        return res
''',
        "approach": (
            "**Key insight: a partition is determined by where each piece ends, so recurse on the start index "
            "and only extend with pieces that are palindromes.** Non-palindromic prefixes are pruned immediately, "
            "which is what makes this backtracking rather than enumerating all 2^(n-1) cut sets.\n\n"
            "**Algorithm.** `backtrack(start)`: if `start == n` record the path. Otherwise for each `end` in "
            "`[start, n)`, if `s[start..end]` is a palindrome, push it, recurse from `end + 1`, pop.\n\n"
            "**Why it works.** Every valid partition corresponds to a unique sequence of palindrome end points, "
            "and every such sequence is visited exactly once. The palindrome test is the only pruning needed.\n\n"
            "**Common mistakes:** off-by-one on the slice (`s[start:end+1]`); recomputing palindrome checks "
            "without noticing the O(n^2) DP table is available; returning references to `path`.\n\n"
            "**Interview follow-ups:** Minimum number of cuts instead of all partitions? (Palindrome "
            "Partitioning II, O(n^2) DP.) Precompute `is_pal` with the expand-from-the-inside recurrence "
            "`is_pal[i][j] = s[i]==s[j] and is_pal[i+1][j-1]`? (yes, fill by increasing length.) Worst case? "
            "(a string of one repeated letter: every split is valid, 2^(n-1) partitions.)"
        ),
        "complexity": {"time": "O(n * 2^n)", "space": "O(n) recursion, plus O(n^2) if a palindrome table is used"},
        "similar": ["palindrome-partitioning-ii", "word-break", "subsets"],
    },
    # ---------------------------------------- letter-combinations-of-a-phone-number
    {
        "id": "letter-combinations-of-a-phone-number",
        "title": "Letter Combinations of a Phone Number",
        "difficulty": "Medium",
        "pattern": "Backtracking",
        "tags": ["String", "Backtracking", "Hash Table"],
        "companies": {"google": 3, "apple": 2, "meta": 3, "amazon": 4, "microsoft": 3},
        "description": (
            "On a classic phone keypad each digit from 2 to 9 maps to letters: 2 -> abc, 3 -> def, 4 -> ghi, "
            "5 -> jkl, 6 -> mno, 7 -> pqrs, 8 -> tuv, 9 -> wxyz.\n\n"
            "Given a string `digits` containing only characters `2`-`9`, return every string that can be typed "
            "by picking one letter for each digit, in order. If `digits` is empty return an empty list. "
            "The results may be in any order."
        ),
        "examples": [
            {"input": "digits = \"23\"", "output": "[\"ad\",\"ae\",\"af\",\"bd\",\"be\",\"bf\",\"cd\",\"ce\",\"cf\"]",
             "explanation": "3 choices for '2' times 3 choices for '3'."},
            {"input": "digits = \"\"", "output": "[]"},
            {"input": "digits = \"2\"", "output": "[\"a\",\"b\",\"c\"]"},
        ],
        "constraints": ["0 <= digits.length <= 7", "digits[i] is one of '2'..'9'"],
        "hints": [
            "This is a Cartesian product: one letter per digit, independent choices.",
            "Recurse over the digit index; for each letter of the current digit, append it and recurse on the next digit. Record when the index reaches len(digits).",
            "Remember the empty-input special case: no digits means no combinations, not one empty string.",
        ],
        "function": "letterCombinations",
        "signature": "def letterCombinations(self, digits: str) -> List[str]:",
        "arg_types": {"digits": "str"},
        "return_type": "List[str]",
        "compare": "unordered",
        "tests": [
            {"input": {"digits": "23"}, "output": ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]},
            {"input": {"digits": ""}, "output": []},
            {"input": {"digits": "2"}, "output": ["a", "b", "c"]},
            {"input": {"digits": "79"}, "output": ["".join(p) for p in itertools.product("pqrs", "wxyz")]},
            {"input": {"digits": "99"}, "output": ["".join(p) for p in itertools.product("wxyz", "wxyz")]},
            {"input": {"digits": "2345679"},
             "output": ["".join(p) for p in itertools.product("abc", "def", "ghi", "jkl", "mno", "pqrs", "wxyz")]},
        ],
        "solution": '''class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        keypad = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
                  "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
        res = []
        path = []

        def backtrack(i: int) -> None:
            if i == len(digits):
                res.append("".join(path))
                return
            for ch in keypad[digits[i]]:
                path.append(ch)
                backtrack(i + 1)
                path.pop()

        backtrack(0)
        return res
''',
        "approach": (
            "**Key insight: the answer is the Cartesian product of the letter groups, one group per digit.** "
            "Backtracking over the digit index enumerates that product with O(L) extra memory.\n\n"
            "**Algorithm.** Map each digit to its letters. `backtrack(i)`: when `i == len(digits)` join the path "
            "and record it; otherwise for each letter of `digits[i]` push, recurse on `i + 1`, pop. Return `[]` "
            "immediately for empty input.\n\n"
            "**Why it works.** Each leaf fixes one letter per position, and distinct leaf paths give distinct "
            "strings, so every combination appears exactly once.\n\n"
            "**Common mistakes:** returning `[\"\"]` for empty input; building strings by concatenation at every "
            "level (fine for L <= 7 but O(L^2) per leaf in general); forgetting that 7 and 9 have four letters.\n\n"
            "**Interview follow-ups:** Iterative BFS version? (start with `[\"\"]` and for each digit extend "
            "every partial string.) Only count the combinations? (product of group sizes, O(L).) Filter to real "
            "dictionary words, as T9 does? (walk a trie of the dictionary alongside the digits and prune dead "
            "branches.)"
        ),
        "complexity": {"time": "O(L * 4^L)", "space": "O(L) excluding output"},
        "similar": ["subsets", "generate-parentheses", "combinations"],
    },
    # -------------------------------------------------------------------- n-queens
    {
        "id": "n-queens",
        "title": "N-Queens",
        "difficulty": "Hard",
        "pattern": "Backtracking",
        "tags": ["Backtracking", "Array"],
        "companies": {"google": 3, "apple": 2, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "Place `n` chess queens on an `n x n` board so that **no two queens share a row, a column, or a "
            "diagonal**. Return every distinct arrangement.\n\n"
            "Each arrangement is a list of `n` strings, one per row, where `Q` marks a queen and `.` an empty "
            "square. The arrangements may be returned in any order."
        ),
        "examples": [
            {"input": "n = 4", "output": "[[\".Q..\",\"...Q\",\"Q...\",\"..Q.\"],[\"..Q.\",\"Q...\",\"...Q\",\".Q..\"]]",
             "explanation": "The two 4x4 solutions are mirror images of each other."},
            {"input": "n = 1", "output": "[[\"Q\"]]"},
            {"input": "n = 3", "output": "[]", "explanation": "No arrangement exists for n = 2 or n = 3."},
        ],
        "constraints": ["1 <= n <= 9"],
        "hints": [
            "Place exactly one queen per row, top to bottom. Then rows never conflict and you only need to track columns and diagonals.",
            "A queen at (r, c) occupies column c, 'down-right' diagonal r - c, and 'down-left' diagonal r + c. Keep three sets of occupied values.",
            "For each row try every column not blocked by the three sets; add to the sets, recurse to the next row, remove. When row == n, render the board from the chosen column per row.",
        ],
        "function": "solveNQueens",
        "signature": "def solveNQueens(self, n: int) -> List[List[str]]:",
        "arg_types": {"n": "int"},
        "return_type": "List[List[str]]",
        "compare": "unordered",
        "tests": [
            {"input": {"n": 4}, "output": [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]},
            {"input": {"n": 1}, "output": [["Q"]]},
            {"input": {"n": 3}, "output": []},
            {"input": {"n": 2}, "output": []},
            {"input": {"n": 5}, "output": _queens_brute(5)},
            {"input": {"n": 6}, "output": _queens_brute(6)},
            {"input": {"n": 8}, "output": _queens_brute(8)},
        ],
        "solution": '''class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        res = []
        cols_used = set()
        diag1 = set()  # r - c
        diag2 = set()  # r + c
        placement = []  # placement[r] = column of the queen in row r

        def backtrack(r: int) -> None:
            if r == n:
                res.append(["." * c + "Q" + "." * (n - c - 1) for c in placement])
                return
            for c in range(n):
                if c in cols_used or (r - c) in diag1 or (r + c) in diag2:
                    continue
                cols_used.add(c); diag1.add(r - c); diag2.add(r + c)
                placement.append(c)
                backtrack(r + 1)
                placement.pop()
                cols_used.remove(c); diag1.remove(r - c); diag2.remove(r + c)

        backtrack(0)
        return res
''',
        "approach": (
            "**Key insight: one queen per row, so the search is over columns, and the three kinds of attack "
            "lines (column, r - c diagonal, r + c diagonal) can each be tracked with a set for O(1) conflict "
            "checks.**\n\n"
            "**Algorithm.** `backtrack(r)`: if `r == n` render the board from the per-row column list. Otherwise "
            "for each column `c` not in `cols`, `r - c` not in `diag1`, `r + c` not in `diag2`: add all three, "
            "push `c`, recurse to `r + 1`, then undo. Return the collected boards.\n\n"
            "**Why it works.** Two queens attack along a column iff they share `c`, along a diagonal iff they "
            "share `r - c` or `r + c`. Since rows are distinct by construction, those three sets capture every "
            "conflict, and the search enumerates every conflict-free assignment exactly once.\n\n"
            "**Common mistakes:** scanning previously placed queens for conflicts (O(n) per check, still passes "
            "but misses the point); mixing up the two diagonal keys; rendering the board with the wrong row/column "
            "orientation; forgetting to undo one of the three sets.\n\n"
            "**Interview follow-ups:** Only count the solutions (N-Queens II)? (same search, increment a counter; "
            "bitmasks for the three sets make it very fast.) Exploit symmetry? (only try the first n/2 columns "
            "in row 0 and mirror, handling the middle column for odd n.) How large can n get? (the count grows "
            "super-exponentially; backtracking is practical to roughly n = 15.)"
        ),
        "complexity": {"time": "O(n!) upper bound on the search tree", "space": "O(n) for sets and recursion, excluding output"},
        "similar": ["n-queens-ii", "sudoku-solver", "permutations"],
    },
    # -------------------------------------------------------- generate-parentheses
    {
        "id": "generate-parentheses",
        "title": "Generate Parentheses",
        "difficulty": "Medium",
        "pattern": "Backtracking",
        "tags": ["String", "Backtracking", "Dynamic Programming"],
        "companies": {"google": 3, "apple": 2, "meta": 3, "amazon": 4, "microsoft": 3},
        "description": (
            "Given an integer `n`, produce every string made of exactly `n` opening and `n` closing parentheses "
            "that is **well-formed**: reading left to right, the number of `)` seen never exceeds the number of "
            "`(`, and the totals match at the end.\n\n"
            "Return the strings in any order."
        ),
        "examples": [
            {"input": "n = 3", "output": "[\"((()))\",\"(()())\",\"(())()\",\"()(())\",\"()()()\"]",
             "explanation": "There are 5 well-formed strings of length 6 (the third Catalan number)."},
            {"input": "n = 1", "output": "[\"()\"]"},
        ],
        "constraints": ["1 <= n <= 10"],
        "hints": [
            "Build the string one character at a time. When is it still possible to add '(' ? When is it legal to add ')' ?",
            "Track how many opens and closes you have used. Add '(' if open < n; add ')' if close < open.",
            "Record the string when its length reaches 2n. Those two rules alone guarantee every produced string is balanced, so there is nothing to validate at the end.",
        ],
        "function": "generateParenthesis",
        "signature": "def generateParenthesis(self, n: int) -> List[str]:",
        "arg_types": {"n": "int"},
        "return_type": "List[str]",
        "compare": "unordered",
        "tests": [
            {"input": {"n": 3}, "output": ["((()))", "(()())", "(())()", "()(())", "()()()"]},
            {"input": {"n": 1}, "output": ["()"]},
            {"input": {"n": 2}, "output": ["(())", "()()"]},
            {"input": {"n": 4}, "output": _balanced(4)},
            {"input": {"n": 6}, "output": _balanced(6)},
            {"input": {"n": 10}, "output": _balanced(10)},
        ],
        "solution": '''class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        res = []
        path = []

        def backtrack(open_count: int, close_count: int) -> None:
            if len(path) == 2 * n:
                res.append("".join(path))
                return
            if open_count < n:
                path.append("(")
                backtrack(open_count + 1, close_count)
                path.pop()
            if close_count < open_count:
                path.append(")")
                backtrack(open_count, close_count + 1)
                path.pop()

        backtrack(0, 0)
        return res
''',
        "approach": (
            "**Key insight: a prefix can be extended to a balanced string iff it has used at most n opens and "
            "no more closes than opens.** Enforcing those two rules while building means the search never "
            "generates an invalid string, so the recursion tree has exactly as many leaves as answers.\n\n"
            "**Algorithm.** `backtrack(open, close)`: record when the path has length `2n`. Otherwise, if "
            "`open < n` push `(` and recurse; if `close < open` push `)` and recurse; pop after each.\n\n"
            "**Why it works.** The conditions are exactly the characterisation of prefixes of Dyck words. "
            "Every balanced string of length 2n has all its prefixes valid, so it is reached; every leaf has "
            "`open == close == n` and no bad prefix, so it is balanced.\n\n"
            "**Common mistakes:** generating all 2^(2n) strings and filtering (exponentially slower); using "
            "`close < n` instead of `close < open`; string concatenation in the recursion is acceptable here but "
            "the list-plus-join form is cleaner to reason about.\n\n"
            "**Interview follow-ups:** How many results are there? (the Catalan number "
            "C(n) = (2n)! / ((n+1)! n!).) A non-recursive construction? (closure form: every string is "
            "`(` A `)` B with A and B balanced of smaller sizes, which gives a DP over n.) Count only? "
            "(closed-form Catalan, or the DP in O(n^2).)"
        ),
        "complexity": {"time": "O(4^n / sqrt(n)) output-sensitive, i.e. proportional to the number of results times n", "space": "O(n) recursion excluding output"},
        "similar": ["valid-parentheses", "letter-combinations-of-a-phone-number", "subsets"],
    },
]
