"""Sliding Window problems. See SCHEMA.md for the dict format."""

PROBLEMS = [
    {
        "id": "best-time-to-buy-and-sell-stock",
        "title": "Best Time to Buy and Sell Stock",
        "difficulty": "Easy",
        "pattern": "Sliding Window",
        "tags": ["Array", "Dynamic Programming", "Sliding Window"],
        "companies": {"google": 3, "apple": 3, "meta": 3, "amazon": 4, "microsoft": 3},
        "description": (
            "`prices[i]` is the price of a stock on day `i`. You may buy on one day and sell on a **later** day, at most "
            "once. Return the largest profit you can make, or `0` if no profitable trade exists."
        ),
        "examples": [
            {"input": "prices = [7,1,5,3,6,4]", "output": "5", "explanation": "Buy at 1 on day 1, sell at 6 on day 4. Buying at 1 and selling at 7 is not allowed because 7 comes earlier."},
            {"input": "prices = [7,6,4,3,1]", "output": "0", "explanation": "Prices only fall, so the best move is not to trade."},
        ],
        "constraints": ["1 <= prices.length <= 10^5", "0 <= prices[i] <= 10^4"],
        "hints": [
            "Trying every (buy, sell) pair is O(n^2). What single piece of information about the past do you need on each day?",
            "On each day the best sale is today's price minus the lowest price seen before today.",
            "Keep a running minimum and a running best profit; one pass does it.",
        ],
        "function": "maxProfit",
        "signature": "def maxProfit(self, prices: List[int]) -> int:",
        "arg_types": {"prices": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"prices": [7, 1, 5, 3, 6, 4]}, "output": 5},
            {"input": {"prices": [7, 6, 4, 3, 1]}, "output": 0},
            {"input": {"prices": [1]}, "output": 0},
            {"input": {"prices": [2, 4, 1]}, "output": 2},
            {"input": {"prices": [3, 3, 3]}, "output": 0},
            {"input": {"prices": [1, 2]}, "output": 1},
            {"input": {"prices": [2, 1, 2, 1, 0, 1, 2]}, "output": 2},
            {"input": {"prices": list(range(5000))}, "output": 4999},
            {"input": {"prices": list(range(5000, 0, -1)) + [2]}, "output": 1},
        ],
        "solution": '''\
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        lowest = prices[0]
        best = 0
        for price in prices[1:]:
            best = max(best, price - lowest)
            lowest = min(lowest, price)
        return best
''',
        "approach": (
            "**Running minimum.** Walk the days in order. The best profit if you sell today is `today - min(prices so far)`. "
            "Keep that running minimum and the best difference seen; the answer is the best difference (never negative, "
            "because we start `best` at 0).\n\n"
            "**Why it works:** every valid trade sells on some day `j` and buys on some day `i < j`; for a fixed `j` the "
            "optimal `i` is the one with the minimum price before `j`, which is exactly what we track. This is also the "
            "sliding-window view: the window's left edge jumps to any new minimum.\n\n"
            "**Common mistakes:** updating the minimum before computing today's profit (allows buy and sell on the same day, "
            "harmless here since that yields 0, but conceptually wrong); returning a negative value when prices only fall; "
            "a brute-force double loop that times out on 10^5 days.\n\n"
            "**Interview follow-ups:** Unlimited transactions (sum every positive day-to-day rise). At most two transactions, "
            "or at most k (DP over states). With a cooldown or a transaction fee (state machine DP). "
            "Relation to Maximum Subarray (profit is the max-sum subarray of daily differences, Kadane's algorithm)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["maximum-subarray", "best-time-to-buy-and-sell-stock-ii"],
    },
    {
        "id": "longest-substring-without-repeating-characters",
        "title": "Longest Substring Without Repeating Characters",
        "difficulty": "Medium",
        "pattern": "Sliding Window",
        "tags": ["Hash Table", "String", "Sliding Window"],
        "companies": {"google": 3, "apple": 3, "meta": 3, "amazon": 5, "microsoft": 4},
        "description": (
            "Given a string `s`, return the length of the longest **contiguous** substring in which no character appears "
            "more than once."
        ),
        "examples": [
            {"input": "s = \"abcabcbb\"", "output": "3", "explanation": "`abc` is the longest such substring."},
            {"input": "s = \"bbbbb\"", "output": "1"},
            {"input": "s = \"pwwkew\"", "output": "3", "explanation": "`wke` works; `pwke` is a subsequence, not a substring."},
        ],
        "constraints": ["0 <= s.length <= 5 * 10^4", "s consists of ASCII characters (letters, digits, symbols, spaces)."],
        "hints": [
            "Expand a window to the right one character at a time. When does the window become invalid?",
            "Keep the set of characters in the window. When the new character is already in it, shrink from the left until it is gone.",
            "Faster: store each character's last index. If the repeat is inside the current window, jump the left edge to just past that index instead of shrinking one step at a time.",
        ],
        "function": "lengthOfLongestSubstring",
        "signature": "def lengthOfLongestSubstring(self, s: str) -> int:",
        "arg_types": {"s": "str"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"s": "abcabcbb"}, "output": 3},
            {"input": {"s": "bbbbb"}, "output": 1},
            {"input": {"s": "pwwkew"}, "output": 3},
            {"input": {"s": ""}, "output": 0},
            {"input": {"s": "a"}, "output": 1},
            {"input": {"s": "abba"}, "output": 2},
            {"input": {"s": "dvdf"}, "output": 3},
            {"input": {"s": "tmmzuxt"}, "output": 5},
            {"input": {"s": " "}, "output": 1},
            {"input": {"s": "".join(chr(97 + i % 26) for i in range(10000))}, "output": 26},
            {"input": {"s": "abcdefghij" * 1000}, "output": 10},
        ],
        "solution": '''\
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen = {}
        left = 0
        best = 0
        for right, ch in enumerate(s):
            if ch in last_seen and last_seen[ch] >= left:
                left = last_seen[ch] + 1
            last_seen[ch] = right
            best = max(best, right - left + 1)
        return best
''',
        "approach": (
            "**Sliding window with last-seen indices.** Maintain a window `[left, right]` that contains no repeats. When "
            "the character at `right` was last seen at an index inside the window, move `left` to one past that index; "
            "otherwise the window simply grows. Record the character's new position and update the best length.\n\n"
            "**Why it works:** the window is always the longest duplicate-free substring ending at `right`, because `left` "
            "is placed just after the nearest earlier occurrence of any character in the window. Every substring is "
            "considered implicitly through its right endpoint.\n\n"
            "**Common mistakes:** setting `left = last_seen[ch] + 1` without checking `last_seen[ch] >= left` (then `left` "
            "can move backwards on input like `abba`, which is exactly what the `abba -> 2` test catches); using a set and "
            "shrinking one step at a time is correct but you should know the jump version; treating the problem as "
            "'distinct characters' rather than 'contiguous substring'.\n\n"
            "**Interview follow-ups:** Return the substring itself (remember the best `left`). Longest substring with at most "
            "k distinct characters (count map, shrink while `len(map) > k`). Longest substring with at most k repeats "
            "allowed per character."
        ),
        "complexity": {"time": "O(n)", "space": "O(min(n, alphabet))"},
        "similar": ["longest-repeating-character-replacement", "minimum-window-substring", "permutation-in-string"],
    },
    {
        "id": "longest-repeating-character-replacement",
        "title": "Longest Repeating Character Replacement",
        "difficulty": "Medium",
        "pattern": "Sliding Window",
        "tags": ["Hash Table", "String", "Sliding Window"],
        "companies": {"google": 2, "meta": 1, "amazon": 2, "microsoft": 1},
        "description": (
            "You have a string `s` of uppercase English letters and an integer `k`. You may change at most `k` characters "
            "to any other uppercase letter.\n\n"
            "Return the length of the longest substring that can be made to consist of a single repeated letter after "
            "those changes."
        ),
        "examples": [
            {"input": "s = \"ABAB\", k = 2", "output": "4", "explanation": "Change both Bs to A (or both As to B)."},
            {"input": "s = \"AABABBA\", k = 1", "output": "4", "explanation": "Change the middle B of `AABA` to get `AAAA`; `ABBB` works equally well."},
        ],
        "constraints": ["1 <= s.length <= 10^5", "s consists of uppercase English letters.", "0 <= k <= s.length"],
        "hints": [
            "A window is achievable when (window length) - (count of its most frequent letter) <= k: those are the characters you must change.",
            "Grow the window to the right, maintaining letter counts. When the window becomes invalid, move the left edge right by one.",
            "You do not need to recompute the max frequency when shrinking: the window never has to shrink below the best valid size, so a stale max only delays growth, never produces a wrong answer.",
        ],
        "function": "characterReplacement",
        "signature": "def characterReplacement(self, s: str, k: int) -> int:",
        "arg_types": {"s": "str", "k": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"s": "ABAB", "k": 2}, "output": 4},
            {"input": {"s": "AABABBA", "k": 1}, "output": 4},
            {"input": {"s": "A", "k": 0}, "output": 1},
            {"input": {"s": "AAAA", "k": 0}, "output": 4},
            {"input": {"s": "ABCDE", "k": 1}, "output": 2},
            {"input": {"s": "ABCDE", "k": 0}, "output": 1},
            {"input": {"s": "ABBB", "k": 2}, "output": 4},
            {"input": {"s": "AABBBCC", "k": 2}, "output": 5},
            {"input": {"s": "AB" * 5000, "k": 100}, "output": 201},
            {"input": {"s": "A" * 5000 + "B" * 5000, "k": 0}, "output": 5000},
        ],
        "solution": '''\
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        counts = defaultdict(int)
        left = 0
        max_freq = 0  # highest count of any letter seen in any window so far
        best = 0
        for right, ch in enumerate(s):
            counts[ch] += 1
            max_freq = max(max_freq, counts[ch])
            # Window is invalid when the characters to replace exceed k.
            if (right - left + 1) - max_freq > k:
                counts[s[left]] -= 1
                left += 1
            best = max(best, right - left + 1)
        return best
''',
        "approach": (
            "**Window validity = length minus majority count <= k.** Expand the window with `right`, keeping letter counts. "
            "The letters that need changing are all those that are not the most frequent one, so the window is valid when "
            "`length - max_freq <= k`. If it is not, slide `left` forward by one.\n\n"
            "**The subtle part:** `max_freq` is a historical maximum and is never decreased when a letter leaves the window. "
            "That is safe because we only care about the *longest* valid window: a window of size `best` was valid at some "
            "point, and a stale (too large) `max_freq` can only make us keep the window at its current size, never report a "
            "size we have not actually achieved. The window therefore never shrinks, it only slides.\n\n"
            "**Common mistakes:** recomputing the max count over 26 letters every step (O(26n), fine, but be able to explain "
            "why it is unnecessary); using `while` to shrink and then wondering why the result is the same; using the "
            "count of the *current* character rather than the maximum over all letters.\n\n"
            "**Interview follow-ups:** Prove that never shrinking is correct (the argument above). Return the substring and "
            "the letter chosen. Variant: longest run of 1s after flipping at most k zeros (Max Consecutive Ones III, same "
            "pattern with a binary alphabet)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1) (26 letters)"},
        "similar": ["max-consecutive-ones-iii", "longest-substring-without-repeating-characters"],
    },
    {
        "id": "permutation-in-string",
        "title": "Permutation in String",
        "difficulty": "Medium",
        "pattern": "Sliding Window",
        "tags": ["Hash Table", "String", "Sliding Window", "Two Pointers"],
        "companies": {"google": 2, "meta": 2, "amazon": 2, "microsoft": 3},
        "description": (
            "Given two lowercase strings `s1` and `s2`, return `true` if `s2` contains some permutation of `s1` as a "
            "**contiguous substring**, otherwise `false`.\n\n"
            "Equivalently: is there a window of `s2` of length `len(s1)` with exactly the same letter counts as `s1`?"
        ),
        "examples": [
            {"input": "s1 = \"ab\", s2 = \"eidbaooo\"", "output": "true", "explanation": "`ba` is a permutation of `ab`."},
            {"input": "s1 = \"ab\", s2 = \"eidboaoo\"", "output": "false", "explanation": "`a` and `b` never sit next to each other."},
        ],
        "constraints": ["1 <= s1.length, s2.length <= 10^4", "s1 and s2 consist of lowercase English letters."],
        "hints": [
            "Every candidate window has the same length as s1, so this is a fixed-size sliding window.",
            "Compare letter counts of the window with those of s1. Slide by adding the entering character and removing the leaving one.",
            "Comparing two 26-slot arrays each step is O(26n). Track how many of the 26 counts currently match to make each step O(1).",
        ],
        "function": "checkInclusion",
        "signature": "def checkInclusion(self, s1: str, s2: str) -> bool:",
        "arg_types": {"s1": "str", "s2": "str"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"s1": "ab", "s2": "eidbaooo"}, "output": True},
            {"input": {"s1": "ab", "s2": "eidboaoo"}, "output": False},
            {"input": {"s1": "a", "s2": "a"}, "output": True},
            {"input": {"s1": "abc", "s2": "ab"}, "output": False},
            {"input": {"s1": "adc", "s2": "dcda"}, "output": True},
            {"input": {"s1": "hello", "s2": "ooolleoooleh"}, "output": False},
            {"input": {"s1": "aab", "s2": "abab"}, "output": True},
            {"input": {"s1": "aab", "s2": "abba"}, "output": False},
            {"input": {"s1": "abc", "s2": "x" * 10000}, "output": False},
            {"input": {"s1": "ab" * 50, "s2": "a" * 5000 + "b" * 5000}, "output": True},
        ],
        "solution": '''\
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        n, m = len(s1), len(s2)
        if n > m:
            return False
        need = [0] * 26
        window = [0] * 26
        for i in range(n):
            need[ord(s1[i]) - 97] += 1
            window[ord(s2[i]) - 97] += 1
        matches = sum(1 for i in range(26) if need[i] == window[i])
        if matches == 26:
            return True
        for right in range(n, m):
            # character entering the window
            idx = ord(s2[right]) - 97
            window[idx] += 1
            if window[idx] == need[idx]:
                matches += 1
            elif window[idx] == need[idx] + 1:
                matches -= 1
            # character leaving the window
            idx = ord(s2[right - n]) - 97
            window[idx] -= 1
            if window[idx] == need[idx]:
                matches += 1
            elif window[idx] == need[idx] - 1:
                matches -= 1
            if matches == 26:
                return True
        return False
''',
        "approach": (
            "**Fixed-size window over letter counts.** Build the count array for `s1` and for the first `len(s1)` characters "
            "of `s2`. Then slide one position at a time: increment the entering letter, decrement the leaving letter. The "
            "window is a permutation of `s1` exactly when all 26 counts agree.\n\n"
            "**O(1) per step:** instead of comparing 26 values each time, maintain `matches`, the number of letters whose "
            "count agrees. Each increment or decrement changes exactly one letter's count by one, so it can change "
            "`matches` by at most one: it becomes a match when the counts become equal, and stops being one when it moves "
            "from equal to one off. Check `matches == 26`.\n\n"
            "**Common mistakes:** forgetting the `len(s1) > len(s2)` early exit; off-by-one in which character leaves "
            "(`s2[right - n]`, not `s2[right - n - 1]`); re-sorting each window (O(n * k log k)).\n\n"
            "**Interview follow-ups:** Return all starting indices instead of a boolean (Find All Anagrams in a String). "
            "Unicode alphabet (hash map plus a 'letters still mismatched' counter). Minimum window containing all "
            "characters of `s1`, order free, possibly with extras (Minimum Window Substring, a variable-size window)."
        ),
        "complexity": {"time": "O(len(s1) + len(s2))", "space": "O(1) (two 26-slot arrays)"},
        "similar": ["valid-anagram", "find-all-anagrams-in-a-string", "minimum-window-substring"],
    },
    {
        "id": "minimum-window-substring",
        "title": "Minimum Window Substring",
        "difficulty": "Hard",
        "pattern": "Sliding Window",
        "tags": ["Hash Table", "String", "Sliding Window"],
        "companies": {"google": 3, "apple": 2, "meta": 4, "amazon": 3, "microsoft": 3},
        "description": (
            "Given strings `s` and `t`, return the shortest substring of `s` that contains every character of `t` "
            "**with multiplicity** (if `t` has two `a`s, the window needs at least two `a`s). Return `\"\"` if no such "
            "window exists. The answer is guaranteed to be unique when it exists."
        ),
        "examples": [
            {"input": "s = \"ADOBECODEBANC\", t = \"ABC\"", "output": "\"BANC\"", "explanation": "`BANC` is the shortest stretch that has an A, a B and a C."},
            {"input": "s = \"a\", t = \"a\"", "output": "\"a\""},
            {"input": "s = \"a\", t = \"aa\"", "output": "\"\"", "explanation": "Two `a`s are required but `s` has only one."},
        ],
        "constraints": ["1 <= s.length, t.length <= 10^5", "s and t consist of uppercase and lowercase English letters."],
        "hints": [
            "Grow a window to the right until it covers all of t, then shrink from the left while it still covers t; record the best, then keep going.",
            "Keep a count map of what t needs and a counter `formed` of how many distinct characters currently meet their required count.",
            "The window is complete when `formed` equals the number of distinct characters in t. Only update `formed` when a count crosses the required threshold in either direction.",
        ],
        "function": "minWindow",
        "signature": "def minWindow(self, s: str, t: str) -> str:",
        "arg_types": {"s": "str", "t": "str"},
        "return_type": "str",
        "compare": "exact",
        "tests": [
            {"input": {"s": "ADOBECODEBANC", "t": "ABC"}, "output": "BANC"},
            {"input": {"s": "a", "t": "a"}, "output": "a"},
            {"input": {"s": "a", "t": "aa"}, "output": ""},
            {"input": {"s": "ab", "t": "b"}, "output": "b"},
            {"input": {"s": "aa", "t": "aa"}, "output": "aa"},
            {"input": {"s": "xyz", "t": "q"}, "output": ""},
            {"input": {"s": "abcabdebac", "t": "cda"}, "output": "cabd"},
            {"input": {"s": "aAbB", "t": "Ab"}, "output": "Ab"},
            {"input": {"s": "x" * 5000 + "abc" + "x" * 4997, "t": "abc"}, "output": "abc"},
            {"input": {"s": "a" * 10000, "t": "aaa"}, "output": "aaa"},
        ],
        "solution": '''\
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(t) > len(s):
            return ""
        need = Counter(t)
        required = len(need)       # distinct characters that must be satisfied
        window = defaultdict(int)
        formed = 0                 # distinct characters currently satisfied
        best_len = float("inf")
        best_start = 0
        left = 0
        for right, ch in enumerate(s):
            window[ch] += 1
            if ch in need and window[ch] == need[ch]:
                formed += 1
            while formed == required:
                if right - left + 1 < best_len:
                    best_len = right - left + 1
                    best_start = left
                out = s[left]
                window[out] -= 1
                if out in need and window[out] < need[out]:
                    formed -= 1
                left += 1
        return "" if best_len == float("inf") else s[best_start:best_start + best_len]
''',
        "approach": (
            "**Expand to satisfy, contract to minimise.** Keep a map of what `t` needs and a map of what the window holds. "
            "`formed` counts how many distinct characters of `t` are fully satisfied. Move `right` to the right until "
            "`formed == required`; then move `left` to the right as far as possible while the window stays complete, "
            "recording the shortest complete window seen. Continue until `right` reaches the end.\n\n"
            "**Why it works:** for every position of `left`, the first `right` that completes the window gives the "
            "minimal window starting at `left`; the inner `while` enumerates those `left` values in increasing order and "
            "never needs to move `left` back. Each index enters and leaves the window once, so the total work is linear.\n\n"
            "**Common mistakes:** incrementing `formed` every time a needed character arrives rather than only when its "
            "count *reaches* the requirement (overcounts duplicates); shrinking with `if` instead of `while`; building the "
            "substring at every step instead of storing `(start, length)`; forgetting the empty-result case.\n\n"
            "**Interview follow-ups:** Characters must appear in order as a subsequence (Minimum Window Subsequence, a "
            "different two-pointer scan). Return all minimum windows if uniqueness is not promised. Streaming `s` with "
            "limited memory (keep only the window and counts, which this already does)."
        ),
        "complexity": {"time": "O(|s| + |t|)", "space": "O(alphabet)"},
        "similar": ["permutation-in-string", "longest-substring-without-repeating-characters", "sliding-window-maximum"],
    },
    {
        "id": "sliding-window-maximum",
        "title": "Sliding Window Maximum",
        "difficulty": "Hard",
        "pattern": "Sliding Window",
        "tags": ["Array", "Queue", "Sliding Window", "Monotonic Queue", "Heap"],
        "companies": {"google": 3, "apple": 2, "meta": 2, "amazon": 4, "microsoft": 2},
        "description": (
            "Given an integer array `nums` and a window size `k`, slide a window of exactly `k` elements from the left end "
            "to the right end one step at a time. Return the maximum of each window position, as a list of "
            "`len(nums) - k + 1` values in order."
        ),
        "examples": [
            {"input": "nums = [1,3,-1,-3,5,3,6,7], k = 3", "output": "[3,3,5,5,6,7]", "explanation": "Windows: [1,3,-1] [3,-1,-3] [-1,-3,5] [-3,5,3] [5,3,6] [3,6,7]."},
            {"input": "nums = [1], k = 1", "output": "[1]"},
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4", "1 <= k <= nums.length"],
        "hints": [
            "Recomputing the max of each window is O(nk). A heap with lazy deletion gets O(n log n). Can you reach O(n)?",
            "Once a larger element enters the window, every smaller element to its left can never be a window maximum again. Discard them.",
            "Keep a deque of indices whose values are decreasing. Pop from the back while the new value is >= the back; pop from the front when the front index leaves the window. The front is always the current max.",
        ],
        "function": "maxSlidingWindow",
        "signature": "def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:",
        "arg_types": {"nums": "List[int]", "k": "int"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [1, 3, -1, -3, 5, 3, 6, 7], "k": 3}, "output": [3, 3, 5, 5, 6, 7]},
            {"input": {"nums": [1], "k": 1}, "output": [1]},
            {"input": {"nums": [1, -1], "k": 1}, "output": [1, -1]},
            {"input": {"nums": [9, 8, 7, 6], "k": 2}, "output": [9, 8, 7]},
            {"input": {"nums": [4, 4, 4], "k": 3}, "output": [4]},
            {"input": {"nums": [1, 2, 3, 4, 5], "k": 5}, "output": [5]},
            {"input": {"nums": [-7, -8, 7, 5, 7, 1, 6, 0], "k": 4}, "output": [7, 7, 7, 7, 7]},
            {"input": {"nums": list(range(10000, 0, -1)), "k": 5000}, "output": list(range(10000, 4999, -1))},
            {"input": {"nums": list(range(10000)), "k": 5000}, "output": list(range(4999, 10000))},
        ],
        "solution": '''\
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        dq = deque()  # indices; values are strictly decreasing from front to back
        result = []
        for i, x in enumerate(nums):
            while dq and nums[dq[-1]] <= x:
                dq.pop()
            dq.append(i)
            if dq[0] <= i - k:
                dq.popleft()  # front index has slid out of the window
            if i >= k - 1:
                result.append(nums[dq[0]])
        return result
''',
        "approach": (
            "**Monotonic deque of candidate indices.** Store indices whose values decrease from front to back. When a new "
            "element arrives, pop from the back every index whose value is `<=` the new one: those elements are both older "
            "and smaller, so they can never again be a window maximum. Push the new index. If the front index has fallen "
            "outside the window (`dq[0] <= i - k`), pop it. Once the first full window is reached, the front is the answer "
            "for every step.\n\n"
            "**Why it is O(n):** each index is pushed once and popped at most once, so all deque operations together are "
            "O(n) even though some steps pop many elements.\n\n"
            "**Common mistakes:** storing values instead of indices (then you cannot tell when the front expires); popping "
            "the front with `<` instead of `<=` on `i - k` (off by one keeps a stale max for one step); using `<` instead of "
            "`<=` when popping the back is also correct but keeps duplicate values around unnecessarily.\n\n"
            "**Interview follow-ups:** Sliding window minimum (flip the comparison) or both at once. Heap version and its "
            "lazy-deletion details (O(n log n)). Shortest subarray with sum at least K (monotonic deque over prefix sums, "
            "the same tool in a different setting)."
        ),
        "complexity": {"time": "O(n)", "space": "O(k)"},
        "similar": ["minimum-window-substring", "shortest-subarray-with-sum-at-least-k", "daily-temperatures"],
    },
    {
        "id": "max-consecutive-ones-iii",
        "title": "Max Consecutive Ones III",
        "difficulty": "Medium",
        "pattern": "Sliding Window",
        "tags": ["Array", "Binary Search", "Sliding Window", "Prefix Sum"],
        "companies": {"google": 2, "meta": 3, "amazon": 2, "microsoft": 1},
        "description": (
            "Given a binary array `nums` and an integer `k`, you may flip at most `k` zeros to ones. Return the length of "
            "the longest contiguous run of ones you can obtain."
        ),
        "examples": [
            {"input": "nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2", "output": "6", "explanation": "Flip the two zeros at indices 4 and 5 to get six consecutive ones (indices 4 through 9)."},
            {"input": "nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3", "output": "10", "explanation": "Indices 2 through 11 contain exactly three zeros."},
        ],
        "constraints": ["1 <= nums.length <= 10^5", "nums[i] is 0 or 1.", "0 <= k <= nums.length"],
        "hints": [
            "Rephrase: find the longest window that contains at most k zeros.",
            "Expand the window to the right, counting zeros. When the count exceeds k, move the left edge right until it does not.",
            "As in Longest Repeating Character Replacement, the window never needs to shrink below the best size, so a single `if` step for the left edge suffices.",
        ],
        "function": "longestOnes",
        "signature": "def longestOnes(self, nums: List[int], k: int) -> int:",
        "arg_types": {"nums": "List[int]", "k": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], "k": 2}, "output": 6},
            {"input": {"nums": [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], "k": 3}, "output": 10},
            {"input": {"nums": [0, 0, 0], "k": 0}, "output": 0},
            {"input": {"nums": [1, 1, 1], "k": 0}, "output": 3},
            {"input": {"nums": [0, 0, 0], "k": 3}, "output": 3},
            {"input": {"nums": [1, 0, 1], "k": 1}, "output": 3},
            {"input": {"nums": [0], "k": 0}, "output": 0},
            {"input": {"nums": [1, 0, 0, 1, 1, 0, 1], "k": 1}, "output": 4},
            {"input": {"nums": [1, 0] * 5000, "k": 100}, "output": 201},
            {"input": {"nums": [0] * 5000 + [1] * 5000, "k": 7}, "output": 5007},
        ],
        "solution": '''\
class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        left = 0
        zeros = 0
        best = 0
        for right, x in enumerate(nums):
            if x == 0:
                zeros += 1
            while zeros > k:
                if nums[left] == 0:
                    zeros -= 1
                left += 1
            best = max(best, right - left + 1)
        return best
''',
        "approach": (
            "**Longest window with at most k zeros.** Flipping up to `k` zeros inside a window makes it all ones, so the "
            "question is purely about zero counts. Expand `right`, counting zeros; while there are more than `k`, advance "
            "`left`, decrementing the count when a zero leaves. The window is always valid after the shrink step, so its "
            "length is a candidate answer.\n\n"
            "**Why it works:** for each `right`, the loop leaves `left` at the smallest index such that `nums[left..right]` "
            "has at most `k` zeros, so every maximal valid window is measured. `left` only moves right, giving O(n).\n\n"
            "**Common mistakes:** actually mutating the array to flip zeros (unnecessary and makes the shrink step wrong); "
            "forgetting that `k = 0` must still work (longest run of existing ones); mixing up the roles of the counters.\n\n"
            "**Interview follow-ups:** Delete exactly one element and maximise the run of ones (window with at most one "
            "zero, answer is length minus one). Return the indices to flip (the zeros in the best window). "
            "Generalise to 'at most k elements not equal to v' for any value v, which is the character replacement problem."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["longest-repeating-character-replacement", "fruit-into-baskets", "longest-subarray-of-1s-after-deleting-one-element"],
    },
    {
        "id": "fruit-into-baskets",
        "title": "Fruit Into Baskets",
        "difficulty": "Medium",
        "pattern": "Sliding Window",
        "tags": ["Array", "Hash Table", "Sliding Window"],
        "companies": {"google": 3, "meta": 1, "amazon": 2, "microsoft": 1},
        "description": (
            "`fruits[i]` is the type of fruit on tree `i` in a row of trees. You have two baskets and each basket can hold "
            "only one type of fruit (unlimited quantity). Starting at any tree you pick one fruit from every tree moving "
            "right, and you must stop as soon as you meet a type that fits in neither basket.\n\n"
            "Return the maximum number of fruits you can pick. In other words: the length of the longest contiguous "
            "subarray with at most **two distinct values**."
        ),
        "examples": [
            {"input": "fruits = [1,2,1]", "output": "3", "explanation": "All three trees fit into two baskets."},
            {"input": "fruits = [0,1,2,2]", "output": "3", "explanation": "Start at the second tree: types 1 and 2 give [1,2,2]."},
            {"input": "fruits = [1,2,3,2,2]", "output": "4", "explanation": "[2,3,2,2] uses types 2 and 3."},
        ],
        "constraints": ["1 <= fruits.length <= 10^5", "0 <= fruits[i] < fruits.length"],
        "hints": [
            "Translate the story: longest subarray containing at most two distinct values.",
            "Sliding window with a map type -> count. Expand right; while the map has more than two keys, shrink from the left and delete keys whose count drops to zero.",
            "Each index enters and leaves the window once, so the total is O(n) even with the inner while loop.",
        ],
        "function": "totalFruit",
        "signature": "def totalFruit(self, fruits: List[int]) -> int:",
        "arg_types": {"fruits": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"fruits": [1, 2, 1]}, "output": 3},
            {"input": {"fruits": [0, 1, 2, 2]}, "output": 3},
            {"input": {"fruits": [1, 2, 3, 2, 2]}, "output": 4},
            {"input": {"fruits": [3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4]}, "output": 5},
            {"input": {"fruits": [1]}, "output": 1},
            {"input": {"fruits": [1, 1, 1, 1]}, "output": 4},
            {"input": {"fruits": [1, 2]}, "output": 2},
            {"input": {"fruits": [1, 0, 1, 4, 1, 4, 1, 2, 3]}, "output": 5},
            {"input": {"fruits": list(range(5000))}, "output": 2},
            {"input": {"fruits": [i // 1000 for i in range(5000)]}, "output": 2000},
            {"input": {"fruits": [i % 3 for i in range(6000)]}, "output": 2},
        ],
        "solution": '''\
class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        counts = defaultdict(int)
        left = 0
        best = 0
        for right, kind in enumerate(fruits):
            counts[kind] += 1
            while len(counts) > 2:
                out = fruits[left]
                counts[out] -= 1
                if counts[out] == 0:
                    del counts[out]
                left += 1
            best = max(best, right - left + 1)
        return best
''',
        "approach": (
            "**Longest subarray with at most two distinct values.** Maintain a window and a map from fruit type to its "
            "count inside the window. Extend `right` one tree at a time; whenever a third type appears, advance `left`, "
            "decrementing counts and removing a type when its count hits zero, until only two types remain. Track the "
            "longest window.\n\n"
            "**Why it works:** the map's key count equals the number of distinct types in the window, so the shrink loop "
            "restores validity exactly. For each `right` the window is the longest valid one ending there, and `left` is "
            "monotone, so the total work is linear.\n\n"
            "**Common mistakes:** not deleting zero-count keys (then `len(counts)` overstates the distinct types and the "
            "window shrinks too much); hard-coding two variables for the basket types and getting tangled in the swap "
            "logic; misreading the story and allowing non-contiguous picking.\n\n"
            "**Interview follow-ups:** Generalise to k baskets (replace 2 with k, same code). Count the number of subarrays "
            "with at most k distinct values (add `right - left + 1` per step) and exactly k (atMost(k) - atMost(k-1)). "
            "Return the two types chosen for the best window."
        ),
        "complexity": {"time": "O(n)", "space": "O(1) (at most three keys)"},
        "similar": ["longest-substring-without-repeating-characters", "max-consecutive-ones-iii", "subarrays-with-k-different-integers"],
    },
]
