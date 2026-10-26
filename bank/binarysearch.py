"""Binary Search pattern problems. See SCHEMA.md for the dict format."""

PROBLEMS = [
    {
        "id": "binary-search",
        "title": "Binary Search",
        "difficulty": "Easy",
        "pattern": "Binary Search",
        "tags": ["Array", "Binary Search"],
        "companies": {"google": 2, "apple": 3, "meta": 1, "amazon": 3, "microsoft": 3},
        "description": (
            "You are given an array `nums` of **distinct** integers sorted in ascending order and a value `target`. "
            "Return the index of `target` in `nums`, or `-1` if it is not present.\n\n"
            "Your algorithm must run in **O(log n)** time."
        ),
        "examples": [
            {"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4"},
            {"input": "nums = [-1,0,3,5,9,12], target = 2", "output": "-1"},
        ],
        "constraints": ["1 <= nums.length <= 10^4", "-10^4 < nums[i], target < 10^4", "All values in nums are distinct and sorted ascending"],
        "hints": [
            "Comparing the target with the middle element tells you which half it cannot be in.",
            "Maintain an inclusive window [lo, hi]. Compute mid, and move lo or hi past mid depending on the comparison.",
            "Loop while lo <= hi. Use lo + (hi - lo) // 2 for mid if you are in a language with fixed-width integers.",
        ],
        "function": "search",
        "signature": "def search(self, nums: List[int], target: int) -> int:",
        "arg_types": {"nums": "List[int]", "target": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [-1, 0, 3, 5, 9, 12], "target": 9}, "output": 4},
            {"input": {"nums": [-1, 0, 3, 5, 9, 12], "target": 2}, "output": -1},
            {"input": {"nums": [5], "target": 5}, "output": 0},
            {"input": {"nums": [5], "target": -5}, "output": -1},
            {"input": {"nums": [1, 3], "target": 3}, "output": 1},
            {"input": {"nums": [1, 3], "target": 0}, "output": -1},
            {"input": {"nums": [-9, -7, -5, -3], "target": -9}, "output": 0},
            {"input": {"nums": list(range(0, 200000, 2)), "target": 123456}, "output": 61728},
            {"input": {"nums": list(range(0, 200000, 2)), "target": 123457}, "output": -1},
        ],
        "solution": '''\
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1
''',
        "approach": (
            "**Key insight: in a sorted array one comparison with the middle element rules out half of the remaining "
            "candidates.** Halving repeatedly gives O(log n).\n\n"
            "**Algorithm.** Keep an inclusive search window `[lo, hi]`. While it is non-empty, look at `mid`. If it holds the "
            "target, return `mid`. If it is smaller, the target can only be to the right, so `lo = mid + 1`; otherwise "
            "`hi = mid - 1`. If the window empties, the target is absent.\n\n"
            "**Why it works.** Invariant: if the target is in the array, it lies within `[lo, hi]`. Each iteration preserves "
            "the invariant and shrinks the window, so the loop terminates after at most `log2(n) + 1` steps.\n\n"
            "**Common mistakes.** Off-by-one choices: using `lo < hi` with `hi = len(nums) - 1` skips the last candidate; "
            "setting `hi = mid` (not `mid - 1`) with `lo <= hi` can loop forever. Mixing inclusive and exclusive conventions. "
            "In C-like languages, `(lo + hi) / 2` can overflow.\n\n"
            "**Interview follow-ups.** (1) Return the insertion index when the target is absent (lower bound). "
            "(2) Duplicates allowed: return the first or last occurrence. (3) The array is sorted but has unknown length "
            "(exponential search to find a bound, then binary search). Be ready to write both the `lo <= hi` and the "
            "half-open `lo < hi` templates without hesitation; interviewers watch for this fluency."
        ),
        "complexity": {"time": "O(log n)", "space": "O(1)"},
        "similar": ["search-insert-position", "find-first-and-last-position-of-element", "search-in-rotated-sorted-array"],
        "followups": ["Lower bound / insertion position.", "Unknown-length sorted array."],
    },
    {
        "id": "search-a-2d-matrix",
        "title": "Search a 2D Matrix",
        "difficulty": "Medium",
        "pattern": "Binary Search",
        "tags": ["Array", "Binary Search", "Matrix"],
        "companies": {"google": 2, "apple": 2, "meta": 1, "amazon": 3, "microsoft": 3},
        "description": (
            "You are given an `m x n` integer matrix with two properties: each row is sorted ascending, and the first "
            "element of every row is greater than the last element of the row above it.\n\n"
            "Given an integer `target`, return `true` if it appears in the matrix and `false` otherwise. "
            "Aim for **O(log(m * n))** time."
        ),
        "examples": [
            {"input": "matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3", "output": "true"},
            {"input": "matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13", "output": "false"},
        ],
        "constraints": ["1 <= m, n <= 100", "-10^4 <= matrix[i][j], target <= 10^4"],
        "hints": [
            "Because rows are sorted and each row starts after the previous one ends, reading the matrix row by row gives one fully sorted list.",
            "Binary search over the virtual index range [0, m*n). Map index i to matrix[i // n][i % n].",
            "An alternative two-step approach (binary search for the row, then within the row) is also O(log m + log n).",
        ],
        "function": "searchMatrix",
        "signature": "def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:",
        "arg_types": {"matrix": "List[List[int]]", "target": "int"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"matrix": [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], "target": 3}, "output": True},
            {"input": {"matrix": [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], "target": 13}, "output": False},
            {"input": {"matrix": [[1]], "target": 1}, "output": True},
            {"input": {"matrix": [[1]], "target": 2}, "output": False},
            {"input": {"matrix": [[1, 3]], "target": 3}, "output": True},
            {"input": {"matrix": [[1], [3]], "target": 2}, "output": False},
            {"input": {"matrix": [[-5, -3], [-1, 0]], "target": -1}, "output": True},
            {"input": {"matrix": [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], "target": 60}, "output": True},
            {"input": {"matrix": [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], "target": 0}, "output": False},
            {"input": {"matrix": [[i * 100 + j for j in range(100)] for i in range(100)], "target": 5555}, "output": True},
            {"input": {"matrix": [[2 * (i * 100 + j) for j in range(100)] for i in range(100)], "target": 5555}, "output": False},
        ],
        "solution": '''\
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        lo, hi = 0, m * n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            val = matrix[mid // n][mid % n]
            if val == target:
                return True
            if val < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return False
''',
        "approach": (
            "**Key insight: the two ordering properties mean the matrix, read row-major, is a single sorted array of "
            "`m * n` elements.** You never need to materialise it; index arithmetic does the mapping.\n\n"
            "**Algorithm.** Binary search over the virtual indices `0 .. m*n - 1`. For index `mid`, the element is "
            "`matrix[mid // n][mid % n]`. Compare with the target and shrink the window as in ordinary binary search.\n\n"
            "**Why it works.** The mapping `i -> (i // n, i % n)` is a bijection between virtual indices and cells that "
            "preserves row-major order, and row-major order is sorted by the problem's guarantee.\n\n"
            "**Common mistakes.** Swapping `//` and `%` (row is the quotient, column the remainder). Using `m` instead of `n` "
            "as the divisor. Treating the matrix as Search a 2D Matrix II, where only rows and columns are sorted and the "
            "staircase walk from the top-right corner is required instead.\n\n"
            "**Interview follow-ups.** (1) Search a 2D Matrix II (rows and columns sorted but rows overlap): O(m + n) "
            "staircase search. (2) Count elements smaller than `target`. (3) Kth smallest element in a sorted matrix, which "
            "uses binary search on the value range plus a counting walk."
        ),
        "complexity": {"time": "O(log(m * n))", "space": "O(1)"},
        "similar": ["binary-search", "search-a-2d-matrix-ii", "kth-smallest-element-in-a-sorted-matrix"],
        "followups": ["Rows and columns sorted independently.", "Kth smallest in a sorted matrix."],
    },
    {
        "id": "koko-eating-bananas",
        "title": "Koko Eating Bananas",
        "difficulty": "Medium",
        "pattern": "Binary Search",
        "tags": ["Array", "Binary Search"],
        "companies": {"google": 3, "apple": 1, "meta": 2, "amazon": 2, "microsoft": 1},
        "description": (
            "There are `n` piles of bananas; `piles[i]` is the number of bananas in pile `i`. Koko chooses an eating speed "
            "`k` (bananas per hour). Each hour she picks one pile and eats `k` bananas from it; if the pile has fewer than "
            "`k` left she finishes it and does not touch another pile that hour.\n\n"
            "Return the **minimum integer speed `k`** that lets her eat every banana within `h` hours. It is guaranteed "
            "that `h >= n`, so a solution always exists."
        ),
        "examples": [
            {"input": "piles = [3,6,7,11], h = 8", "output": "4", "explanation": "At speed 4 the piles take 1 + 2 + 2 + 3 = 8 hours. Speed 3 would need 10."},
            {"input": "piles = [30,11,23,4,20], h = 5", "output": "30", "explanation": "With only 5 hours for 5 piles she must finish each pile in one hour."},
            {"input": "piles = [30,11,23,4,20], h = 6", "output": "23"},
        ],
        "constraints": ["1 <= piles.length <= 10^4", "piles.length <= h <= 10^9", "1 <= piles[i] <= 10^9"],
        "hints": [
            "If speed k is fast enough, every speed above k is fast enough too. That monotonic yes/no structure is what binary search needs.",
            "The answer lies in [1, max(piles)]. For a candidate k, the total hours is the sum of ceil(pile / k).",
            "Binary search for the smallest k whose hours <= h. Use the half-open template: if feasible, hi = mid, else lo = mid + 1.",
        ],
        "function": "minEatingSpeed",
        "signature": "def minEatingSpeed(self, piles: List[int], h: int) -> int:",
        "arg_types": {"piles": "List[int]", "h": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"piles": [3, 6, 7, 11], "h": 8}, "output": 4},
            {"input": {"piles": [30, 11, 23, 4, 20], "h": 5}, "output": 30},
            {"input": {"piles": [30, 11, 23, 4, 20], "h": 6}, "output": 23},
            {"input": {"piles": [1], "h": 1}, "output": 1},
            {"input": {"piles": [1000000000], "h": 2}, "output": 500000000},
            {"input": {"piles": [2, 2], "h": 4}, "output": 1},
            {"input": {"piles": [312884470], "h": 968709470}, "output": 1},
            {"input": {"piles": list(range(1, 5001)), "h": 5000}, "output": 5000},
            {"input": {"piles": list(range(1, 5001)), "h": 10000}, "output": 1667},
            {"input": {"piles": [1000000000] * 5000, "h": 1000000000}, "output": 5000},
        ],
        "solution": '''\
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        def hours_needed(k: int) -> int:
            return sum((p + k - 1) // k for p in piles)

        lo, hi = 1, max(piles)
        while lo < hi:
            mid = (lo + hi) // 2
            if hours_needed(mid) <= h:
                hi = mid          # mid works; try slower
            else:
                lo = mid + 1      # too slow
        return lo
''',
        "approach": (
            "**Key insight: binary search on the answer.** Feasibility is monotonic in the speed: if `k` finishes in time, "
            "any faster speed does too. So the speeds form a `False...False True...True` sequence and we want the first `True`.\n\n"
            "**Algorithm.** The speed is at least 1 and never needs to exceed `max(piles)` (then every pile takes one hour). "
            "Binary search that range; for each candidate compute `sum(ceil(p / k))` and compare with `h`. Keep the smallest "
            "feasible speed.\n\n"
            "**Why it works.** The predicate `hours(k) <= h` is monotone, so binary search over the predicate finds its "
            "boundary in O(log max(piles)) checks, each O(n).\n\n"
            "**Common mistakes.** Using floating-point `math.ceil(p / k)` (fine in Python, overflow-prone elsewhere); the "
            "integer form `(p + k - 1) // k` is preferred. Starting `lo` at 0 and dividing by zero. Early-exiting the sum "
            "when it exceeds `h` is a nice micro-optimisation, not a correctness issue. Searching over hours instead of speed.\n\n"
            "**Interview follow-ups.** (1) Tighten the lower bound to `ceil(sum(piles) / h)` and explain why it is valid. "
            "(2) Same template: Capacity to Ship Packages Within D Days, Minimum Days to Make m Bouquets, Split Array Largest Sum. "
            "(3) What if `h < n`? (No valid answer; discuss returning -1.)"
        ),
        "complexity": {"time": "O(n log M) where M = max(piles)", "space": "O(1)"},
        "similar": ["split-array-largest-sum", "capacity-to-ship-packages-within-d-days", "minimum-number-of-days-to-make-m-bouquets"],
        "followups": ["Tighter search bounds.", "Generalise the binary-search-on-answer template."],
    },
    {
        "id": "find-minimum-in-rotated-sorted-array",
        "title": "Find Minimum in Rotated Sorted Array",
        "difficulty": "Medium",
        "pattern": "Binary Search",
        "tags": ["Array", "Binary Search"],
        "companies": {"google": 2, "apple": 2, "meta": 3, "amazon": 3, "microsoft": 3},
        "description": (
            "An array of **distinct** integers was sorted ascending and then rotated some number of times "
            "(for example `[0,1,2,4,5,6,7]` rotated 4 times becomes `[4,5,6,7,0,1,2]`).\n\n"
            "Given the rotated array `nums`, return its minimum element in **O(log n)** time."
        ),
        "examples": [
            {"input": "nums = [3,4,5,1,2]", "output": "1"},
            {"input": "nums = [4,5,6,7,0,1,2]", "output": "0"},
            {"input": "nums = [11,13,15,17]", "output": "11", "explanation": "Rotated a multiple of its length, so it is still sorted."},
        ],
        "constraints": ["1 <= nums.length <= 5000", "-5000 <= nums[i] <= 5000", "All values distinct"],
        "hints": [
            "The array is two sorted runs; the minimum is the first element of the second run (or the first element overall if unrotated).",
            "Compare nums[mid] with nums[hi]. If nums[mid] > nums[hi], the drop (and the minimum) is to the right of mid; otherwise it is at mid or to the left.",
            "Use the half-open template with lo < hi, hi = mid or lo = mid + 1. When the loop ends lo points at the minimum.",
        ],
        "function": "findMin",
        "signature": "def findMin(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [3, 4, 5, 1, 2]}, "output": 1},
            {"input": {"nums": [4, 5, 6, 7, 0, 1, 2]}, "output": 0},
            {"input": {"nums": [11, 13, 15, 17]}, "output": 11},
            {"input": {"nums": [1]}, "output": 1},
            {"input": {"nums": [2, 1]}, "output": 1},
            {"input": {"nums": [-2, -1, -5, -4, -3]}, "output": -5},
            {"input": {"nums": [2, 3, 4, 5, 1]}, "output": 1},
            {"input": {"nums": list(range(3000, 10000)) + list(range(0, 3000))}, "output": 0},
            {"input": {"nums": list(range(1, 5000)) + [0]}, "output": 0},
        ],
        "solution": '''\
class Solution:
    def findMin(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] > nums[hi]:
                lo = mid + 1      # minimum is strictly to the right
            else:
                hi = mid          # minimum is at mid or to the left
        return nums[lo]
''',
        "approach": (
            "**Key insight: comparing the middle with the right end tells you which side contains the rotation point.** "
            "If `nums[mid] > nums[hi]`, the array is not sorted on `[mid, hi]`, so the drop and the minimum lie to the right "
            "of `mid`. Otherwise `[mid, hi]` is sorted, so `mid` may be the minimum and nothing right of it is smaller.\n\n"
            "**Algorithm.** Half-open binary search: while `lo < hi`, compute `mid`; set `lo = mid + 1` when "
            "`nums[mid] > nums[hi]`, else `hi = mid`. Return `nums[lo]`.\n\n"
            "**Why it works.** Invariant: the minimum is always within `[lo, hi]`. Both updates keep it, and the window "
            "strictly shrinks because `mid < hi` in the half-open template, so `hi = mid` always makes progress.\n\n"
            "**Common mistakes.** Comparing with `nums[lo]` instead of `nums[hi]`, which fails for unrotated arrays "
            "(`[1,2,3]`: `nums[mid] > nums[lo]` wrongly sends you right). Using `hi = mid - 1`, which can skip the minimum. "
            "Returning `lo` (the index) instead of `nums[lo]`.\n\n"
            "**Interview follow-ups.** (1) Duplicates allowed (Find Minimum II): when `nums[mid] == nums[hi]` you can only "
            "do `hi -= 1`, making the worst case O(n). (2) Return the rotation count (it equals the index of the minimum). "
            "(3) Use this as a first step to search for a target in the rotated array."
        ),
        "complexity": {"time": "O(log n)", "space": "O(1)"},
        "similar": ["search-in-rotated-sorted-array", "find-minimum-in-rotated-sorted-array-ii", "find-peak-element"],
        "followups": ["Handle duplicates.", "Return the rotation count."],
    },
    {
        "id": "search-in-rotated-sorted-array",
        "title": "Search in Rotated Sorted Array",
        "difficulty": "Medium",
        "pattern": "Binary Search",
        "tags": ["Array", "Binary Search"],
        "companies": {"google": 3, "apple": 3, "meta": 4, "amazon": 4, "microsoft": 4},
        "description": (
            "`nums` is an array of **distinct** integers that was sorted ascending and then rotated at some unknown pivot. "
            "Given a `target`, return its index in `nums`, or `-1` if it is not present.\n\n"
            "The solution must run in **O(log n)** time."
        ),
        "examples": [
            {"input": "nums = [4,5,6,7,0,1,2], target = 0", "output": "4"},
            {"input": "nums = [4,5,6,7,0,1,2], target = 3", "output": "-1"},
            {"input": "nums = [1], target = 0", "output": "-1"},
        ],
        "constraints": ["1 <= nums.length <= 5000", "-10^4 <= nums[i], target <= 10^4", "All values distinct"],
        "hints": [
            "Split at mid: at least one of the two halves [lo, mid] and [mid, hi] is sorted. You can tell which by comparing nums[lo] and nums[mid].",
            "If the sorted half contains the target (range check), search there; otherwise search the other half.",
            "Alternatively find the rotation index first, then do a normal binary search in the correct half: two searches, still O(log n).",
        ],
        "function": "search",
        "signature": "def search(self, nums: List[int], target: int) -> int:",
        "arg_types": {"nums": "List[int]", "target": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 0}, "output": 4},
            {"input": {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 3}, "output": -1},
            {"input": {"nums": [1], "target": 0}, "output": -1},
            {"input": {"nums": [1], "target": 1}, "output": 0},
            {"input": {"nums": [3, 1], "target": 1}, "output": 1},
            {"input": {"nums": [5, 1, 3], "target": 5}, "output": 0},
            {"input": {"nums": [1, 2, 3, 4, 5], "target": 4}, "output": 3},
            {"input": {"nums": [-3, -2, -1, -7, -6, -5, -4], "target": -7}, "output": 3},
            {"input": {"nums": list(range(3000, 10000)) + list(range(0, 3000)), "target": 1234}, "output": 8234},
            {"input": {"nums": list(range(3000, 10000)) + list(range(0, 3000)), "target": 10000}, "output": -1},
            {"input": {"nums": list(range(3000, 10000)) + list(range(0, 3000)), "target": 9999}, "output": 6999},
        ],
        "solution": '''\
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            if nums[lo] <= nums[mid]:            # left half [lo, mid] is sorted
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:                                # right half [mid, hi] is sorted
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return -1
''',
        "approach": (
            "**Key insight: whichever way you split a rotated sorted array, at least one half is a plain sorted array, and "
            "a sorted half lets you decide with a range check whether the target can be inside it.** That is enough to "
            "discard half the array per step.\n\n"
            "**Algorithm.** Standard `lo <= hi` loop. If `nums[mid]` is the target, return. If `nums[lo] <= nums[mid]`, "
            "the left half is sorted: if `nums[lo] <= target < nums[mid]` go left, else go right. Otherwise the right half "
            "is sorted: if `nums[mid] < target <= nums[hi]` go right, else go left.\n\n"
            "**Why it works.** The rotation point can be in only one half, so the other half is sorted. If the target's "
            "value falls within the sorted half's range it must be there (values are distinct); if not, it can only be in "
            "the other half. Either way we keep exactly the half that may contain it.\n\n"
            "**Common mistakes.** Writing `nums[lo] < nums[mid]` instead of `<=`: when `lo == mid` (two-element window) the "
            "left half is trivially sorted and the strict check mis-routes, e.g. `[3,1]` searching for 1. Getting the range "
            "checks inclusive/exclusive wrong on the `mid` side. Forgetting the problem guarantees distinct values; with "
            "duplicates the sorted-half test can be ambiguous.\n\n"
            "**Interview follow-ups.** (1) Search in Rotated Sorted Array II with duplicates: when `nums[lo] == nums[mid] == "
            "nums[hi]` shrink both ends, worst case O(n). (2) Two-pass approach: find the pivot with Find Minimum, then "
            "binary search the right segment. (3) Return the rotation amount, or search for a range of targets."
        ),
        "complexity": {"time": "O(log n)", "space": "O(1)"},
        "similar": ["find-minimum-in-rotated-sorted-array", "search-in-rotated-sorted-array-ii", "binary-search"],
        "followups": ["Duplicates allowed.", "Two-pass pivot-then-search approach."],
    },
    {
        "id": "median-of-two-sorted-arrays",
        "title": "Median of Two Sorted Arrays",
        "difficulty": "Hard",
        "pattern": "Binary Search",
        "tags": ["Array", "Binary Search", "Divide and Conquer"],
        "companies": {"google": 4, "apple": 3, "meta": 3, "amazon": 4, "microsoft": 3},
        "description": (
            "You are given two sorted integer arrays `nums1` and `nums2` of sizes `m` and `n`. Return the **median** of "
            "the combined sorted sequence as a float. When the total count is even, the median is the average of the two "
            "middle values.\n\n"
            "The combined length is at least 1. The intended solution runs in **O(log(m + n))**."
        ),
        "examples": [
            {"input": "nums1 = [1,3], nums2 = [2]", "output": "2.00000", "explanation": "Merged: [1,2,3], median 2."},
            {"input": "nums1 = [1,2], nums2 = [3,4]", "output": "2.50000", "explanation": "Merged: [1,2,3,4], median (2 + 3) / 2."},
        ],
        "constraints": ["0 <= m, n <= 1000", "1 <= m + n <= 2000", "-10^6 <= nums1[i], nums2[i] <= 10^6", "Both arrays are sorted ascending"],
        "hints": [
            "Merging is O(m + n). To do better, think about partitioning rather than merging: the median splits the combined data into a left half and a right half of known sizes.",
            "Take i elements from nums1 and j = half - i from nums2 for the left part. The partition is correct when every left element is <= every right element, which only needs four boundary comparisons.",
            "Binary search i over the shorter array. If nums1[i-1] > nums2[j], i is too large; if nums2[j-1] > nums1[i], i is too small. Use +/- infinity for empty sides.",
        ],
        "function": "findMedianSortedArrays",
        "signature": "def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:",
        "arg_types": {"nums1": "List[int]", "nums2": "List[int]"},
        "return_type": "float",
        "compare": "float",
        "tests": [
            {"input": {"nums1": [1, 3], "nums2": [2]}, "output": 2.0},
            {"input": {"nums1": [1, 2], "nums2": [3, 4]}, "output": 2.5},
            {"input": {"nums1": [], "nums2": [1]}, "output": 1.0},
            {"input": {"nums1": [2], "nums2": []}, "output": 2.0},
            {"input": {"nums1": [1, 1], "nums2": [1, 1]}, "output": 1.0},
            {"input": {"nums1": [-5, -3, -1], "nums2": [-4, -2]}, "output": -3.0},
            {"input": {"nums1": [1, 2, 3, 4, 5], "nums2": [6, 7, 8, 9, 10]}, "output": 5.5},
            {"input": {"nums1": [100], "nums2": [1, 2, 3]}, "output": 2.5},
            {"input": {"nums1": [1, 2], "nums2": [1, 2, 3]}, "output": 2.0},
            {"input": {"nums1": list(range(0, 10000, 2)), "nums2": list(range(1, 10000, 2))}, "output": 4999.5},
            {"input": {"nums1": list(range(0, 5000)), "nums2": list(range(5000, 10001))}, "output": 5000.0},
        ],
        "solution": '''\
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        a, b = nums1, nums2
        if len(a) > len(b):
            a, b = b, a                       # binary search over the shorter array
        m, n = len(a), len(b)
        total = m + n
        half = (total + 1) // 2               # size of the left partition
        lo, hi = 0, m
        while lo <= hi:
            i = (lo + hi) // 2                # elements taken from a
            j = half - i                      # elements taken from b
            a_left = a[i - 1] if i > 0 else float("-inf")
            a_right = a[i] if i < m else float("inf")
            b_left = b[j - 1] if j > 0 else float("-inf")
            b_right = b[j] if j < n else float("inf")
            if a_left <= b_right and b_left <= a_right:
                if total % 2:
                    return float(max(a_left, b_left))
                return (max(a_left, b_left) + min(a_right, b_right)) / 2
            if a_left > b_right:
                hi = i - 1                    # took too many from a
            else:
                lo = i + 1                    # took too few from a
        raise ValueError("inputs are not sorted")
''',
        "approach": (
            "**Key insight: the median is defined by a partition, not by a merge.** Cut the combined data into a left half "
            "with `(m + n + 1) // 2` elements and a right half with the rest. If `i` elements of the left half come from "
            "`nums1`, then `j = half - i` come from `nums2`, and the cut is valid exactly when the largest left element of "
            "each array is <= the smallest right element of the other. Finding the right `i` is a binary search.\n\n"
            "**Algorithm.** Ensure `nums1` is the shorter array (so `j` never goes out of range). Binary search "
            "`i in [0, m]`. Compute the four boundary values, using +/- infinity for empty sides. If `a_left > b_right`, "
            "decrease `i`; if `b_left > a_right`, increase `i`; otherwise the partition is correct. For odd total the median "
            "is `max(a_left, b_left)`; for even it is the mean of that and `min(a_right, b_right)`.\n\n"
            "**Why it works.** As `i` increases, `a_left` grows and `b_right` grows too (since `j` shrinks) in a way that makes "
            "`a_left <= b_right` monotone: true for small `i`, false for large `i`. Similarly for the other condition in the "
            "opposite direction. Hence exactly one `i` satisfies both, and the conditions tell you which way to move.\n\n"
            "**Common mistakes.** Not swapping so the search runs over the shorter array (then `j` can be negative). "
            "Off-by-one in `half` for odd lengths. Forgetting the infinity sentinels. Returning an int for odd totals in a "
            "language where that matters. Many candidates can describe the idea but stumble on the boundary handling; "
            "practise writing it cleanly.\n\n"
            "**Interview follow-ups.** (1) Generalise to the k-th smallest element of two sorted arrays (same partition with "
            "`half = k`). (2) Why can't you do better than O(log(min(m, n)))? (3) Median of k sorted arrays, or a streaming "
            "median using two heaps."
        ),
        "complexity": {"time": "O(log(min(m, n)))", "space": "O(1)"},
        "similar": ["kth-smallest-element-in-a-sorted-matrix", "find-median-from-data-stream", "merge-two-sorted-lists"],
        "followups": ["k-th smallest of two sorted arrays.", "Streaming median with two heaps."],
    },
    {
        "id": "find-first-and-last-position-of-element",
        "title": "Find First and Last Position of Element in Sorted Array",
        "difficulty": "Medium",
        "pattern": "Binary Search",
        "tags": ["Array", "Binary Search"],
        "companies": {"google": 2, "apple": 1, "meta": 3, "amazon": 3, "microsoft": 2},
        "description": (
            "Given an integer array `nums` sorted in non-decreasing order (duplicates allowed) and a `target`, return "
            "`[first, last]`, the indices of the first and last occurrence of `target`. If the target does not occur, "
            "return `[-1, -1]`.\n\n"
            "Required time complexity: **O(log n)**."
        ),
        "examples": [
            {"input": "nums = [5,7,7,8,8,10], target = 8", "output": "[3,4]"},
            {"input": "nums = [5,7,7,8,8,10], target = 6", "output": "[-1,-1]"},
            {"input": "nums = [], target = 0", "output": "[-1,-1]"},
        ],
        "constraints": ["0 <= nums.length <= 10^5", "-10^9 <= nums[i], target <= 10^9", "nums is sorted in non-decreasing order"],
        "hints": [
            "A plain binary search stops at some occurrence, not necessarily the first. Scanning outward from it is O(n) in the worst case.",
            "Run two binary searches: one for the leftmost index with nums[i] >= target (lower bound), one for the leftmost index with nums[i] > target (upper bound).",
            "first = lower_bound; last = upper_bound - 1. If first is out of range or nums[first] != target, return [-1, -1].",
        ],
        "function": "searchRange",
        "signature": "def searchRange(self, nums: List[int], target: int) -> List[int]:",
        "arg_types": {"nums": "List[int]", "target": "int"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [5, 7, 7, 8, 8, 10], "target": 8}, "output": [3, 4]},
            {"input": {"nums": [5, 7, 7, 8, 8, 10], "target": 6}, "output": [-1, -1]},
            {"input": {"nums": [], "target": 0}, "output": [-1, -1]},
            {"input": {"nums": [1], "target": 1}, "output": [0, 0]},
            {"input": {"nums": [2, 2, 2, 2], "target": 2}, "output": [0, 3]},
            {"input": {"nums": [1, 2, 3], "target": 4}, "output": [-1, -1]},
            {"input": {"nums": [1, 2, 3], "target": 0}, "output": [-1, -1]},
            {"input": {"nums": [-3, -3, -1, 0, 0, 0, 2], "target": 0}, "output": [3, 5]},
            {"input": {"nums": [0] * 1000 + [1] * 5000 + [2] * 1000, "target": 1}, "output": [1000, 5999]},
            {"input": {"nums": [0] * 1000 + [1] * 5000 + [2] * 1000, "target": 2}, "output": [6000, 6999]},
        ],
        "solution": '''\
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def lower_bound(x: int) -> int:
            # first index i with nums[i] >= x (len(nums) if none)
            lo, hi = 0, len(nums)
            while lo < hi:
                mid = (lo + hi) // 2
                if nums[mid] < x:
                    lo = mid + 1
                else:
                    hi = mid
            return lo

        first = lower_bound(target)
        if first == len(nums) or nums[first] != target:
            return [-1, -1]
        last = lower_bound(target + 1) - 1
        return [first, last]
''',
        "approach": (
            "**Key insight: both boundaries are lower bounds.** The first occurrence is the first index with "
            "`nums[i] >= target`; the position just after the last occurrence is the first index with `nums[i] >= target + 1` "
            "(for integers) or `nums[i] > target` in general. One well-written lower-bound routine solves the whole problem.\n\n"
            "**Algorithm.** Implement `lower_bound(x)` with the half-open template `[lo, hi)`: move `lo` past `mid` when "
            "`nums[mid] < x`, else `hi = mid`. Compute `first = lower_bound(target)`. If it is out of range or does not hold "
            "the target, return `[-1, -1]`. Otherwise `last = lower_bound(target + 1) - 1`.\n\n"
            "**Why it works.** The predicate `nums[i] >= x` is monotone over a sorted array, so binary search finds its first "
            "true index. All occurrences of `target` form a contiguous block, bounded exactly by these two lower bounds.\n\n"
            "**Common mistakes.** Finding one occurrence and expanding linearly (O(n) for arrays full of the target). "
            "Off-by-one when converting the upper bound to `last`. Forgetting the empty-array and not-found checks before "
            "indexing `nums[first]`. Writing two slightly different binary searches by hand and getting one of them wrong; "
            "reusing a single lower-bound helper is safer. In Python, `bisect_left` and `bisect_right` do exactly this.\n\n"
            "**Interview follow-ups.** (1) Count occurrences of `target` in O(log n). (2) Find the number of elements in a "
            "value range `[a, b]`. (3) The array is rotated as well as sorted."
        ),
        "complexity": {"time": "O(log n)", "space": "O(1)"},
        "similar": ["binary-search", "search-insert-position", "count-of-range-sum"],
        "followups": ["Count occurrences.", "Count elements in a value range."],
    },
    {
        "id": "find-peak-element",
        "title": "Find Peak Element",
        "difficulty": "Medium",
        "pattern": "Binary Search",
        "tags": ["Array", "Binary Search"],
        "companies": {"google": 3, "apple": 1, "meta": 3, "amazon": 2, "microsoft": 2},
        "description": (
            "A **peak** is an element strictly greater than both of its neighbours. Imagine `nums[-1]` and `nums[n]` are "
            "negative infinity, so the ends only need to beat their single neighbour. Adjacent elements are never equal.\n\n"
            "Given `nums`, return the index of **any** peak. The array always has at least one. Your solution must run in "
            "**O(log n)** time."
        ),
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "2", "explanation": "3 is greater than both 2 and 1."},
            {"input": "nums = [1,2,1,3,5,6,4]", "output": "5", "explanation": "Index 1 (value 2) and index 5 (value 6) are both peaks; either answer is accepted."},
        ],
        "constraints": ["1 <= nums.length <= 1000", "-2^31 <= nums[i] <= 2^31 - 1", "nums[i] != nums[i + 1] for all valid i"],
        "hints": [
            "A linear scan for the first i with nums[i] > nums[i+1] works, but is O(n). What does the comparison nums[mid] vs nums[mid+1] tell you?",
            "If nums[mid] < nums[mid+1] you are on an upward slope: following it to the right must eventually reach a peak before the virtual -infinity at the end. Otherwise a peak exists at mid or to its left.",
            "Half-open binary search: lo = mid + 1 on an upward slope, else hi = mid. When lo == hi you are on a peak.",
        ],
        "function": "findPeakElement",
        "signature": "def findPeakElement(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "compare": "any_of",
        "tests": [
            {"input": {"nums": [1, 2, 3, 1]}, "output": [2]},
            {"input": {"nums": [1, 2, 1, 3, 5, 6, 4]}, "output": [1, 5]},
            {"input": {"nums": [1]}, "output": [0]},
            {"input": {"nums": [1, 2]}, "output": [1]},
            {"input": {"nums": [2, 1]}, "output": [0]},
            {"input": {"nums": [3, 2, 1]}, "output": [0]},
            {"input": {"nums": [1, 2, 3]}, "output": [2]},
            {"input": {"nums": [-5, -3, -4, -2, -6]}, "output": [1, 3]},
            {"input": {"nums": [5, 1, 5, 1, 5]}, "output": [0, 2, 4]},
            {"input": {"nums": list(range(5000)) + list(range(5000, 0, -1))}, "output": [5000]},
            {"input": {"nums": list(range(8000, 0, -1))}, "output": [0]},
        ],
        "solution": '''\
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < nums[mid + 1]:
                lo = mid + 1      # ascending: a peak lies to the right
            else:
                hi = mid          # descending: mid or something left of it is a peak
        return lo
''',
        "approach": (
            "**Key insight: if you stand on an upward slope, walking uphill must reach a peak, because the array ends in "
            "virtual negative infinity.** So the single comparison `nums[mid] < nums[mid + 1]` tells you a side that is "
            "guaranteed to contain a peak, even though the array is not sorted.\n\n"
            "**Algorithm.** Half-open binary search over `[lo, hi]` with `lo < hi`. If `nums[mid] < nums[mid + 1]`, set "
            "`lo = mid + 1`; otherwise `hi = mid`. When `lo == hi`, that index is a peak.\n\n"
            "**Why it works.** Invariant: `nums[lo - 1] < nums[lo]` (or `lo == 0`) and `nums[hi] > nums[hi + 1]` (or "
            "`hi == n - 1`), i.e. the window is entered going up and left going down, so it contains a peak. Both updates "
            "preserve this. Because `mid < hi` in the half-open template, `mid + 1` is always a valid index.\n\n"
            "**Common mistakes.** Using `lo <= hi` with `hi = len - 1`, which can index `nums[mid + 1]` out of range. "
            "Assuming the array is sorted or has a single peak; the proof only needs the slope argument. Thinking a "
            "linear scan is the only way because the array is unsorted.\n\n"
            "**Interview follow-ups.** (1) Find a peak in a 2D grid in O(m log n) by binary searching columns and taking the "
            "column maximum. (2) Why does the absence of equal neighbours matter? (With plateaus you cannot tell which side "
            "to go, worst case O(n).) (3) Peak Index in a Mountain Array / unimodal search and ternary search on functions."
        ),
        "complexity": {"time": "O(log n)", "space": "O(1)"},
        "similar": ["find-minimum-in-rotated-sorted-array", "peak-index-in-a-mountain-array", "find-a-peak-element-ii"],
        "followups": ["2D peak finding.", "Plateaus / equal neighbours."],
    },
    {
        "id": "split-array-largest-sum",
        "title": "Split Array Largest Sum",
        "difficulty": "Hard",
        "pattern": "Binary Search",
        "tags": ["Array", "Binary Search", "Greedy", "Dynamic Programming"],
        "companies": {"google": 3, "meta": 2, "amazon": 1, "microsoft": 1},
        "description": (
            "Split the array `nums` of non-negative integers into exactly `k` **non-empty contiguous** subarrays. "
            "Each split has a cost equal to the largest subarray sum among its pieces.\n\n"
            "Return the smallest possible cost over all valid splits."
        ),
        "examples": [
            {"input": "nums = [7,2,5,10,8], k = 2", "output": "18", "explanation": "[7,2,5] and [10,8] have sums 14 and 18. No split does better than 18."},
            {"input": "nums = [1,2,3,4,5], k = 2", "output": "9", "explanation": "[1,2,3] and [4,5]."},
            {"input": "nums = [1,4,4], k = 3", "output": "4"},
        ],
        "constraints": ["1 <= nums.length <= 1000", "0 <= nums[i] <= 10^6", "1 <= k <= min(50, nums.length)"],
        "hints": [
            "Flip the question: given a cap C on the subarray sum, what is the fewest pieces you need? That can be answered greedily in one pass.",
            "If a cap C is achievable with at most k pieces, every larger cap is too. Binary search on C between max(nums) and sum(nums).",
            "Greedy check: walk the array, start a new piece whenever adding the next number would exceed C. Count pieces and compare with k.",
        ],
        "function": "splitArray",
        "signature": "def splitArray(self, nums: List[int], k: int) -> int:",
        "arg_types": {"nums": "List[int]", "k": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [7, 2, 5, 10, 8], "k": 2}, "output": 18},
            {"input": {"nums": [1, 2, 3, 4, 5], "k": 2}, "output": 9},
            {"input": {"nums": [1, 4, 4], "k": 3}, "output": 4},
            {"input": {"nums": [10], "k": 1}, "output": 10},
            {"input": {"nums": [1, 1, 1, 1], "k": 4}, "output": 1},
            {"input": {"nums": [1, 2, 3, 4, 5], "k": 1}, "output": 15},
            {"input": {"nums": [0, 0, 0, 5], "k": 2}, "output": 5},
            {"input": {"nums": [2, 3, 1, 2, 4, 3], "k": 3}, "output": 6},
            {"input": {"nums": [1] * 5000, "k": 7}, "output": 715},
            {"input": {"nums": list(range(1, 5001)), "k": 1}, "output": 12502500},
            {"input": {"nums": [1000000] * 5000, "k": 50}, "output": 100000000},
        ],
        "solution": '''\
class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        def pieces_needed(cap: int) -> int:
            count, running = 1, 0
            for x in nums:
                if running + x > cap:
                    count += 1
                    running = x
                else:
                    running += x
            return count

        lo, hi = max(nums), sum(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if pieces_needed(mid) <= k:
                hi = mid          # cap is achievable; try a smaller one
            else:
                lo = mid + 1
        return lo
''',
        "approach": (
            "**Key insight: binary search on the answer with a greedy feasibility check.** Deciding whether a cost `C` is "
            "achievable is easy: greedily extend the current piece until adding the next number would exceed `C`, then start "
            "a new piece. The number of pieces this produces is the minimum for that cap, and feasibility is monotone in `C`.\n\n"
            "**Algorithm.** The answer lies in `[max(nums), sum(nums)]`: no piece can be smaller than the largest element, "
            "and one piece holding everything costs the total. Binary search this range; for each `mid`, count the greedy "
            "pieces. If `count <= k` the cap works (we can always split a piece further to use exactly `k`, since numbers are "
            "non-negative), so try smaller; otherwise go larger.\n\n"
            "**Why it works.** The greedy packing is optimal for a fixed cap: starting a new piece earlier than necessary "
            "never helps. Monotonicity makes the binary search valid. Each check is O(n), and there are O(log(sum)) checks.\n\n"
            "**Common mistakes.** Starting `lo` at 0 or 1 instead of `max(nums)` (then the greedy check sees an element that "
            "does not fit in any piece and silently miscounts). Using `count < k` instead of `<= k`. Reaching for the "
            "O(k * n^2) DP first; it is correct but the interviewer will push for this approach.\n\n"
            "**Interview follow-ups.** (1) Return the actual split, not just the cost. (2) The same template solves Koko "
            "Eating Bananas, Capacity to Ship Packages, Minimize Max Distance to Gas Station. (3) Negative numbers break the "
            "greedy check and the `max(nums)` lower bound; discuss why and what changes. (4) Compare with the DP solution "
            "and its complexity."
        ),
        "complexity": {"time": "O(n log S) where S = sum(nums)", "space": "O(1)"},
        "similar": ["koko-eating-bananas", "capacity-to-ship-packages-within-d-days", "painters-partition"],
        "followups": ["Reconstruct the split.", "Compare with the O(k n^2) DP."],
    },
    {
        "id": "sqrt-x",
        "title": "Sqrt(x)",
        "difficulty": "Easy",
        "pattern": "Binary Search",
        "tags": ["Math", "Binary Search"],
        "companies": {"google": 2, "apple": 3, "meta": 3, "amazon": 2, "microsoft": 2},
        "description": (
            "Given a non-negative integer `x`, return the integer square root of `x`: the largest integer `r` such that "
            "`r * r <= x`. In other words, the exact square root **rounded down**.\n\n"
            "Do not use any built-in exponent or square-root function."
        ),
        "examples": [
            {"input": "x = 4", "output": "2"},
            {"input": "x = 8", "output": "2", "explanation": "The square root of 8 is about 2.828; the decimal part is dropped."},
        ],
        "constraints": ["0 <= x <= 2^31 - 1"],
        "hints": [
            "r * r <= x is true for small r and false for large r. That monotone boundary is a binary search.",
            "Search r in [0, x] (or [0, x // 2 + 1] for x >= 2). Find the largest r whose square does not exceed x.",
            "Keep track of the last mid that satisfied mid * mid <= x, or use the half-open template to find the first r with r * r > x and subtract one.",
        ],
        "function": "mySqrt",
        "signature": "def mySqrt(self, x: int) -> int:",
        "arg_types": {"x": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"x": 4}, "output": 2},
            {"input": {"x": 8}, "output": 2},
            {"input": {"x": 0}, "output": 0},
            {"input": {"x": 1}, "output": 1},
            {"input": {"x": 2}, "output": 1},
            {"input": {"x": 3}, "output": 1},
            {"input": {"x": 99}, "output": 9},
            {"input": {"x": 100}, "output": 10},
            {"input": {"x": 2147395599}, "output": 46339},
            {"input": {"x": 2147395600}, "output": 46340},
            {"input": {"x": 2147483647}, "output": 46340},
        ],
        "solution": '''\
class Solution:
    def mySqrt(self, x: int) -> int:
        lo, hi = 0, x
        while lo < hi:
            mid = (lo + hi + 1) // 2      # upper mid so lo = mid always makes progress
            if mid * mid <= x:
                lo = mid                  # mid is a valid root candidate
            else:
                hi = mid - 1
        return lo
''',
        "approach": (
            "**Key insight: `r * r <= x` is a monotone predicate in `r`, so the largest `r` satisfying it can be found by "
            "binary search.** No floating point is needed.\n\n"
            "**Algorithm.** Search `r` in `[0, x]`. Use the upper-mid variant `mid = (lo + hi + 1) // 2`: if `mid * mid <= x`, "
            "`mid` is a valid answer so set `lo = mid`; otherwise `hi = mid - 1`. The loop ends with `lo == hi` at the "
            "largest valid root.\n\n"
            "**Why it works.** Invariant: `lo` always satisfies the predicate and nothing above `hi` does. The upper-mid "
            "choice guarantees `mid > lo` when `lo < hi`, so `lo = mid` strictly shrinks the window and the loop terminates.\n\n"
            "**Common mistakes.** Using lower mid with `lo = mid`, which loops forever on a two-element window. Comparing "
            "`mid <= x / mid` with floating-point division. In fixed-width languages `mid * mid` can overflow for `x` near "
            "2^31 - 1; compare `mid <= x // mid` instead. Returning `hi` or `lo` from the wrong template.\n\n"
            "**Interview follow-ups.** (1) Newton's method: `r = (r + x // r) // 2` converges quadratically; be able to "
            "explain why it stays above the true root and when to stop. (2) Return the result with k decimal places. "
            "(3) Valid Perfect Square and Pow(x, n) as related numeric problems."
        ),
        "complexity": {"time": "O(log x)", "space": "O(1)"},
        "similar": ["valid-perfect-square", "pow-x-n", "binary-search"],
        "followups": ["Newton's method.", "Square root with decimal precision."],
    },
]
