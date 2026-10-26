"""2-D Dynamic Programming problems. See SCHEMA.md for the dict format."""

import math

PROBLEMS = [
    {
        "id": "unique-paths",
        "title": "Unique Paths",
        "difficulty": "Medium",
        "pattern": "2-D Dynamic Programming",
        "tags": ["Math", "Dynamic Programming", "Combinatorics"],
        "companies": {"google": 3, "apple": 2, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "A robot sits in the top-left cell of an `m x n` grid and wants to reach the bottom-right cell. "
            "At every step it may move **only right or only down**.\n\n"
            "Return how many distinct routes exist from the start to the goal."
        ),
        "examples": [
            {"input": "m = 3, n = 7", "output": "28"},
            {"input": "m = 3, n = 2", "output": "3",
             "explanation": "The three routes are Right-Down-Down, Down-Right-Down and Down-Down-Right."},
            {"input": "m = 1, n = 1", "output": "1", "explanation": "Already at the goal; the empty route counts."},
        ],
        "constraints": ["1 <= m, n <= 100", "The answer fits in a 32-bit signed integer."],
        "hints": [
            "How many ways are there to reach a cell on the top row or the left column? Exactly one.",
            "Any other cell is entered from the cell above it or the cell to its left, so its count is the sum of those two.",
            "You only ever need the previous row, so a single 1-D array of length n is enough. There is also a closed form: choose which of the m+n-2 moves are 'down'.",
        ],
        "function": "uniquePaths",
        "signature": "def uniquePaths(self, m: int, n: int) -> int:",
        "arg_types": {"m": "int", "n": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"m": 3, "n": 7}, "output": 28},
            {"input": {"m": 3, "n": 2}, "output": 3},
            {"input": {"m": 1, "n": 1}, "output": 1},
            {"input": {"m": 1, "n": 10}, "output": 1},
            {"input": {"m": 10, "n": 10}, "output": 48620},
            {"input": {"m": 19, "n": 13}, "output": math.comb(30, 12)},
            {"input": {"m": 300, "n": 300}, "output": math.comb(598, 299)},
        ],
        "solution": (
            "class Solution:\n"
            "    def uniquePaths(self, m: int, n: int) -> int:\n"
            "        # row[j] = number of ways to reach column j in the current row\n"
            "        row = [1] * n\n"
            "        for _ in range(1, m):\n"
            "            for j in range(1, n):\n"
            "                row[j] += row[j - 1]   # from above (old row[j]) + from the left (new row[j-1])\n"
            "        return row[-1]\n"
        ),
        "approach": (
            "**Key insight: a cell can only be entered from above or from the left, so its route count is the sum of those two counts.**\n\n"
            "Define `dp[i][j]` = number of routes from `(0,0)` to `(i,j)`. Every cell in row 0 or column 0 has exactly one route "
            "(a straight line). For the rest, `dp[i][j] = dp[i-1][j] + dp[i][j-1]`. The answer is `dp[m-1][n-1]`.\n\n"
            "**Why it is correct:** the last move into `(i,j)` is either a Down move from `(i-1,j)` or a Right move from `(i,j-1)`; "
            "those two sets of routes are disjoint and together cover every route.\n\n"
            "**Space optimisation:** when filling row `i` left to right, `row[j]` still holds the value from row `i-1` (the cell above) "
            "and `row[j-1]` already holds the new value (the cell to the left), so `row[j] += row[j-1]` updates in place with O(n) memory.\n\n"
            "**Closed form:** every route is a sequence of `m-1` downs and `n-1` rights, so the answer is `C(m+n-2, m-1)`. "
            "Compute it incrementally to avoid huge factorials.\n\n"
            "**Common mistakes:** forgetting that the 1 x 1 grid has exactly one route; mixing up which index is rows versus columns "
            "(the answer is symmetric, so it does not matter here, but it will in Unique Paths II).\n\n"
            "**Interview follow-ups:** (1) Add obstacles (Unique Paths II: an obstacle cell gets 0 routes). "
            "(2) Allow diagonal moves (add a third term `dp[i-1][j-1]`). "
            "(3) Return the number of routes modulo a prime when the grid is large, or derive the combinatorial formula and discuss overflow."
        ),
        "complexity": {"time": "O(m * n)", "space": "O(n)"},
        "similar": ["minimum-path-sum", "unique-paths-ii", "climbing-stairs"],
    },
    {
        "id": "longest-common-subsequence",
        "title": "Longest Common Subsequence",
        "difficulty": "Medium",
        "pattern": "2-D Dynamic Programming",
        "tags": ["String", "Dynamic Programming"],
        "companies": {"google": 2, "apple": 1, "meta": 1, "amazon": 3, "microsoft": 2},
        "description": (
            "Given two strings `text1` and `text2`, return the length of their longest **common subsequence**. "
            "A subsequence keeps the relative order of characters but may skip any of them. If the strings share no characters, "
            "return `0`.\n\n"
            "For example, `\"ace\"` is a subsequence of `\"abcde\"`, but `\"aec\"` is not."
        ),
        "examples": [
            {"input": "text1 = \"abcde\", text2 = \"ace\"", "output": "3", "explanation": "\"ace\" appears in both in order."},
            {"input": "text1 = \"abc\", text2 = \"abc\"", "output": "3"},
            {"input": "text1 = \"abc\", text2 = \"def\"", "output": "0", "explanation": "No character is shared."},
        ],
        "constraints": ["1 <= text1.length, text2.length <= 1000", "Both strings consist of lowercase English letters."],
        "hints": [
            "Compare the last characters of both strings. If they match, they can both be part of the answer.",
            "Let dp[i][j] be the LCS length of the first i characters of text1 and the first j characters of text2. When text1[i-1] == text2[j-1], dp[i][j] = dp[i-1][j-1] + 1; otherwise take the better of dropping one character from either string.",
            "Each row only depends on the previous row, so two rows of length len(text2)+1 suffice.",
        ],
        "function": "longestCommonSubsequence",
        "signature": "def longestCommonSubsequence(self, text1: str, text2: str) -> int:",
        "arg_types": {"text1": "str", "text2": "str"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"text1": "abcde", "text2": "ace"}, "output": 3},
            {"input": {"text1": "abc", "text2": "abc"}, "output": 3},
            {"input": {"text1": "abc", "text2": "def"}, "output": 0},
            {"input": {"text1": "a", "text2": "a"}, "output": 1},
            {"input": {"text1": "", "text2": "abc"}, "output": 0},
            {"input": {"text1": "bsbininm", "text2": "jmjkbkjkv"}, "output": 1},
            {"input": {"text1": "abcba", "text2": "abcbcba"}, "output": 5},
            {"input": {"text1": "ab" * 400, "text2": "ba" * 400}, "output": 799},
            {"input": {"text1": "abcdefghij" * 80, "text2": "abcdefghij" * 80}, "output": 800},
        ],
        "solution": (
            "class Solution:\n"
            "    def longestCommonSubsequence(self, text1: str, text2: str) -> int:\n"
            "        if len(text2) > len(text1):\n"
            "            text1, text2 = text2, text1   # keep the shorter string on the inner dimension\n"
            "        n = len(text2)\n"
            "        prev = [0] * (n + 1)\n"
            "        for ch in text1:\n"
            "            cur = [0] * (n + 1)\n"
            "            for j in range(1, n + 1):\n"
            "                if ch == text2[j - 1]:\n"
            "                    cur[j] = prev[j - 1] + 1\n"
            "                else:\n"
            "                    cur[j] = max(prev[j], cur[j - 1])\n"
            "            prev = cur\n"
            "        return prev[n]\n"
        ),
        "approach": (
            "**Key insight: compare the strings one prefix at a time. If the last characters of two prefixes match, they belong to a "
            "common subsequence; otherwise at least one of them can be discarded.**\n\n"
            "Let `dp[i][j]` be the LCS length of `text1[:i]` and `text2[:j]`. Then\n\n"
            "- `dp[i][j] = dp[i-1][j-1] + 1` if `text1[i-1] == text2[j-1]`\n"
            "- `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` otherwise\n\n"
            "with `dp[0][*] = dp[*][0] = 0`. The answer is `dp[len1][len2]`.\n\n"
            "**Why it is correct:** when the last characters match, some optimal common subsequence can be made to end with that pair "
            "(exchange argument), so extending the LCS of the two shorter prefixes by one is optimal. When they differ, the two last "
            "characters cannot both be the final matched pair, so dropping one of them loses nothing.\n\n"
            "**Space optimisation:** row `i` depends only on row `i-1`, so keep two rows. With the shorter string on the inner dimension "
            "memory is `O(min(m, n))`. Recovering the subsequence itself requires the full table (walk back from the corner).\n\n"
            "**Common mistakes:** confusing subsequence with substring (substring requires contiguity and resets to 0 on mismatch); "
            "off-by-one errors between 0-indexed characters and 1-indexed table entries; taking `dp[i-1][j-1] + 1` even when the "
            "characters differ.\n\n"
            "**Interview follow-ups:** (1) Print one actual LCS, not just its length. (2) Edit Distance and Shortest Common Supersequence "
            "are the same table with different transitions. (3) Longest Palindromic Subsequence is LCS of a string with its reverse."
        ),
        "complexity": {"time": "O(m * n)", "space": "O(min(m, n))"},
        "similar": ["edit-distance", "distinct-subsequences", "longest-palindromic-subsequence"],
    },
    {
        "id": "best-time-to-buy-and-sell-stock-with-cooldown",
        "title": "Best Time to Buy and Sell Stock with Cooldown",
        "difficulty": "Medium",
        "pattern": "2-D Dynamic Programming",
        "tags": ["Array", "Dynamic Programming", "State Machine"],
        "companies": {"google": 1, "amazon": 2, "microsoft": 1},
        "description": (
            "You are given `prices`, where `prices[i]` is the price of a stock on day `i`. You may complete as many "
            "buy-then-sell transactions as you like, with two rules:\n\n"
            "- You may hold at most one share at a time (you must sell before buying again).\n"
            "- After you sell, you must skip the next day entirely: you cannot buy on the day right after a sale.\n\n"
            "Return the maximum total profit you can achieve."
        ),
        "examples": [
            {"input": "prices = [1,2,3,0,2]", "output": "3",
             "explanation": "Buy at 1, sell at 2 (profit 1), cool down on day 2, buy at 0, sell at 2 (profit 2)."},
            {"input": "prices = [1]", "output": "0"},
            {"input": "prices = [6,1,3,2,4,7]", "output": "6", "explanation": "Buy at 1 and sell at 7."},
        ],
        "constraints": ["1 <= prices.length <= 5000", "0 <= prices[i] <= 1000"],
        "hints": [
            "At the end of each day you are in one of three situations: holding a share, just sold today, or free with no share and no cooldown.",
            "Write how each of the three states on day i is reached from the states on day i-1, taking the best option for each.",
            "Holding today comes from holding yesterday or buying today out of the free state. Sold today comes only from holding yesterday. Free today comes from free yesterday or from having sold yesterday (cooldown finished).",
        ],
        "function": "maxProfit",
        "signature": "def maxProfit(self, prices: List[int]) -> int:",
        "arg_types": {"prices": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"prices": [1, 2, 3, 0, 2]}, "output": 3},
            {"input": {"prices": [1]}, "output": 0},
            {"input": {"prices": [6, 1, 3, 2, 4, 7]}, "output": 6},
            {"input": {"prices": [2, 1]}, "output": 0},
            {"input": {"prices": [1, 2, 4]}, "output": 3},
            {"input": {"prices": [1, 2, 3, 4, 5]}, "output": 4},
            {"input": {"prices": [1, 4, 2]}, "output": 3},
            {"input": {"prices": list(range(1, 1001))}, "output": 999},
            {"input": {"prices": list(range(1000, 0, -1))}, "output": 0},
            {"input": {"prices": [(i * 37 + 11) % 101 for i in range(1000)]}, "output": 13542},
        ],
        "solution": (
            "class Solution:\n"
            "    def maxProfit(self, prices: List[int]) -> int:\n"
            "        hold = float('-inf')   # best profit while holding a share\n"
            "        sold = 0               # best profit having sold today (cooldown tomorrow)\n"
            "        free = 0               # best profit with no share and no cooldown\n"
            "        for p in prices:\n"
            "            hold, sold, free = (\n"
            "                max(hold, free - p),   # keep holding, or buy today from the free state\n"
            "                hold + p,              # sell what we were holding\n"
            "                max(free, sold),       # stay free, or finish the cooldown\n"
            "            )\n"
            "        return max(sold, free)\n"
        ),
        "approach": (
            "**Key insight: model the day as a finite state machine with three states (holding, just sold, free) and keep the best "
            "profit for each state.**\n\n"
            "Transitions for day `i` with price `p`:\n\n"
            "- `hold[i] = max(hold[i-1], free[i-1] - p)` : keep the share, or buy it today (only allowed from the free state, which encodes the cooldown)\n"
            "- `sold[i] = hold[i-1] + p` : sell the share we were holding\n"
            "- `free[i] = max(free[i-1], sold[i-1])` : do nothing, or come out of yesterday's sale\n\n"
            "Start with `hold = -inf` (we cannot be holding before day 0), `sold = free = 0`. The answer is `max(sold, free)` after "
            "the last day; ending while still holding is never optimal.\n\n"
            "**Why it is correct:** every legal sequence of actions is a walk through this automaton, and the cooldown rule is "
            "enforced structurally because the only path from `sold` back to `hold` goes through `free`, which costs one day. "
            "Keeping only the maximum per state is safe because future transitions add the same amounts regardless of history.\n\n"
            "**Space optimisation:** each day depends only on the previous day, so three scalars replace the `n x 3` table. "
            "Evaluate the three new values simultaneously (tuple assignment) so that an updated `hold` is not used to compute `sold`.\n\n"
            "**Common mistakes:** letting `sold` feed directly into `hold` (ignores the cooldown); initialising `hold` to 0 instead of "
            "-infinity, which allows a free share; returning `hold` as a candidate answer.\n\n"
            "**Interview follow-ups:** (1) Transaction fee instead of cooldown (subtract the fee on sell). (2) At most `k` transactions "
            "(add a transaction-count dimension). (3) Cooldown of `c` days (keep a window of the last `c` sold values, or an array indexed by day)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["best-time-to-buy-and-sell-stock", "best-time-to-buy-and-sell-stock-ii", "best-time-to-buy-and-sell-stock-with-transaction-fee"],
    },
    {
        "id": "coin-change-ii",
        "title": "Coin Change II",
        "difficulty": "Medium",
        "pattern": "2-D Dynamic Programming",
        "tags": ["Array", "Dynamic Programming"],
        "companies": {"google": 2, "apple": 1, "amazon": 2, "microsoft": 1},
        "description": (
            "You have an unlimited supply of coins in the denominations listed in `coins`, and a target `amount`. "
            "Return the number of **distinct combinations** of coins that sum exactly to `amount`. Two combinations are the same if "
            "they use the same multiset of coins, regardless of order. If no combination works, return `0`.\n\n"
            "The answer fits in a 64-bit signed integer."
        ),
        "examples": [
            {"input": "amount = 5, coins = [1,2,5]", "output": "4",
             "explanation": "5 = 5 = 2+2+1 = 2+1+1+1 = 1+1+1+1+1."},
            {"input": "amount = 3, coins = [2]", "output": "0", "explanation": "You cannot make an odd amount from 2s."},
            {"input": "amount = 10, coins = [10]", "output": "1"},
        ],
        "constraints": ["1 <= coins.length <= 300", "1 <= coins[i] <= 5000", "All coin values are distinct.", "0 <= amount <= 5000"],
        "hints": [
            "This counts combinations, not permutations: 1+2 and 2+1 must be counted once. Think about how to avoid double counting.",
            "Process coins one at a time. Decide, for each coin, how it contributes to every amount before moving to the next coin.",
            "dp[a] = number of ways to make amount a using the coins seen so far. For each coin c, loop a from c up to amount and add dp[a - c] to dp[a]. The outer loop over coins is what guarantees each combination is counted once.",
        ],
        "function": "change",
        "signature": "def change(self, amount: int, coins: List[int]) -> int:",
        "arg_types": {"amount": "int", "coins": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"amount": 5, "coins": [1, 2, 5]}, "output": 4},
            {"input": {"amount": 3, "coins": [2]}, "output": 0},
            {"input": {"amount": 10, "coins": [10]}, "output": 1},
            {"input": {"amount": 0, "coins": [7]}, "output": 1},
            {"input": {"amount": 4, "coins": [1, 2, 3]}, "output": 4},
            {"input": {"amount": 7, "coins": [3, 5]}, "output": 0},
            {"input": {"amount": 5000, "coins": [1, 2, 5, 10, 20, 50, 100, 200]}, "output": 10082315214426},
            {"input": {"amount": 5000, "coins": [5000]}, "output": 1},
        ],
        "solution": (
            "class Solution:\n"
            "    def change(self, amount: int, coins: List[int]) -> int:\n"
            "        dp = [0] * (amount + 1)\n"
            "        dp[0] = 1   # one way to make zero: use no coins\n"
            "        for c in coins:\n"
            "            for a in range(c, amount + 1):\n"
            "                dp[a] += dp[a - c]\n"
            "        return dp[amount]\n"
        ),
        "approach": (
            "**Key insight: to count combinations rather than orderings, fix the order in which coin types are considered. "
            "Loop over coins on the outside and amounts on the inside.**\n\n"
            "The 2-D formulation is `dp[i][a]` = ways to make `a` using only the first `i` coin types. Either the i-th coin is not used "
            "(`dp[i-1][a]`) or it is used at least once (`dp[i][a - coins[i]]`, staying in row `i` because the supply is unlimited):\n\n"
            "`dp[i][a] = dp[i-1][a] + dp[i][a - c]`\n\n"
            "**Why the loop order matters:** with coins outside, every combination is built in a canonical order (all 1s, then all 2s, ...), "
            "so `{1,2}` and `{2,1}` are the same path. Swapping the loops (amount outside, coins inside) counts ordered sequences, "
            "which is the Combination Sum IV problem.\n\n"
            "**Space optimisation:** row `i` reads row `i-1` at the same column and row `i` at a smaller column. Iterating `a` upward "
            "over a single array gives exactly that: `dp[a - c]` has already been updated for the current coin and `dp[a]` has not.\n\n"
            "**Common mistakes:** the loop order above; forgetting `dp[0] = 1`; iterating `a` downward (which would count each coin at most once, "
            "the 0/1 knapsack behaviour).\n\n"
            "**Interview follow-ups:** (1) Minimum number of coins instead of count (Coin Change I, replace sum with min). "
            "(2) Each coin usable at most once (reverse the inner loop). (3) Count ordered sequences instead (swap the loops)."
        ),
        "complexity": {"time": "O(amount * len(coins))", "space": "O(amount)"},
        "similar": ["coin-change", "combination-sum-iv", "target-sum"],
    },
    {
        "id": "target-sum",
        "title": "Target Sum",
        "difficulty": "Medium",
        "pattern": "2-D Dynamic Programming",
        "tags": ["Array", "Dynamic Programming", "Backtracking"],
        "companies": {"google": 2, "meta": 3, "amazon": 2, "microsoft": 1},
        "description": (
            "You are given an array of non-negative integers `nums` and an integer `target`. Place either a `+` or a `-` in front of "
            "**every** element and evaluate the resulting expression.\n\n"
            "Return the number of different sign assignments whose expression evaluates to `target`."
        ),
        "examples": [
            {"input": "nums = [1,1,1,1,1], target = 3", "output": "5",
             "explanation": "Exactly one of the five 1s must be negative: 5 choices."},
            {"input": "nums = [1], target = 1", "output": "1"},
            {"input": "nums = [2,3], target = 1", "output": "1", "explanation": "-2 + 3 = 1 is the only way."},
        ],
        "constraints": ["1 <= nums.length <= 20", "0 <= nums[i] <= 1000", "0 <= sum(nums) <= 1000", "-1000 <= target <= 1000"],
        "hints": [
            "Brute force tries 2^n sign patterns. The running total only ranges over a bounded set of values, so many prefixes end in the same total.",
            "Let P be the elements given a plus sign and N the rest. Then P - N = target and P + N = total, so P = (total + target) / 2. The question becomes: how many subsets sum to P?",
            "If total + target is odd or negative there is no solution. Otherwise count subsets with a 0/1 knapsack: for each number iterate the sum downward and add dp[s - x] to dp[s].",
        ],
        "function": "findTargetSumWays",
        "signature": "def findTargetSumWays(self, nums: List[int], target: int) -> int:",
        "arg_types": {"nums": "List[int]", "target": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [1, 1, 1, 1, 1], "target": 3}, "output": 5},
            {"input": {"nums": [1], "target": 1}, "output": 1},
            {"input": {"nums": [2, 3], "target": 1}, "output": 1},
            {"input": {"nums": [1], "target": 2}, "output": 0},
            {"input": {"nums": [0, 0, 0, 0, 0, 0, 0, 0, 1], "target": 1}, "output": 256},
            {"input": {"nums": [1, 2, 3], "target": -6}, "output": 1},
            {"input": {"nums": [1, 2, 3], "target": 7}, "output": 0},
            {"input": {"nums": [1] * 40, "target": 0}, "output": math.comb(40, 20)},
            {"input": {"nums": list(range(1, 101)), "target": 50}, "output": 1724754104723121472580217751},
        ],
        "solution": (
            "class Solution:\n"
            "    def findTargetSumWays(self, nums: List[int], target: int) -> int:\n"
            "        total = sum(nums)\n"
            "        if abs(target) > total or (total + target) % 2:\n"
            "            return 0\n"
            "        want = (total + target) // 2   # sum of the elements that receive a plus sign\n"
            "        dp = [0] * (want + 1)\n"
            "        dp[0] = 1\n"
            "        for x in nums:\n"
            "            for s in range(want, x - 1, -1):   # downward: each element used at most once\n"
            "                dp[s] += dp[s - x]\n"
            "        return dp[want]\n"
        ),
        "approach": (
            "**Key insight: choosing signs is the same as choosing a subset. If the plus-signed elements sum to `P` and the total is `S`, "
            "then `P - (S - P) = target`, so `P = (S + target) / 2`. Count subsets that sum to `P`.**\n\n"
            "If `S + target` is odd, or `|target| > S`, no assignment works. Otherwise run a 0/1 knapsack count: `dp[s]` = number of "
            "subsets of the elements seen so far with sum `s`. For each `x`, update `s` from high to low with `dp[s] += dp[s - x]`.\n\n"
            "**The direct 2-D view:** `dp[i][v]` = number of ways to assign signs to the first `i` elements and reach running total `v`, "
            "with `dp[i][v] = dp[i-1][v - x] + dp[i-1][v + x]`. The total ranges over `[-S, S]`, so a hash map or an offset array works. "
            "The subset-sum reduction halves the state space and avoids negative indices.\n\n"
            "**Why downward iteration:** reading `dp[s - x]` before it has been touched by the current element guarantees each element "
            "is used at most once (otherwise it becomes the unbounded knapsack from Coin Change II).\n\n"
            "**Common mistakes:** forgetting the odd-parity check; dividing before checking negativity; zeros in `nums` are fine with this "
            "formulation (each zero doubles the count) but trip up solutions that special-case them.\n\n"
            "**Interview follow-ups:** (1) Return one valid assignment, not the count (store parent pointers or backtrack through the table). "
            "(2) What if `nums` can contain negatives (shift by the sum of absolute values and use the 2-D view). "
            "(3) Partition Equal Subset Sum is the special case `target = 0` asked as a yes/no question."
        ),
        "complexity": {"time": "O(n * (sum + target))", "space": "O(sum + target)"},
        "similar": ["partition-equal-subset-sum", "coin-change-ii", "last-stone-weight-ii"],
    },
    {
        "id": "interleaving-string",
        "title": "Interleaving String",
        "difficulty": "Medium",
        "pattern": "2-D Dynamic Programming",
        "tags": ["String", "Dynamic Programming"],
        "companies": {"google": 1, "amazon": 1, "microsoft": 1},
        "description": (
            "Given strings `s1`, `s2` and `s3`, decide whether `s3` can be formed by **interleaving** `s1` and `s2`: split both "
            "`s1` and `s2` into pieces, then alternate pieces from each so that the characters of `s1` stay in their original order "
            "and so do the characters of `s2`.\n\n"
            "Return `true` if such an interleaving exists, otherwise `false`."
        ),
        "examples": [
            {"input": "s1 = \"aabcc\", s2 = \"dbbca\", s3 = \"aadbbcbcac\"", "output": "true",
             "explanation": "aa | dbb | c | bca | c alternates pieces of s1 and s2."},
            {"input": "s1 = \"aabcc\", s2 = \"dbbca\", s3 = \"aadbbbaccc\"", "output": "false"},
            {"input": "s1 = \"\", s2 = \"\", s3 = \"\"", "output": "true"},
        ],
        "constraints": ["0 <= s1.length, s2.length <= 100", "0 <= s3.length <= 200", "Lowercase English letters only."],
        "hints": [
            "If the lengths do not add up, the answer is immediately false.",
            "Think of walking through s3. At each step the next character came from either s1 or s2. The state you need is how many characters of each you have consumed so far.",
            "dp[i][j] = can the first i+j characters of s3 be formed from s1[:i] and s2[:j]. It is true if (dp[i-1][j] and s1[i-1] == s3[i+j-1]) or (dp[i][j-1] and s2[j-1] == s3[i+j-1]). One row of length len(s2)+1 suffices.",
        ],
        "function": "isInterleave",
        "signature": "def isInterleave(self, s1: str, s2: str, s3: str) -> bool:",
        "arg_types": {"s1": "str", "s2": "str", "s3": "str"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"s1": "aabcc", "s2": "dbbca", "s3": "aadbbcbcac"}, "output": True},
            {"input": {"s1": "aabcc", "s2": "dbbca", "s3": "aadbbbaccc"}, "output": False},
            {"input": {"s1": "", "s2": "", "s3": ""}, "output": True},
            {"input": {"s1": "a", "s2": "", "s3": "a"}, "output": True},
            {"input": {"s1": "a", "s2": "b", "s3": "ab"}, "output": True},
            {"input": {"s1": "ab", "s2": "cd", "s3": "abdc"}, "output": False},
            {"input": {"s1": "abc", "s2": "", "s3": "ab"}, "output": False},
            {"input": {"s1": "a" * 100, "s2": "a" * 100, "s3": "a" * 200}, "output": True},
            {"input": {"s1": "a" * 100, "s2": "b" * 100, "s3": "ab" * 99 + "ba"}, "output": True},
            {"input": {"s1": "a" * 100, "s2": "b" * 100, "s3": "ab" * 99 + "aa"}, "output": False},
        ],
        "solution": (
            "class Solution:\n"
            "    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:\n"
            "        m, n = len(s1), len(s2)\n"
            "        if m + n != len(s3):\n"
            "            return False\n"
            "        # dp[j]: can s3[:i+j] be built from s1[:i] and s2[:j] (i is the outer loop)\n"
            "        dp = [False] * (n + 1)\n"
            "        dp[0] = True\n"
            "        for j in range(1, n + 1):\n"
            "            dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]\n"
            "        for i in range(1, m + 1):\n"
            "            dp[0] = dp[0] and s1[i - 1] == s3[i - 1]\n"
            "            for j in range(1, n + 1):\n"
            "                k = i + j - 1\n"
            "                dp[j] = (dp[j] and s1[i - 1] == s3[k]) or (dp[j - 1] and s2[j - 1] == s3[k])\n"
            "        return dp[n]\n"
        ),
        "approach": (
            "**Key insight: the only thing that matters about a partial interleaving is how many characters of `s1` and of `s2` have "
            "been used. Those two counters also determine the position in `s3`.**\n\n"
            "Let `dp[i][j]` be true when `s3[:i+j]` is an interleaving of `s1[:i]` and `s2[:j]`. The last character `s3[i+j-1]` came "
            "from one of the two strings:\n\n"
            "`dp[i][j] = (dp[i-1][j] and s1[i-1] == s3[i+j-1]) or (dp[i][j-1] and s2[j-1] == s3[i+j-1])`\n\n"
            "with `dp[0][0] = true`. The answer is `dp[m][n]`, after an early exit when `m + n != len(s3)`.\n\n"
            "**Why it is correct:** any interleaving of the prefixes ends with a character from `s1` or from `s2`, and removing it leaves "
            "an interleaving of shorter prefixes. The recurrence considers both cases exhaustively, so no valid interleaving is missed "
            "and no invalid one is accepted.\n\n"
            "**Space optimisation:** `dp[i][j]` depends only on `dp[i-1][j]` (same column, previous row) and `dp[i][j-1]` (already "
            "computed in this row), so a single row of length `n+1` updated in place is enough: before overwriting, `dp[j]` still holds "
            "the value from the previous row.\n\n"
            "**Common mistakes:** greedy matching (when both strings offer the same next character you must try both); forgetting the "
            "length check, which breaks the index arithmetic; treating the problem as checking that `s1` and `s2` are both subsequences "
            "of `s3`, which is necessary but not sufficient.\n\n"
            "**Interview follow-ups:** (1) Return one actual interleaving (keep parent choices and walk back). "
            "(2) Count the number of distinct interleavings (replace `or` with `+`). "
            "(3) Three input strings: the state becomes `(i, j, k)` and the table 3-D."
        ),
        "complexity": {"time": "O(m * n)", "space": "O(n)"},
        "similar": ["distinct-subsequences", "edit-distance", "longest-common-subsequence"],
    },
    {
        "id": "longest-increasing-path-in-a-matrix",
        "title": "Longest Increasing Path in a Matrix",
        "difficulty": "Hard",
        "pattern": "2-D Dynamic Programming",
        "tags": ["Matrix", "DFS", "Memoization", "Topological Sort"],
        "companies": {"google": 4, "apple": 1, "meta": 2, "amazon": 2, "microsoft": 1},
        "description": (
            "Given an `m x n` integer matrix, return the length of the longest path along which the values are **strictly "
            "increasing**. From any cell you may step up, down, left or right (not diagonally, and not outside the grid).\n\n"
            "A single cell counts as a path of length 1."
        ),
        "examples": [
            {"input": "matrix = [[9,9,4],[6,6,8],[2,1,1]]", "output": "4", "explanation": "1 -> 2 -> 6 -> 9."},
            {"input": "matrix = [[3,4,5],[3,2,6],[2,2,1]]", "output": "4", "explanation": "3 -> 4 -> 5 -> 6."},
            {"input": "matrix = [[1]]", "output": "1"},
        ],
        "constraints": ["1 <= m, n <= 200", "0 <= matrix[i][j] <= 2^31 - 1"],
        "hints": [
            "Because the path must strictly increase, you can never revisit a cell. There are no cycles to worry about, so no visited set is needed.",
            "The longest path starting at a cell depends only on the longest paths starting at its larger neighbours. That is a recursive definition with overlapping subproblems.",
            "DFS from every cell with memoization: best(r, c) = 1 + max(best(nr, nc)) over neighbours with a larger value. Alternatively, treat the grid as a DAG and process cells in topological (Kahn) order.",
        ],
        "function": "longestIncreasingPath",
        "signature": "def longestIncreasingPath(self, matrix: List[List[int]]) -> int:",
        "arg_types": {"matrix": "List[List[int]]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"matrix": [[9, 9, 4], [6, 6, 8], [2, 1, 1]]}, "output": 4},
            {"input": {"matrix": [[3, 4, 5], [3, 2, 6], [2, 2, 1]]}, "output": 4},
            {"input": {"matrix": [[1]]}, "output": 1},
            {"input": {"matrix": [[1, 2, 3, 4, 5]]}, "output": 5},
            {"input": {"matrix": [[7, 7], [7, 7]]}, "output": 1},
            {"input": {"matrix": [[5, 4], [1, 2]]}, "output": 4},
            {"input": {"matrix": [[i * 100 + j for j in range(100)] for i in range(100)]}, "output": 199},
            {"input": {"matrix": [[i * 50 + (j if i % 2 == 0 else 49 - j) for j in range(50)] for i in range(50)]}, "output": 2500},
        ],
        "solution": (
            "class Solution:\n"
            "    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:\n"
            "        m, n = len(matrix), len(matrix[0])\n"
            "        memo = [[0] * n for _ in range(m)]   # 0 = not computed yet\n"
            "\n"
            "        def best(r: int, c: int) -> int:\n"
            "            if memo[r][c]:\n"
            "                return memo[r][c]\n"
            "            longest = 1\n"
            "            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):\n"
            "                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:\n"
            "                    longest = max(longest, 1 + best(nr, nc))\n"
            "            memo[r][c] = longest\n"
            "            return longest\n"
            "\n"
            "        return max(best(r, c) for r in range(m) for c in range(n))\n"
        ),
        "approach": (
            "**Key insight: strictly increasing means the move graph is a DAG, so the longest path from each cell is a pure function of "
            "its larger neighbours and can be memoized.**\n\n"
            "Define `best(r, c)` = length of the longest increasing path that starts at `(r, c)`. Then "
            "`best(r, c) = 1 + max(best(nr, nc))` over the up-to-four neighbours whose value is strictly greater, or `1` if none exist. "
            "Run the DFS from every cell, caching results in an `m x n` table; the answer is the maximum entry.\n\n"
            "**Why it is correct:** values increase along every edge, so the recursion can never return to a cell (no cycles, no visited "
            "set needed) and each cell's value is final once computed. Every cell is expanded once and each expansion looks at four "
            "neighbours, so the work is linear in the grid size.\n\n"
            "**Alternative (iterative):** compute each cell's out-degree (number of larger neighbours), start a BFS from cells with "
            "out-degree 0 (local maxima), and peel layers like Kahn's algorithm; the number of layers is the answer. This avoids recursion "
            "depth problems in languages with small stacks.\n\n"
            "**Common mistakes:** adding a visited set and un-marking it (correct but exponential); using `>=` instead of `>` which "
            "creates cycles; forgetting that the answer for a single cell is 1, not 0.\n\n"
            "**Interview follow-ups:** (1) Return the path itself (store the best neighbour per cell). (2) Allow diagonal moves "
            "(eight neighbours; the same reasoning holds). (3) Count the number of distinct increasing paths of maximum length."
        ),
        "complexity": {"time": "O(m * n)", "space": "O(m * n)"},
        "similar": ["number-of-islands", "pacific-atlantic-water-flow", "course-schedule"],
    },
    {
        "id": "edit-distance",
        "title": "Edit Distance",
        "difficulty": "Medium",
        "pattern": "2-D Dynamic Programming",
        "tags": ["String", "Dynamic Programming"],
        "companies": {"google": 3, "apple": 2, "meta": 2, "amazon": 3, "microsoft": 3},
        "description": (
            "Given two strings `word1` and `word2`, return the minimum number of single-character edits needed to turn `word1` into "
            "`word2`. An edit is one of:\n\n"
            "- insert a character\n"
            "- delete a character\n"
            "- replace a character with another\n\n"
            "This value is also known as the Levenshtein distance."
        ),
        "examples": [
            {"input": "word1 = \"horse\", word2 = \"ros\"", "output": "3",
             "explanation": "horse -> rorse (replace h with r) -> rose (delete r) -> ros (delete e)."},
            {"input": "word1 = \"intention\", word2 = \"execution\"", "output": "5"},
            {"input": "word1 = \"\", word2 = \"abc\"", "output": "3", "explanation": "Insert all three characters."},
        ],
        "constraints": ["0 <= word1.length, word2.length <= 500", "Lowercase English letters only."],
        "hints": [
            "Turning an empty string into a string of length k costs k inserts; the reverse costs k deletes. Those are your base cases.",
            "Let dp[i][j] be the distance between word1[:i] and word2[:j]. If the last characters match, dp[i][j] = dp[i-1][j-1]. Otherwise one edit plus the best of the three smaller problems.",
            "dp[i][j] = 1 + min(dp[i-1][j] (delete), dp[i][j-1] (insert), dp[i-1][j-1] (replace)). Two rows of memory are enough.",
        ],
        "function": "minDistance",
        "signature": "def minDistance(self, word1: str, word2: str) -> int:",
        "arg_types": {"word1": "str", "word2": "str"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"word1": "horse", "word2": "ros"}, "output": 3},
            {"input": {"word1": "intention", "word2": "execution"}, "output": 5},
            {"input": {"word1": "", "word2": "abc"}, "output": 3},
            {"input": {"word1": "abc", "word2": ""}, "output": 3},
            {"input": {"word1": "same", "word2": "same"}, "output": 0},
            {"input": {"word1": "a", "word2": "b"}, "output": 1},
            {"input": {"word1": "kitten", "word2": "sitting"}, "output": 3},
            {"input": {"word1": "a" * 500, "word2": "b" * 500}, "output": 500},
            {"input": {"word1": "ab" * 250, "word2": "ba" * 250}, "output": 2},
            {"input": {"word1": "abcdefghij" * 50, "word2": "abcdefghij" * 50}, "output": 0},
        ],
        "solution": (
            "class Solution:\n"
            "    def minDistance(self, word1: str, word2: str) -> int:\n"
            "        m, n = len(word1), len(word2)\n"
            "        prev = list(range(n + 1))   # distance from \"\" to word2[:j] is j inserts\n"
            "        for i in range(1, m + 1):\n"
            "            cur = [i] + [0] * n      # distance from word1[:i] to \"\" is i deletes\n"
            "            for j in range(1, n + 1):\n"
            "                if word1[i - 1] == word2[j - 1]:\n"
            "                    cur[j] = prev[j - 1]\n"
            "                else:\n"
            "                    cur[j] = 1 + min(prev[j - 1],   # replace\n"
            "                                     prev[j],       # delete word1[i-1]\n"
            "                                     cur[j - 1])    # insert word2[j-1]\n"
            "            prev = cur\n"
            "        return prev[n]\n"
        ),
        "approach": (
            "**Key insight: look at the last characters of the two prefixes. Either they already match (free), or exactly one edit "
            "fixes the mismatch and reduces to a strictly smaller pair of prefixes.**\n\n"
            "Let `dp[i][j]` be the edit distance between `word1[:i]` and `word2[:j]`. Base cases: `dp[i][0] = i`, `dp[0][j] = j`. Then\n\n"
            "- if `word1[i-1] == word2[j-1]`: `dp[i][j] = dp[i-1][j-1]`\n"
            "- else: `dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])` for replace, delete and insert respectively.\n\n"
            "**Why it is correct:** in any optimal edit script, consider what happens to the last character of `word1[:i]`: it is kept and "
            "matched (only possible if the characters are equal), replaced, deleted, or a character is inserted after it to match "
            "`word2[j-1]`. Those four cases are exhaustive and each reduces to a subproblem already solved optimally.\n\n"
            "**Space optimisation:** row `i` only reads row `i-1` and the current row, so two 1-D arrays (or one array plus a saved "
            "diagonal value) give `O(min(m, n))` memory. To reconstruct the actual edits you need the full table.\n\n"
            "**Common mistakes:** forgetting that a match costs 0 and taking `1 + dp[i-1][j-1]` regardless; swapping the meaning of "
            "insert and delete (harmless for the count, confusing when reconstructing); off-by-one between string indices and table indices.\n\n"
            "**Interview follow-ups:** (1) Only insert and delete allowed (then distance = `m + n - 2 * LCS`). "
            "(2) Weighted operations or a cheap adjacent-swap operation (Damerau-Levenshtein, adds a `dp[i-2][j-2]` term). "
            "(3) Early exit when the distance is known to exceed a threshold `k` (band of width `2k+1` around the diagonal, `O(k * min(m, n))`)."
        ),
        "complexity": {"time": "O(m * n)", "space": "O(min(m, n))"},
        "similar": ["longest-common-subsequence", "one-edit-distance", "delete-operation-for-two-strings"],
    },
    {
        "id": "distinct-subsequences",
        "title": "Distinct Subsequences",
        "difficulty": "Hard",
        "pattern": "2-D Dynamic Programming",
        "tags": ["String", "Dynamic Programming"],
        "companies": {"google": 1, "amazon": 1},
        "description": (
            "Given two strings `s` and `t`, return the number of distinct ways to pick a subsequence of `s` that equals `t`. "
            "Two ways are different if they use a different set of positions in `s`, even when the chosen characters look identical.\n\n"
            "The answer fits in a 32-bit signed integer."
        ),
        "examples": [
            {"input": "s = \"rabbbit\", t = \"rabbit\"", "output": "3",
             "explanation": "Drop any one of the three b's in \"rabbbit\": three different position sets."},
            {"input": "s = \"babgbag\", t = \"bag\"", "output": "5"},
            {"input": "s = \"abc\", t = \"\"", "output": "1", "explanation": "The empty subsequence can be picked in exactly one way."},
        ],
        "constraints": ["0 <= s.length, t.length <= 1000", "Both strings consist of English letters."],
        "hints": [
            "For each character of s decide: skip it, or use it to match the next needed character of t (only if they are equal).",
            "dp[i][j] = number of ways s[:i] can produce t[:j]. Skipping s[i-1] gives dp[i-1][j]; using it (when s[i-1] == t[j-1]) adds dp[i-1][j-1].",
            "Only the previous row is needed. With a single array, iterate j from high to low so dp[j-1] is still the previous row's value.",
        ],
        "function": "numDistinct",
        "signature": "def numDistinct(self, s: str, t: str) -> int:",
        "arg_types": {"s": "str", "t": "str"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"s": "rabbbit", "t": "rabbit"}, "output": 3},
            {"input": {"s": "babgbag", "t": "bag"}, "output": 5},
            {"input": {"s": "abc", "t": ""}, "output": 1},
            {"input": {"s": "", "t": "a"}, "output": 0},
            {"input": {"s": "aaa", "t": "a"}, "output": 3},
            {"input": {"s": "abc", "t": "abcd"}, "output": 0},
            {"input": {"s": "ab" * 300, "t": "ab"}, "output": 45150},
            {"input": {"s": "a" * 500, "t": "a" * 250}, "output": math.comb(500, 250)},
            {"input": {"s": "abcdefghij" * 60, "t": "xyz"}, "output": 0},
        ],
        "solution": (
            "class Solution:\n"
            "    def numDistinct(self, s: str, t: str) -> int:\n"
            "        n = len(t)\n"
            "        if n > len(s):\n"
            "            return 0\n"
            "        dp = [0] * (n + 1)   # dp[j] = ways to form t[:j] from the prefix of s seen so far\n"
            "        dp[0] = 1            # the empty target is formed exactly once\n"
            "        for ch in s:\n"
            "            for j in range(n, 0, -1):   # downward so dp[j-1] is still from the previous prefix\n"
            "                if t[j - 1] == ch:\n"
            "                    dp[j] += dp[j - 1]\n"
            "        return dp[n]\n"
        ),
        "approach": (
            "**Key insight: scan `s` once; each character is either skipped or consumed to match the next character of `t`. "
            "Counting both branches gives the number of position sets.**\n\n"
            "Let `dp[i][j]` be the number of ways `s[:i]` produces `t[:j]`. Base cases: `dp[i][0] = 1` (empty target, one way) and "
            "`dp[0][j] = 0` for `j > 0`. The recurrence:\n\n"
            "`dp[i][j] = dp[i-1][j] + (dp[i-1][j-1] if s[i-1] == t[j-1] else 0)`\n\n"
            "The first term skips `s[i-1]`; the second uses it as the match for `t[j-1]`. The answer is `dp[len(s)][len(t)]`.\n\n"
            "**Why it is correct:** every valid position set either includes index `i-1` or it does not, and those two families are "
            "disjoint and exhaustive. Because we count position sets rather than resulting strings, identical characters at different "
            "indices are correctly counted separately.\n\n"
            "**Space optimisation:** row `i` reads row `i-1` at columns `j` and `j-1`. Iterating `j` downward over one array means "
            "`dp[j-1]` has not yet been overwritten for the current `i`, so a single array of length `len(t)+1` suffices. "
            "Iterating upward would let a character of `s` match several characters of `t`, which is wrong.\n\n"
            "**Common mistakes:** iterating `j` upward with the 1-D array; initialising `dp[0][0] = 0`; recomputing with exponential "
            "backtracking because the branching looks like a subset enumeration.\n\n"
            "**Interview follow-ups:** (1) Return the count modulo `10^9 + 7` when the strings are long. (2) Count distinct subsequences "
            "of `s` (no target): a different recurrence that subtracts the last occurrence contribution. (3) Early termination when "
            "the remaining length of `s` is shorter than what `t` still needs."
        ),
        "complexity": {"time": "O(len(s) * len(t))", "space": "O(len(t))"},
        "similar": ["longest-common-subsequence", "interleaving-string", "edit-distance"],
    },
    {
        "id": "burst-balloons",
        "title": "Burst Balloons",
        "difficulty": "Hard",
        "pattern": "2-D Dynamic Programming",
        "tags": ["Array", "Dynamic Programming", "Interval DP"],
        "companies": {"google": 2, "amazon": 1, "microsoft": 1},
        "description": (
            "You have `n` balloons in a row; balloon `i` is labelled `nums[i]`. Burst them one at a time. Bursting balloon `i` earns "
            "`nums[left] * nums[i] * nums[right]` coins, where `left` and `right` are the balloons currently adjacent to `i` (the "
            "original neighbours may already be gone). After it bursts, `left` and `right` become adjacent to each other.\n\n"
            "Treat the positions just outside the row as balloons labelled `1` that never burst. Return the maximum coins you can collect."
        ),
        "examples": [
            {"input": "nums = [3,1,5,8]", "output": "167",
             "explanation": "Burst 1 (3*1*5 = 15), then 5 (3*5*8 = 120), then 3 (1*3*8 = 24), then 8 (1*8*1 = 8). Total 167."},
            {"input": "nums = [1,5]", "output": "10", "explanation": "Burst 1 first (1*1*5 = 5), then 5 (1*5*1 = 5)."},
            {"input": "nums = [1,2,3]", "output": "12", "explanation": "Burst 2 (1*2*3 = 6), then 1 (1*1*3 = 3), then 3 (1*3*1 = 3)."},
        ],
        "constraints": ["1 <= nums.length <= 300", "0 <= nums[i] <= 100"],
        "hints": [
            "Thinking about which balloon to burst first is hard because its neighbours keep changing. Think about which balloon in a range is burst LAST instead.",
            "If balloon k is the last one burst in the open range (i, j), then at that moment its neighbours are exactly i and j, and the two sides (i, k) and (k, j) were solved independently before.",
            "Pad nums with a 1 on each end. dp[i][j] = max over i < k < j of nums[i]*nums[k]*nums[j] + dp[i][k] + dp[k][j]. Fill by increasing range length; answer is dp[0][n+1].",
        ],
        "function": "maxCoins",
        "signature": "def maxCoins(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [3, 1, 5, 8]}, "output": 167},
            {"input": {"nums": [1, 5]}, "output": 10},
            {"input": {"nums": [1, 2, 3]}, "output": 12},
            {"input": {"nums": [7]}, "output": 7},
            {"input": {"nums": []}, "output": 0},
            {"input": {"nums": [0, 0, 0]}, "output": 0},
            {"input": {"nums": [9, 76, 64, 21]}, "output": 116718},
            {"input": {"nums": [(i * 37) % 100 + 1 for i in range(120)]}, "output": 45078732},
        ],
        "solution": (
            "class Solution:\n"
            "    def maxCoins(self, nums: List[int]) -> int:\n"
            "        arr = [1] + nums + [1]\n"
            "        n = len(arr)\n"
            "        # dp[i][j] = max coins from bursting every balloon strictly between i and j\n"
            "        dp = [[0] * n for _ in range(n)]\n"
            "        for length in range(2, n):            # distance j - i\n"
            "            for i in range(0, n - length):\n"
            "                j = i + length\n"
            "                best = 0\n"
            "                for k in range(i + 1, j):     # k is the LAST balloon burst in (i, j)\n"
            "                    best = max(best, arr[i] * arr[k] * arr[j] + dp[i][k] + dp[k][j])\n"
            "                dp[i][j] = best\n"
            "        return dp[0][n - 1]\n"
        ),
        "approach": (
            "**Key insight: reverse the question. Instead of asking which balloon to burst first (its neighbours depend on history), "
            "ask which balloon in a range is burst last. At that moment its neighbours are the fixed boundaries of the range.**\n\n"
            "Pad the array with sentinels `1` at both ends. Define `dp[i][j]` as the maximum coins from bursting every balloon strictly "
            "between indices `i` and `j` (exclusive), with `i` and `j` still present. If `k` is the last balloon burst in that open range, "
            "it earns `arr[i] * arr[k] * arr[j]`, and the two sub-ranges `(i, k)` and `(k, j)` are independent because `k` separates them "
            "until the very end:\n\n"
            "`dp[i][j] = max over i < k < j of arr[i] * arr[k] * arr[j] + dp[i][k] + dp[k][j]`\n\n"
            "Fill by increasing `j - i`; the answer is `dp[0][n+1]`.\n\n"
            "**Why it is correct:** every bursting order has a last balloon in each range, so the maximum over `k` is exhaustive. "
            "The sub-ranges really are independent: nothing inside `(i, k)` ever touches anything inside `(k, j)` while `k` is standing.\n\n"
            "**Space:** this interval DP genuinely needs the `O(n^2)` table; there is no row-by-row reduction because `dp[i][j]` reads "
            "entries at arbitrary distances. A top-down memoized recursion over `(i, j)` has the same complexity and is often easier to "
            "explain in an interview.\n\n"
            "**Common mistakes:** choosing the first balloon instead of the last; using the original neighbours `nums[k-1]` and "
            "`nums[k+1]` instead of the range boundaries; forgetting the sentinels (zeros in `nums` are fine, but the ends must be 1).\n\n"
            "**Interview follow-ups:** (1) Minimum Cost to Merge Stones and Matrix Chain Multiplication share the same 'pick the last "
            "split point' structure. (2) Strange Printer and Remove Boxes are harder interval DPs. (3) Return the bursting order "
            "(store the argmax `k` per range and recurse)."
        ),
        "complexity": {"time": "O(n^3)", "space": "O(n^2)"},
        "similar": ["minimum-cost-tree-from-leaf-values", "strange-printer", "matrix-chain-multiplication"],
    },
    {
        "id": "regular-expression-matching",
        "title": "Regular Expression Matching",
        "difficulty": "Hard",
        "pattern": "2-D Dynamic Programming",
        "tags": ["String", "Dynamic Programming", "Recursion"],
        "companies": {"google": 3, "apple": 2, "meta": 4, "amazon": 2, "microsoft": 2},
        "description": (
            "Implement a matcher for a tiny regular-expression dialect. Given a string `s` and a pattern `p`, decide whether `p` matches "
            "**the entire** string `s`. The pattern may contain:\n\n"
            "- lowercase letters, which match themselves\n"
            "- `.`, which matches any single character\n"
            "- `*`, which means 'zero or more of the preceding element'\n\n"
            "`*` always follows a letter or a `.`. Return `true` for a full match, `false` otherwise."
        ),
        "examples": [
            {"input": "s = \"aa\", p = \"a\"", "output": "false", "explanation": "The pattern matches only one character."},
            {"input": "s = \"aa\", p = \"a*\"", "output": "true", "explanation": "a* can expand to two a's."},
            {"input": "s = \"aab\", p = \"c*a*b\"", "output": "true", "explanation": "c* matches nothing, a* matches aa, b matches b."},
        ],
        "constraints": ["0 <= s.length <= 20", "0 <= p.length <= 20", "s contains only lowercase letters; p contains lowercase letters, '.' and '*'.", "Every '*' has a valid preceding element."],
        "hints": [
            "A single character of the pattern matches s[i] if it is equal to it or is a dot. The hard part is '*'.",
            "When you see x* in the pattern, you have two choices: skip the pair entirely (zero occurrences), or, if x matches the current character, consume that character and stay on the same x*.",
            "dp[i][j] = does s[i:] match p[j:]. If p[j+1] == '*': dp[i][j] = dp[i][j+2] or (first_matches and dp[i+1][j]). Otherwise dp[i][j] = first_matches and dp[i+1][j+1]. Base case dp[len(s)][len(p)] = True.",
        ],
        "function": "isMatch",
        "signature": "def isMatch(self, s: str, p: str) -> bool:",
        "arg_types": {"s": "str", "p": "str"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"s": "aa", "p": "a"}, "output": False},
            {"input": {"s": "aa", "p": "a*"}, "output": True},
            {"input": {"s": "aab", "p": "c*a*b"}, "output": True},
            {"input": {"s": "ab", "p": ".*"}, "output": True},
            {"input": {"s": "mississippi", "p": "mis*is*p*."}, "output": False},
            {"input": {"s": "", "p": "a*"}, "output": True},
            {"input": {"s": "", "p": ""}, "output": True},
            {"input": {"s": "a", "p": ""}, "output": False},
            {"input": {"s": "ab", "p": ".*c"}, "output": False},
            {"input": {"s": "aaa", "p": "ab*a*c*a"}, "output": True},
            {"input": {"s": "a" * 500, "p": "a*" * 250}, "output": True},
            {"input": {"s": "a" * 400, "p": "a*" * 100 + "b"}, "output": False},
            {"input": {"s": "ab" * 300, "p": ".*"}, "output": True},
        ],
        "solution": (
            "class Solution:\n"
            "    def isMatch(self, s: str, p: str) -> bool:\n"
            "        m, n = len(s), len(p)\n"
            "        # dp[i][j] = True if s[i:] matches p[j:]\n"
            "        dp = [[False] * (n + 1) for _ in range(m + 1)]\n"
            "        dp[m][n] = True\n"
            "        for i in range(m, -1, -1):\n"
            "            for j in range(n - 1, -1, -1):\n"
            "                first = i < m and (p[j] == s[i] or p[j] == '.')\n"
            "                if j + 1 < n and p[j + 1] == '*':\n"
            "                    # zero copies of p[j], or one more copy consuming s[i]\n"
            "                    dp[i][j] = dp[i][j + 2] or (first and dp[i + 1][j])\n"
            "                else:\n"
            "                    dp[i][j] = first and dp[i + 1][j + 1]\n"
            "        return dp[0][0]\n"
        ),
        "approach": (
            "**Key insight: a star always applies to the element before it, so read the pattern in units of one element plus an optional "
            "star. For `x*` there are only two choices at any point: use zero copies, or match one more character and stay on `x*`.**\n\n"
            "Define `dp[i][j]` as 'does `s[i:]` match `p[j:]`'. Let `first = i < len(s) and (p[j] == s[i] or p[j] == '.')`.\n\n"
            "- If `p[j+1] == '*'`: `dp[i][j] = dp[i][j+2] or (first and dp[i+1][j])`\n"
            "- Otherwise: `dp[i][j] = first and dp[i+1][j+1]`\n\n"
            "Base case `dp[len(s)][len(p)] = true`; every other `dp[i][len(p)]` is false (pattern exhausted, string not). Fill from the "
            "bottom-right and read `dp[0][0]`. A top-down memoized recursion over `(i, j)` is the same algorithm and is often what people "
            "write first.\n\n"
            "**Why it is correct:** `x*` matches some count `c >= 0` of characters. `c = 0` is the first branch. For `c >= 1` the first "
            "character must match `x` and the remaining `c-1` copies are handled by recursing on the same pattern position, so all counts are "
            "covered without enumerating them. The non-star case is forced.\n\n"
            "**Space:** row `i` depends only on row `i+1`, so two rows of length `n+1` suffice. The full table is kept here for clarity.\n\n"
            "**Common mistakes:** handling the empty string as a special case instead of letting `first` be false when `i == len(s)`; "
            "treating `.*` as a special token rather than `.` followed by `*`; letting `*` consume greedily without the zero-copy branch "
            "(fails `aab` vs `c*a*b`); and the pure recursive solution without memoization, which is exponential on patterns like `a*a*a*...b`.\n\n"
            "**Interview follow-ups:** (1) Wildcard Matching (`?` and `*` where `*` matches any sequence) has a very similar table. "
            "(2) Add `+` (one or more) by rewriting `x+` as `xx*`. (3) Compile the pattern to an NFA and simulate it for a streaming input."
        ),
        "complexity": {"time": "O(m * n)", "space": "O(m * n)"},
        "similar": ["wildcard-matching", "edit-distance", "interleaving-string"],
    },
    {
        "id": "minimum-path-sum",
        "title": "Minimum Path Sum",
        "difficulty": "Medium",
        "pattern": "2-D Dynamic Programming",
        "tags": ["Array", "Matrix", "Dynamic Programming"],
        "companies": {"google": 2, "apple": 2, "meta": 1, "amazon": 3, "microsoft": 1},
        "description": (
            "Given an `m x n` grid of non-negative integers, find a path from the top-left cell to the bottom-right cell that "
            "**minimises the sum** of the numbers visited. You may move only right or down.\n\n"
            "Return that minimum sum."
        ),
        "examples": [
            {"input": "grid = [[1,3,1],[1,5,1],[4,2,1]]", "output": "7", "explanation": "1 -> 3 -> 1 -> 1 -> 1 sums to 7."},
            {"input": "grid = [[1,2,3],[4,5,6]]", "output": "12", "explanation": "1 -> 2 -> 3 -> 6."},
            {"input": "grid = [[5]]", "output": "5"},
        ],
        "constraints": ["1 <= m, n <= 200", "0 <= grid[i][j] <= 200"],
        "hints": [
            "Cells in the first row can only be reached from the left; cells in the first column only from above.",
            "Any other cell is reached from above or from the left; its best cost is its own value plus the cheaper of those two.",
            "Reuse one row of length n: when processing row i left to right, row[j] still holds the cost from the cell above and row[j-1] the new cost from the left.",
        ],
        "function": "minPathSum",
        "signature": "def minPathSum(self, grid: List[List[int]]) -> int:",
        "arg_types": {"grid": "List[List[int]]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"grid": [[1, 3, 1], [1, 5, 1], [4, 2, 1]]}, "output": 7},
            {"input": {"grid": [[1, 2, 3], [4, 5, 6]]}, "output": 12},
            {"input": {"grid": [[5]]}, "output": 5},
            {"input": {"grid": [[1, 2, 3, 4]]}, "output": 10},
            {"input": {"grid": [[1], [2], [3]]}, "output": 6},
            {"input": {"grid": [[0, 0], [0, 0]]}, "output": 0},
            {"input": {"grid": [[9, 1, 1], [9, 9, 1], [9, 9, 1]]}, "output": 13},
            {"input": {"grid": [[1] * 200 for _ in range(200)]}, "output": 399},
            {"input": {"grid": [[(i + j) % 7 for j in range(200)] for i in range(200)]}, "output": 1197},
        ],
        "solution": (
            "class Solution:\n"
            "    def minPathSum(self, grid: List[List[int]]) -> int:\n"
            "        m, n = len(grid), len(grid[0])\n"
            "        row = [0] * n\n"
            "        row[0] = grid[0][0]\n"
            "        for j in range(1, n):\n"
            "            row[j] = row[j - 1] + grid[0][j]\n"
            "        for i in range(1, m):\n"
            "            row[0] += grid[i][0]\n"
            "            for j in range(1, n):\n"
            "                row[j] = grid[i][j] + min(row[j], row[j - 1])   # above vs left\n"
            "        return row[n - 1]\n"
        ),
        "approach": (
            "**Key insight: because moves only go right or down, the cheapest way into a cell is its value plus the cheaper of the two "
            "cells that can lead into it.**\n\n"
            "Let `dp[i][j]` be the minimum sum of a path from `(0,0)` to `(i,j)`. The first row and column are prefix sums (only one way "
            "in). For every other cell: `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`. The answer is `dp[m-1][n-1]`.\n\n"
            "**Why it is correct:** the last step into `(i,j)` comes from above or from the left; the optimal path to `(i,j)` must use an "
            "optimal path to whichever of those it passes through (cutting and pasting a cheaper prefix would only reduce the total). "
            "Since the grid is a DAG under these moves, filling row by row processes every predecessor first.\n\n"
            "**Space optimisation:** when sweeping row `i` left to right over a single array, `row[j]` still contains `dp[i-1][j]` (above) "
            "and `row[j-1]` already contains `dp[i][j-1]` (left), so `row[j] = grid[i][j] + min(row[j], row[j-1])` works in place. "
            "Modifying `grid` itself is another O(1)-extra-space option, but ask before destroying the input.\n\n"
            "**Common mistakes:** initialising `row` to all zeros and then taking `min` with a fake 0 on the first row/column; "
            "treating the problem as a shortest path that allows moving up or left (then you need Dijkstra, not this DP).\n\n"
            "**Interview follow-ups:** (1) Allow all four directions (Dijkstra on the grid, `O(mn log(mn))`). (2) Return the actual path "
            "(walk backwards choosing the predecessor that produced the minimum). (3) Maximise instead of minimise, or count the number of "
            "minimum-sum paths (carry a second table)."
        ),
        "complexity": {"time": "O(m * n)", "space": "O(n)"},
        "similar": ["unique-paths", "dungeon-game", "triangle"],
    },
]
