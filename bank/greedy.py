"""Greedy: problems where a local choice provably never hurts."""

PROBLEMS = [
    {
        "id": "jump-game",
        "title": "Jump Game",
        "difficulty": "Medium",
        "pattern": "Greedy",
        "tags": ["Greedy", "Array", "Dynamic Programming"],
        "companies": {"google": 2, "apple": 2, "meta": 1, "amazon": 3, "microsoft": 2},
        "description": (
            "You start at index `0` of an integer array `nums`. The value at each index is the **maximum** number of "
            "positions you may jump forward from there (you can also jump fewer).\n\n"
            "Return `true` if you can reach the last index, otherwise `false`."
        ),
        "examples": [
            {"input": "nums = [2,3,1,1,4]", "output": "true", "explanation": "Jump 1 to index 1, then 3 to the end."},
            {"input": "nums = [3,2,1,0,4]", "output": "false", "explanation": "Every route lands on index 3, whose value 0 traps you."},
        ],
        "constraints": ["1 <= nums.length <= 10^4", "0 <= nums[i] <= 10^5"],
        "hints": [
            "You do not need to know which jumps to take, only how far it is possible to get.",
            "Scan left to right keeping `farthest`, the largest index reachable so far. If the current index is beyond `farthest` you are stuck.",
            "Equivalent backwards view: keep the leftmost 'good' index that can reach the end and move it left whenever i + nums[i] reaches it.",
        ],
        "function": "canJump",
        "signature": "def canJump(self, nums: List[int]) -> bool:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [2, 3, 1, 1, 4]}, "output": True},
            {"input": {"nums": [3, 2, 1, 0, 4]}, "output": False},
            {"input": {"nums": [0]}, "output": True},
            {"input": {"nums": [1, 0]}, "output": True},
            {"input": {"nums": [0, 1]}, "output": False},
            {"input": {"nums": [2, 0, 0]}, "output": True},
            {"input": {"nums": [2, 0] * 2500}, "output": True},
            {"input": {"nums": [1] * 2500 + [0] + [1] * 2499}, "output": False},
            {"input": {"nums": [3] * 3000 + [0, 0, 0] + [1] * 5}, "output": False},
        ],
        "solution": (
            "class Solution:\n"
            "    def canJump(self, nums: List[int]) -> bool:\n"
            "        farthest = 0\n"
            "        for i, step in enumerate(nums):\n"
            "            if i > farthest:\n"
            "                return False  # this index is unreachable, and so is everything after it\n"
            "            farthest = max(farthest, i + step)\n"
            "        return True\n"
        ),
        "approach": (
            "**Reachability is a prefix: if index `i` is reachable then so is every index before it, so a single "
            "number, the farthest reachable index, captures the whole state.** Walk left to right. If `i` exceeds "
            "`farthest`, no earlier index could jump to `i` and nothing beyond it is reachable either. Otherwise "
            "update `farthest = max(farthest, i + nums[i])`. Surviving the loop means the last index is reachable.\n\n"
            "**Why it works:** from any reachable index `j <= farthest` you may jump a shorter distance, so the "
            "reachable set is exactly `[0, farthest]`; the invariant is maintained by each update. The DP view "
            "(`good[i] = any(good[j] for j reaching i)`) is O(n^2); the greedy collapses it because only the "
            "maximum matters.\n\n"
            "**Common mistakes:** depth-first search over all jumps (exponential), checking `i >= farthest` instead "
            "of `>` (fails on `[0]`), and returning early when `farthest >= n-1` without first checking the current "
            "index is reachable (fine as an optimisation, but order matters).\n\n"
            "**Interview follow-ups:** Minimum number of jumps? (Jump Game II: BFS layers via the same `farthest`.) "
            "Jumps that can go left or right, or a fixed-size jump like `nums[i]` exactly? (Jump Game III: BFS/DFS "
            "with a visited set.) Return one valid sequence of jumps? (Backwards: from the end, greedily pick the "
            "leftmost index that reaches the current target.)"
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["jump-game-ii", "jump-game-iii", "gas-station"],
    },
    {
        "id": "jump-game-ii",
        "title": "Jump Game II",
        "difficulty": "Medium",
        "pattern": "Greedy",
        "tags": ["Greedy", "Array", "BFS"],
        "companies": {"google": 2, "apple": 1, "amazon": 2, "microsoft": 1},
        "description": (
            "Same movement rule as Jump Game: from index `i` you may jump forward up to `nums[i]` positions. It is "
            "guaranteed that the last index is reachable.\n\n"
            "Return the **minimum** number of jumps needed to go from index `0` to the last index."
        ),
        "examples": [
            {"input": "nums = [2,3,1,1,4]", "output": "2", "explanation": "Index 0 -> 1 -> 4."},
            {"input": "nums = [2,3,0,1,4]", "output": "2"},
            {"input": "nums = [0]", "output": "0", "explanation": "Already at the last index."},
        ],
        "constraints": ["1 <= nums.length <= 10^4", "0 <= nums[i] <= 1000", "The last index is always reachable."],
        "hints": [
            "Think of it as BFS where level k is the set of indices reachable in exactly k jumps. Those indices form a contiguous window.",
            "Keep the right edge of the current window `cur_end` and the farthest index any element in the window can reach. When i hits cur_end, take one jump and move the window to `farthest`.",
            "Stop scanning at n-2: once the window covers the last index no further jump is needed.",
        ],
        "function": "jump",
        "signature": "def jump(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [2, 3, 1, 1, 4]}, "output": 2},
            {"input": {"nums": [2, 3, 0, 1, 4]}, "output": 2},
            {"input": {"nums": [0]}, "output": 0},
            {"input": {"nums": [1, 1, 1, 1]}, "output": 3},
            {"input": {"nums": [1, 2, 3]}, "output": 2},
            {"input": {"nums": [2] * 5000}, "output": 2500},
            {"input": {"nums": [(i * 13) % 4 + 1 for i in range(5000)]}, "output": 1251},
        ],
        "solution": (
            "class Solution:\n"
            "    def jump(self, nums: List[int]) -> int:\n"
            "        jumps = 0\n"
            "        cur_end = 0   # right edge of the indices reachable with `jumps` jumps\n"
            "        farthest = 0  # right edge reachable with one more jump\n"
            "        for i in range(len(nums) - 1):\n"
            "            farthest = max(farthest, i + nums[i])\n"
            "            if i == cur_end:\n"
            "                jumps += 1\n"
            "                cur_end = farthest\n"
            "        return jumps\n"
        ),
        "approach": (
            "**Implicit BFS: the indices reachable in exactly `k` jumps form a contiguous window, so each BFS level "
            "is just an interval.** Maintain `cur_end`, the right edge of the window for the current number of jumps, "
            "and `farthest`, the maximum `i + nums[i]` seen inside that window. When the scan reaches `cur_end`, "
            "every index in the level has been examined; the next level is `(cur_end, farthest]`, so increment "
            "`jumps` and set `cur_end = farthest`.\n\n"
            "**Why it works:** BFS over indices with edges `i -> i+1..i+nums[i]` gives the minimum jump count, and "
            "because the edge set from each index is a prefix of what lies ahead, levels are intervals. Tracking "
            "only the interval's right end is therefore lossless. The loop stops at `n - 2` because reaching or "
            "covering the last index in the current window means no extra jump is needed.\n\n"
            "**Common mistakes:** iterating to `n - 1` (counts one jump too many when the last index itself is "
            "`cur_end`), the O(n^2) DP `dp[i] = 1 + min(dp[j])`, and greedily jumping to the index with the largest "
            "`nums[i]` rather than the largest reach `i + nums[i]`.\n\n"
            "**Interview follow-ups:** Return the sequence of jumps? (Record, for each level, which index produced "
            "`farthest`.) What if the last index might be unreachable? (Return -1 when `i > cur_end`, as in Jump "
            "Game.) Jumps have a cost and you want the cheapest path? (Then it is a shortest-path problem: DP or "
            "Dijkstra, the interval trick no longer applies.)"
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["jump-game", "minimum-number-of-refueling-stops", "video-stitching"],
    },
    {
        "id": "gas-station",
        "title": "Gas Station",
        "difficulty": "Medium",
        "pattern": "Greedy",
        "tags": ["Greedy", "Array"],
        "companies": {"google": 2, "apple": 1, "amazon": 3, "microsoft": 2},
        "description": (
            "There are `n` gas stations on a circular route. Station `i` offers `gas[i]` units of fuel, and driving "
            "from station `i` to station `i + 1` consumes `cost[i]` units. You start with an empty tank at some "
            "station, fill up there, and drive clockwise.\n\n"
            "Return the index of the starting station from which you can complete one full loop, or `-1` if it is "
            "impossible. If a solution exists it is guaranteed to be unique."
        ),
        "examples": [
            {"input": "gas = [1,2,3,4,5], cost = [3,4,5,1,2]", "output": "3",
             "explanation": "From station 3: tank 4 -> 3 -> 6 -> 4 -> 3 -> 3, never negative. Any earlier start runs dry."},
            {"input": "gas = [2,3,4], cost = [3,4,3]", "output": "-1", "explanation": "Total gas 9 is less than total cost 10."},
        ],
        "constraints": ["n == gas.length == cost.length", "1 <= n <= 10^5", "0 <= gas[i], cost[i] <= 10^4"],
        "hints": [
            "If the total gas is at least the total cost, a valid start exists; otherwise return -1.",
            "Simulate once with a running tank. Whenever it goes negative at station i, no station between your current start and i can work either, so restart from i + 1 with an empty tank.",
            "The start that survives to the end of the single pass is the answer; no second loop is needed.",
        ],
        "function": "canCompleteCircuit",
        "signature": "def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:",
        "arg_types": {"gas": "List[int]", "cost": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"gas": [1, 2, 3, 4, 5], "cost": [3, 4, 5, 1, 2]}, "output": 3},
            {"input": {"gas": [2, 3, 4], "cost": [3, 4, 3]}, "output": -1},
            {"input": {"gas": [5], "cost": [4]}, "output": 0},
            {"input": {"gas": [5], "cost": [6]}, "output": -1},
            {"input": {"gas": [3, 1, 1], "cost": [1, 2, 2]}, "output": 0},
            {"input": {"gas": [0] * 4999 + [5000], "cost": [1] * 5000}, "output": 4999},
        ],
        "solution": (
            "class Solution:\n"
            "    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:\n"
            "        if sum(gas) < sum(cost):\n"
            "            return -1\n"
            "        start = 0\n"
            "        tank = 0\n"
            "        for i in range(len(gas)):\n"
            "            tank += gas[i] - cost[i]\n"
            "            if tank < 0:\n"
            "                start = i + 1  # no station in [start, i] can be the answer\n"
            "                tank = 0\n"
            "        return start\n"
        ),
        "approach": (
            "**Two facts make a single pass sufficient.** (1) If total gas >= total cost, some start works; "
            "otherwise none does. (2) If you start at `s` and the tank first goes negative after station `i`, then "
            "no station in `s..i` can be a valid start: starting later in that range only means arriving at `i` "
            "with less fuel (you skipped the non-negative surplus accumulated before). So the candidate start jumps "
            "to `i + 1`.\n\n"
            "Run the simulation once with `start = 0`; each time the tank dips below zero, reset it and move `start` "
            "past the failure point. Because of fact (1) the final `start` is valid: the segment from `start` to the "
            "end has non-negative running sum, and the wrap-around is covered because the total surplus is "
            "non-negative and all earlier segments had negative sums that the surplus exactly compensates.\n\n"
            "**Equivalent view:** with `diff[i] = gas[i] - cost[i]`, the answer is the index right after the minimum "
            "prefix sum; starting there makes every prefix non-negative.\n\n"
            "**Common mistakes:** trying every start (O(n^2), the large test makes that visibly slow), simulating "
            "two laps unnecessarily, and forgetting the single-station case.\n\n"
            "**Interview follow-ups:** Prove fact (2) formally. If several starts were valid, how would you return "
            "all of them? (Prefix sums: every index following a global-minimum prefix.) Driving counter-clockwise "
            "as well? (Run the same algorithm on the reversed arrays with costs shifted.) Tank capacity limit? (Then "
            "greedy breaks; it becomes a simulation per start or a sliding window problem.)"
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["jump-game", "maximum-subarray", "minimum-number-of-refueling-stops"],
    },
    {
        "id": "hand-of-straights",
        "title": "Hand of Straights",
        "difficulty": "Medium",
        "pattern": "Greedy",
        "tags": ["Greedy", "Hash Table", "Sorting", "Heap / Priority Queue"],
        "companies": {"google": 2, "amazon": 1},
        "description": (
            "You hold cards with integer values `hand`. You want to arrange **all** of them into groups of exactly "
            "`groupSize` cards, where each group consists of consecutive values (like `3,4,5`).\n\n"
            "Return `true` if such an arrangement exists, `false` otherwise."
        ),
        "examples": [
            {"input": "hand = [1,2,3,6,2,3,4,7,8], groupSize = 3", "output": "true", "explanation": "Groups [1,2,3], [2,3,4], [6,7,8]."},
            {"input": "hand = [1,2,3,4,5], groupSize = 4", "output": "false", "explanation": "5 cards cannot form groups of 4."},
        ],
        "constraints": ["1 <= hand.length <= 10^4", "0 <= hand[i] <= 10^9", "1 <= groupSize <= hand.length"],
        "hints": [
            "If the count of cards is not divisible by groupSize, fail immediately.",
            "The smallest remaining card has no choice: it must start a group. Remove that whole run of consecutive values from the counts.",
            "Count values in a hash map, iterate the distinct values in sorted order, and for each value with count c > 0 subtract c from the next groupSize values; if any of them has fewer than c, fail.",
        ],
        "function": "isNStraightHand",
        "signature": "def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:",
        "arg_types": {"hand": "List[int]", "groupSize": "int"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"hand": [1, 2, 3, 6, 2, 3, 4, 7, 8], "groupSize": 3}, "output": True},
            {"input": {"hand": [1, 2, 3, 4, 5], "groupSize": 4}, "output": False},
            {"input": {"hand": [1], "groupSize": 1}, "output": True},
            {"input": {"hand": [8, 10, 12], "groupSize": 1}, "output": True},
            {"input": {"hand": [1, 1, 2, 2, 3, 3], "groupSize": 3}, "output": True},
            {"input": {"hand": [1, 2, 4, 5], "groupSize": 2}, "output": True},
            {"input": {"hand": [1, 2, 3, 4, 5, 6], "groupSize": 4}, "output": False},
            {"input": {"hand": [(i * 7919) % 5000 for i in range(5000)], "groupSize": 5}, "output": True},
            {"input": {"hand": [i // 2 for i in range(5000)], "groupSize": 2}, "output": True},
            {"input": {"hand": [1] * 5000, "groupSize": 2}, "output": False},
        ],
        "solution": (
            "class Solution:\n"
            "    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:\n"
            "        if len(hand) % groupSize:\n"
            "            return False\n"
            "        count = Counter(hand)\n"
            "        for value in sorted(count):\n"
            "            need = count[value]\n"
            "            if need == 0:\n"
            "                continue  # already consumed by earlier groups\n"
            "            for v in range(value, value + groupSize):\n"
            "                if count[v] < need:\n"
            "                    return False\n"
            "                count[v] -= need\n"
            "        return True\n"
        ),
        "approach": (
            "**The smallest card still in hand is forced: it can only be the first card of a group.** So count the "
            "cards, visit the distinct values in increasing order, and whenever a value `v` still has `c` copies, "
            "all `c` of them must start groups `v, v+1, ..., v+groupSize-1`. Subtract `c` from each of those "
            "values; if one of them has fewer than `c` copies, no arrangement exists.\n\n"
            "**Why it works (exchange argument):** in any valid arrangement the minimum value begins its group, "
            "and groups starting at the same value are interchangeable, so taking all `c` of them at once loses "
            "nothing. After removal the remaining multiset is independent of how we labelled the groups, so the "
            "greedy choice is never regretted.\n\n"
            "Processing by distinct value (not card by card) keeps the work at O(distinct * groupSize), and the "
            "`Counter` makes `count[v]` return 0 for absent values without a special case. A min-heap over distinct "
            "values gives the same complexity and is what you would use if values arrived online.\n\n"
            "**Common mistakes:** forgetting the divisibility check, sorting the whole hand and simulating "
            "removals from a list (O(n^2)), and not skipping values whose count has already dropped to 0.\n\n"
            "**Interview follow-ups:** Values up to 10^9: does your solution depend on the value range? (No, only "
            "on the number of distinct values.) Return the groups themselves? (Emit a tuple each time you consume "
            "a run.) A variant where groups need only be consecutive *or* equal, like a rummy hand? (Then it is a "
            "DP over counts, greedy no longer suffices.) Allow jokers that fill gaps? (Track a wildcard budget.)"
        ),
        "complexity": {"time": "O(n log n)", "space": "O(n)"},
        "similar": ["divide-array-in-sets-of-k-consecutive-numbers", "split-array-into-consecutive-subsequences"],
    },
    {
        "id": "partition-labels",
        "title": "Partition Labels",
        "difficulty": "Medium",
        "pattern": "Greedy",
        "tags": ["Greedy", "String", "Hash Table", "Two Pointers"],
        "companies": {"google": 2, "meta": 2, "amazon": 3, "microsoft": 1},
        "description": (
            "Split the string `s` into as many contiguous parts as possible such that every letter appears in **at "
            "most one** part.\n\n"
            "Return the lengths of the parts in order. The parts, concatenated, must give back `s`."
        ),
        "examples": [
            {"input": "s = \"ababcbacadefegdehijhklij\"", "output": "[9,7,8]",
             "explanation": "\"ababcbaca\" | \"defegde\" | \"hijhklij\". The letter a stretches from index 0 to 8, so the first part cannot end sooner."},
            {"input": "s = \"eccbbbbdec\"", "output": "[10]", "explanation": "e and c appear at both ends, so the whole string is one part."},
        ],
        "constraints": ["1 <= s.length <= 500", "s consists of lowercase English letters."],
        "hints": [
            "A part that contains a letter must extend at least to that letter's last occurrence in s.",
            "Precompute the last index of every letter. Scan with a running `end` = max last index of letters seen in the current part.",
            "When the scan index equals `end`, the part is complete: record its length and start a new one.",
        ],
        "function": "partitionLabels",
        "signature": "def partitionLabels(self, s: str) -> List[int]:",
        "arg_types": {"s": "str"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"s": "ababcbacadefegdehijhklij"}, "output": [9, 7, 8]},
            {"input": {"s": "eccbbbbdec"}, "output": [10]},
            {"input": {"s": "a"}, "output": [1]},
            {"input": {"s": "abcdef"}, "output": [1, 1, 1, 1, 1, 1]},
            {"input": {"s": "abab"}, "output": [4]},
            {"input": {"s": "".join(c * 200 for c in "abcdefghijklmnopqrstuvwxy")}, "output": [200] * 25},
            {"input": {"s": "abcdefghijklmnopqrstuvwxyz" * 190}, "output": [4940]},
        ],
        "solution": (
            "class Solution:\n"
            "    def partitionLabels(self, s: str) -> List[int]:\n"
            "        last = {ch: i for i, ch in enumerate(s)}\n"
            "        sizes = []\n"
            "        start = end = 0\n"
            "        for i, ch in enumerate(s):\n"
            "            end = max(end, last[ch])\n"
            "            if i == end:\n"
            "                sizes.append(end - start + 1)\n"
            "                start = i + 1\n"
            "        return sizes\n"
        ),
        "approach": (
            "**Each letter forces an interval `[first, last]`, and a part boundary may only be placed where no "
            "interval crosses it.** Record every letter's last index in one pass. Then scan: `end` is the farthest "
            "last-occurrence among letters seen since the current part began. The moment the scan index `i` "
            "catches up with `end`, every letter in the part has been fully used and nothing seen so far appears "
            "later, so cutting here is safe and, because we cut at the first legal position, it yields the most parts.\n\n"
            "**Why it works:** the cut positions are exactly the indices `i` where no letter occurring at or before "
            "`i` occurs after `i`. The running maximum of last occurrences is the smallest `end` satisfying that for "
            "the current part; cutting as early as possible can only increase the number of parts (merging intervals "
            "greedily from the left). This is the same mechanism as merging overlapping intervals.\n\n"
            "**Common mistakes:** recomputing the last index inside the loop with `rfind` (O(n * 26) is fine, but "
            "O(n^2) scans are not), returning the substrings instead of their lengths, and forgetting to reset "
            "`start`.\n\n"
            "**Interview follow-ups:** Return the parts rather than the sizes. Minimise the number of parts "
            "subject to a maximum part length? (Then it is no longer greedy-trivial; think DP over cut positions.) "
            "Unicode input? (Replace the 26-slot array with a dict, which the solution already does.) Relate it to "
            "Merge Intervals."
        ),
        "complexity": {"time": "O(n)", "space": "O(1) beyond the output (at most 26 letters)"},
        "similar": ["merge-intervals", "hand-of-straights", "jump-game-ii"],
    },
    {
        "id": "valid-parenthesis-string",
        "title": "Valid Parenthesis String",
        "difficulty": "Medium",
        "pattern": "Greedy",
        "tags": ["Greedy", "String", "Stack", "Dynamic Programming"],
        "companies": {"google": 2, "meta": 3, "amazon": 2, "microsoft": 1},
        "description": (
            "A string `s` contains `'('`, `')'` and `'*'`. Each `'*'` may be interpreted as `'('`, `')'`, or an empty "
            "string. Decide whether there is some interpretation under which `s` becomes a **balanced** parenthesis "
            "string (every opening bracket closed by a later matching one, never a close without an open)."
        ),
        "examples": [
            {"input": "s = \"()\"", "output": "true"},
            {"input": "s = \"(*)\"", "output": "true", "explanation": "Treat * as empty."},
            {"input": "s = \"(*))\"", "output": "true", "explanation": "Treat * as '('."},
            {"input": "s = \")(\"", "output": "false"},
        ],
        "constraints": ["1 <= s.length <= 100", "s[i] is '(', ')' or '*'."],
        "hints": [
            "Trying all 3^k interpretations is hopeless. Track a range instead: the minimum and maximum possible number of currently open brackets.",
            "'(' adds 1 to both; ')' subtracts 1 from both; '*' subtracts 1 from the minimum and adds 1 to the maximum.",
            "If the maximum ever drops below 0 there are too many ')' and you fail. Clamp the minimum at 0 (interpret surplus * as empty). Valid iff the minimum is 0 at the end.",
        ],
        "function": "checkValidString",
        "signature": "def checkValidString(self, s: str) -> bool:",
        "arg_types": {"s": "str"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"s": "()"}, "output": True},
            {"input": {"s": "(*)"}, "output": True},
            {"input": {"s": "(*))"}, "output": True},
            {"input": {"s": ")("}, "output": False},
            {"input": {"s": "*"}, "output": True},
            {"input": {"s": "(((**"}, "output": False},
            {"input": {"s": "((*)"}, "output": True},
            {"input": {"s": "**(("}, "output": False},
            {"input": {"s": "(*" * 2500}, "output": True},
            {"input": {"s": "(" * 2000 + "*" * 1000 + ")" * 2000}, "output": True},
            {"input": {"s": "(" * 2500 + "*" * 2499}, "output": False},
        ],
        "solution": (
            "class Solution:\n"
            "    def checkValidString(self, s: str) -> bool:\n"
            "        lo = hi = 0  # min and max possible count of unmatched '(' so far\n"
            "        for ch in s:\n"
            "            if ch == '(':\n"
            "                lo += 1\n"
            "                hi += 1\n"
            "            elif ch == ')':\n"
            "                lo -= 1\n"
            "                hi -= 1\n"
            "            else:\n"
            "                lo -= 1  # '*' as ')'\n"
            "                hi += 1  # '*' as '('\n"
            "            if hi < 0:\n"
            "                return False  # too many ')' even if every '*' was '('\n"
            "            lo = max(lo, 0)  # never let the floor go negative: those '*' become empty\n"
            "        return lo == 0\n"
        ),
        "approach": (
            "**Instead of enumerating interpretations, track the set of possible open-bracket counts, which is "
            "always a contiguous range `[lo, hi]`.** A `'('` shifts the range up by 1, a `')'` shifts it down, and a "
            "`'*'` widens it by 1 on each side (it may be `'('`, `')'`, or nothing). Two checks keep it honest: if "
            "`hi < 0` even the most generous reading has an unmatched `')'`, so fail; and `lo` is clamped at 0 "
            "because a negative count is not a real state (the corresponding `'*'` are read as empty). The string "
            "is valid iff 0 is in the final range, i.e. `lo == 0`.\n\n"
            "**Why the range is contiguous:** every step maps an interval to an interval (shift or widen), and "
            "clamping at 0 keeps it an interval, so the two endpoints describe every achievable count exactly. "
            "This is the standard trick of compressing a DP over `(index, open_count)` into its reachable interval.\n\n"
            "**Alternatives to mention:** a two-pass greedy (left to right treating `*` as `(`, right to left "
            "treating `*` as `)`), or two stacks holding indices of `'('` and `'*'`, matching each `')'` with the "
            "nearest `'('` first and finally pairing leftover `'('` with `'*'` that come *after* them. The O(n^2) "
            "DP `valid[i][j]` is what you would reach for if the operators were more complicated.\n\n"
            "**Common mistakes:** returning `lo <= 0 <= hi` without clamping (then `lo` can go very negative and "
            "hide errors), forgetting the `hi < 0` early exit (fails on `\")(\"`), and backtracking over all 3^k choices.\n\n"
            "**Interview follow-ups:** Produce one concrete valid interpretation? (The two-stack method yields the "
            "assignments.) Count the number of valid interpretations? (DP on `(i, open)` with counts, O(n^2).) "
            "Multiple bracket types with wildcards? (Interval trick fails because type matters; stack-based DP.)"
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["valid-parentheses", "minimum-remove-to-make-valid-parentheses", "longest-valid-parentheses"],
    },
    {
        "id": "candy",
        "title": "Candy",
        "difficulty": "Hard",
        "pattern": "Greedy",
        "tags": ["Greedy", "Array"],
        "companies": {"google": 2, "apple": 1, "amazon": 2, "microsoft": 1},
        "description": (
            "Children stand in a line; `ratings[i]` is the rating of child `i`. You hand out candies so that every "
            "child gets **at least one**, and any child with a strictly higher rating than an immediate neighbour "
            "gets more candies than that neighbour.\n\n"
            "Return the minimum total number of candies required."
        ),
        "examples": [
            {"input": "ratings = [1,0,2]", "output": "5", "explanation": "Candies [2,1,2]."},
            {"input": "ratings = [1,2,2]", "output": "4", "explanation": "Candies [1,2,1]; equal ratings carry no constraint."},
        ],
        "constraints": ["1 <= ratings.length <= 2 * 10^4", "0 <= ratings[i] <= 2 * 10^4"],
        "hints": [
            "Each child has two independent constraints: against the left neighbour and against the right neighbour.",
            "Left-to-right pass: if ratings[i] > ratings[i-1], candies[i] = candies[i-1] + 1. This satisfies every left constraint.",
            "Right-to-left pass: if ratings[i] > ratings[i+1], candies[i] = max(candies[i], candies[i+1] + 1). The max keeps the left constraints intact.",
        ],
        "function": "candy",
        "signature": "def candy(self, ratings: List[int]) -> int:",
        "arg_types": {"ratings": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"ratings": [1, 0, 2]}, "output": 5},
            {"input": {"ratings": [1, 2, 2]}, "output": 4},
            {"input": {"ratings": [1]}, "output": 1},
            {"input": {"ratings": [1, 3, 2, 2, 1]}, "output": 7},
            {"input": {"ratings": [1, 2, 87, 87, 87, 2, 1]}, "output": 13},
            {"input": {"ratings": [5, 4, 3, 2, 1]}, "output": 15},
            {"input": {"ratings": list(range(5000))}, "output": 12502500},
            {"input": {"ratings": [i % 7 for i in range(4998)]}, "output": 19992},
            {"input": {"ratings": [1, 2] * 2500}, "output": 7500},
        ],
        "solution": (
            "class Solution:\n"
            "    def candy(self, ratings: List[int]) -> int:\n"
            "        n = len(ratings)\n"
            "        candies = [1] * n\n"
            "        for i in range(1, n):  # satisfy constraints against the left neighbour\n"
            "            if ratings[i] > ratings[i - 1]:\n"
            "                candies[i] = candies[i - 1] + 1\n"
            "        for i in range(n - 2, -1, -1):  # then against the right neighbour, never decreasing\n"
            "            if ratings[i] > ratings[i + 1]:\n"
            "                candies[i] = max(candies[i], candies[i + 1] + 1)\n"
            "        return sum(candies)\n"
        ),
        "approach": (
            "**Split the two-sided constraint into two one-sided ones and satisfy each with a greedy sweep.** Start "
            "everyone at 1 candy. A left-to-right pass enforces 'higher than the left neighbour gets more than the "
            "left neighbour' by setting `candies[i] = candies[i-1] + 1` on every ascent. A right-to-left pass enforces "
            "the mirror rule, taking `max` with the existing value so the first pass's guarantees survive.\n\n"
            "**Why the result is minimal:** after both passes every child's count equals 1 plus the length of the "
            "longest strictly monotone run ending at them from either side, which is a lower bound any valid "
            "distribution must meet (walk down the run: each step needs one more candy). Meeting a lower bound "
            "everywhere means the total is minimal.\n\n"
            "**One-pass O(1) space variant** worth describing: track the current ascending and descending run "
            "lengths and the peak; when a descent ends, add the arithmetic sums of both runs and correct the peak "
            "so it exceeds the longer side. It is fiddly, which is why the two-pass version is the one to write.\n\n"
            "**Common mistakes:** handling equal ratings as if they needed different counts, doing only one pass, "
            "and forgetting the `max` in the second pass (which can undo the first pass on a peak).\n\n"
            "**Interview follow-ups:** Do it in O(1) extra space (the slope-counting pass). Children in a circle? "
            "(Rotate so the minimum rating is at index 0; then the circular constraint between the ends is "
            "automatically satisfied.) Return the distribution, not the sum? (Already available in `candies`.)"
        ),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "similar": ["trapping-rain-water", "product-of-array-except-self"],
    },
    {
        "id": "boats-to-save-people",
        "title": "Boats to Save People",
        "difficulty": "Medium",
        "pattern": "Greedy",
        "tags": ["Greedy", "Two Pointers", "Sorting"],
        "companies": {"google": 2, "meta": 1, "amazon": 2},
        "description": (
            "`people[i]` is the weight of person `i`. Each boat carries at most **two** people and at most `limit` "
            "total weight; every individual weighs no more than `limit`.\n\n"
            "Return the minimum number of boats needed to carry everyone."
        ),
        "examples": [
            {"input": "people = [1,2], limit = 3", "output": "1"},
            {"input": "people = [3,2,2,1], limit = 3", "output": "3", "explanation": "(1,2), (2), (3)."},
            {"input": "people = [3,5,3,4], limit = 5", "output": "4", "explanation": "No pair fits, so one boat each."},
        ],
        "constraints": ["1 <= people.length <= 5 * 10^4", "1 <= people[i] <= limit <= 3 * 10^4"],
        "hints": [
            "Sort. The heaviest person needs a boat no matter what; the only question is who, if anyone, rides along.",
            "Pair the heaviest with the lightest when they fit, otherwise the heaviest goes alone. Two pointers from both ends.",
            "Every iteration launches exactly one boat and retires the heaviest remaining person.",
        ],
        "function": "numRescueBoats",
        "signature": "def numRescueBoats(self, people: List[int], limit: int) -> int:",
        "arg_types": {"people": "List[int]", "limit": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"people": [1, 2], "limit": 3}, "output": 1},
            {"input": {"people": [3, 2, 2, 1], "limit": 3}, "output": 3},
            {"input": {"people": [3, 5, 3, 4], "limit": 5}, "output": 4},
            {"input": {"people": [5], "limit": 5}, "output": 1},
            {"input": {"people": [1, 1, 1, 1], "limit": 3}, "output": 2},
            {"input": {"people": [2, 2, 2, 2, 2, 2], "limit": 4}, "output": 3},
            {"input": {"people": [i % 100 + 1 for i in range(5000)], "limit": 101}, "output": 2500},
            {"input": {"people": [3] * 5000, "limit": 3}, "output": 5000},
        ],
        "solution": (
            "class Solution:\n"
            "    def numRescueBoats(self, people: List[int], limit: int) -> int:\n"
            "        people.sort()\n"
            "        light, heavy = 0, len(people) - 1\n"
            "        boats = 0\n"
            "        while light <= heavy:\n"
            "            if people[light] + people[heavy] <= limit:\n"
            "                light += 1  # the lightest rides with the heaviest\n"
            "            heavy -= 1      # the heaviest always leaves on this boat\n"
            "            boats += 1\n"
            "        return boats\n"
        ),
        "complexity": {"time": "O(n log n)", "space": "O(1) beyond the sort"},
        "approach": (
            "**The heaviest remaining person must board some boat now, and the best possible companion is the "
            "lightest remaining person.** Sort, then use two pointers: if lightest + heaviest fits, send both; "
            "otherwise the heaviest goes alone (nobody lighter than the lightest exists to pair with). Each "
            "iteration launches one boat and removes the heaviest, so the loop runs at most n times.\n\n"
            "**Exchange argument:** let `H` be the heaviest and `l` the lightest remaining, with `H + l <= limit`. "
            "Take any optimal solution in which `H` rides with some `x != l` and `l` rides with `y` (or alone). "
            "Swap partners to form `(H, l)` and `(x, y)`. The first boat fits by assumption. For the second, "
            "`y <= H` because `H` is the heaviest, so `x + y <= x + H <= limit`. The boat count is unchanged, so "
            "some optimal solution contains the greedy pair. If instead `H + l > limit`, nobody can share with `H`, "
            "so every solution sends `H` alone. Either way the greedy step is safe, and induction finishes the proof.\n\n"
            "**Common mistakes:** trying to fill boats greedily from the light end (leaves heavy people stranded "
            "one per boat when they could have shared), allowing more than two per boat, and forgetting that "
            "`light == heavy` still needs a boat.\n\n"
            "**Interview follow-ups:** Boats that carry up to k people? (Greedy no longer works in general; it "
            "becomes bin packing, NP-hard, so discuss heuristics.) Counting sort when weights are bounded? (O(n + "
            "limit), avoids the log factor.) Minimise the number of boats and then the total weight imbalance? "
            "(Secondary objective; the greedy pairs already balance well but you would need to prove or adjust.)"
        ),
        "similar": ["two-sum-ii-sorted", "assign-cookies", "two-city-scheduling"],
    },
]
