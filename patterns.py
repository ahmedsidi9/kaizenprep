"""Pattern cheat sheet: when to reach for each technique, a template, and the traps."""

PATTERNS = [
    {
        "name": "Arrays & Hashing",
        "signal": "Counting, grouping, membership, 'find a pair/subarray with property X' in one pass.",
        "template": '''# frequency map / seen set / prefix sums
seen = {}
prefix = 0
count = 0
for i, x in enumerate(nums):
    prefix += x
    if prefix - k in seen:          # subarray ending at i sums to k
        count += seen[prefix - k]
    seen[prefix] = seen.get(prefix, 0) + 1''',
        "pitfalls": ["Initialise the prefix map with {0: 1} for subarray-sum problems.", "Sorting a copy costs O(n log n); a map gets O(n) when the key space is small.", "Group anagrams by a tuple of 26 counts, not by sorted string, when strings are long."],
    },
    {
        "name": "Two Pointers",
        "signal": "Sorted input, palindromes, pair sums, partitioning in place, merging two sequences.",
        "template": '''lo, hi = 0, len(nums) - 1
while lo < hi:
    s = nums[lo] + nums[hi]
    if s == target:
        return [lo, hi]
    if s < target:
        lo += 1
    else:
        hi -= 1''',
        "pitfalls": ["Skip duplicates after a match in 3Sum or you double count.", "Slow/fast pointers for in-place removal: write index only advances on keep.", "Trapping rain water: move the side with the smaller max."],
    },
    {
        "name": "Sliding Window",
        "signal": "Longest/shortest contiguous substring or subarray satisfying a constraint; 'at most k distinct'.",
        "template": '''from collections import defaultdict
count = defaultdict(int)
left = best = 0
for right, ch in enumerate(s):
    count[ch] += 1
    while INVALID(count):          # shrink until valid
        count[s[left]] -= 1
        left += 1
    best = max(best, right - left + 1)''',
        "pitfalls": ["Fixed-size windows: add right, remove left in the same step.", "Minimum window: record the answer while valid, before shrinking past validity.", "Sliding window maximum needs a monotonic deque of indices, not a heap."],
    },
    {
        "name": "Stack",
        "signal": "Matching brackets, nested structures, 'next greater element', evaluating expressions, histogram areas.",
        "template": '''# monotonic decreasing stack of indices
stack = []
answer = [0] * len(temps)
for i, t in enumerate(temps):
    while stack and temps[stack[-1]] < t:
        j = stack.pop()
        answer[j] = i - j
    stack.append(i)''',
        "pitfalls": ["Push a sentinel (e.g. height 0) at the end of histogram problems to flush the stack.", "Calculator: apply * and / immediately, defer + and - via a sign variable.", "Decode string: push (current string, repeat count) as a pair."],
    },
    {
        "name": "Binary Search",
        "signal": "Sorted or rotated array, monotonic predicate, 'minimum X such that feasible(X)', search on the answer.",
        "template": '''# first index where predicate(mid) is True (predicate is monotone False..True)
lo, hi = 0, n            # hi is exclusive / 'not found' sentinel
while lo < hi:
    mid = (lo + hi) // 2
    if predicate(mid):
        hi = mid
    else:
        lo = mid + 1
return lo''',
        "pitfalls": ["Decide inclusive/exclusive bounds once and keep them; off-by-one bugs come from mixing.", "Rotated arrays: one half is always sorted; check which.", "Search on the answer (Koko, split array): the predicate must be monotone."],
    },
    {
        "name": "Linked List",
        "signal": "In-place reversal, cycle detection, merging, k-group operations, finding the middle.",
        "template": '''dummy = ListNode(0, head)
prev, cur = dummy, head
while cur and cur.next:
    a, b = cur, cur.next          # swap pair
    prev.next, a.next, b.next = b, b.next, a
    prev, cur = a, a.next
return dummy.next''',
        "pitfalls": ["Always use a dummy head when the real head can change.", "Floyd: fast moves 2, slow moves 1; meeting point then restart one from head to find the cycle start.", "Draw the pointers before coding reversal; write the three assignments in a fixed order."],
    },
    {
        "name": "Trees",
        "signal": "Recursion over subtrees, path properties, BST ordering, level-by-level output.",
        "template": '''def dfs(node):
    if not node:
        return 0                      # base value for an empty subtree
    left = dfs(node.left)
    right = dfs(node.right)
    self.best = max(self.best, left + right + node.val)   # answer through this node
    return node.val + max(left, right, 0)                 # value passed to parent''',
        "pitfalls": ["Distinguish 'answer that passes through this node' from 'value returned to the parent'.", "Validate BST with (low, high) bounds, not by comparing with the parent only.", "BFS level order: capture len(queue) before the inner loop."],
    },
    {
        "name": "Tries",
        "signal": "Prefix queries, many words against a board or text, wildcard matching over a dictionary.",
        "template": '''class TrieNode:
    __slots__ = ("children", "end")
    def __init__(self):
        self.children = {}
        self.end = False

def insert(root, word):
    node = root
    for ch in word:
        node = node.children.setdefault(ch, TrieNode())
    node.end = True''',
        "pitfalls": ["Word Search II: prune by deleting leaves after a word is found to stay fast.", "Store the full word at the terminal node to avoid rebuilding it.", "Wildcard search recurses over all children at a '.'."],
    },
    {
        "name": "Heap / Priority Queue",
        "signal": "'k largest/smallest/closest', streaming median, merging k sorted sources, scheduling by priority.",
        "template": '''import heapq
# k largest: keep a min-heap of size k
heap = []
for x in nums:
    heapq.heappush(heap, x)
    if len(heap) > k:
        heapq.heappop(heap)
# heap[0] is the k-th largest

# max-heap: push negatives
heapq.heappush(maxheap, -x)''',
        "pitfalls": ["Two heaps for the running median: max-heap for the low half, min-heap for the high half, keep sizes within 1.", "Quickselect gives average O(n) for k-th largest and is a common follow-up.", "Task scheduler: the answer is max(len(tasks), (maxfreq - 1) * (n + 1) + count_of_max)."],
    },
    {
        "name": "Backtracking",
        "signal": "Enumerate all subsets / permutations / combinations / placements; constraints prune the search.",
        "template": '''def backtrack(start, path):
    result.append(path[:])            # or: if len(path) == k
    for i in range(start, len(nums)):
        if i > start and nums[i] == nums[i - 1]:
            continue                  # skip duplicates (nums sorted)
        path.append(nums[i])
        backtrack(i + 1, path)        # i for reuse allowed, i + 1 otherwise
        path.pop()''',
        "pitfalls": ["Copy the path when recording; appending the same list gives aliased results.", "Sort first when the input has duplicates.", "Word Search: mark the cell visited, recurse, then restore it."],
    },
    {
        "name": "Graphs",
        "signal": "Grids, connectivity, shortest unweighted path, dependency order, cycle detection.",
        "template": '''from collections import deque
def bfs(start):
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in neighbors(u):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

# topological sort (Kahn)
indeg = [0] * n
for u, v in edges: indeg[v] += 1
q = deque(i for i in range(n) if indeg[i] == 0)
order = []
while q:
    u = q.popleft(); order.append(u)
    for v in adj[u]:
        indeg[v] -= 1
        if indeg[v] == 0: q.append(v)
# cycle iff len(order) < n''',
        "pitfalls": ["Multi-source BFS: seed the queue with all sources (rotting oranges, gates).", "Mark visited when enqueuing, not when dequeuing, or nodes get enqueued many times.", "Grid DFS recursion depth can exceed limits on 1000x1000; use an explicit stack."],
    },
    {
        "name": "Advanced Graphs",
        "signal": "Weighted shortest paths, minimum spanning tree, Eulerian path, union of components, k-stop limits.",
        "template": '''import heapq
def dijkstra(adj, src):
    dist = {src: 0}
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float("inf")):
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

# union-find with path compression
parent = list(range(n))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb: return False
    parent[ra] = rb
    return True''',
        "pitfalls": ["Dijkstra needs non-negative weights; with k-stop limits use Bellman-Ford over a copy of the distances per round.", "Prim on dense points: O(n^2) with an array beats a heap.", "Hierholzer for itineraries: sort destinations, build the path on post-order, reverse at the end."],
    },
    {
        "name": "1-D Dynamic Programming",
        "signal": "Optimal count/cost over a sequence where the choice at i depends on a few earlier positions.",
        "template": '''# dp[i] = best answer for prefix of length i
dp = [0] * (n + 1)
dp[0] = BASE
for i in range(1, n + 1):
    dp[i] = combine(dp[i - 1], dp[i - 2], ...)
# space optimise: keep only the last k values''',
        "pitfalls": ["Write the recurrence in words before code: 'dp[i] is the best X using the first i items'.", "Coin change: iterate amounts outer and coins inner for min count; coins outer for counting combinations.", "LIS in O(n log n): patience sorting with bisect on tails."],
    },
    {
        "name": "2-D Dynamic Programming",
        "signal": "Two sequences (edit distance, LCS), grids with moves, intervals (burst balloons), matching with wildcards.",
        "template": '''# dp[i][j] over prefixes of a and b
dp = [[0] * (m + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, m + 1):
        if a[i - 1] == b[j - 1]:
            dp[i][j] = dp[i - 1][j - 1] + 1
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
# interval DP: for length in 2..n, for left, right = left + length - 1, choose the split k''',
        "pitfalls": ["Pad with a row and column of base cases so i-1 and j-1 never go negative.", "Interval DP ordering: solve smaller intervals first, loop by length.", "Regex matching: handle 'x*' as zero occurrences (dp[i][j-2]) or one more (dp[i-1][j] if match)."],
    },
    {
        "name": "Greedy",
        "signal": "A locally optimal choice is provably safe: furthest reach, earliest finish, most frequent first.",
        "template": '''# jump game: furthest reachable index
reach = 0
for i, step in enumerate(nums):
    if i > reach:
        return False
    reach = max(reach, i + step)
return True''',
        "pitfalls": ["Prove the exchange argument in one sentence or the interviewer will ask.", "Gas station: if total gas >= total cost an answer exists; restart after the tank goes negative.", "Partition labels: track the last index of each char and cut when i reaches the running max."],
    },
    {
        "name": "Intervals",
        "signal": "Merging, overlap counting, rooms/resources needed, point-in-interval queries.",
        "template": '''intervals.sort()
merged = [intervals[0]]
for s, e in intervals[1:]:
    if s <= merged[-1][1]:
        merged[-1][1] = max(merged[-1][1], e)
    else:
        merged.append([s, e])

# min rooms: sweep line
events = sorted([(s, 1) for s, e in iv] + [(e, -1) for s, e in iv])
# or: sort starts and ends separately and walk two pointers''',
        "pitfalls": ["Sort by start for merging, by end for 'max non-overlapping' (activity selection).", "Ties: process an end before a start at the same time if touching intervals do not overlap.", "Queries over intervals: sort both and sweep with a heap keyed by size."],
    },
    {
        "name": "Math & Bit Manipulation",
        "signal": "XOR tricks, powers, matrix rotation, digit manipulation, overflow rules.",
        "template": '''x & (x - 1)        # clears the lowest set bit
x & -x             # isolates the lowest set bit
a ^ b              # add without carry; (a & b) << 1 is the carry
# 32-bit signed wrap in Python
MASK = 0xFFFFFFFF
x &= MASK
if x > 0x7FFFFFFF: x -= 1 << 32''',
        "pitfalls": ["Python ints do not overflow; emulate 32-bit limits when the problem demands.", "Rotate image: transpose then reverse each row.", "Set matrix zeroes in O(1) space: use the first row and column as markers, with a separate flag for the first column."],
    },
    {
        "name": "Design",
        "signal": "Implement a class with O(1) or O(log n) operations; combine a map with a list, heap or linked list.",
        "template": '''# O(1) insert/delete/getRandom: list + index map, swap-with-last on delete
def remove(self, val):
    if val not in self.idx: return False
    i, last = self.idx[val], self.vals[-1]
    self.vals[i], self.idx[last] = last, i
    self.vals.pop(); del self.idx[val]
    return True''',
        "pitfalls": ["State the complexity of each method before coding.", "Say how you would make it thread safe (one lock, or lock striping) when asked.", "Time-based KV: append in time order and bisect on timestamps."],
    },
    {
        "name": "Strings",
        "signal": "Parsing, in-place transformation, palindromes, normalisation, formatting rules.",
        "template": '''# two-pointer compression / in-place write index
write = 0
read = 0
while read < len(chars):
    ch = chars[read]
    run = read
    while run < len(chars) and chars[run] == ch:
        run += 1
    chars[write] = ch; write += 1
    if run - read > 1:
        for d in str(run - read):
            chars[write] = d; write += 1
    read = run
return write''',
        "pitfalls": ["Atoi: strip, sign, digits, clamp; stop at the first non-digit.", "Build strings with a list and join; repeated concatenation is quadratic.", "Text justification: handle the last line and single-word lines (left-justified) separately."],
    },
]
