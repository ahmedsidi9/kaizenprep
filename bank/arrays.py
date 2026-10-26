"""Arrays & Hashing problems. See SCHEMA.md for the dict format."""

# A complete, valid 9x9 sudoku grid built from a shifted pattern:
# row r, column c holds (3r + r//3 + c) % 9 + 1. Rows, columns and boxes are all permutations of 1..9.
_SUDOKU_FULL = [[str((3 * r + r // 3 + c) % 9 + 1) for c in range(9)] for r in range(9)]


def _sudoku(cells: dict) -> list:
    """Build a mostly-empty board from {(row, col): digit}."""
    board = [["."] * 9 for _ in range(9)]
    for (r, c), v in cells.items():
        board[r][c] = v
    return board


# Partially filled valid board: keep the cells of the full grid where (r * 7 + c * 3) % 5 == 0.
_SUDOKU_PARTIAL = [[_SUDOKU_FULL[r][c] if (r * 7 + c * 3) % 5 == 0 else "." for c in range(9)] for r in range(9)]

PROBLEMS = [
    {
        "id": "contains-duplicate",
        "title": "Contains Duplicate",
        "difficulty": "Easy",
        "pattern": "Arrays & Hashing",
        "tags": ["Array", "Hash Table", "Sorting"],
        "companies": {"google": 2, "apple": 3, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "You are given an integer array `nums`. Return `true` if some value occurs **more than once** "
            "in the array, and `false` if every value is distinct."
        ),
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "true", "explanation": "The value 1 appears at index 0 and index 3."},
            {"input": "nums = [1,2,3,4]", "output": "false", "explanation": "All four values are different."},
            {"input": "nums = [1,1,1,3,3,4,3,2,4,2]", "output": "true"},
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
        "hints": [
            "Comparing every pair is O(n^2). Can you remember the values you have already passed?",
            "A hash set gives O(1) membership checks. Add each value as you go and stop as soon as you see one that is already present.",
            "Sorting first and comparing neighbours also works in O(n log n) with O(1) extra space if the array may be modified.",
        ],
        "function": "containsDuplicate",
        "signature": "def containsDuplicate(self, nums: List[int]) -> bool:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [1, 2, 3, 1]}, "output": True},
            {"input": {"nums": [1, 2, 3, 4]}, "output": False},
            {"input": {"nums": [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]}, "output": True},
            {"input": {"nums": []}, "output": False},
            {"input": {"nums": [5]}, "output": False},
            {"input": {"nums": [-1, -1]}, "output": True},
            {"input": {"nums": list(range(10000))}, "output": False},
            {"input": {"nums": list(range(10000)) + [0]}, "output": True},
        ],
        "solution": '''\
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for x in nums:
            if x in seen:
                return True
            seen.add(x)
        return False
''',
        "approach": (
            "**Hash set of seen values.** Scan left to right; before inserting a value, check whether the set already "
            "holds it. The first hit proves a duplicate, so you can return immediately without finishing the scan.\n\n"
            "**Why it works:** a value is a duplicate exactly when an earlier index held the same value, and the set is "
            "precisely the collection of earlier values.\n\n"
            "**Common mistakes:** forgetting that `len(set(nums)) < len(nums)` is a fine one-liner but always does the full "
            "O(n) work; sorting the input when the caller did not allow mutation.\n\n"
            "**Interview follow-ups:** Can you do it with O(1) extra space? (sort then compare neighbours, O(n log n)). "
            "What if the values are bounded in `[0, n)`? (use the array itself as a bitmap by negating visited indices). "
            "What about a stream where you must answer after each element? (the set approach is already online)."
        ),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "similar": ["valid-anagram", "two-sum"],
    },
    {
        "id": "valid-anagram",
        "title": "Valid Anagram",
        "difficulty": "Easy",
        "pattern": "Arrays & Hashing",
        "tags": ["Hash Table", "String", "Sorting"],
        "companies": {"google": 2, "apple": 2, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "Given two strings `s` and `t`, decide whether `t` is an **anagram** of `s`: the same multiset of "
            "characters arranged in any order. Return `true` or `false`."
        ),
        "examples": [
            {"input": "s = \"anagram\", t = \"nagaram\"", "output": "true"},
            {"input": "s = \"rat\", t = \"car\"", "output": "false", "explanation": "`t` has a `c` that `s` lacks."},
            {"input": "s = \"aacc\", t = \"ccac\"", "output": "false", "explanation": "Same letters, but the counts differ (two `a` vs one)."},
        ],
        "constraints": ["0 <= s.length, t.length <= 5 * 10^4", "s and t consist of lowercase English letters."],
        "hints": [
            "Two strings of different length can never be anagrams. Check that first.",
            "Anagrams have identical character counts. Count the letters of each string and compare the counts.",
            "With a 26-letter alphabet a fixed-size array of counts is enough: add for `s`, subtract for `t`, and every slot must end at zero.",
        ],
        "function": "isAnagram",
        "signature": "def isAnagram(self, s: str, t: str) -> bool:",
        "arg_types": {"s": "str", "t": "str"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"s": "anagram", "t": "nagaram"}, "output": True},
            {"input": {"s": "rat", "t": "car"}, "output": False},
            {"input": {"s": "aacc", "t": "ccac"}, "output": False},
            {"input": {"s": "", "t": ""}, "output": True},
            {"input": {"s": "a", "t": "ab"}, "output": False},
            {"input": {"s": "ab", "t": "ba"}, "output": True},
            {"input": {"s": "ab" * 5000, "t": "ba" * 5000}, "output": True},
            {"input": {"s": "a" * 10000, "t": "a" * 9999 + "b"}, "output": False},
        ],
        "solution": '''\
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        counts = [0] * 26
        for a, b in zip(s, t):
            counts[ord(a) - 97] += 1
            counts[ord(b) - 97] -= 1
        return all(c == 0 for c in counts)
''',
        "approach": (
            "**Character counting.** Two strings are anagrams exactly when every character appears the same number of "
            "times in both. Walk both strings together, incrementing a counter for the letter from `s` and decrementing "
            "for the letter from `t`. If all 26 counters finish at zero the strings match.\n\n"
            "**Why it works:** the counter array is the difference of the two multisets; it is all zeros exactly when the "
            "multisets are equal. The early length check is what makes a single `zip` pass safe.\n\n"
            "**Common mistakes:** skipping the length check (then `zip` silently truncates); sorting both strings is correct "
            "but O(n log n) and interviewers usually ask for the linear version.\n\n"
            "**Interview follow-ups:** What if the strings contain Unicode? (use a hash map instead of a 26-slot array). "
            "How would you find all anagrams of a pattern inside a long text? (sliding window over counts). "
            "How do you group many words by anagram class? (see Group Anagrams)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1) (26 counters)"},
        "similar": ["group-anagrams", "permutation-in-string"],
    },
    {
        "id": "group-anagrams",
        "title": "Group Anagrams",
        "difficulty": "Medium",
        "pattern": "Arrays & Hashing",
        "tags": ["Array", "Hash Table", "String", "Sorting"],
        "companies": {"google": 2, "apple": 2, "meta": 3, "amazon": 4, "microsoft": 3},
        "description": (
            "Given a list of strings `strs`, partition them into groups where every string in a group is an anagram of "
            "the others. Return the list of groups; the order of groups and the order inside a group do not matter."
        ),
        "examples": [
            {"input": "strs = [\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]", "output": "[[\"bat\"],[\"nat\",\"tan\"],[\"ate\",\"eat\",\"tea\"]]"},
            {"input": "strs = [\"\"]", "output": "[[\"\"]]"},
            {"input": "strs = [\"a\"]", "output": "[[\"a\"]]"},
        ],
        "constraints": ["1 <= strs.length <= 10^4", "0 <= strs[i].length <= 100", "strs[i] consists of lowercase English letters."],
        "hints": [
            "All anagrams share something that does not depend on letter order. What canonical form could you compute for each word?",
            "Use that canonical form as a dictionary key and append each word to its bucket.",
            "The sorted word works as a key in O(k log k) per word. A tuple of 26 letter counts is O(k) and avoids sorting.",
        ],
        "function": "groupAnagrams",
        "signature": "def groupAnagrams(self, strs: List[str]) -> List[List[str]]:",
        "arg_types": {"strs": "List[str]"},
        "return_type": "List[List[str]]",
        "compare": "unordered_nested",
        "tests": [
            {"input": {"strs": ["eat", "tea", "tan", "ate", "nat", "bat"]}, "output": [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]},
            {"input": {"strs": [""]}, "output": [[""]]},
            {"input": {"strs": ["a"]}, "output": [["a"]]},
            {"input": {"strs": ["ab", "ba", "abc", "cab", "bca", "x"]}, "output": [["ab", "ba"], ["abc", "cab", "bca"], ["x"]]},
            {"input": {"strs": ["", "", "b"]}, "output": [["", ""], ["b"]]},
            {"input": {"strs": ["aab", "aba", "baa", "abb"]}, "output": [["aab", "aba", "baa"], ["abb"]]},
            {
                # 26*26*8 = 5408 two-letter words; "cd" and "dc" land in the same group.
                "input": {"strs": [c + d for c in "abcdefghijklmnopqrstuvwxyz" for d in "abcdefghijklmnopqrstuvwxyz" for _ in range(8)]},
                "output": (
                    [[c + d] * 8 + [d + c] * 8 for c in "abcdefghijklmnopqrstuvwxyz" for d in "abcdefghijklmnopqrstuvwxyz" if c < d]
                    + [[c + c] * 8 for c in "abcdefghijklmnopqrstuvwxyz"]
                ),
            },
        ],
        "solution": '''\
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for word in strs:
            counts = [0] * 26
            for ch in word:
                counts[ord(ch) - 97] += 1
            groups[tuple(counts)].append(word)
        return list(groups.values())
''',
        "approach": (
            "**Bucket by a canonical key.** Every anagram class has a unique fingerprint that ignores order: the sorted "
            "word, or the tuple of 26 letter counts. Map fingerprint -> list of words, then return the lists.\n\n"
            "**Why it works:** two words are anagrams iff their letter multisets are equal iff their fingerprints are equal, "
            "so each bucket is exactly one anagram class.\n\n"
            "**Common mistakes:** using a list as a dict key (unhashable, must be a tuple); building the key with "
            "`''.join(sorted(word))` and then being surprised by the extra log factor when asked about complexity; "
            "forgetting that the empty string is a valid word with an all-zero fingerprint.\n\n"
            "**Interview follow-ups:** What if the alphabet is Unicode? (sorted-string key, or a frozenset of (char, count) pairs). "
            "Memory for 10^5 words? (the count tuple is 26 ints per distinct class, not per word). "
            "How would you stream words and emit a group as soon as it is complete? (you cannot know a group is complete; "
            "discuss why and what the caller could tolerate)."
        ),
        "complexity": {"time": "O(n * k) with the count key (O(n * k log k) with sorting)", "space": "O(n * k)"},
        "similar": ["valid-anagram", "top-k-frequent-elements"],
    },
    {
        "id": "top-k-frequent-elements",
        "title": "Top K Frequent Elements",
        "difficulty": "Medium",
        "pattern": "Arrays & Hashing",
        "tags": ["Array", "Hash Table", "Heap", "Bucket Sort"],
        "companies": {"google": 3, "apple": 3, "meta": 3, "amazon": 4, "microsoft": 2},
        "description": (
            "Given an integer array `nums` and an integer `k`, return the `k` values that occur most often. "
            "The input is guaranteed to have a unique answer, and the result may be in any order.\n\n"
            "Aim for something faster than sorting all distinct values by frequency."
        ),
        "examples": [
            {"input": "nums = [1,1,1,2,2,3], k = 2", "output": "[1,2]", "explanation": "1 appears three times and 2 twice; 3 only once."},
            {"input": "nums = [1], k = 1", "output": "[1]"},
            {"input": "nums = [4,4,4,5,5,6], k = 1", "output": "[4]"},
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4", "1 <= k <= number of distinct values", "The answer is unique."],
        "hints": [
            "Start by counting how often each value appears with a hash map.",
            "You need the k largest counts. A min-heap of size k gives O(n log k).",
            "A frequency can never exceed n. Put each value into bucket[frequency] and read the buckets from the top down for O(n).",
        ],
        "function": "topKFrequent",
        "signature": "def topKFrequent(self, nums: List[int], k: int) -> List[int]:",
        "arg_types": {"nums": "List[int]", "k": "int"},
        "return_type": "List[int]",
        "compare": "unordered",
        "tests": [
            {"input": {"nums": [1, 1, 1, 2, 2, 3], "k": 2}, "output": [1, 2]},
            {"input": {"nums": [1], "k": 1}, "output": [1]},
            {"input": {"nums": [4, 4, 4, 5, 5, 6], "k": 1}, "output": [4]},
            {"input": {"nums": [-1, -1, -2, -2, 3], "k": 2}, "output": [-1, -2]},
            {"input": {"nums": [1, 2, 3, 4, 5], "k": 5}, "output": [1, 2, 3, 4, 5]},
            {"input": {"nums": [0, 0, 0, 0], "k": 1}, "output": [0]},
            {"input": {"nums": list(range(5000)) + [7] * 3 + [42] * 2, "k": 2}, "output": [7, 42]},
        ],
        "solution": '''\
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = Counter(nums)
        buckets = [[] for _ in range(len(nums) + 1)]
        for value, count in freq.items():
            buckets[count].append(value)
        result = []
        for count in range(len(nums), 0, -1):
            for value in buckets[count]:
                result.append(value)
                if len(result) == k:
                    return result
        return result
''',
        "approach": (
            "**Count, then bucket by frequency.** A hash map gives every distinct value its count. Since a count is at most "
            "`n`, an array of `n + 1` buckets indexed by count sorts the values by frequency without comparisons. Read the "
            "buckets from `n` down to `1` and stop after collecting `k` values.\n\n"
            "**Why it works:** walking buckets from high to low visits values in non-increasing frequency, and the problem "
            "promises the top `k` are unambiguous, so the first `k` collected are the answer.\n\n"
            "**Common mistakes:** sorting the whole frequency map (O(m log m), fine but not what is asked); using a max-heap "
            "of all values instead of a min-heap of size k; off-by-one on the bucket array size (a value can appear `n` times).\n\n"
            "**Interview follow-ups:** How does the heap version compare? (O(n log k) time, O(k) extra, better when k is tiny). "
            "What about Quickselect on the frequency list? (average O(n), worst O(n^2)). "
            "How would you do this over a stream with limited memory? (approximate counting such as Count-Min sketch plus a heap)."
        ),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "similar": ["group-anagrams", "kth-largest-element-in-an-array", "sort-characters-by-frequency"],
    },
    {
        "id": "product-of-array-except-self",
        "title": "Product of Array Except Self",
        "difficulty": "Medium",
        "pattern": "Arrays & Hashing",
        "tags": ["Array", "Prefix Sum"],
        "companies": {"google": 2, "apple": 3, "meta": 3, "amazon": 5, "microsoft": 3},
        "description": (
            "Given an integer array `nums`, build an array `answer` where `answer[i]` is the product of every element "
            "of `nums` **except** `nums[i]`.\n\n"
            "You must do it in O(n) time **without using division**. Every product is guaranteed to fit in a 32-bit integer."
        ),
        "examples": [
            {"input": "nums = [1,2,3,4]", "output": "[24,12,8,6]", "explanation": "answer[0] = 2*3*4 = 24, answer[1] = 1*3*4 = 12, and so on."},
            {"input": "nums = [-1,1,0,-3,3]", "output": "[0,0,9,0,0]", "explanation": "Only index 2 excludes the zero, so only it is non-zero: (-1)*1*(-3)*3 = 9."},
        ],
        "constraints": ["2 <= nums.length <= 10^5", "-30 <= nums[i] <= 30", "Every prefix and suffix product fits in a 32-bit integer."],
        "hints": [
            "Division is ruled out, and zeros make it fragile anyway. Think about what multiplies to give the answer at index i.",
            "The product of everything left of i times the product of everything right of i is exactly what you need.",
            "Fill the output with prefix products in one pass, then sweep from the right multiplying in a running suffix product. No extra arrays needed.",
        ],
        "function": "productExceptSelf",
        "signature": "def productExceptSelf(self, nums: List[int]) -> List[int]:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [1, 2, 3, 4]}, "output": [24, 12, 8, 6]},
            {"input": {"nums": [-1, 1, 0, -3, 3]}, "output": [0, 0, 9, 0, 0]},
            {"input": {"nums": [2, 3]}, "output": [3, 2]},
            {"input": {"nums": [0, 0]}, "output": [0, 0]},
            {"input": {"nums": [5, 0]}, "output": [0, 5]},
            {"input": {"nums": [1, -1, 1, -1]}, "output": [1, -1, 1, -1]},
            {"input": {"nums": [1] * 2500 + [2] + [1] * 2499}, "output": [2] * 2500 + [1] + [2] * 2499},
        ],
        "solution": '''\
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        answer = [1] * n
        prefix = 1
        for i in range(n):
            answer[i] = prefix
            prefix *= nums[i]
        suffix = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= suffix
            suffix *= nums[i]
        return answer
''',
        "approach": (
            "**Prefix products times suffix products.** `answer[i] = (nums[0] * ... * nums[i-1]) * (nums[i+1] * ... * nums[n-1])`. "
            "A left-to-right pass stores the left product in `answer[i]`; a right-to-left pass multiplies in the right product "
            "using a single running variable. The output array is the only storage, so extra space is O(1).\n\n"
            "**Why it works:** the two factors together cover every index except `i` exactly once, and no division is "
            "involved so zeros are handled naturally (a zero on either side makes that side's product zero).\n\n"
            "**Common mistakes:** dividing the total product by `nums[i]` (breaks on zero and is forbidden); allocating "
            "separate prefix and suffix arrays when asked for constant extra space; off-by-one when the running product "
            "should be updated after writing, not before.\n\n"
            "**Interview follow-ups:** How would you handle it if division were allowed? (count zeros: 0 zeros divide, 1 zero "
            "only that slot is non-zero, 2+ zeros all zero). "
            "What if the products can overflow? (modular arithmetic or big integers, and discuss what the caller wants). "
            "Can you do the same for sums? (trivial: total minus element, which is why the product version forbids division)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1) beyond the output"},
        "similar": ["subarray-sum-equals-k", "trapping-rain-water"],
    },
    {
        "id": "longest-consecutive-sequence",
        "title": "Longest Consecutive Sequence",
        "difficulty": "Medium",
        "pattern": "Arrays & Hashing",
        "tags": ["Array", "Hash Table", "Union Find"],
        "companies": {"google": 3, "apple": 1, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "Given an unsorted integer array `nums`, return the length of the longest run of **consecutive integers** "
            "that all appear in the array (for example `3, 4, 5, 6`). The values do not have to be adjacent in the input.\n\n"
            "Your algorithm must run in O(n) time."
        ),
        "examples": [
            {"input": "nums = [100,4,200,1,3,2]", "output": "4", "explanation": "1, 2, 3, 4 are all present."},
            {"input": "nums = [0,3,7,2,5,8,4,6,0,1]", "output": "9", "explanation": "0 through 8 are all present; the duplicate 0 does not count twice."},
            {"input": "nums = []", "output": "0"},
        ],
        "constraints": ["0 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
        "hints": [
            "Sorting gives O(n log n). To beat it, use a set for O(1) 'is x present?' queries.",
            "A number x is the start of a run exactly when x - 1 is not in the set. Only start counting from such numbers.",
            "From each start, walk x, x+1, x+2 ... while present. Each number is visited by at most one walk, so the total work is linear.",
        ],
        "function": "longestConsecutive",
        "signature": "def longestConsecutive(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [100, 4, 200, 1, 3, 2]}, "output": 4},
            {"input": {"nums": [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]}, "output": 9},
            {"input": {"nums": []}, "output": 0},
            {"input": {"nums": [1]}, "output": 1},
            {"input": {"nums": [1, 1, 1]}, "output": 1},
            {"input": {"nums": [-3, -2, -1, 0, 5]}, "output": 4},
            {"input": {"nums": [9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6]}, "output": 7},
            {"input": {"nums": list(range(0, 10000, 2)) + list(range(1, 3001, 2))}, "output": 3001},
        ],
        "solution": '''\
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        present = set(nums)
        best = 0
        for x in present:
            if x - 1 in present:
                continue  # not the start of a run
            length = 1
            while x + length in present:
                length += 1
            best = max(best, length)
        return best
''',
        "approach": (
            "**Hash set and only expand from run starts.** Put all values in a set. For each value `x` whose predecessor "
            "`x - 1` is absent, `x` begins a run; count upward while `x + 1, x + 2, ...` are present.\n\n"
            "**Why it is linear:** each run is walked exactly once, from its unique start, and the walks are disjoint. "
            "Non-start values cost one O(1) lookup each. Duplicates collapse in the set, so they cannot inflate a run.\n\n"
            "**Common mistakes:** iterating over the original list rather than the set (duplicates then redo the same walk); "
            "starting a walk from every number, which degrades to O(n^2) on a sorted input; assuming sorting is acceptable "
            "when the prompt explicitly says O(n).\n\n"
            "**Interview follow-ups:** How would you return the run itself, not just its length? (remember the best start). "
            "Can this be done with union-find? (yes, union x with x+1 when both exist; same complexity, more code). "
            "What if the numbers arrive as a stream? (keep interval endpoints in a map and merge neighbours on insert)."
        ),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "similar": ["contains-duplicate", "merge-intervals"],
    },
    {
        "id": "subarray-sum-equals-k",
        "title": "Subarray Sum Equals K",
        "difficulty": "Medium",
        "pattern": "Arrays & Hashing",
        "tags": ["Array", "Hash Table", "Prefix Sum"],
        "companies": {"google": 3, "apple": 2, "meta": 5, "amazon": 3, "microsoft": 2},
        "description": (
            "Given an integer array `nums` (which may contain negatives and zeros) and an integer `k`, return the number "
            "of **contiguous** subarrays whose elements sum to exactly `k`."
        ),
        "examples": [
            {"input": "nums = [1,1,1], k = 2", "output": "2", "explanation": "[1,1] starting at index 0 and [1,1] starting at index 1."},
            {"input": "nums = [1,2,3], k = 3", "output": "2", "explanation": "[1,2] and [3]."},
            {"input": "nums = [1,-1,0], k = 0", "output": "3", "explanation": "[1,-1], [0] and [1,-1,0]."},
        ],
        "constraints": ["1 <= nums.length <= 2 * 10^4", "-1000 <= nums[i] <= 1000", "-10^7 <= k <= 10^7"],
        "hints": [
            "Negative numbers break the sliding-window approach, because growing the window does not always grow the sum.",
            "The sum of nums[i..j] equals prefix[j] - prefix[i-1]. You want pairs of prefix sums that differ by exactly k.",
            "Scan once keeping a running sum and a map prefix -> how many times seen. For each position add map[running - k] to the answer, then record the running sum. Seed the map with {0: 1}.",
        ],
        "function": "subarraySum",
        "signature": "def subarraySum(self, nums: List[int], k: int) -> int:",
        "arg_types": {"nums": "List[int]", "k": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [1, 1, 1], "k": 2}, "output": 2},
            {"input": {"nums": [1, 2, 3], "k": 3}, "output": 2},
            {"input": {"nums": [1, -1, 0], "k": 0}, "output": 3},
            {"input": {"nums": [1], "k": 0}, "output": 0},
            {"input": {"nums": [-1, -1, 1], "k": 0}, "output": 1},
            {"input": {"nums": [0, 0, 0, 0], "k": 0}, "output": 10},
            {"input": {"nums": [3, 4, 7, 2, -3, 1, 4, 2], "k": 7}, "output": 4},
            {"input": {"nums": [1] * 5000, "k": 5}, "output": 4996},
        ],
        "solution": '''\
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        seen = defaultdict(int)
        seen[0] = 1  # the empty prefix
        running = 0
        count = 0
        for x in nums:
            running += x
            count += seen[running - k]
            seen[running] += 1
        return count
''',
        "approach": (
            "**Prefix sums in a hash map.** Let `P[j]` be the sum of the first `j` elements. The subarray ending at index "
            "`j` and starting after index `i` sums to `P[j] - P[i]`, so we want the number of earlier prefixes equal to "
            "`P[j] - k`. Keep a map from prefix value to how many times it has occurred; at each step add "
            "`map[running - k]` to the answer and then record `running`.\n\n"
            "**Why it works:** every subarray corresponds to exactly one ordered pair of prefix indices `(i, j)` with "
            "`i < j`, and recording the current prefix *after* querying guarantees `i < j`. Seeding `{0: 1}` accounts "
            "for subarrays that start at index 0.\n\n"
            "**Common mistakes:** trying a sliding window (fails with negatives and zeros); recording before querying "
            "(counts the empty subarray when `k == 0`); forgetting the `{0: 1}` seed.\n\n"
            "**Interview follow-ups:** Return the longest or shortest such subarray instead of the count? (store first or last "
            "index per prefix). Count subarrays whose sum is divisible by k? (same idea keyed on `prefix % k`). "
            "Two-dimensional version, counting submatrices summing to a target? (fix a row pair, collapse columns, reuse this)."
        ),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "similar": ["two-sum", "product-of-array-except-self", "continuous-subarray-sum"],
    },
    {
        "id": "majority-element",
        "title": "Majority Element",
        "difficulty": "Easy",
        "pattern": "Arrays & Hashing",
        "tags": ["Array", "Hash Table", "Divide and Conquer", "Counting"],
        "companies": {"google": 2, "apple": 2, "meta": 1, "amazon": 3, "microsoft": 2},
        "description": (
            "Given an array `nums` of length `n`, return the value that appears **more than** `n / 2` times. "
            "Such a value is guaranteed to exist.\n\n"
            "Can you do it in linear time and O(1) extra space?"
        ),
        "examples": [
            {"input": "nums = [3,2,3]", "output": "3"},
            {"input": "nums = [2,2,1,1,1,2,2]", "output": "2", "explanation": "2 appears 4 times out of 7."},
        ],
        "constraints": ["1 <= nums.length <= 5 * 10^4", "-10^9 <= nums[i] <= 10^9", "A majority element always exists."],
        "hints": [
            "A hash map of counts solves it in O(n) time and O(n) space. The interesting part is dropping the space.",
            "Pair up each occurrence of the majority value with a different value and cancel them. The majority survives because it has more than half.",
            "Boyer-Moore voting: keep a candidate and a counter. Same value: +1. Different value: -1. Counter at zero: adopt the current value as the new candidate.",
        ],
        "function": "majorityElement",
        "signature": "def majorityElement(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [3, 2, 3]}, "output": 3},
            {"input": {"nums": [2, 2, 1, 1, 1, 2, 2]}, "output": 2},
            {"input": {"nums": [1]}, "output": 1},
            {"input": {"nums": [-5, -5, -5, 2, 3]}, "output": -5},
            {"input": {"nums": [6, 5, 5]}, "output": 5},
            {"input": {"nums": [1, 2, 1, 2, 1]}, "output": 1},
            {"input": {"nums": [7] * 5001 + list(range(5000))}, "output": 7},
        ],
        "solution": '''\
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        candidate = None
        count = 0
        for x in nums:
            if count == 0:
                candidate = x
            count += 1 if x == candidate else -1
        return candidate
''',
        "approach": (
            "**Boyer-Moore majority vote.** Hold one candidate and a counter. Each element that matches the candidate adds a "
            "vote, each mismatch removes one, and when the counter hits zero the next element becomes the candidate.\n\n"
            "**Why it works:** every decrement pairs one majority occurrence with one non-majority occurrence (or cancels two "
            "non-majority values against each other, which only helps). Since the majority has strictly more than half the "
            "slots, it cannot be fully cancelled, so it is the candidate standing at the end.\n\n"
            "**Common mistakes:** returning the candidate without the 'more than n/2' guarantee (without it you need a second "
            "verification pass); using `n // 2` as a threshold and confusing 'at least' with 'more than'.\n\n"
            "**Interview follow-ups:** What if no majority is guaranteed? (verify the candidate with one more pass). "
            "Find all elements appearing more than n/3 times? (generalised voting with two candidates). "
            "Alternative approaches? (sort and take the middle element, O(n log n); randomised sampling with verification)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["majority-element-ii", "top-k-frequent-elements"],
    },
    {
        "id": "first-missing-positive",
        "title": "First Missing Positive",
        "difficulty": "Hard",
        "pattern": "Arrays & Hashing",
        "tags": ["Array", "Hash Table"],
        "companies": {"google": 2, "apple": 2, "meta": 2, "amazon": 3, "microsoft": 3},
        "description": (
            "Given an unsorted integer array `nums`, return the smallest positive integer (1, 2, 3, ...) that is **not** "
            "present in it.\n\n"
            "The expected solution runs in O(n) time and uses only **constant** extra space; you may modify the input."
        ),
        "examples": [
            {"input": "nums = [1,2,0]", "output": "3", "explanation": "1 and 2 are present, 3 is not."},
            {"input": "nums = [3,4,-1,1]", "output": "2"},
            {"input": "nums = [7,8,9,11,12]", "output": "1", "explanation": "1 is the smallest positive integer and it is missing."},
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-2^31 <= nums[i] <= 2^31 - 1"],
        "hints": [
            "A hash set gives O(n) time with O(n) space. The challenge is the constant extra space.",
            "The answer is always in the range 1..n+1, because n numbers can cover at most n of the positives 1..n.",
            "Use the array as its own hash table: try to place each value v in 1..n at index v - 1 by swapping. Afterwards the first index i with nums[i] != i + 1 gives the answer i + 1.",
        ],
        "function": "firstMissingPositive",
        "signature": "def firstMissingPositive(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [1, 2, 0]}, "output": 3},
            {"input": {"nums": [3, 4, -1, 1]}, "output": 2},
            {"input": {"nums": [7, 8, 9, 11, 12]}, "output": 1},
            {"input": {"nums": [1]}, "output": 2},
            {"input": {"nums": [2]}, "output": 1},
            {"input": {"nums": [1, 1]}, "output": 2},
            {"input": {"nums": [2, 2, 2]}, "output": 1},
            {"input": {"nums": [1, 2, 3, 4, 5]}, "output": 6},
            {"input": {"nums": [-1, -2, -3]}, "output": 1},
            {"input": {"nums": list(range(5000, 0, -1)) + [1]}, "output": 5001},
            {"input": {"nums": list(range(2, 6000))}, "output": 1},
        ],
        "solution": '''\
class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        for i in range(n):
            # Keep swapping until the value at i is out of range, already home, or a duplicate.
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                target = nums[i] - 1
                nums[i], nums[target] = nums[target], nums[i]
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1
''',
        "approach": (
            "**Cyclic sort: put value v at index v - 1.** Only the values `1..n` matter; anything else can never be the "
            "answer's blocker. For each position, while its value `v` is in range and slot `v - 1` does not already hold "
            "`v`, swap it home. A second pass finds the first slot `i` not holding `i + 1`; that `i + 1` is missing. "
            "If every slot is correct the answer is `n + 1`.\n\n"
            "**Why it is linear:** each swap places one value in its final home permanently, so there are at most `n` swaps in "
            "total even though the inner loop is a `while`. The duplicate check `nums[nums[i] - 1] != nums[i]` is what "
            "prevents an infinite loop on repeated values.\n\n"
            "**Common mistakes:** omitting the duplicate check (infinite loop on `[1, 1]`); using `if` instead of `while` "
            "(the value swapped in is never processed); sorting the array (O(n log n)).\n\n"
            "**Interview follow-ups:** Do it without modifying the input? (then you need O(n) extra space, or discuss "
            "restoring the array). Alternative constant-space trick? (negate `nums[|v| - 1]` as a presence mark after "
            "replacing out-of-range values with `n + 1`). Find the k-th missing positive instead? (count gaps while scanning the sorted-in-place array)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["missing-number", "find-all-duplicates-in-an-array", "find-the-duplicate-number"],
    },
    {
        "id": "merge-sorted-array",
        "title": "Merge Sorted Array",
        "difficulty": "Easy",
        "pattern": "Arrays & Hashing",
        "tags": ["Array", "Two Pointers", "Sorting"],
        "companies": {"google": 2, "apple": 3, "meta": 4, "amazon": 3, "microsoft": 3},
        "description": (
            "You are given two sorted integer arrays. `nums1` has length `m + n`: its first `m` entries are the real "
            "data and the last `n` entries are zeros reserved as scratch space. `nums2` has exactly `n` elements.\n\n"
            "Merge `nums2` into `nums1` so that `nums1` ends up sorted, **in place**. Do not return anything."
        ),
        "examples": [
            {"input": "nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3", "output": "[1,2,2,3,5,6]"},
            {"input": "nums1 = [1], m = 1, nums2 = [], n = 0", "output": "[1]"},
            {"input": "nums1 = [0], m = 0, nums2 = [1], n = 1", "output": "[1]", "explanation": "nums1 held no real data; the single slot is filled from nums2."},
        ],
        "constraints": ["nums1.length == m + n", "nums2.length == n", "0 <= m, n <= 200", "1 <= m + n <= 200", "-10^9 <= nums1[i], nums2[j] <= 10^9"],
        "hints": [
            "Merging from the front overwrites values of nums1 you still need.",
            "The free space is at the back of nums1. Fill from the back with the larger of the two current tails.",
            "Three indices: i = m - 1, j = n - 1, write = m + n - 1. If nums2 runs out first you are done; if nums1 runs out, copy the rest of nums2.",
        ],
        "function": "merge",
        "signature": "def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:",
        "arg_types": {"nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int"},
        "return_type": "None",
        "output_mode": "arg:nums1",
        "compare": "exact",
        "tests": [
            {"input": {"nums1": [1, 2, 3, 0, 0, 0], "m": 3, "nums2": [2, 5, 6], "n": 3}, "output": [1, 2, 2, 3, 5, 6]},
            {"input": {"nums1": [1], "m": 1, "nums2": [], "n": 0}, "output": [1]},
            {"input": {"nums1": [0], "m": 0, "nums2": [1], "n": 1}, "output": [1]},
            {"input": {"nums1": [4, 5, 6, 0, 0, 0], "m": 3, "nums2": [1, 2, 3], "n": 3}, "output": [1, 2, 3, 4, 5, 6]},
            {"input": {"nums1": [-3, -1, 0, 0], "m": 2, "nums2": [-2, 2], "n": 2}, "output": [-3, -2, -1, 2]},
            {"input": {"nums1": [2, 2, 0, 0], "m": 2, "nums2": [2, 2], "n": 2}, "output": [2, 2, 2, 2]},
            {"input": {"nums1": list(range(0, 10000, 2)) + [0] * 5000, "m": 5000, "nums2": list(range(1, 10000, 2)), "n": 5000}, "output": list(range(10000))},
        ],
        "solution": '''\
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        i, j, write = m - 1, n - 1, m + n - 1
        while j >= 0:
            if i >= 0 and nums1[i] > nums2[j]:
                nums1[write] = nums1[i]
                i -= 1
            else:
                nums1[write] = nums2[j]
                j -= 1
            write -= 1
''',
        "approach": (
            "**Merge backwards.** The empty slots are at the end of `nums1`, so write the merged output from the back: "
            "compare the current largest unplaced element of each array and place the bigger one at `write`. Only `j` "
            "needs to reach `-1` for the loop to stop; any leftover `nums1` elements are already in place.\n\n"
            "**Why it works:** the write pointer is always at or ahead of `i`, so we never overwrite an element of `nums1` "
            "that has not yet been consumed. Each step places the largest remaining value, producing sorted output.\n\n"
            "**Common mistakes:** merging from the front (needs a copy of `nums1`); looping on `i >= 0` instead of `j >= 0` "
            "(either terminates early or does useless work); forgetting the `i >= 0` guard inside the comparison when "
            "`nums1`'s real data is exhausted.\n\n"
            "**Interview follow-ups:** Merge k sorted arrays? (heap of heads, O(N log k)). "
            "Merge two sorted linked lists? (dummy head and the same comparison, no backward trick needed). "
            "What if `nums1` had no slack and you had to merge with O(1) extra space? (discuss the in-place merge, which is hard and rarely expected)."
        ),
        "complexity": {"time": "O(m + n)", "space": "O(1)"},
        "similar": ["merge-two-sorted-lists", "squares-of-a-sorted-array"],
    },
    {
        "id": "valid-sudoku",
        "title": "Valid Sudoku",
        "difficulty": "Medium",
        "pattern": "Arrays & Hashing",
        "tags": ["Array", "Hash Table", "Matrix"],
        "companies": {"google": 2, "apple": 2, "meta": 1, "amazon": 3, "microsoft": 2},
        "description": (
            "A 9 x 9 sudoku `board` is partially filled: each cell holds a digit `'1'`-`'9'` or `'.'` for empty. "
            "Decide whether the filled cells so far obey the rules:\n\n"
            "- no digit repeats within a row,\n"
            "- no digit repeats within a column,\n"
            "- no digit repeats within any of the nine 3 x 3 boxes.\n\n"
            "Only the current state is checked; the board does **not** have to be solvable."
        ),
        "examples": [
            {
                "input": (
                    "board =\n[[\"1\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],\n"
                    " [\".\",\".\",\"6\",\".\",\".\",\".\",\".\",\"2\",\".\"],\n"
                    " [\".\",\".\",\".\",\".\",\"2\",\".\",\".\",\".\",\".\"],\n"
                    " [\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],\n"
                    " [\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],\n"
                    " [\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],\n"
                    " [\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],\n"
                    " [\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],\n"
                    " [\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\"8\"]]"
                ),
                "output": "true",
                "explanation": "The two 2s share neither a row, a column nor a box.",
            },
            {
                "input": (
                    "board =\n[[\"5\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],\n"
                    " [\".\",\"5\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],\n"
                    " [\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\",\".\"],\n"
                    " ... (remaining rows empty)]"
                ),
                "output": "false",
                "explanation": "Both 5s are inside the top-left 3 x 3 box.",
            },
        ],
        "constraints": ["board.length == 9", "board[i].length == 9", "board[i][j] is a digit '1'-'9' or '.'."],
        "hints": [
            "You need to know, for every row, column and box, which digits have already been used.",
            "Keep 27 sets: 9 for rows, 9 for columns, 9 for boxes. The box index of cell (r, c) is (r // 3) * 3 + c // 3.",
            "One pass over the 81 cells: for each digit check all three sets, then insert into all three. Any hit means the board is invalid.",
        ],
        "function": "isValidSudoku",
        "signature": "def isValidSudoku(self, board: List[List[str]]) -> bool:",
        "arg_types": {"board": "List[List[str]]"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"board": _sudoku({(0, 0): "1", (1, 2): "6", (1, 7): "2", (2, 4): "2", (8, 8): "8"})}, "output": True},
            {"input": {"board": _sudoku({(0, 0): "5", (1, 1): "5"})}, "output": False},
            {"input": {"board": _sudoku({(0, 0): "5", (0, 8): "5"})}, "output": False},
            {"input": {"board": _sudoku({(0, 0): "5", (8, 0): "5"})}, "output": False},
            {"input": {"board": _sudoku({(0, 0): "5", (1, 3): "5"})}, "output": True},
            {"input": {"board": _sudoku({})}, "output": True},
            {"input": {"board": _SUDOKU_FULL}, "output": True},
            {"input": {"board": _SUDOKU_PARTIAL}, "output": True},
            {"input": {"board": [row[:] for row in _SUDOKU_FULL[:4]] + [["."] * 9 for _ in range(5)]}, "output": True},
            {"input": {"board": [row[:] if r != 4 else _SUDOKU_FULL[1][:] for r, row in enumerate(_SUDOKU_FULL)]}, "output": False},
        ],
        "solution": '''\
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        for r in range(9):
            for c in range(9):
                d = board[r][c]
                if d == ".":
                    continue
                b = (r // 3) * 3 + c // 3
                if d in rows[r] or d in cols[c] or d in boxes[b]:
                    return False
                rows[r].add(d)
                cols[c].add(d)
                boxes[b].add(d)
        return True
''',
        "approach": (
            "**One pass with 27 'seen' sets.** Every filled cell belongs to exactly one row, one column and one 3 x 3 box. "
            "Keep a set of used digits for each of the 27 units; for each digit, reject if it is already in any of its three "
            "units, otherwise record it in all three.\n\n"
            "**The one formula to remember:** the box containing `(r, c)` is `(r // 3) * 3 + c // 3`, numbering boxes "
            "left to right, top to bottom.\n\n"
            "**Common mistakes:** computing the box index as `r // 3 + c // 3` (collides); checking for solvability, which "
            "is not asked; treating `'.'` as a value.\n\n"
            "**Interview follow-ups:** Can you reduce memory? (a 9-bit mask per unit instead of a set, or a single set of "
            "encoded strings such as `('r', r, d)`). How would you *solve* the board? (backtracking with the same three "
            "constraint structures). Generalise to an N^2 x N^2 board? (replace 3 with N and 9 with N^2)."
        ),
        "complexity": {"time": "O(1) (81 cells)", "space": "O(1) (27 small sets)"},
        "similar": ["sudoku-solver", "spiral-matrix"],
    },
    {
        "id": "spiral-matrix",
        "title": "Spiral Matrix",
        "difficulty": "Medium",
        "pattern": "Arrays & Hashing",
        "tags": ["Array", "Matrix", "Simulation"],
        "companies": {"google": 3, "apple": 3, "meta": 2, "amazon": 3, "microsoft": 4},
        "description": (
            "Given an `m x n` matrix of integers, return all of its elements in **spiral order**: start at the top-left "
            "corner, move right along the top row, then down the right column, then left along the bottom row, then up "
            "the left column, and keep spiralling inward until every element has been visited."
        ),
        "examples": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "output": "[1,2,3,6,9,8,7,4,5]"},
            {"input": "matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]", "output": "[1,2,3,4,8,12,11,10,9,5,6,7]"},
            {"input": "matrix = [[1],[2],[3]]", "output": "[1,2,3]"},
        ],
        "constraints": ["1 <= m, n <= 10", "-100 <= matrix[i][j] <= 100"],
        "hints": [
            "Track four boundaries: top, bottom, left, right. Each full lap peels one layer off the matrix.",
            "Walk top row left to right, right column top to bottom, bottom row right to left, left column bottom to top; shrink the matching boundary after each side.",
            "After the first two sides check that top <= bottom and left <= right before doing the other two, otherwise a single remaining row or column gets emitted twice.",
        ],
        "function": "spiralOrder",
        "signature": "def spiralOrder(self, matrix: List[List[int]]) -> List[int]:",
        "arg_types": {"matrix": "List[List[int]]"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}, "output": [1, 2, 3, 6, 9, 8, 7, 4, 5]},
            {"input": {"matrix": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]}, "output": [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]},
            {"input": {"matrix": [[1], [2], [3]]}, "output": [1, 2, 3]},
            {"input": {"matrix": [[1]]}, "output": [1]},
            {"input": {"matrix": [[1, 2, 3]]}, "output": [1, 2, 3]},
            {"input": {"matrix": [[1, 2], [3, 4]]}, "output": [1, 2, 4, 3]},
            {"input": {"matrix": [[-1, -2], [-3, -4], [-5, -6]]}, "output": [-1, -2, -4, -6, -5, -3]},
            {"input": {"matrix": [[1, 2, 3, 4], [5, 6, 7, 8]]}, "output": [1, 2, 3, 4, 8, 7, 6, 5]},
            {"input": {"matrix": [list(range(2500)), list(range(2500, 5000))]}, "output": list(range(2500)) + list(range(4999, 2499, -1))},
        ],
        "solution": '''\
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        result = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1
        while top <= bottom and left <= right:
            for c in range(left, right + 1):
                result.append(matrix[top][c])
            top += 1
            for r in range(top, bottom + 1):
                result.append(matrix[r][right])
            right -= 1
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    result.append(matrix[bottom][c])
                bottom -= 1
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    result.append(matrix[r][left])
                left += 1
        return result
''',
        "approach": (
            "**Peel layers with four shrinking boundaries.** Maintain `top`, `bottom`, `left`, `right`. Emit the top row and "
            "move `top` down; emit the right column and move `right` in; then, *only if rows remain*, emit the bottom row "
            "backwards and move `bottom` up; *only if columns remain*, emit the left column upwards and move `left` in. "
            "Repeat while the rectangle is non-empty.\n\n"
            "**Why the two guards matter:** when the remaining region is a single row (or single column), the first two "
            "sides already consume it; without the checks the third and fourth sides would re-emit those cells.\n\n"
            "**Common mistakes:** omitting the guards (duplicates on non-square inputs); off-by-one in the range endpoints "
            "(ranges are inclusive on both ends here); using a visited matrix and direction array, which works but costs "
            "O(mn) extra space.\n\n"
            "**Interview follow-ups:** Generate the spiral instead of reading it (Spiral Matrix II: same loop, write "
            "increasing numbers). Start from a given cell and spiral outward on an infinite grid (Spiral Matrix III). "
            "Rotate the matrix 90 degrees in place? (transpose then reverse rows)."
        ),
        "complexity": {"time": "O(m * n)", "space": "O(1) beyond the output"},
        "similar": ["rotate-image", "valid-sudoku", "set-matrix-zeroes"],
    },
]
