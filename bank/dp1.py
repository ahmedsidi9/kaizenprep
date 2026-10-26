"""1-D Dynamic Programming: linear recurrences, rolling variables, and the classic string/array DPs."""


def _fib(k):
    """F(k) with F(0)=0, F(1)=1; used for expected values of exponentially large counts."""
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


PROBLEMS = [
    {
        "id": "climbing-stairs",
        "title": "Climbing Stairs",
        "difficulty": "Easy",
        "pattern": "1-D Dynamic Programming",
        "tags": ["Dynamic Programming", "Math", "Memoization"],
        "companies": {"google": 3, "apple": 3, "meta": 2, "amazon": 4, "microsoft": 3},
        "description": (
            "A staircase has `n` steps. From any position you can climb either **1** or **2** steps at a time.\n\n"
            "Return the number of distinct ways to reach the top."
        ),
        "examples": [
            {"input": "n = 2", "output": "2", "explanation": "1+1 or 2."},
            {"input": "n = 3", "output": "3", "explanation": "1+1+1, 1+2, 2+1."},
            {"input": "n = 5", "output": "8"},
        ],
        "constraints": ["1 <= n <= 45"],
        "hints": [
            "The last move onto step n came from step n-1 or step n-2.",
            "So ways(n) = ways(n-1) + ways(n-2): the Fibonacci recurrence with ways(1) = 1, ways(2) = 2.",
            "Two rolling variables are enough; no array needed.",
        ],
        "function": "climbStairs",
        "signature": "def climbStairs(self, n: int) -> int:",
        "arg_types": {"n": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"n": 2}, "output": 2},
            {"input": {"n": 3}, "output": 3},
            {"input": {"n": 5}, "output": 8},
            {"input": {"n": 1}, "output": 1},
            {"input": {"n": 10}, "output": 89},
            {"input": {"n": 45}, "output": 1836311903},
        ],
        "solution": (
            "class Solution:\n"
            "    def climbStairs(self, n: int) -> int:\n"
            "        prev, cur = 1, 1  # ways to reach step 0 and step 1\n"
            "        for _ in range(n - 1):\n"
            "            prev, cur = cur, prev + cur\n"
            "        return cur\n"
        ),
        "approach": (
            "**The number of ways to stand on step `i` is the sum of the ways to stand on the two steps you could "
            "have come from.** `ways(i) = ways(i-1) + ways(i-2)`, with `ways(0) = ways(1) = 1`. That is the Fibonacci "
            "sequence shifted by one.\n\n"
            "Naive recursion recomputes the same subproblems and is O(2^n); n = 45 already takes minutes. "
            "Memoising or iterating bottom-up makes it O(n). Since each state only depends on the previous two, "
            "**two rolling variables** give O(1) space, which is the version to present.\n\n"
            "**Common mistakes:** off-by-one at the base cases (ways(2) must be 2), and starting the loop at the wrong "
            "index so that n = 1 returns 2.\n\n"
            "**Interview follow-ups:** Allow steps of size 1..k? (Sum the previous k values with a sliding window "
            "sum.) Enumerate the actual sequences rather than count them? (Backtracking; the output itself is "
            "exponential.) Compute in O(log n)? (Fast matrix exponentiation of [[1,1],[1,0]].) Forbidden steps? "
            "(Set ways(i) = 0 for broken steps.)"
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["min-cost-climbing-stairs", "decode-ways", "house-robber"],
    },
    {
        "id": "min-cost-climbing-stairs",
        "title": "Min Cost Climbing Stairs",
        "difficulty": "Easy",
        "pattern": "1-D Dynamic Programming",
        "tags": ["Dynamic Programming", "Array"],
        "companies": {"google": 2, "apple": 1, "amazon": 3, "microsoft": 1},
        "description": (
            "`cost[i]` is the price of stepping on stair `i`. Once you pay for a stair you may climb 1 or 2 stairs "
            "onward. You may begin on stair `0` or stair `1`, and the goal is to get past the last stair (to position `len(cost)`).\n\n"
            "Return the minimum total cost."
        ),
        "examples": [
            {"input": "cost = [10,15,20]", "output": "15", "explanation": "Start on stair 1 (pay 15) and jump two steps to the top."},
            {"input": "cost = [1,100,1,1,1,100,1,1,100,1]", "output": "6",
             "explanation": "Start on stair 0 and take every stair that costs 1, skipping each 100: 1+1+1+1+1+1 = 6."},
        ],
        "constraints": ["2 <= cost.length <= 1000", "0 <= cost[i] <= 999"],
        "hints": [
            "Let f(i) be the cheapest way to reach position i (standing just past stair i-1, not yet paid for stair i).",
            "f(i) = min(f(i-1) + cost[i-1], f(i-2) + cost[i-2]); f(0) = f(1) = 0 because you may start on either of the first two stairs for free.",
            "Only the last two values are needed, so roll two variables.",
        ],
        "function": "minCostClimbingStairs",
        "signature": "def minCostClimbingStairs(self, cost: List[int]) -> int:",
        "arg_types": {"cost": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"cost": [10, 15, 20]}, "output": 15},
            {"input": {"cost": [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]}, "output": 6},
            {"input": {"cost": [5, 3]}, "output": 3},
            {"input": {"cost": [0, 0, 0, 1]}, "output": 0},
            {"input": {"cost": [1, 2, 3, 4, 5]}, "output": 6},
            {"input": {"cost": [(i * 37) % 101 for i in range(5000)]}, "output": 99824},
        ],
        "solution": (
            "class Solution:\n"
            "    def minCostClimbingStairs(self, cost: List[int]) -> int:\n"
            "        two_back, one_back = 0, 0  # cheapest cost to reach positions i-2 and i-1\n"
            "        for c in cost:\n"
            "            two_back, one_back = one_back, c + min(one_back, two_back)\n"
            "        return min(one_back, two_back)\n"
        ),
        "approach": (
            "**Define `f(i)` as the minimum cost to be standing on stair `i` (having paid for it).** You arrived from "
            "`i-1` or `i-2`, so `f(i) = cost[i] + min(f(i-1), f(i-2))`, with `f(0) = cost[0]` and `f(1) = cost[1]`. The "
            "top lies past the last stair, reachable from either of the last two, so the answer is `min(f(n-1), f(n-2))`.\n\n"
            "The loop above folds the base cases in by starting both rolling values at 0 (standing before the "
            "staircase costs nothing) and treating `cost[i]` as paid on arrival.\n\n"
            "**Why it works:** every path to the top ends on stair n-1 or n-2, and the cheapest way to each stair "
            "depends only on the cheapest way to the two stairs below it (optimal substructure), so the greedy local "
            "min is globally optimal.\n\n"
            "**Common mistakes:** forgetting that the goal is *past* the last stair (returning f(n-1) alone), or "
            "forcing a start at stair 0.\n\n"
            "**Interview follow-ups:** Reconstruct the stairs stepped on? (Keep a `choice[i]` flag recording which "
            "predecessor won, then walk back from the cheaper of the last two.) Allow steps up to k? (Sliding-window "
            "minimum with a monotonic deque gives O(n).) What if some stairs are closed? (Set their cost to infinity.)"
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["climbing-stairs", "house-robber"],
    },
    {
        "id": "house-robber",
        "title": "House Robber",
        "difficulty": "Medium",
        "pattern": "1-D Dynamic Programming",
        "tags": ["Dynamic Programming", "Array"],
        "companies": {"google": 3, "apple": 2, "meta": 2, "amazon": 4, "microsoft": 3},
        "description": (
            "`nums[i]` is the amount of cash in house `i` on a street. You may rob any subset of houses, but robbing "
            "two **adjacent** houses triggers an alarm.\n\n"
            "Return the largest total you can take without ever robbing two neighbours."
        ),
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "4", "explanation": "Houses 0 and 2: 1 + 3 = 4."},
            {"input": "nums = [2,7,9,3,1]", "output": "12", "explanation": "Houses 0, 2 and 4: 2 + 9 + 1 = 12."},
        ],
        "constraints": ["1 <= nums.length <= 100", "0 <= nums[i] <= 400"],
        "hints": [
            "For each house you either rob it (and must have skipped the previous one) or skip it.",
            "best(i) = max(best(i-1), best(i-2) + nums[i]).",
            "Keep only the last two values: `prev, cur = cur, max(cur, prev + x)`.",
        ],
        "function": "rob",
        "signature": "def rob(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [1, 2, 3, 1]}, "output": 4},
            {"input": {"nums": [2, 7, 9, 3, 1]}, "output": 12},
            {"input": {"nums": [5]}, "output": 5},
            {"input": {"nums": [2, 1]}, "output": 2},
            {"input": {"nums": [0, 0]}, "output": 0},
            {"input": {"nums": [4, 1, 2, 7, 5, 3, 1]}, "output": 14},
            {"input": {"nums": [1] * 5000}, "output": 2500},
            {"input": {"nums": [(i * 31) % 97 for i in range(5000)]}, "output": 136167},
        ],
        "solution": (
            "class Solution:\n"
            "    def rob(self, nums: List[int]) -> int:\n"
            "        skip, take = 0, 0  # best totals through the previous house: not robbed / robbed\n"
            "        for x in nums:\n"
            "            skip, take = max(skip, take), skip + x\n"
            "        return max(skip, take)\n"
        ),
        "approach": (
            "**At each house the only decision is rob or skip, and the best outcome through house `i` depends only on "
            "the best outcomes through `i-1` and `i-2`.** Let `best(i)` be the maximum loot using houses `0..i`. "
            "Then `best(i) = max(best(i-1), best(i-2) + nums[i])`: either skip house i (keep best(i-1)) or rob it, "
            "which forces house i-1 to be skipped so we add to best(i-2).\n\n"
            "The code keeps two numbers: `take`, the best total if the previous house was robbed, and `skip`, the "
            "best if it was not. Robbing the current house is only allowed on top of `skip`.\n\n"
            "**Why it works:** any legal plan restricted to the first i houses is still legal, so an optimal plan "
            "for 0..i is built from an optimal plan for a shorter prefix; there are no other interactions beyond adjacency.\n\n"
            "**Common mistakes:** assuming you must alternate houses (greedy on odd/even indices fails on [2,1,1,2]), "
            "and the O(n) array when O(1) space is expected.\n\n"
            "**Interview follow-ups:** Reconstruct which houses were robbed? (Store `best[]` as an array and walk "
            "backwards: if best[i] != best[i-1] then house i was taken and jump to i-2.) Houses in a circle? "
            "(House Robber II: run twice excluding the first or the last.) Houses arranged as a tree? (House Robber "
            "III: post-order DFS returning (rob, skip) per node.)"
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["house-robber-ii", "min-cost-climbing-stairs", "delete-and-earn"],
    },
    {
        "id": "house-robber-ii",
        "title": "House Robber II",
        "difficulty": "Medium",
        "pattern": "1-D Dynamic Programming",
        "tags": ["Dynamic Programming", "Array"],
        "companies": {"google": 2, "apple": 1, "amazon": 3, "microsoft": 2},
        "description": (
            "Same rules as House Robber, except the houses now form a **circle**: the first and last houses are "
            "neighbours, so they cannot both be robbed.\n\n"
            "Given `nums`, return the maximum amount you can take."
        ),
        "examples": [
            {"input": "nums = [2,3,2]", "output": "3", "explanation": "Houses 0 and 2 are adjacent on the circle, so the best is house 1 alone."},
            {"input": "nums = [1,2,3,1]", "output": "4", "explanation": "Houses 0 and 2 give 4."},
            {"input": "nums = [1,2,3]", "output": "3"},
        ],
        "constraints": ["1 <= nums.length <= 100", "0 <= nums[i] <= 1000"],
        "hints": [
            "The only new constraint couples the first and last houses. In any plan at least one of them is skipped.",
            "Run the linear House Robber twice: once on nums[1:], once on nums[:-1], and take the larger. Watch the single-house case.",
        ],
        "function": "rob",
        "signature": "def rob(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [2, 3, 2]}, "output": 3},
            {"input": {"nums": [1, 2, 3, 1]}, "output": 4},
            {"input": {"nums": [1, 2, 3]}, "output": 3},
            {"input": {"nums": [5]}, "output": 5},
            {"input": {"nums": [1, 2]}, "output": 2},
            {"input": {"nums": [200, 3, 140, 20, 10]}, "output": 340},
            {"input": {"nums": [1] * 5000}, "output": 2500},
            {"input": {"nums": [1] * 4999}, "output": 2499},
            {"input": {"nums": [(i * 31) % 97 for i in range(5000)]}, "output": 136167},
        ],
        "solution": (
            "class Solution:\n"
            "    def rob(self, nums: List[int]) -> int:\n"
            "        if len(nums) == 1:\n"
            "            return nums[0]\n\n"
            "        def linear(houses):\n"
            "            skip, take = 0, 0\n"
            "            for x in houses:\n"
            "                skip, take = max(skip, take), skip + x\n"
            "            return max(skip, take)\n\n"
            "        return max(linear(nums[1:]), linear(nums[:-1]))\n"
        ),
        "approach": (
            "**Break the circle by cases: the first house is skipped, or the last house is skipped (at least one "
            "must be).** Each case is an ordinary linear street, so the answer is "
            "`max(rob(nums[1:]), rob(nums[:-1]))` using the House Robber recurrence "
            "`best(i) = max(best(i-1), best(i-2) + nums[i])` with two rolling variables.\n\n"
            "**Why it works:** the two subproblems cover every legal circular plan (a plan robbing both ends is "
            "illegal; any other plan omits an end and is legal in the corresponding linear street), and every "
            "linear plan is legal on the circle because the dangerous pair is never both present.\n\n"
            "**Common mistakes:** the n = 1 case, where both slices are empty and the code would return 0 instead "
            "of nums[0]; forgetting that for n = 2 the answer is simply the max.\n\n"
            "**Interview follow-ups:** Reconstruct the chosen houses? (Keep the DP arrays for both runs and "
            "backtrack in the winning one; shift indices by one for the nums[1:] run.) Could you do it in one "
            "pass? (Carry two pairs of rolling variables simultaneously, one per case.) What if no two houses "
            "within distance k may be robbed? (Sliding-window max over best(i-k-1 .. ) with a deque.)"
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["house-robber", "house-robber-iii"],
    },
    {
        "id": "longest-palindromic-substring",
        "title": "Longest Palindromic Substring",
        "difficulty": "Medium",
        "pattern": "1-D Dynamic Programming",
        "tags": ["String", "Dynamic Programming", "Two Pointers"],
        "companies": {"google": 3, "apple": 3, "meta": 3, "amazon": 5, "microsoft": 4},
        "description": (
            "Given a string `s`, return the longest contiguous substring that reads the same forwards and backwards.\n\n"
            "If several palindromic substrings share the maximum length, any one of them is accepted."
        ),
        "examples": [
            {"input": "s = \"babad\"", "output": "\"bab\"", "explanation": "\"aba\" is equally valid."},
            {"input": "s = \"cbbd\"", "output": "\"bb\""},
            {"input": "s = \"a\"", "output": "\"a\""},
        ],
        "constraints": ["1 <= s.length <= 1000", "s consists of digits and English letters."],
        "hints": [
            "Checking every substring is O(n^3). Think about where a palindrome is centred instead.",
            "There are 2n - 1 centres (each character, and each gap between characters). Expand outwards from each centre while the ends match.",
            "Track the best (start, length). The DP table dp[i][j] = s[i] == s[j] and dp[i+1][j-1] is an alternative O(n^2) time, O(n^2) space approach.",
        ],
        "function": "longestPalindrome",
        "signature": "def longestPalindrome(self, s: str) -> str:",
        "arg_types": {"s": "str"},
        "return_type": "str",
        "compare": "any_of",
        "tests": [
            {"input": {"s": "babad"}, "output": ["bab", "aba"]},
            {"input": {"s": "cbbd"}, "output": ["bb"]},
            {"input": {"s": "a"}, "output": ["a"]},
            {"input": {"s": "ac"}, "output": ["a", "c"]},
            {"input": {"s": "forgeeksskeegfor"}, "output": ["geeksskeeg"]},
            {"input": {"s": "abacdfgdcaba"}, "output": ["aba"]},
            {"input": {"s": "aaaa"}, "output": ["aaaa"]},
            {"input": {"s": "abc" * 800 + "racecar" + "abc" * 800}, "output": ["racecar"]},
        ],
        "solution": (
            "class Solution:\n"
            "    def longestPalindrome(self, s: str) -> str:\n"
            "        best_start, best_len = 0, 0\n"
            "        n = len(s)\n"
            "        for centre in range(n):\n"
            "            for lo, hi in ((centre, centre), (centre, centre + 1)):  # odd and even length\n"
            "                while lo >= 0 and hi < n and s[lo] == s[hi]:\n"
            "                    lo -= 1\n"
            "                    hi += 1\n"
            "                length = hi - lo - 1\n"
            "                if length > best_len:\n"
            "                    best_start, best_len = lo + 1, length\n"
            "        return s[best_start:best_start + best_len]\n"
        ),
        "approach": (
            "**Every palindrome has a centre, and there are only `2n - 1` of them.** For each index treat it as the "
            "middle of an odd palindrome and the gap after it as the middle of an even one, then expand two "
            "pointers outward while `s[lo] == s[hi]`. The widest expansion over all centres is the answer.\n\n"
            "**Why it works:** a palindrome of length L centred at c contains the palindromes of length L-2, L-4, ... "
            "at the same centre, so the expansion never needs to skip; stopping at the first mismatch is exact. "
            "Worst case (all one character) is O(n^2), typical inputs are much faster.\n\n"
            "**The DP view** the interviewer may want you to name: `pal[i][j]` is true when `s[i] == s[j]` and "
            "`pal[i+1][j-1]` is true, filled by increasing length. It is also O(n^2) time but uses O(n^2) memory, "
            "so centre expansion is the better presentation. Manacher's algorithm reaches O(n) and is a reasonable "
            "thing to mention without being asked to code.\n\n"
            "**Common mistakes:** forgetting the even-length centres (fails on \"cbbd\"), off-by-one when converting "
            "the final (lo, hi) back to a slice (`lo + 1` to `hi - 1` inclusive), and the brute force O(n^3) check.\n\n"
            "**Interview follow-ups:** Count all palindromic substrings instead (same loop, count each successful "
            "expansion). Longest palindromic *subsequence* (2-D DP on s and reversed s). Can you do O(n)? (Manacher.)"
        ),
        "complexity": {"time": "O(n^2) worst case", "space": "O(1)"},
        "similar": ["palindromic-substrings", "longest-palindromic-subsequence", "valid-palindrome"],
    },
    {
        "id": "palindromic-substrings",
        "title": "Palindromic Substrings",
        "difficulty": "Medium",
        "pattern": "1-D Dynamic Programming",
        "tags": ["String", "Dynamic Programming", "Two Pointers"],
        "companies": {"google": 2, "meta": 3, "amazon": 2, "microsoft": 2},
        "description": (
            "Given a string `s`, count how many of its substrings are palindromes. Substrings at different "
            "positions count separately even if their text is identical."
        ),
        "examples": [
            {"input": "s = \"abc\"", "output": "3", "explanation": "Only the three single characters."},
            {"input": "s = \"aaa\"", "output": "6", "explanation": "\"a\" three times, \"aa\" twice, \"aaa\" once."},
        ],
        "constraints": ["1 <= s.length <= 1000", "s consists of lowercase English letters."],
        "hints": [
            "Each palindrome has a unique centre: a character (odd length) or a gap between two characters (even length).",
            "Expand from every centre while the two ends match; each successful step is one more palindrome.",
        ],
        "function": "countSubstrings",
        "signature": "def countSubstrings(self, s: str) -> int:",
        "arg_types": {"s": "str"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"s": "abc"}, "output": 3},
            {"input": {"s": "aaa"}, "output": 6},
            {"input": {"s": "a"}, "output": 1},
            {"input": {"s": "abba"}, "output": 6},
            {"input": {"s": "a" * 300}, "output": 45150},
            {"input": {"s": "abc" * 1666}, "output": 4998},
        ],
        "solution": (
            "class Solution:\n"
            "    def countSubstrings(self, s: str) -> int:\n"
            "        n = len(s)\n"
            "        count = 0\n"
            "        for centre in range(n):\n"
            "            for lo, hi in ((centre, centre), (centre, centre + 1)):\n"
            "                while lo >= 0 and hi < n and s[lo] == s[hi]:\n"
            "                    count += 1\n"
            "                    lo -= 1\n"
            "                    hi += 1\n"
            "        return count\n"
        ),
        "approach": (
            "**Group palindromes by their centre.** For each of the `2n - 1` centres (n characters, n-1 gaps), expand "
            "outward while the end characters match; every successful expansion is exactly one palindrome, and "
            "every palindrome is produced exactly once by its own centre. Summing gives the count.\n\n"
            "**Why it works:** if `s[lo..hi]` is a palindrome centred at c, so is every shorter substring with the "
            "same centre, so the sequence of matches from the centre outward is a prefix of the expansion; the "
            "first mismatch ends all longer candidates at that centre.\n\n"
            "**DP alternative:** `pal[i][j] = (s[i] == s[j]) and (j - i < 2 or pal[i+1][j-1])`, counting the true "
            "cells. Same O(n^2) time but O(n^2) space; worth describing because it generalises to related "
            "problems, but present the expansion.\n\n"
            "**Common mistakes:** only handling odd centres (\"abba\" gives 4 instead of 6), counting substrings by "
            "text rather than by position, and checking every substring with a reversal (O(n^3)).\n\n"
            "**Interview follow-ups:** Return the longest one instead (track the best expansion). Count distinct "
            "palindromic substrings by text (collect them in a set, or use a palindromic tree / Eertree). Can you do "
            "O(n)? (Manacher gives the radius at every centre; sum of (radius+1)/2 terms.)"
        ),
        "complexity": {"time": "O(n^2) worst case", "space": "O(1)"},
        "similar": ["longest-palindromic-substring", "palindrome-partitioning"],
    },
    {
        "id": "decode-ways",
        "title": "Decode Ways",
        "difficulty": "Medium",
        "pattern": "1-D Dynamic Programming",
        "tags": ["String", "Dynamic Programming"],
        "companies": {"google": 3, "apple": 1, "meta": 4, "amazon": 3, "microsoft": 2},
        "description": (
            "Letters were encoded as numbers: `'A' -> 1`, `'B' -> 2`, ..., `'Z' -> 26`, and the codes were written "
            "one after another with no separators, giving a digit string `s`.\n\n"
            "Return how many different letter strings could have produced `s`. A group that starts with `0`, or "
            "whose value exceeds 26, is not a valid code. The answer fits in a 32-bit integer for the official "
            "constraints."
        ),
        "examples": [
            {"input": "s = \"12\"", "output": "2", "explanation": "\"AB\" (1 2) or \"L\" (12)."},
            {"input": "s = \"226\"", "output": "3", "explanation": "\"BZ\" (2 26), \"VF\" (22 6), \"BBF\" (2 2 6)."},
            {"input": "s = \"06\"", "output": "0", "explanation": "\"06\" is not a code; the leading zero makes it undecodable."},
        ],
        "constraints": ["1 <= s.length <= 100", "s contains only digits."],
        "hints": [
            "The last letter of a decoding covers either the final digit alone or the final two digits.",
            "ways(i) = (ways(i-1) if s[i-1] != '0') + (ways(i-2) if s[i-2:i] is between 10 and 26). ways(0) = 1.",
            "Zeros are the only real difficulty: a '0' must pair with a preceding 1 or 2, otherwise the count collapses to zero.",
        ],
        "function": "numDecodings",
        "signature": "def numDecodings(self, s: str) -> int:",
        "arg_types": {"s": "str"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"s": "12"}, "output": 2},
            {"input": {"s": "226"}, "output": 3},
            {"input": {"s": "06"}, "output": 0},
            {"input": {"s": "0"}, "output": 0},
            {"input": {"s": "10"}, "output": 1},
            {"input": {"s": "27"}, "output": 1},
            {"input": {"s": "1010"}, "output": 1},
            {"input": {"s": "2101"}, "output": 1},
            {"input": {"s": "11106"}, "output": 2},
            {"input": {"s": "100"}, "output": 0},
            {"input": {"s": "1" * 2000}, "output": _fib(2001)},
        ],
        "solution": (
            "class Solution:\n"
            "    def numDecodings(self, s: str) -> int:\n"
            "        if not s or s[0] == '0':\n"
            "            return 0\n"
            "        two_back, one_back = 1, 1  # ways to decode s[:i-1] and s[:i]\n"
            "        for i in range(1, len(s)):\n"
            "            cur = 0\n"
            "            if s[i] != '0':\n"
            "                cur += one_back  # s[i] stands alone\n"
            "            if s[i - 1] == '1' or (s[i - 1] == '2' and s[i] <= '6'):\n"
            "                cur += two_back  # s[i-1:i+1] is one letter 10..26\n"
            "            two_back, one_back = one_back, cur\n"
            "        return one_back\n"
        ),
        "approach": (
            "**The last code in any decoding is one digit or two digits, so count both options for the prefix.** Let "
            "`ways(i)` be the number of decodings of `s[:i]`. Then\n\n"
            "`ways(i) = [s[i-1] != '0'] * ways(i-1) + [10 <= int(s[i-2:i]) <= 26] * ways(i-2)`, with `ways(0) = 1` "
            "(empty prefix) and `ways(1) = 1` if the first digit is non-zero.\n\n"
            "This is Climbing Stairs with conditional edges: each step is allowed only when the digit group is a "
            "legal letter. Only two previous values are needed, hence O(1) space.\n\n"
            "**Why it works:** decodings of `s[:i]` partition by the length of their last code; the two classes are "
            "disjoint and each is in bijection with decodings of the corresponding shorter prefix.\n\n"
            "**Common mistakes:** treating \"0\" as a letter, accepting \"27\"..\"99\" as pairs, not returning 0 for a "
            "leading zero, and recursion without memoisation (exponential on long runs of 1s and 2s).\n\n"
            "**Interview follow-ups:** Decode Ways II with `*` wildcards (same recurrence with multipliers, modulo "
            "a prime). Reconstruct one or all decodings? (Backtrack through the DP; the number of decodings can be "
            "exponential so enumerate lazily.) Validate the string in a single pass as you go? (The DP already "
            "returns 0 when invalid.)"
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["climbing-stairs", "decode-ways-ii", "word-break"],
    },
    {
        "id": "coin-change",
        "title": "Coin Change",
        "difficulty": "Medium",
        "pattern": "1-D Dynamic Programming",
        "tags": ["Dynamic Programming", "Array", "BFS"],
        "companies": {"google": 3, "apple": 3, "meta": 2, "amazon": 4, "microsoft": 3},
        "description": (
            "You have coins of the denominations in `coins`, with an unlimited supply of each. Return the **fewest** "
            "coins whose values add up exactly to `amount`. If the amount cannot be made, return `-1`."
        ),
        "examples": [
            {"input": "coins = [1,2,5], amount = 11", "output": "3", "explanation": "5 + 5 + 1."},
            {"input": "coins = [2], amount = 3", "output": "-1"},
            {"input": "coins = [1], amount = 0", "output": "0"},
        ],
        "constraints": ["1 <= coins.length <= 12", "1 <= coins[i] <= 2^31 - 1", "0 <= amount <= 10^4"],
        "hints": [
            "Greedy (largest coin first) fails: coins [1,3,4], amount 6 wants 3+3, not 4+1+1.",
            "Let dp[a] be the fewest coins making amount a. The last coin used has some value c, so dp[a] = 1 + min(dp[a - c]) over coins c <= a.",
            "Fill dp from 0 up to amount with an 'infinity' sentinel; dp[0] = 0. Unreachable amounts stay infinite.",
        ],
        "function": "coinChange",
        "signature": "def coinChange(self, coins: List[int], amount: int) -> int:",
        "arg_types": {"coins": "List[int]", "amount": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"coins": [1, 2, 5], "amount": 11}, "output": 3},
            {"input": {"coins": [2], "amount": 3}, "output": -1},
            {"input": {"coins": [1], "amount": 0}, "output": 0},
            {"input": {"coins": [1, 3, 4], "amount": 6}, "output": 2},
            {"input": {"coins": [5, 10], "amount": 3}, "output": -1},
            {"input": {"coins": [186, 419, 83, 408], "amount": 6249}, "output": 20},
            {"input": {"coins": [1, 2, 5], "amount": 10000}, "output": 2000},
        ],
        "solution": (
            "class Solution:\n"
            "    def coinChange(self, coins: List[int], amount: int) -> int:\n"
            "        INF = amount + 1  # more coins than any real answer can use\n"
            "        dp = [0] + [INF] * amount\n"
            "        for a in range(1, amount + 1):\n"
            "            for c in coins:\n"
            "                if c <= a and dp[a - c] + 1 < dp[a]:\n"
            "                    dp[a] = dp[a - c] + 1\n"
            "        return dp[amount] if dp[amount] != INF else -1\n"
        ),
        "approach": (
            "**Unbounded knapsack, minimising count.** Define `dp[a]` as the fewest coins that sum to `a`. Whatever "
            "the optimal combination is, remove its last coin `c` and what remains is an optimal combination for "
            "`a - c` (otherwise swap in a better one). Hence\n\n"
            "`dp[a] = 1 + min(dp[a - c] for c in coins if c <= a)`, `dp[0] = 0`, unreachable amounts stay at the "
            "sentinel. Fill bottom-up from 1 to `amount`.\n\n"
            "The equivalent **BFS** view: amounts are nodes, each coin is an edge, and we want the shortest path "
            "from 0 to `amount`; level-by-level BFS stops as soon as `amount` is reached and can be faster when "
            "the answer is small.\n\n"
            "**Why greedy fails:** denominations are arbitrary, so taking the largest coin can leave a remainder "
            "that needs many small coins ([1,3,4], 6). The DP tries every last coin, so it cannot miss.\n\n"
            "**Common mistakes:** using `float('inf')` then returning it rather than -1, iterating coins in the "
            "outer loop with a 2-D table when 1-D suffices, and forgetting `amount = 0` returns 0.\n\n"
            "**Interview follow-ups:** Count the number of combinations instead of the minimum (Coin Change II; "
            "put coins in the outer loop to avoid counting permutations). Reconstruct the coins used? (Store "
            "`last[a] = c` when dp[a] improves, then walk back from amount.) Space is already O(amount); can the "
            "time improve? (Not in general; for 'canonical' coin systems greedy works and you can test for that.)"
        ),
        "complexity": {"time": "O(amount * len(coins))", "space": "O(amount)"},
        "similar": ["coin-change-ii", "perfect-squares", "minimum-cost-for-tickets"],
    },
    {
        "id": "maximum-product-subarray",
        "title": "Maximum Product Subarray",
        "difficulty": "Medium",
        "pattern": "1-D Dynamic Programming",
        "tags": ["Dynamic Programming", "Array"],
        "companies": {"google": 2, "apple": 1, "meta": 1, "amazon": 3, "microsoft": 3},
        "description": (
            "Given an integer array `nums`, find a non-empty contiguous subarray whose elements have the largest "
            "product, and return that product. The result is guaranteed to fit in a 32-bit integer."
        ),
        "examples": [
            {"input": "nums = [2,3,-2,4]", "output": "6", "explanation": "[2,3] gives 6; including -2 would make it negative."},
            {"input": "nums = [-2,0,-1]", "output": "0", "explanation": "Any subarray containing both negatives also contains the 0."},
        ],
        "constraints": ["1 <= nums.length <= 2 * 10^4", "-10 <= nums[i] <= 10", "The product of any prefix or suffix fits in a 32-bit integer."],
        "hints": [
            "Kadane's idea almost works, but a negative number flips the sign: the smallest (most negative) product so far may become the largest after multiplying by a negative.",
            "Track both the maximum and the minimum product of a subarray ending at the current index.",
            "At each element x: new_max = max(x, max*x, min*x), new_min = min(x, max*x, min*x). A zero resets both to 0, which is handled automatically by including x itself.",
        ],
        "function": "maxProduct",
        "signature": "def maxProduct(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [2, 3, -2, 4]}, "output": 6},
            {"input": {"nums": [-2, 0, -1]}, "output": 0},
            {"input": {"nums": [-2]}, "output": -2},
            {"input": {"nums": [-2, 3, -4]}, "output": 24},
            {"input": {"nums": [0, 2]}, "output": 2},
            {"input": {"nums": [-1, -2, -3, 0]}, "output": 6},
            {"input": {"nums": [(-1) ** i for i in range(4000)] + [3, -2, 4]}, "output": 24},
        ],
        "solution": (
            "class Solution:\n"
            "    def maxProduct(self, nums: List[int]) -> int:\n"
            "        best = cur_max = cur_min = nums[0]\n"
            "        for x in nums[1:]:\n"
            "            candidates = (x, cur_max * x, cur_min * x)\n"
            "            cur_max, cur_min = max(candidates), min(candidates)\n"
            "            best = max(best, cur_max)\n"
            "        return best\n"
        ),
        "approach": (
            "**Carry both the largest and the smallest product ending at each index, because a negative number "
            "swaps their roles.** Let `hi[i]` / `lo[i]` be the maximum / minimum product of a subarray ending at `i`. "
            "The subarray either starts at i (product `x`) or extends one ending at i-1, so\n\n"
            "`hi[i] = max(x, hi[i-1]*x, lo[i-1]*x)` and `lo[i] = min(x, hi[i-1]*x, lo[i-1]*x)`. The answer is "
            "`max(hi)`. Only the previous pair is needed, so two variables suffice.\n\n"
            "**Why it works:** the set of products of subarrays ending at i is `{x} ∪ {p*x : p ends at i-1}`; "
            "multiplying by a constant maps the extreme values of a set to extreme values, so tracking just the min "
            "and max of the previous set is sufficient. Zeros are handled because `x` itself (0) becomes both extremes "
            "and the next element restarts.\n\n"
            "**Common mistakes:** plain Kadane with products (fails on [-2,3,-4]), initialising best to 0 or 1 "
            "(fails on all-negative single element), and evaluating `cur_max` before computing `cur_min` from the old value.\n\n"
            "**Interview follow-ups:** The two-pass trick: the answer is the max over prefix products and suffix "
            "products with resets at zero; explain why. Return the subarray bounds? (Store the start index alongside "
            "hi and lo.) What about floating point or very large products? (Use logarithms or track sign and count "
            "of negatives; a 32-bit overflow-safe variant.)"
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["maximum-subarray", "maximum-product-of-three-numbers", "subarray-product-less-than-k"],
    },
    {
        "id": "word-break",
        "title": "Word Break",
        "difficulty": "Medium",
        "pattern": "1-D Dynamic Programming",
        "tags": ["String", "Dynamic Programming", "Hash Table", "Trie"],
        "companies": {"google": 3, "apple": 3, "meta": 4, "amazon": 4, "microsoft": 3},
        "description": (
            "Given a string `s` and a list of dictionary words `wordDict`, decide whether `s` can be split into a "
            "sequence of one or more dictionary words placed end to end. Words may be reused any number of times."
        ),
        "examples": [
            {"input": "s = \"leetcode\", wordDict = [\"leet\",\"code\"]", "output": "true"},
            {"input": "s = \"applepenapple\", wordDict = [\"apple\",\"pen\"]", "output": "true", "explanation": "\"apple\" is reused."},
            {"input": "s = \"catsandog\", wordDict = [\"cats\",\"dog\",\"sand\",\"and\",\"cat\"]", "output": "false",
             "explanation": "Every split leaves an unmatched piece (\"og\" or \"andog\")."},
        ],
        "constraints": ["1 <= s.length <= 300", "1 <= wordDict.length <= 1000", "1 <= wordDict[i].length <= 20",
                        "Lowercase English letters; dictionary words are distinct."],
        "hints": [
            "Let ok[i] mean 's[:i] can be segmented'. ok[0] is true (empty prefix).",
            "ok[i] is true if some j < i has ok[j] true and s[j:i] in the dictionary.",
            "Only look back as far as the longest dictionary word, and store the dictionary in a set for O(1) membership.",
        ],
        "function": "wordBreak",
        "signature": "def wordBreak(self, s: str, wordDict: List[str]) -> bool:",
        "arg_types": {"s": "str", "wordDict": "List[str]"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"s": "leetcode", "wordDict": ["leet", "code"]}, "output": True},
            {"input": {"s": "applepenapple", "wordDict": ["apple", "pen"]}, "output": True},
            {"input": {"s": "catsandog", "wordDict": ["cats", "dog", "sand", "and", "cat"]}, "output": False},
            {"input": {"s": "a", "wordDict": ["b"]}, "output": False},
            {"input": {"s": "cars", "wordDict": ["car", "ca", "rs"]}, "output": True},
            {"input": {"s": "aaaaaaa", "wordDict": ["aaaa", "aaa"]}, "output": True},
            {"input": {"s": "a" * 3000 + "b", "wordDict": ["a", "aa", "aaa", "aaaa"]}, "output": False},
            {"input": {"s": "catsanddog" * 300, "wordDict": ["cats", "dog", "sand", "and", "cat"]}, "output": True},
        ],
        "solution": (
            "class Solution:\n"
            "    def wordBreak(self, s: str, wordDict: List[str]) -> bool:\n"
            "        words = set(wordDict)\n"
            "        longest = max(len(w) for w in words)\n"
            "        ok = [True] + [False] * len(s)  # ok[i]: s[:i] is segmentable\n"
            "        for i in range(1, len(s) + 1):\n"
            "            for j in range(max(0, i - longest), i):\n"
            "                if ok[j] and s[j:i] in words:\n"
            "                    ok[i] = True\n"
            "                    break\n"
            "        return ok[-1]\n"
        ),
        "approach": (
            "**Whether a prefix is segmentable depends only on shorter prefixes: the last word must end at the "
            "prefix boundary.** Let `ok[i]` be true when `s[:i]` can be segmented. Then\n\n"
            "`ok[i] = any(ok[j] and s[j:i] in words for j in range(i))`, with `ok[0] = True`.\n\n"
            "Fill left to right. Restricting `j` to the last `maxlen` positions is a free win because a longer "
            "slice can never be a dictionary word. The set makes membership O(1) (plus the O(L) hashing of the slice).\n\n"
            "**Why it works:** any valid segmentation of `s[:i]` ends with a word `s[j:i]`, and the part before it is "
            "a valid segmentation of `s[:j]`; conversely such a pair yields a segmentation of `s[:i]`. Memoised "
            "top-down recursion from index 0 is the same DP in reverse.\n\n"
            "**Common mistakes:** naive recursion without memoisation (exponential on inputs like 'aaaa...ab'), "
            "scanning the whole dictionary at every position instead of slicing, and treating `wordDict` as a "
            "list for membership (O(dictionary size) per check).\n\n"
            "**Interview follow-ups:** Return all segmentations (Word Break II: memoised DFS returning lists; "
            "explain why the output can be exponential). Find a segmentation with the fewest words? (Store "
            "`best[i]` = min count, same transitions.) Speed up the inner loop with a trie walked from `j` "
            "forward, or when the dictionary is huge compared with `s`?"
        ),
        "complexity": {"time": "O(n * L^2) where L is the longest word (O(n * L) comparisons each hashing up to L chars)", "space": "O(n + total dictionary size)"},
        "similar": ["word-break-ii", "decode-ways", "concatenated-words"],
    },
    {
        "id": "longest-increasing-subsequence",
        "title": "Longest Increasing Subsequence",
        "difficulty": "Medium",
        "pattern": "1-D Dynamic Programming",
        "tags": ["Dynamic Programming", "Binary Search", "Array"],
        "companies": {"google": 3, "apple": 2, "meta": 2, "amazon": 3, "microsoft": 3},
        "description": (
            "Given an integer array `nums`, return the length of the longest **strictly increasing** subsequence "
            "(elements kept in their original order, not necessarily contiguous)."
        ),
        "examples": [
            {"input": "nums = [10,9,2,5,3,7,101,18]", "output": "4", "explanation": "One longest subsequence is [2,3,7,101]."},
            {"input": "nums = [0,1,0,3,2,3]", "output": "4", "explanation": "[0,1,2,3]."},
            {"input": "nums = [7,7,7,7]", "output": "1", "explanation": "Strictly increasing, so equal values cannot chain."},
        ],
        "constraints": ["1 <= nums.length <= 2500", "-10^4 <= nums[i] <= 10^4"],
        "hints": [
            "O(n^2): dp[i] = 1 + max(dp[j]) over j < i with nums[j] < nums[i].",
            "For O(n log n), keep tails[k] = the smallest possible last element of an increasing subsequence of length k+1. tails is always sorted.",
            "For each x, binary search the first tail >= x: replace it (a better ending for that length) or append if none exists. The answer is len(tails).",
        ],
        "function": "lengthOfLIS",
        "signature": "def lengthOfLIS(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [10, 9, 2, 5, 3, 7, 101, 18]}, "output": 4},
            {"input": {"nums": [0, 1, 0, 3, 2, 3]}, "output": 4},
            {"input": {"nums": [7, 7, 7, 7]}, "output": 1},
            {"input": {"nums": [1]}, "output": 1},
            {"input": {"nums": [5, 4, 3, 2, 1]}, "output": 1},
            {"input": {"nums": [1, 3, 6, 7, 9, 4, 10, 5, 6]}, "output": 6},
            {"input": {"nums": list(range(2500)) * 2}, "output": 2500},
            {"input": {"nums": [(i * 7919) % 10007 for i in range(5000)]}, "output": 63},
        ],
        "solution": (
            "class Solution:\n"
            "    def lengthOfLIS(self, nums: List[int]) -> int:\n"
            "        tails = []  # tails[k] = smallest last value of an increasing subsequence of length k + 1\n"
            "        for x in nums:\n"
            "            k = bisect.bisect_left(tails, x)\n"
            "            if k == len(tails):\n"
            "                tails.append(x)\n"
            "            else:\n"
            "                tails[k] = x\n"
            "        return len(tails)\n"
        ),
        "approach": (
            "**Patience sorting: for each length keep only the smallest possible ending value.** Maintain `tails`, "
            "where `tails[k]` is the minimum last element over all increasing subsequences of length `k + 1` seen so "
            "far. Scanning `x`, binary search for the first `tails[k] >= x`. If none, `x` extends the longest "
            "subsequence: append. Otherwise `x` is a better (smaller) ending for length `k + 1`: overwrite. "
            "`len(tails)` is the answer.\n\n"
            "**Invariants that make it correct:** `tails` is strictly increasing (a longer subsequence has a larger "
            "minimum tail, otherwise drop its last element for a contradiction), so binary search is valid; and "
            "replacing with a smaller tail never loses a length that was achievable. Note `tails` is *not* itself an "
            "LIS, just a record of best endings.\n\n"
            "**The O(n^2) DP** should be stated first: `dp[i] = 1 + max(dp[j] : j < i, nums[j] < nums[i])`. It is "
            "the natural route to reconstruction and to variants with extra constraints.\n\n"
            "**Common mistakes:** using `bisect_right` (allows equal elements, giving a non-decreasing subsequence), "
            "returning `tails` as if it were the subsequence, and off-by-one in the quadratic DP's base case.\n\n"
            "**Interview follow-ups:** Reconstruct an actual LIS? (In the O(n log n) version store for each element "
            "the index it replaced in `tails` and a predecessor pointer, then walk back from the last appended "
            "element; in the O(n^2) version keep `prev[i]`.) Longest non-decreasing? (`bisect_right`.) Count the "
            "number of LIS? (Pair dp length with a count array.) Russian Doll Envelopes reduces to this after a "
            "careful sort."
        ),
        "complexity": {"time": "O(n log n)", "space": "O(n)"},
        "similar": ["russian-doll-envelopes", "number-of-longest-increasing-subsequence", "longest-common-subsequence"],
    },
    {
        "id": "partition-equal-subset-sum",
        "title": "Partition Equal Subset Sum",
        "difficulty": "Medium",
        "pattern": "1-D Dynamic Programming",
        "tags": ["Dynamic Programming", "Array", "Bit Manipulation"],
        "companies": {"google": 2, "apple": 1, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "Given an array `nums` of positive integers, decide whether it can be split into two groups with "
            "**equal sums**. Every element must go to exactly one group."
        ),
        "examples": [
            {"input": "nums = [1,5,11,5]", "output": "true", "explanation": "{1,5,5} and {11} both sum to 11."},
            {"input": "nums = [1,2,3,5]", "output": "false", "explanation": "The total is 11, which is odd, so no equal split exists."},
        ],
        "constraints": ["1 <= nums.length <= 200", "1 <= nums[i] <= 100"],
        "hints": [
            "If the total is odd the answer is immediately false. Otherwise you need a subset summing to total / 2.",
            "This is 0/1 knapsack feasibility: reachable[s] = can some subset sum to s. Process each number once and update sums from high to low so an element is not reused.",
            "In Python a single integer can be the whole bitset: bits |= bits << x. Check bit total//2 at the end.",
        ],
        "function": "canPartition",
        "signature": "def canPartition(self, nums: List[int]) -> bool:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [1, 5, 11, 5]}, "output": True},
            {"input": {"nums": [1, 2, 3, 5]}, "output": False},
            {"input": {"nums": [1]}, "output": False},
            {"input": {"nums": [2, 2]}, "output": True},
            {"input": {"nums": [1, 2, 5]}, "output": False},
            {"input": {"nums": [2, 2, 3, 5]}, "output": False},
            {"input": {"nums": [100] * 200}, "output": True},
            {"input": {"nums": [i % 100 + 1 for i in range(200)]}, "output": True},
            {"input": {"nums": [3] * 199 + [5]}, "output": False},
        ],
        "solution": (
            "class Solution:\n"
            "    def canPartition(self, nums: List[int]) -> bool:\n"
            "        total = sum(nums)\n"
            "        if total % 2:\n"
            "            return False\n"
            "        target = total // 2\n"
            "        reachable = 1  # bit s is set when some subset sums to s; bit 0 = empty subset\n"
            "        for x in nums:\n"
            "            reachable |= reachable << x\n"
            "        return (reachable >> target) & 1 == 1\n"
        ),
        "approach": (
            "**Reduce to subset-sum: does any subset sum to exactly half the total?** If the total is odd, no. "
            "Otherwise this is 0/1 knapsack feasibility. Let `reach[s]` be true when some subset of the elements "
            "processed so far sums to `s`. Adding element `x` makes `reach[s] |= reach[s - x]`; iterate `s` "
            "downward so that the same element is not counted twice.\n\n"
            "Representing `reach` as a Python integer bitset turns the whole inner loop into `bits |= bits << x`, "
            "which is both the fastest and the shortest version; mention the boolean-array form (`for s in "
            "range(target, x-1, -1)`) so the interviewer sees you know what the shift is doing.\n\n"
            "**Why it works:** after processing a prefix of `nums`, the set bits are exactly the achievable subset "
            "sums of that prefix, by induction: a sum of the longer prefix either omits `x` (already set) or "
            "includes it (set at `s - x` before this step).\n\n"
            "**Common mistakes:** iterating sums upward with a 1-D array (lets an element be reused, turning it into "
            "unbounded knapsack), forgetting the odd-total shortcut, and recursing over all 2^n subsets.\n\n"
            "**Interview follow-ups:** Reconstruct one of the two groups? (Keep a 2-D table `reach[i][s]` or a "
            "`parent` bitset per step, then walk back; O(n * target) space.) Partition into k equal groups? "
            "(Bitmask DP over subsets, or backtracking with pruning.) Minimise the difference between the two "
            "group sums? (Largest reachable s <= total // 2.) Can you bound the running time by the value range "
            "instead of n * target? (Yes: target <= 10^4 here, so the bitset has at most 10^4 bits.)"
        ),
        "complexity": {"time": "O(n * total / w) with word size w (O(n * total) in the array form)", "space": "O(total)"},
        "similar": ["target-sum", "last-stone-weight-ii", "coin-change"],
    },
    {
        "id": "maximum-subarray",
        "title": "Maximum Subarray",
        "difficulty": "Medium",
        "pattern": "1-D Dynamic Programming",
        "tags": ["Dynamic Programming", "Array", "Divide and Conquer"],
        "companies": {"google": 3, "apple": 4, "meta": 3, "amazon": 4, "microsoft": 4},
        "description": (
            "Given an integer array `nums`, return the largest possible sum of a non-empty **contiguous** subarray."
        ),
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "[4,-1,2,1] sums to 6."},
            {"input": "nums = [1]", "output": "1"},
            {"input": "nums = [5,4,-1,7,8]", "output": "23", "explanation": "The whole array."},
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "hints": [
            "Consider the best subarray that ends exactly at index i. It either starts at i or extends the best one ending at i-1.",
            "cur = max(x, cur + x); the answer is the maximum cur seen. This is Kadane's algorithm.",
            "A negative running sum can never help, so it is dropped: that is the whole insight.",
        ],
        "function": "maxSubArray",
        "signature": "def maxSubArray(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4]}, "output": 6},
            {"input": {"nums": [1]}, "output": 1},
            {"input": {"nums": [5, 4, -1, 7, 8]}, "output": 23},
            {"input": {"nums": [-3, -1, -2]}, "output": -1},
            {"input": {"nums": [0]}, "output": 0},
            {"input": {"nums": [-2, -1]}, "output": -1},
            {"input": {"nums": [i % 10 - 4 for i in range(5000)]}, "output": 2510},
        ],
        "solution": (
            "class Solution:\n"
            "    def maxSubArray(self, nums: List[int]) -> int:\n"
            "        best = cur = nums[0]  # cur: best sum of a subarray ending at the current index\n"
            "        for x in nums[1:]:\n"
            "            cur = max(x, cur + x)\n"
            "            best = max(best, cur)\n"
            "        return best\n"
        ),
        "approach": (
            "**Kadane's algorithm: the best subarray ending at `i` is either `nums[i]` alone or `nums[i]` glued onto "
            "the best subarray ending at `i-1`.** Formally `end[i] = max(nums[i], end[i-1] + nums[i])` and the answer "
            "is `max(end)`. Since `end[i]` depends only on `end[i-1]`, one variable suffices.\n\n"
            "**Why it works:** every subarray ends somewhere, so the maximum over `end[i]` covers all of them. "
            "Extending a negative-sum prefix can only hurt, which is exactly what the `max(x, ...)` encodes: restart "
            "when the running sum would drag `x` down.\n\n"
            "**Alternative views the interviewer may raise:** prefix sums (answer = max over i of prefix[i] - min "
            "prefix before i), and divide-and-conquer in O(n log n) which returns the best crossing the midpoint; "
            "the latter is the only reason this problem is sometimes filed under divide and conquer.\n\n"
            "**Common mistakes:** initialising `best` to 0 (fails when all elements are negative), allowing an empty "
            "subarray, and resetting `cur` to 0 instead of to `x`.\n\n"
            "**Interview follow-ups:** Return the subarray indices? (Record a tentative start whenever `cur` restarts "
            "and commit it when `best` improves.) Circular array? (max(Kadane, total - min subarray), with the "
            "all-negative special case.) Maximum sum with length at most k? (Prefix sums plus a monotonic deque.) "
            "Maximum product instead of sum? (Track min and max, see Maximum Product Subarray.)"
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["maximum-product-subarray", "maximum-sum-circular-subarray", "best-time-to-buy-and-sell-stock"],
    },
]
