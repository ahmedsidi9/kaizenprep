"""Two Pointers problems. See SCHEMA.md for the dict format."""

PROBLEMS = [
    {
        "id": "valid-palindrome",
        "title": "Valid Palindrome",
        "difficulty": "Easy",
        "pattern": "Two Pointers",
        "tags": ["Two Pointers", "String"],
        "companies": {"google": 2, "apple": 3, "meta": 5, "amazon": 3, "microsoft": 3},
        "description": (
            "A string is a palindrome if it reads the same forwards and backwards once you **ignore case** and **drop every "
            "character that is not a letter or digit**.\n\n"
            "Given `s`, return `true` if it is a palindrome under those rules, otherwise `false`. A string with no "
            "alphanumeric characters at all counts as a palindrome."
        ),
        "examples": [
            {"input": "s = \"A man, a plan, a canal: Panama\"", "output": "true", "explanation": "Cleaned up it reads `amanaplanacanalpanama`."},
            {"input": "s = \"race a car\"", "output": "false", "explanation": "`raceacar` is not the same reversed."},
            {"input": "s = \" \"", "output": "true", "explanation": "Nothing is left after filtering, and the empty string is a palindrome."},
        ],
        "constraints": ["1 <= s.length <= 2 * 10^5", "s contains printable ASCII characters."],
        "hints": [
            "Building a cleaned, lower-cased copy and comparing it to its reverse works in O(n) extra space. Can you avoid the copy?",
            "Walk two indices inward from both ends, skipping anything that is not alphanumeric.",
            "Compare `s[i].lower()` with `s[j].lower()` only when both point at alphanumerics; mismatch means not a palindrome. Stop when the indices cross.",
        ],
        "function": "isPalindrome",
        "signature": "def isPalindrome(self, s: str) -> bool:",
        "arg_types": {"s": "str"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"s": "A man, a plan, a canal: Panama"}, "output": True},
            {"input": {"s": "race a car"}, "output": False},
            {"input": {"s": " "}, "output": True},
            {"input": {"s": ""}, "output": True},
            {"input": {"s": "0P"}, "output": False},
            {"input": {"s": "ab@a"}, "output": True},
            {"input": {"s": "Was it a car or a cat I saw?"}, "output": True},
            {"input": {"s": "a" * 5000 + "b" * 5000}, "output": False},
            {"input": {"s": "ab" * 2500 + "ba" * 2500}, "output": True},
            {"input": {"s": "a, " * 3000}, "output": True},
        ],
        "solution": '''\
class Solution:
    def isPalindrome(self, s: str) -> bool:
        i, j = 0, len(s) - 1
        while i < j:
            while i < j and not s[i].isalnum():
                i += 1
            while i < j and not s[j].isalnum():
                j -= 1
            if s[i].lower() != s[j].lower():
                return False
            i += 1
            j -= 1
        return True
''',
        "approach": (
            "**Two pointers converging from the ends.** Skip non-alphanumeric characters on each side, then compare the two "
            "characters case-insensitively. Any mismatch is a definitive no; if the pointers cross without one, the string "
            "is a palindrome.\n\n"
            "**Why it works:** a string is a palindrome iff the k-th character from the front equals the k-th from the back "
            "for all k, and skipping filtered characters on both sides preserves that correspondence in the cleaned string "
            "without materialising it.\n\n"
            "**Common mistakes:** forgetting the `i < j` guard inside the skip loops (index runs off the end on inputs like "
            "`\"!!!\"`); treating digits as non-alphanumeric (`\"0P\"` is not a palindrome because `0` and `p` differ); "
            "the one-liner `cleaned == cleaned[::-1]` is accepted but uses O(n) extra space, so mention the trade-off.\n\n"
            "**Interview follow-ups:** Allow deleting at most one character (Valid Palindrome II: on mismatch try skipping "
            "either side). Find the longest palindromic substring (expand around centres). Check a linked list for a "
            "palindrome in O(1) space (reverse the second half)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["valid-palindrome-ii", "palindrome-linked-list", "longest-palindromic-substring"],
    },
    {
        "id": "two-sum-ii-sorted",
        "title": "Two Sum II - Input Array Is Sorted",
        "difficulty": "Medium",
        "pattern": "Two Pointers",
        "tags": ["Array", "Two Pointers", "Binary Search"],
        "companies": {"google": 1, "apple": 2, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "You are given an array `numbers` sorted in non-decreasing order and an integer `target`. Exactly one pair of "
            "distinct positions adds up to `target`.\n\n"
            "Return those two positions as **1-indexed** values `[index1, index2]` with `index1 < index2`. "
            "Use only constant extra space."
        ),
        "examples": [
            {"input": "numbers = [2,7,11,15], target = 9", "output": "[1,2]", "explanation": "2 + 7 = 9; they sit at positions 1 and 2."},
            {"input": "numbers = [2,3,4], target = 6", "output": "[1,3]"},
            {"input": "numbers = [-1,0], target = -1", "output": "[1,2]"},
        ],
        "constraints": ["2 <= numbers.length <= 3 * 10^4", "-1000 <= numbers[i] <= 1000", "numbers is sorted in non-decreasing order.", "Exactly one solution exists."],
        "hints": [
            "The hash-map approach from Two Sum works but ignores the sorted order and uses O(n) space.",
            "Place one pointer at each end. If the sum is too small, only moving the left pointer right can increase it; if too large, move the right pointer left.",
            "Each step discards one element that cannot be part of the answer, so the pointers meet after at most n steps. Remember to add 1 to both indices.",
        ],
        "function": "twoSum",
        "signature": "def twoSum(self, numbers: List[int], target: int) -> List[int]:",
        "arg_types": {"numbers": "List[int]", "target": "int"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"numbers": [2, 7, 11, 15], "target": 9}, "output": [1, 2]},
            {"input": {"numbers": [2, 3, 4], "target": 6}, "output": [1, 3]},
            {"input": {"numbers": [-1, 0], "target": -1}, "output": [1, 2]},
            {"input": {"numbers": [1, 2, 3, 4, 4, 9, 56, 90], "target": 8}, "output": [4, 5]},
            {"input": {"numbers": [5, 25, 75], "target": 100}, "output": [2, 3]},
            {"input": {"numbers": [-10, -3, 0, 2, 8], "target": -1}, "output": [2, 4]},
            {"input": {"numbers": list(range(1, 10001)), "target": 19999}, "output": [9999, 10000]},
            {"input": {"numbers": list(range(1, 10001)), "target": 3}, "output": [1, 2]},
        ],
        "solution": '''\
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        lo, hi = 0, len(numbers) - 1
        while lo < hi:
            total = numbers[lo] + numbers[hi]
            if total == target:
                return [lo + 1, hi + 1]
            if total < target:
                lo += 1
            else:
                hi -= 1
        return []
''',
        "approach": (
            "**Opposite-end two pointers.** Start with the smallest and largest values. If their sum is below the target the "
            "smallest value can never be part of a solution with anything remaining (every partner is at most the current "
            "largest), so discard it by moving `lo` right. Symmetrically, a sum above the target discards the largest.\n\n"
            "**Why it works:** the invariant is that the answer pair always lies within `[lo, hi]`; each step removes an index "
            "that provably cannot be in the answer, and the problem guarantees a solution exists so the loop finds it.\n\n"
            "**Common mistakes:** returning 0-indexed positions; using the unsorted Two Sum hash map and failing the O(1) "
            "space requirement; binary searching for each complement (O(n log n), correct but slower than needed).\n\n"
            "**Interview follow-ups:** Why not binary search per element? (works, O(n log n), worse constant). "
            "Extend to three numbers summing to a target (sort, fix one, two-pointer the rest). "
            "Count the pairs with sum less than the target (when `total < target`, all `hi - lo` pairs with `lo` qualify)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["two-sum", "3sum", "container-with-most-water"],
    },
    {
        "id": "3sum",
        "title": "3Sum",
        "difficulty": "Medium",
        "pattern": "Two Pointers",
        "tags": ["Array", "Two Pointers", "Sorting"],
        "companies": {"google": 3, "apple": 3, "meta": 4, "amazon": 4, "microsoft": 3},
        "description": (
            "Given an integer array `nums`, return every triplet of values `[a, b, c]` taken from three different positions "
            "such that `a + b + c == 0`.\n\n"
            "The output must not contain duplicate triplets (two triplets with the same three values in any order count as "
            "the same). Triplets and the values inside them may be returned in any order."
        ),
        "examples": [
            {"input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]", "explanation": "Both -1 + 0 + 1 and -1 + -1 + 2 are zero. The triplet [-1,0,1] can be formed two ways but is listed once."},
            {"input": "nums = [0,1,1]", "output": "[]"},
            {"input": "nums = [0,0,0]", "output": "[[0,0,0]]"},
        ],
        "constraints": ["0 <= nums.length <= 3000", "-10^5 <= nums[i] <= 10^5"],
        "hints": [
            "Sorting makes duplicates adjacent and lets you reason about sums monotonically.",
            "Fix the smallest element nums[i], then find pairs in the suffix that sum to -nums[i] with two pointers.",
            "Skip repeated values for i, and after recording a triplet advance both pointers past any repeats, so each distinct triplet is produced exactly once.",
        ],
        "function": "threeSum",
        "signature": "def threeSum(self, nums: List[int]) -> List[List[int]]:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "List[List[int]]",
        "compare": "unordered_nested",
        "tests": [
            {"input": {"nums": [-1, 0, 1, 2, -1, -4]}, "output": [[-1, -1, 2], [-1, 0, 1]]},
            {"input": {"nums": [0, 1, 1]}, "output": []},
            {"input": {"nums": [0, 0, 0]}, "output": [[0, 0, 0]]},
            {"input": {"nums": []}, "output": []},
            {"input": {"nums": [1, 2, -3, 4, -1]}, "output": [[-3, 1, 2], [-3, -1, 4]]},
            {"input": {"nums": [0, 0, 0, 0]}, "output": [[0, 0, 0]]},
            {"input": {"nums": [-2, 0, 1, 1, 2]}, "output": [[-2, 0, 2], [-2, 1, 1]]},
            {"input": {"nums": [3, -2, 1, 0]}, "output": []},
            {
                # Distinct values -500..500: every a < b < c with a + b + c = 0, generated by construction.
                "input": {"nums": list(range(-500, 501))},
                "output": [[a, b, -a - b] for a in range(-500, 501) for b in range(a + 1, 501) if -a - b > b and -a - b <= 500],
            },
        ],
        "solution": '''\
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        result = []
        for i in range(n - 2):
            if nums[i] > 0:
                break  # all remaining values are positive, no zero sum possible
            if i > 0 and nums[i] == nums[i - 1]:
                continue  # same first value already handled
            lo, hi = i + 1, n - 1
            while lo < hi:
                total = nums[i] + nums[lo] + nums[hi]
                if total < 0:
                    lo += 1
                elif total > 0:
                    hi -= 1
                else:
                    result.append([nums[i], nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1
                    while lo < hi and nums[lo] == nums[lo - 1]:
                        lo += 1
                    while lo < hi and nums[hi] == nums[hi + 1]:
                        hi -= 1
        return result
''',
        "approach": (
            "**Sort, fix one, two-pointer the rest.** After sorting, iterate `i` over possible smallest elements. For each, "
            "run the sorted Two Sum on `nums[i+1:]` looking for `-nums[i]`: pointers at both ends, move `lo` up when the sum "
            "is too small and `hi` down when too large.\n\n"
            "**Deduplication without a set:** skip `i` when `nums[i] == nums[i-1]`, and after recording a triplet advance "
            "`lo` and `hi` past values equal to the ones just used. Because the array is sorted, equal values are adjacent, "
            "so these skips are exactly what prevents repeated triplets. The early `break` on `nums[i] > 0` is a cheap "
            "pruning since three positives cannot sum to zero.\n\n"
            "**Common mistakes:** deduplicating with a set of tuples instead of pointer skips (accepted, but interviewers "
            "want you to know the skip logic); skipping duplicates of `i` by comparing with `nums[i+1]` (that drops valid "
            "triplets like `[-1,-1,2]`); forgetting to move *both* pointers after a hit.\n\n"
            "**Interview follow-ups:** 3Sum Closest (track the best absolute difference, no dedup needed). "
            "4Sum (another outer loop, O(n^3)) and the general k-Sum recursion. "
            "Can you beat O(n^2)? (not with known comparison-based methods; it is a famous lower-bound conjecture)."
        ),
        "complexity": {"time": "O(n^2)", "space": "O(1) beyond the output (sorting in place)"},
        "similar": ["two-sum", "two-sum-ii-sorted", "3sum-closest", "4sum"],
    },
    {
        "id": "container-with-most-water",
        "title": "Container With Most Water",
        "difficulty": "Medium",
        "pattern": "Two Pointers",
        "tags": ["Array", "Two Pointers", "Greedy"],
        "companies": {"google": 3, "apple": 2, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "You are given `height`, where `height[i]` is the height of a vertical line drawn at x-coordinate `i`. "
            "Pick two lines; together with the x-axis they form a container whose capacity is "
            "`min(height[i], height[j]) * (j - i)`.\n\n"
            "Return the maximum capacity over all pairs. The container cannot be tilted."
        ),
        "examples": [
            {"input": "height = [1,8,6,2,5,4,8,3,7]", "output": "49", "explanation": "Lines at index 1 (height 8) and index 8 (height 7): min(8,7) * 7 = 49."},
            {"input": "height = [1,1]", "output": "1"},
            {"input": "height = [4,3,2,1,4]", "output": "16", "explanation": "The two outer 4s span width 4."},
        ],
        "constraints": ["2 <= height.length <= 10^5", "0 <= height[i] <= 10^4"],
        "hints": [
            "Checking every pair is O(n^2). Start with the widest container and think about which end is worth moving.",
            "The shorter line limits the capacity. Moving the taller line inward can only shrink the width without raising the limit.",
            "So always move the pointer at the shorter line inward. Track the best area seen; the loop ends when the pointers meet.",
        ],
        "function": "maxArea",
        "signature": "def maxArea(self, height: List[int]) -> int:",
        "arg_types": {"height": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"height": [1, 8, 6, 2, 5, 4, 8, 3, 7]}, "output": 49},
            {"input": {"height": [1, 1]}, "output": 1},
            {"input": {"height": [4, 3, 2, 1, 4]}, "output": 16},
            {"input": {"height": [1, 2, 1]}, "output": 2},
            {"input": {"height": [1, 2, 4, 3]}, "output": 4},
            {"input": {"height": [0, 0]}, "output": 0},
            {"input": {"height": [2, 3, 10, 5, 7, 8, 9]}, "output": 36},
            {"input": {"height": list(range(5000))}, "output": 6247500},
        ],
        "solution": '''\
class Solution:
    def maxArea(self, height: List[int]) -> int:
        lo, hi = 0, len(height) - 1
        best = 0
        while lo < hi:
            best = max(best, min(height[lo], height[hi]) * (hi - lo))
            if height[lo] < height[hi]:
                lo += 1
            else:
                hi -= 1
        return best
''',
        "approach": (
            "**Shrink from the shorter side.** Start with the outermost pair, which has maximum width. The capacity is "
            "bounded by the shorter of the two lines. Moving the taller line inward can never help: the width drops and the "
            "limiting height stays the same or gets worse. Moving the shorter line inward is the only move that *might* "
            "find a taller limit, so do that and record the area at every step.\n\n"
            "**Why it is correct:** when we abandon the shorter line `height[lo]`, every container it could form with the "
            "remaining lines `lo+1..hi` has width less than `hi - lo` and height at most `height[lo]`, hence smaller than the "
            "area we just measured. So nothing better is ever skipped.\n\n"
            "**Common mistakes:** moving both pointers at once; moving the taller one; confusing this with Trapping Rain "
            "Water (which fills every gap, not one container).\n\n"
            "**Interview follow-ups:** Return the indices, not just the area. Prove the greedy step formally (the argument "
            "above). Compare with Trapping Rain Water and explain why that one needs the running max of each side."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["trapping-rain-water", "two-sum-ii-sorted"],
    },
    {
        "id": "trapping-rain-water",
        "title": "Trapping Rain Water",
        "difficulty": "Hard",
        "pattern": "Two Pointers",
        "tags": ["Array", "Two Pointers", "Stack", "Dynamic Programming"],
        "companies": {"google": 4, "apple": 3, "meta": 3, "amazon": 4, "microsoft": 3},
        "description": (
            "`height[i]` is the height of a bar of width 1 in an elevation map. After it rains, water settles in the dips "
            "between taller bars. Return the total number of unit squares of water the map holds."
        ),
        "examples": [
            {"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6"},
            {"input": "height = [4,2,0,3,2,5]", "output": "9", "explanation": "Above indices 1..4 the water level is 4: (4-2) + (4-0) + (4-3) + (4-2) = 9."},
            {"input": "height = [2,0,2]", "output": "2"},
        ],
        "constraints": ["1 <= height.length <= 2 * 10^4", "0 <= height[i] <= 10^5"],
        "hints": [
            "The water above position i rises to min(tallest bar to its left, tallest bar to its right) minus height[i], never below zero.",
            "Two passes can precompute left-max and right-max arrays for an O(n) time, O(n) space solution.",
            "Two pointers: keep running maxima leftMax and rightMax. Whichever side has the smaller max is the one whose water level is already decided, so settle that cell and move its pointer inward.",
        ],
        "function": "trap",
        "signature": "def trap(self, height: List[int]) -> int:",
        "arg_types": {"height": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"height": [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]}, "output": 6},
            {"input": {"height": [4, 2, 0, 3, 2, 5]}, "output": 9},
            {"input": {"height": [2, 0, 2]}, "output": 2},
            {"input": {"height": []}, "output": 0},
            {"input": {"height": [1]}, "output": 0},
            {"input": {"height": [3, 3, 3]}, "output": 0},
            {"input": {"height": [5, 4, 3, 2, 1]}, "output": 0},
            {"input": {"height": [1, 0, 1, 0, 1]}, "output": 2},
            {"input": {"height": [5000] + [0] * 4998 + [5000]}, "output": 24990000},
        ],
        "solution": '''\
class Solution:
    def trap(self, height: List[int]) -> int:
        lo, hi = 0, len(height) - 1
        left_max = right_max = 0
        water = 0
        while lo < hi:
            if height[lo] < height[hi]:
                left_max = max(left_max, height[lo])
                water += left_max - height[lo]
                lo += 1
            else:
                right_max = max(right_max, height[hi])
                water += right_max - height[hi]
                hi -= 1
        return water
''',
        "approach": (
            "**Two pointers with running maxima.** The water above cell `i` is `min(maxLeft(i), maxRight(i)) - height[i]`. "
            "Keep `left_max` and `right_max` for the parts already scanned from each end. If `height[lo] < height[hi]`, "
            "then `right_max >= height[hi] > height[lo]`, so the water level at `lo` is decided purely by `left_max`: "
            "add `left_max - height[lo]` and advance `lo`. Otherwise do the mirror step on `hi`.\n\n"
            "**Why it is correct:** the key invariant is that the side with the smaller current bar is bounded by a taller "
            "bar on the other side, so the smaller side's running max is the true `min` for that cell. Each cell is settled "
            "exactly once.\n\n"
            "**Common mistakes:** comparing `left_max` with `right_max` instead of `height[lo]` with `height[hi]` (both "
            "variants exist; be consistent and able to justify it); forgetting that the running max must include the current "
            "bar before subtracting (otherwise negative water); mixing this up with Container With Most Water.\n\n"
            "**Interview follow-ups:** Solve it with a monotonic stack (pop when a taller bar arrives, fill the pit between). "
            "Two-dimensional version, Trapping Rain Water II (min-heap from the border inward). "
            "If the heights arrive as a stream, what can you compute online? (only the left-max part; discuss limits)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["container-with-most-water", "product-of-array-except-self", "largest-rectangle-in-histogram"],
    },
    {
        "id": "remove-duplicates-from-sorted-array",
        "title": "Remove Duplicates from Sorted Array",
        "difficulty": "Easy",
        "pattern": "Two Pointers",
        "tags": ["Array", "Two Pointers"],
        "companies": {"google": 1, "apple": 2, "meta": 3, "amazon": 2, "microsoft": 2},
        "description": (
            "`nums` is sorted in non-decreasing order. Rearrange it **in place** so that each distinct value appears exactly "
            "once at the front, preserving their relative order, and return the count `k` of distinct values.\n\n"
            "Only the first `k` slots of `nums` are checked; whatever is left beyond them does not matter. "
            "Do not allocate a second array."
        ),
        "examples": [
            {"input": "nums = [1,1,2]", "output": "2, nums = [1,2,_]", "explanation": "Two distinct values; the trailing slot is ignored."},
            {"input": "nums = [0,0,1,1,1,2,2,3,3,4]", "output": "5, nums = [0,1,2,3,4,_,_,_,_,_]"},
        ],
        "constraints": ["1 <= nums.length <= 3 * 10^4", "-100 <= nums[i] <= 100", "nums is sorted in non-decreasing order."],
        "hints": [
            "Because the array is sorted, duplicates are adjacent. A value is new exactly when it differs from the previous one.",
            "Use a slow pointer for the next write position and a fast pointer that scans. Write only when the scanned value differs from the last written value.",
            "The first element is always kept, so start the write pointer at 1 and compare against nums[write - 1].",
        ],
        "function": "removeDuplicates",
        "signature": "def removeDuplicates(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "output_mode": "prefix:nums",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [1, 1, 2]}, "output": [2, [1, 2]]},
            {"input": {"nums": [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]}, "output": [5, [0, 1, 2, 3, 4]]},
            {"input": {"nums": []}, "output": [0, []]},
            {"input": {"nums": [7]}, "output": [1, [7]]},
            {"input": {"nums": [-3, -3, -3]}, "output": [1, [-3]]},
            {"input": {"nums": [1, 2, 3]}, "output": [3, [1, 2, 3]]},
            {"input": {"nums": [-2, -2, -1, 0, 0, 0, 5]}, "output": [4, [-2, -1, 0, 5]]},
            {"input": {"nums": [i // 2 for i in range(10000)]}, "output": [5000, list(range(5000))]},
        ],
        "solution": '''\
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0
        write = 1
        for read in range(1, len(nums)):
            if nums[read] != nums[write - 1]:
                nums[write] = nums[read]
                write += 1
        return write
''',
        "approach": (
            "**Slow/fast pointers.** `write` marks where the next distinct value goes; `read` scans the array. Since the "
            "input is sorted, `nums[read]` is a new value exactly when it differs from the last kept value "
            "`nums[write - 1]`. Copy it there and advance `write`. The final `write` is the number of distinct values.\n\n"
            "**Why it works:** the prefix `nums[:write]` is always a sorted list of the distinct values seen so far, and "
            "`read >= write` so writes never clobber unread data.\n\n"
            "**Common mistakes:** comparing with `nums[read - 1]` instead of the last written value (works here because "
            "the kept value equals the previous element, but breaks in the 'keep at most two' variant); using `del` or "
            "`list.remove` inside the loop (O(n^2)); forgetting the empty-array guard.\n\n"
            "**Interview follow-ups:** Allow each value at most twice (compare with `nums[write - 2]`). "
            "Remove a specific value instead of duplicates (Remove Element, same skeleton). "
            "Do it on a sorted linked list (skip nodes whose next has the same value)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["remove-element", "move-zeroes", "remove-duplicates-from-sorted-array-ii"],
    },
    {
        "id": "move-zeroes",
        "title": "Move Zeroes",
        "difficulty": "Easy",
        "pattern": "Two Pointers",
        "tags": ["Array", "Two Pointers"],
        "companies": {"google": 2, "apple": 3, "meta": 4, "amazon": 2, "microsoft": 2},
        "description": (
            "Given an integer array `nums`, move every `0` to the end **in place** while keeping the relative order of the "
            "non-zero elements. Do not return anything and do not make a copy of the array."
        ),
        "examples": [
            {"input": "nums = [0,1,0,3,12]", "output": "[1,3,12,0,0]"},
            {"input": "nums = [0]", "output": "[0]"},
            {"input": "nums = [0,-1,0,-2]", "output": "[-1,-2,0,0]", "explanation": "Negative values are non-zero and keep their order."},
        ],
        "constraints": ["1 <= nums.length <= 10^4", "-2^31 <= nums[i] <= 2^31 - 1"],
        "hints": [
            "Think of it as compacting the non-zero elements to the front; the zeros end up wherever is left.",
            "Keep a pointer to the next slot for a non-zero value. When you see a non-zero, swap it into that slot and advance the pointer.",
            "Swapping (rather than overwriting then zero-filling) keeps the solution one pass and minimises writes when there are few zeros.",
        ],
        "function": "moveZeroes",
        "signature": "def moveZeroes(self, nums: List[int]) -> None:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "None",
        "output_mode": "arg:nums",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [0, 1, 0, 3, 12]}, "output": [1, 3, 12, 0, 0]},
            {"input": {"nums": [0]}, "output": [0]},
            {"input": {"nums": [0, -1, 0, -2]}, "output": [-1, -2, 0, 0]},
            {"input": {"nums": [1, 2, 3]}, "output": [1, 2, 3]},
            {"input": {"nums": [0, 0, 0]}, "output": [0, 0, 0]},
            {"input": {"nums": [2, 0]}, "output": [2, 0]},
            {"input": {"nums": [0, 0, 1]}, "output": [1, 0, 0]},
            {"input": {"nums": [0, 1] * 2500}, "output": [1] * 2500 + [0] * 2500},
        ],
        "solution": '''\
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        insert = 0  # next position for a non-zero value
        for i in range(len(nums)):
            if nums[i] != 0:
                nums[insert], nums[i] = nums[i], nums[insert]
                insert += 1
''',
        "approach": (
            "**Partition with a write pointer.** `insert` is the boundary of the compacted non-zero prefix. Scan with `i`; "
            "whenever `nums[i]` is non-zero, swap it into position `insert` and advance `insert`. Everything before `insert` "
            "is non-zero and in original order; everything between `insert` and `i` is zero.\n\n"
            "**Why it works:** the invariant `nums[insert..i-1]` are all zeros holds because a non-zero at `i` is always "
            "swapped out of that range immediately, so the swap only ever exchanges a non-zero with a zero (or with itself).\n\n"
            "**Common mistakes:** a two-pass overwrite-then-fill version is fine but interviewers often ask for a single "
            "pass; using `nums.remove(0)` in a loop (O(n^2) and shifts the array); losing stability of the non-zero order "
            "by swapping from the back.\n\n"
            "**Interview follow-ups:** Minimise the number of writes (only swap when `i != insert`). "
            "Move a different value, or all elements satisfying a predicate, to the end (same partition). "
            "Partition into three groups in one pass (Dutch National Flag, see Sort Colors)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["remove-duplicates-from-sorted-array", "sort-colors", "remove-element"],
    },
    {
        "id": "sort-colors",
        "title": "Sort Colors",
        "difficulty": "Medium",
        "pattern": "Two Pointers",
        "tags": ["Array", "Two Pointers", "Sorting"],
        "companies": {"google": 2, "apple": 2, "meta": 3, "amazon": 2, "microsoft": 3},
        "description": (
            "`nums` contains only the values `0`, `1` and `2`, representing red, white and blue. Sort it **in place** so "
            "all 0s come first, then all 1s, then all 2s.\n\n"
            "Do not call a library sort. The goal is a single pass with constant extra space."
        ),
        "examples": [
            {"input": "nums = [2,0,2,1,1,0]", "output": "[0,0,1,1,2,2]"},
            {"input": "nums = [2,0,1]", "output": "[0,1,2]"},
        ],
        "constraints": ["1 <= nums.length <= 300", "nums[i] is 0, 1 or 2."],
        "hints": [
            "Counting sort works in two passes: count the 0s, 1s and 2s, then overwrite the array. Can you do it in one pass?",
            "Maintain three regions: 0s at the front (ending at `low`), 2s at the back (starting at `high`), and unknowns in between scanned by `mid`.",
            "On a 0 swap with `low` and advance both; on a 2 swap with `high` and move `high` left but do NOT advance `mid`, since the swapped-in value is unexamined; on a 1 just advance `mid`.",
        ],
        "function": "sortColors",
        "signature": "def sortColors(self, nums: List[int]) -> None:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "None",
        "output_mode": "arg:nums",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [2, 0, 2, 1, 1, 0]}, "output": [0, 0, 1, 1, 2, 2]},
            {"input": {"nums": [2, 0, 1]}, "output": [0, 1, 2]},
            {"input": {"nums": [0]}, "output": [0]},
            {"input": {"nums": [1, 1]}, "output": [1, 1]},
            {"input": {"nums": [2, 2, 2, 0]}, "output": [0, 2, 2, 2]},
            {"input": {"nums": [1, 0]}, "output": [0, 1]},
            {"input": {"nums": [2, 2, 0, 0, 1, 1]}, "output": [0, 0, 1, 1, 2, 2]},
            {"input": {"nums": [i % 3 for i in range(6000)]}, "output": [0] * 2000 + [1] * 2000 + [2] * 2000},
            {"input": {"nums": [2] * 3000 + [0] * 3000}, "output": [0] * 3000 + [2] * 3000},
        ],
        "solution": '''\
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        low, mid, high = 0, 0, len(nums) - 1
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 2:
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
            else:
                mid += 1
''',
        "approach": (
            "**Dutch National Flag (three-way partition).** Keep three pointers: `low` is the end of the 0-region, `high` "
            "the start of the 2-region, and `mid` scans the unknown middle. A 0 at `mid` is swapped to `low` (both advance, "
            "because what came back from `low` is a 1 or the same 0). A 2 is swapped to `high` and `high` moves left, but "
            "`mid` stays put since the value that arrived has not been examined. A 1 is already in the right region.\n\n"
            "**Why it works:** the invariants are `nums[:low]` all 0, `nums[low:mid]` all 1, `nums[high+1:]` all 2. Each "
            "iteration either advances `mid` or shrinks `high`, so the unknown region `mid..high` shrinks until empty.\n\n"
            "**Common mistakes:** advancing `mid` after swapping with `high` (the classic bug, leaves a 0 or 2 unsorted); "
            "using `<` instead of `<=` in the loop condition (skips the final element); reaching for counting sort when "
            "the interviewer explicitly asks for one pass.\n\n"
            "**Interview follow-ups:** Why is the swap with `low` safe to advance `mid` on? (the region `low..mid-1` is "
            "all 1s, so the swapped-in value is a 1, or `low == mid`). Generalise to k colours? (counting sort, or "
            "repeated partitions; one-pass with k-1 pointers gets unwieldy). Relation to quicksort's 3-way partition (same scheme, with the pivot as the 'middle' value)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["move-zeroes", "remove-duplicates-from-sorted-array", "kth-largest-element-in-an-array"],
    },
]
