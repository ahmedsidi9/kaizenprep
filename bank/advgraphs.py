"""Advanced Graphs: shortest paths, MST, topological order over letters, Euler paths, union-find."""
import itertools


def _alien_words():
    """3000 pseudo-random words sorted under the reversed alphabet; every adjacent letter pair appears."""
    alpha = "zyxwvutsrqponmlkjihgfedcba"
    rank = {c: i for i, c in enumerate(alpha)}
    words, x = [], 12345
    for i in range(3000):
        w = []
        for _ in range(3 + (i * 7) % 4):
            x = (x * 1103515245 + 12345) % (2 ** 31)
            w.append(alpha[(x >> 16) % 26])
        words.append("".join(w))
    words.sort(key=lambda w: [rank[c] for c in w])
    return words


_CODES = [chr(65 + i // 676) + chr(65 + i // 26 % 26) + chr(65 + i % 26) for i in range(1500)]
_PERM = [(i * 7919) % 1500 for i in range(1500)]

PROBLEMS = [
    {
        "id": "network-delay-time",
        "title": "Network Delay Time",
        "difficulty": "Medium",
        "pattern": "Advanced Graphs",
        "tags": ["Graph", "Shortest Path", "Heap / Priority Queue", "Dijkstra"],
        "companies": {"google": 2, "apple": 1, "meta": 1, "amazon": 3, "microsoft": 2},
        "description": (
            "A network has `n` nodes labelled `1..n`. You are given directed edges `times[i] = [u, v, w]`, "
            "meaning a signal sent from `u` arrives at `v` after `w` time units.\n\n"
            "A signal is sent from node `k` at time 0. Return the earliest time at which **every** node has "
            "received it. If some node can never be reached, return `-1`."
        ),
        "examples": [
            {"input": "times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2", "output": "2",
             "explanation": "Nodes 1 and 3 hear the signal at time 1; node 4 hears it from node 3 at time 2."},
            {"input": "times = [[1,2,1]], n = 2, k = 1", "output": "1"},
            {"input": "times = [[1,2,1]], n = 2, k = 2", "output": "-1",
             "explanation": "Node 1 has no incoming edge, so it never receives the signal."},
        ],
        "constraints": ["1 <= k <= n <= 100", "1 <= times.length <= 6000", "1 <= u, v <= n, u != v", "0 <= w <= 100",
                        "No duplicate edges."],
        "hints": [
            "The time the last node hears the signal is the largest shortest-path distance from k.",
            "Non-negative weights point to Dijkstra: a min-heap of (distance, node), relax outgoing edges on pop.",
            "Skip a popped entry if it is stale (its distance is larger than the best known). If fewer than n nodes were ever settled, return -1.",
        ],
        "function": "networkDelayTime",
        "signature": "def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:",
        "arg_types": {"times": "List[List[int]]", "n": "int", "k": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"times": [[2, 1, 1], [2, 3, 1], [3, 4, 1]], "n": 4, "k": 2}, "output": 2},
            {"input": {"times": [[1, 2, 1]], "n": 2, "k": 1}, "output": 1},
            {"input": {"times": [[1, 2, 1]], "n": 2, "k": 2}, "output": -1},
            {"input": {"times": [[1, 2, 1], [2, 3, 2], [1, 3, 4]], "n": 3, "k": 1}, "output": 3},
            {"input": {"times": [], "n": 1, "k": 1}, "output": 0},
            {"input": {"times": [[1, 2, 3], [1, 3, 1], [3, 2, 1]], "n": 3, "k": 1}, "output": 2},
            {"input": {"times": [[i, i + 1, 1] for i in range(1, 5000)] + [[i, i + 2, 5] for i in range(1, 4999)],
                       "n": 5000, "k": 1}, "output": 4999},
        ],
        "solution": (
            "class Solution:\n"
            "    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:\n"
            "        graph = defaultdict(list)\n"
            "        for u, v, w in times:\n"
            "            graph[u].append((v, w))\n"
            "        dist = {}\n"
            "        heap = [(0, k)]\n"
            "        while heap:\n"
            "            d, u = heapq.heappop(heap)\n"
            "            if u in dist:\n"
            "                continue  # already settled with a smaller distance\n"
            "            dist[u] = d\n"
            "            for v, w in graph[u]:\n"
            "                if v not in dist:\n"
            "                    heapq.heappush(heap, (d + w, v))\n"
            "        return max(dist.values()) if len(dist) == n else -1\n"
        ),
        "approach": (
            "**The answer is the largest single-source shortest-path distance from `k`.** Every node hears the "
            "signal along its fastest route, so once the slowest-to-reach node is covered, all are.\n\n"
            "Weights are non-negative, so Dijkstra applies. Build an adjacency list, push `(0, k)` into a min-heap, "
            "and repeatedly pop the closest unsettled node. The first time a node is popped its distance is final "
            "(invariant: every node still in the heap has distance >= the popped one, and edges can only add). "
            "Relax its outgoing edges by pushing `(d + w, v)` for unsettled `v`. When the heap empties, if fewer "
            "than `n` nodes were settled the graph is not fully reachable from `k`; otherwise return the maximum.\n\n"
            "**Common mistakes:** forgetting to skip stale heap entries (leads to wrong answers when a node is "
            "relaxed twice), returning the sum of distances instead of the max, and treating the graph as undirected.\n\n"
            "**Interview follow-ups:** How would you handle negative weights? (Bellman-Ford, O(V*E), or SPFA.) "
            "What if `n` is small but the edge count is huge? (A dense O(V^2) Dijkstra without a heap beats "
            "O(E log V).) Could you return the actual path to the slowest node? (Track a parent pointer at relaxation.)"
        ),
        "complexity": {"time": "O(E log V)", "space": "O(V + E)"},
        "similar": ["cheapest-flights-within-k-stops", "swim-in-rising-water", "path-with-minimum-effort"],
    },
    {
        "id": "min-cost-to-connect-all-points",
        "title": "Min Cost to Connect All Points",
        "difficulty": "Medium",
        "pattern": "Advanced Graphs",
        "tags": ["Graph", "Minimum Spanning Tree", "Union Find", "Heap / Priority Queue"],
        "companies": {"google": 2, "amazon": 2, "microsoft": 1},
        "description": (
            "You are given `points`, a list of distinct integer coordinates `[x, y]` on a plane. Connecting two "
            "points costs their **Manhattan distance** `|x1 - x2| + |y1 - y2|`.\n\n"
            "Return the minimum total cost to connect all points so that there is exactly one simple path "
            "between every pair of points (i.e. a spanning tree)."
        ),
        "examples": [
            {"input": "points = [[0,0],[2,2],[3,10],[5,2],[7,0]]", "output": "20",
             "explanation": "Edges (0,0)-(2,2)=4, (2,2)-(5,2)=3, (5,2)-(7,0)=4, (2,2)-(3,10)=9 give 20, the cheapest spanning tree."},
            {"input": "points = [[3,12],[-2,5],[-4,1]]", "output": "18"},
            {"input": "points = [[0,0]]", "output": "0"},
        ],
        "constraints": ["1 <= points.length <= 1000", "-10^6 <= xi, yi <= 10^6", "All points are distinct."],
        "hints": [
            "Every pair of points is a potential edge, so this is a minimum spanning tree on a complete graph with n^2 edges.",
            "Kruskal works (sort all n^2 edges, union-find), but Prim's algorithm without a heap is O(n^2) time and O(n) space, which is better on a dense graph.",
            "Prim: keep `best[v]` = cheapest edge from the tree to v. Each round pick the unvisited v with the smallest best, add it, then relax every other unvisited point against v.",
        ],
        "function": "minCostConnectPoints",
        "signature": "def minCostConnectPoints(self, points: List[List[int]]) -> int:",
        "arg_types": {"points": "List[List[int]]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"points": [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]}, "output": 20},
            {"input": {"points": [[3, 12], [-2, 5], [-4, 1]]}, "output": 18},
            {"input": {"points": [[0, 0]]}, "output": 0},
            {"input": {"points": [[0, 0], [1, 1], [1, 0], [-1, 1]]}, "output": 4},
            {"input": {"points": [[-1000000, -1000000], [1000000, 1000000]]}, "output": 4000000},
            {"input": {"points": [[(i * 7919) % 1000, 2 * ((i * 7919) % 1000)] for i in range(1000)]}, "output": 2997},
        ],
        "solution": (
            "class Solution:\n"
            "    def minCostConnectPoints(self, points: List[List[int]]) -> int:\n"
            "        n = len(points)\n"
            "        INF = float('inf')\n"
            "        best = [INF] * n      # cheapest known edge from the tree to each point\n"
            "        in_tree = [False] * n\n"
            "        best[0] = 0\n"
            "        total = 0\n"
            "        for _ in range(n):\n"
            "            u = -1\n"
            "            for v in range(n):\n"
            "                if not in_tree[v] and (u == -1 or best[v] < best[u]):\n"
            "                    u = v\n"
            "            in_tree[u] = True\n"
            "            total += best[u]\n"
            "            ux, uy = points[u]\n"
            "            for v in range(n):\n"
            "                if not in_tree[v]:\n"
            "                    d = abs(ux - points[v][0]) + abs(uy - points[v][1])\n"
            "                    if d < best[v]:\n"
            "                        best[v] = d\n"
            "        return total\n"
        ),
        "approach": (
            "**This is a minimum spanning tree on the complete graph of points.** Any valid wiring is a spanning "
            "tree and we want the cheapest one.\n\n"
            "Because the graph is complete (n^2 edges), the array-based **Prim's algorithm** is the natural fit: "
            "maintain `best[v]`, the cheapest edge connecting the current tree to `v`. Each of the `n` rounds scans "
            "for the unvisited point with the smallest `best`, adds it to the tree, and relaxes `best` for every "
            "remaining point using the new vertex. Correctness follows from the cut property: the lightest edge "
            "crossing the cut (tree, not-tree) always belongs to some MST.\n\n"
            "**Kruskal** is the alternative: generate all n(n-1)/2 edges, sort them, and union-find; it costs "
            "O(n^2 log n) time and O(n^2) memory, which is noticeably worse at n = 1000. A heap-based Prim also works "
            "but has the same log factor.\n\n"
            "**Common mistakes:** using Euclidean instead of Manhattan distance, forgetting the single-point case "
            "(answer 0), and pushing every edge into a heap and running out of memory.\n\n"
            "**Interview follow-ups:** Explain the cut property proof. When would you prefer Kruskal? (Sparse "
            "graphs with an explicit edge list.) How would you return the edges of the tree, not just the cost? "
            "(Record `parent[v]` whenever `best[v]` improves.)"
        ),
        "complexity": {"time": "O(n^2)", "space": "O(n)"},
        "similar": ["network-delay-time", "accounts-merge", "connecting-cities-with-minimum-cost"],
    },
    {
        "id": "cheapest-flights-within-k-stops",
        "title": "Cheapest Flights Within K Stops",
        "difficulty": "Medium",
        "pattern": "Advanced Graphs",
        "tags": ["Graph", "Shortest Path", "Dynamic Programming", "Bellman-Ford"],
        "companies": {"google": 3, "apple": 1, "meta": 1, "amazon": 3, "microsoft": 2},
        "description": (
            "There are `n` cities numbered `0..n-1` and a list of one-way flights `flights[i] = [from, to, price]`.\n\n"
            "Find the cheapest price to fly from `src` to `dst` using **at most `k` stops** (intermediate cities), "
            "i.e. at most `k + 1` flights. Return `-1` if no such route exists."
        ),
        "examples": [
            {"input": "n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], src = 0, dst = 3, k = 1",
             "output": "700",
             "explanation": "0 -> 1 -> 3 costs 700 with one stop. The cheaper 0 -> 1 -> 2 -> 3 (400) needs two stops."},
            {"input": "n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 1", "output": "200"},
            {"input": "n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 0", "output": "500"},
        ],
        "constraints": ["1 <= n <= 100", "0 <= flights.length <= n * (n - 1) / 2", "0 <= from, to < n, from != to",
                        "1 <= price <= 10^4", "0 <= src, dst, k < n, src != dst"],
        "hints": [
            "Plain Dijkstra fails here: the cheapest way to reach an intermediate city may use too many stops, blocking a pricier route that fits.",
            "Bellman-Ford relaxes every edge once per round; after i rounds you have the cheapest cost using at most i flights. Run exactly k + 1 rounds.",
            "Relax from a copy of the previous round's distances so a single round cannot chain two flights together.",
        ],
        "function": "findCheapestPrice",
        "signature": "def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:",
        "arg_types": {"n": "int", "flights": "List[List[int]]", "src": "int", "dst": "int", "k": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"n": 4, "flights": [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], "src": 0, "dst": 3, "k": 1}, "output": 700},
            {"input": {"n": 3, "flights": [[0, 1, 100], [1, 2, 100], [0, 2, 500]], "src": 0, "dst": 2, "k": 1}, "output": 200},
            {"input": {"n": 3, "flights": [[0, 1, 100], [1, 2, 100], [0, 2, 500]], "src": 0, "dst": 2, "k": 0}, "output": 500},
            {"input": {"n": 3, "flights": [[0, 1, 100]], "src": 0, "dst": 2, "k": 1}, "output": -1},
            {"input": {"n": 2, "flights": [], "src": 0, "dst": 1, "k": 0}, "output": -1},
            {"input": {"n": 1000,
                       "flights": [[i, i + 1, 1] for i in range(999)] + [[i, i + 2, 3] for i in range(998)] + [[0, 999, 2000]],
                       "src": 0, "dst": 999, "k": 500}, "output": 1497},
            {"input": {"n": 1000,
                       "flights": [[i, i + 1, 1] for i in range(999)] + [[i, i + 2, 3] for i in range(998)] + [[0, 999, 2000]],
                       "src": 0, "dst": 999, "k": 0}, "output": 2000},
        ],
        "solution": (
            "class Solution:\n"
            "    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:\n"
            "        INF = float('inf')\n"
            "        dist = [INF] * n\n"
            "        dist[src] = 0\n"
            "        for _ in range(k + 1):\n"
            "            nxt = dist[:]  # relax from the previous round only\n"
            "            for u, v, w in flights:\n"
            "                if dist[u] + w < nxt[v]:\n"
            "                    nxt[v] = dist[u] + w\n"
            "            dist = nxt\n"
            "        return -1 if dist[dst] == INF else dist[dst]\n"
        ),
        "approach": (
            "**Bellman-Ford limited to `k + 1` rounds.** Define `dist_i[v]` as the cheapest cost to reach `v` using "
            "at most `i` flights. The recurrence is `dist_i[v] = min(dist_{i-1}[v], min over edges (u,v,w) of "
            "dist_{i-1}[u] + w)`. Starting from `dist_0[src] = 0`, run the relaxation exactly `k + 1` times and "
            "read `dist[dst]`.\n\n"
            "The subtle point is relaxing against a **snapshot** of the previous round. If you update in place, "
            "one round could chain several flights and the stop limit would be violated.\n\n"
            "**Why not Dijkstra?** Greedy by cost drops a more expensive partial path that uses fewer stops, which "
            "may be the only one that can still reach `dst` legally. A Dijkstra variant that keys the heap on "
            "`(cost, node, stops)` and does not prune on cost alone also works but is harder to get right.\n\n"
            "**Common mistakes:** running `k` instead of `k + 1` rounds (k stops means k + 1 edges), updating "
            "`dist` in place, and returning `inf` instead of `-1`.\n\n"
            "**Interview follow-ups:** What is the complexity and when is it worse than Dijkstra? (O(k * E); for "
            "large k with no stop limit use Dijkstra.) How would you recover the route? (Keep a parent array per "
            "round, or a 2-D table `dist[i][v]` and walk back.) How does this generalise to detecting negative cycles?"
        ),
        "complexity": {"time": "O(k * E)", "space": "O(n)"},
        "similar": ["network-delay-time", "path-with-maximum-probability"],
    },
    {
        "id": "alien-dictionary",
        "title": "Alien Dictionary",
        "difficulty": "Hard",
        "pattern": "Advanced Graphs",
        "tags": ["Graph", "Topological Sort", "String", "BFS"],
        "companies": {"google": 3, "apple": 2, "meta": 5, "amazon": 3, "microsoft": 2},
        "description": (
            "An unknown language uses lowercase English letters but with its own letter ordering. You are given "
            "a list of `words` that is **sorted** according to that ordering.\n\n"
            "Return a string containing every letter that appears in `words`, arranged in the alien order. If "
            "several orders are consistent with the input, any one is accepted. If no order is consistent "
            "(for example the words contradict each other, or a longer word appears before its own prefix), return `\"\"`."
        ),
        "examples": [
            {"input": "words = [\"wrt\",\"wrf\",\"er\",\"ett\",\"rftt\"]", "output": "\"wertf\"",
             "explanation": "Adjacent pairs reveal t < f, w < e, r < t, e < r. The only order over {w,r,t,f,e} is wertf."},
            {"input": "words = [\"z\",\"x\"]", "output": "\"zx\""},
            {"input": "words = [\"z\",\"x\",\"z\"]", "output": "\"\"",
             "explanation": "The first pair says z < x and the second says x < z, a contradiction."},
            {"input": "words = [\"abc\",\"ab\"]", "output": "\"\"",
             "explanation": "A word cannot come before its own prefix in a sorted list."},
        ],
        "constraints": ["1 <= words.length <= 3000", "1 <= words[i].length <= 20", "words[i] consists of lowercase letters."],
        "hints": [
            "Only the first differing letter between two adjacent words tells you anything: it says letter_a comes before letter_b.",
            "Those relations form a directed graph over letters. A valid ordering is a topological sort; a cycle means no valid order.",
            "Use Kahn's algorithm: compute in-degrees, repeatedly pop letters with in-degree 0. Remember to add letters with no relations at all, and to reject `['abc', 'ab']` style prefix violations before building the graph.",
        ],
        "function": "alienOrder",
        "signature": "def alienOrder(self, words: List[str]) -> str:",
        "arg_types": {"words": "List[str]"},
        "return_type": "str",
        "compare": "any_of",
        "tests": [
            {"input": {"words": ["wrt", "wrf", "er", "ett", "rftt"]}, "output": ["wertf"]},
            {"input": {"words": ["z", "x"]}, "output": ["zx"]},
            {"input": {"words": ["z", "x", "z"]}, "output": [""]},
            {"input": {"words": ["abc", "ab"]}, "output": [""]},
            {"input": {"words": ["z", "z"]}, "output": ["z"]},
            {"input": {"words": ["ab", "cd"]},
             "output": ["".join(p) for p in itertools.permutations("abcd") if p.index("a") < p.index("c")]},
            {"input": {"words": ["ac", "ab", "zc", "zb"]},
             "output": ["".join(p) for p in itertools.permutations("abcz") if p.index("a") < p.index("z") and p.index("c") < p.index("b")]},
            {"input": {"words": _alien_words()}, "output": ["zyxwvutsrqponmlkjihgfedcba"]},
        ],
        "solution": (
            "class Solution:\n"
            "    def alienOrder(self, words: List[str]) -> str:\n"
            "        graph = {c: set() for w in words for c in w}\n"
            "        indeg = {c: 0 for c in graph}\n"
            "        for a, b in zip(words, words[1:]):\n"
            "            for x, y in zip(a, b):\n"
            "                if x != y:\n"
            "                    if y not in graph[x]:\n"
            "                        graph[x].add(y)\n"
            "                        indeg[y] += 1\n"
            "                    break\n"
            "            else:\n"
            "                if len(a) > len(b):\n"
            "                    return ''  # longer word before its own prefix\n"
            "        queue = deque(c for c in graph if indeg[c] == 0)\n"
            "        order = []\n"
            "        while queue:\n"
            "            c = queue.popleft()\n"
            "            order.append(c)\n"
            "            for d in graph[c]:\n"
            "                indeg[d] -= 1\n"
            "                if indeg[d] == 0:\n"
            "                    queue.append(d)\n"
            "        return ''.join(order) if len(order) == len(graph) else ''\n"
        ),
        "approach": (
            "**Each adjacent pair of words yields at most one ordering constraint, and the answer is a topological "
            "sort of those constraints.** Compare `words[i]` and `words[i+1]` character by character; the first "
            "mismatch `x != y` means `x` precedes `y`. Later characters say nothing. If there is no mismatch and the "
            "first word is longer, the input is invalid.\n\n"
            "Build a directed graph over the letters that occur (every letter is a node even if it has no edges), "
            "then run **Kahn's algorithm**: enqueue in-degree-0 letters, pop them in turn, decrement the in-degree "
            "of their successors. If the output has fewer letters than the graph, a cycle exists and we return `\"\"`.\n\n"
            "**Why it works:** the constraints are exactly the information the sorted list provides; any linear "
            "extension of the resulting DAG is consistent with the input, and a cycle means the input is "
            "self-contradictory.\n\n"
            "**Common mistakes:** comparing non-adjacent words (redundant, but fine) while missing the prefix "
            "rule; adding duplicate edges and double-counting in-degree; dropping letters that only appear in "
            "one word with no relations; forgetting that only the first difference counts.\n\n"
            "**Interview follow-ups:** How would you produce the lexicographically smallest valid order? (Replace "
            "the queue with a min-heap.) How do you detect the cycle with DFS instead of Kahn? (Three-colour "
            "marking.) How many constraints can there be at most? (At most `len(words) - 1`, so the graph is tiny.)"
        ),
        "complexity": {"time": "O(total characters + 26^2)", "space": "O(26^2)"},
        "similar": ["course-schedule-ii", "sequence-reconstruction", "verifying-an-alien-dictionary"],
    },
    {
        "id": "reconstruct-itinerary",
        "title": "Reconstruct Itinerary",
        "difficulty": "Hard",
        "pattern": "Advanced Graphs",
        "tags": ["Graph", "Eulerian Path", "DFS", "Heap / Priority Queue"],
        "companies": {"google": 3, "apple": 1, "meta": 2, "amazon": 2, "microsoft": 1},
        "description": (
            "You are given a list of airline `tickets`, each `[from, to]` with three-letter airport codes. "
            "Together the tickets form exactly one trip that starts at `\"JFK\"` and uses **every ticket exactly once**.\n\n"
            "Reconstruct the trip as a list of airports. If more than one trip is possible, return the one that is "
            "lexicographically smallest when read as a single sequence of strings. At least one valid trip is guaranteed."
        ),
        "examples": [
            {"input": "tickets = [[\"MUC\",\"LHR\"],[\"JFK\",\"MUC\"],[\"SFO\",\"SJC\"],[\"LHR\",\"SFO\"]]",
             "output": "[\"JFK\",\"MUC\",\"LHR\",\"SFO\",\"SJC\"]"},
            {"input": "tickets = [[\"JFK\",\"SFO\"],[\"JFK\",\"ATL\"],[\"SFO\",\"ATL\"],[\"ATL\",\"JFK\"],[\"ATL\",\"SFO\"]]",
             "output": "[\"JFK\",\"ATL\",\"JFK\",\"SFO\",\"ATL\",\"SFO\"]",
             "explanation": "[\"JFK\",\"SFO\",\"ATL\",\"JFK\",\"ATL\",\"SFO\"] also uses every ticket but is lexicographically larger."},
            {"input": "tickets = [[\"JFK\",\"KUL\"],[\"JFK\",\"NRT\"],[\"NRT\",\"JFK\"]]",
             "output": "[\"JFK\",\"NRT\",\"JFK\",\"KUL\"]",
             "explanation": "Taking KUL first (the smaller code) strands the NRT tickets, so the greedy choice must be undone."},
        ],
        "constraints": ["1 <= tickets.length <= 3000", "Airport codes are 3 uppercase letters", "from != to", "A valid itinerary exists."],
        "hints": [
            "Every ticket is a directed edge; using each exactly once from JFK is an Eulerian path.",
            "Greedy 'always fly to the smallest destination' can strand you with unused tickets. Hierholzer's algorithm fixes this: when you get stuck, that airport is the END of the trip.",
            "Sort each airport's destinations descending so you can pop the smallest in O(1). DFS, and append an airport to the result when it has no destinations left. Reverse at the end.",
        ],
        "function": "findItinerary",
        "signature": "def findItinerary(self, tickets: List[List[str]]) -> List[str]:",
        "arg_types": {"tickets": "List[List[str]]"},
        "return_type": "List[str]",
        "compare": "exact",
        "tests": [
            {"input": {"tickets": [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]}, "output": ["JFK", "MUC", "LHR", "SFO", "SJC"]},
            {"input": {"tickets": [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]}, "output": ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]},
            {"input": {"tickets": [["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]]}, "output": ["JFK", "NRT", "JFK", "KUL"]},
            {"input": {"tickets": [["JFK", "AAA"]]}, "output": ["JFK", "AAA"]},
            {"input": {"tickets": [["JFK", "AAA"], ["AAA", "JFK"], ["JFK", "AAA"]]}, "output": ["JFK", "AAA", "JFK", "AAA"]},
            {"input": {"tickets": [["EZE", "AXA"], ["TIA", "ANU"], ["ANU", "JFK"], ["JFK", "ANU"], ["ANU", "EZE"], ["TIA", "ANU"], ["AXA", "TIA"], ["TIA", "JFK"], ["ANU", "TIA"], ["JFK", "TIA"]]},
             "output": ["JFK", "ANU", "EZE", "AXA", "TIA", "ANU", "JFK", "TIA", "ANU", "TIA", "JFK"]},
            {"input": {"tickets": [["JFK", _CODES[j]] for j in _PERM] + [[_CODES[j], "JFK"] for j in _PERM]},
             "output": ["JFK"] + [x for c in _CODES for x in (c, "JFK")]},
        ],
        "solution": (
            "class Solution:\n"
            "    def findItinerary(self, tickets: List[List[str]]) -> List[str]:\n"
            "        graph = defaultdict(list)\n"
            "        for src, dst in sorted(tickets, reverse=True):\n"
            "            graph[src].append(dst)  # descending, so pop() yields the smallest\n"
            "        route = []\n"
            "        stack = ['JFK']\n"
            "        while stack:\n"
            "            while graph[stack[-1]]:\n"
            "                stack.append(graph[stack[-1]].pop())\n"
            "            route.append(stack.pop())  # dead end: this airport is fixed at the end\n"
            "        return route[::-1]\n"
        ),
        "approach": (
            "**Tickets are directed edges, and the trip is an Eulerian path starting at JFK; Hierholzer's "
            "algorithm builds it in linear time.** The key observation: when a depth-first walk gets stuck at an "
            "airport with no unused outgoing tickets, that airport must be the *last* stop of the itinerary built "
            "so far. Append it to the output and backtrack; the remaining unused tickets form closed loops that get "
            "spliced in as the walk unwinds. Reversing the output gives the route.\n\n"
            "To get the lexicographically smallest trip, always leave an airport via its smallest unused "
            "destination. Sorting each adjacency list in descending order lets `pop()` deliver the smallest in O(1).\n\n"
            "**Why it works:** the input is guaranteed to have an Eulerian path from JFK, so every dead end is "
            "either the true end or the close of a cycle through the current airport, and the post-order "
            "placement handles both. Smallest-first at each step is optimal because once an Eulerian path is "
            "guaranteed to exist, the post-order construction never needs to undo a choice.\n\n"
            "**Common mistakes:** the naive greedy without post-order (fails example 3), forgetting to reverse, "
            "and using a min-heap per airport which turns the pop into O(log n).\n\n"
            "**Interview follow-ups:** How would you verify an Eulerian path exists? (Out-degree minus in-degree "
            "is +1 at the start, -1 at the end, 0 elsewhere, and the edges are connected.) What changes for an "
            "undirected graph? (Remove the reverse edge too.) Write the recursive version and discuss stack depth."
        ),
        "complexity": {"time": "O(E log E)", "space": "O(E)"},
        "similar": ["valid-arrangement-of-pairs", "course-schedule-ii"],
    },
    {
        "id": "swim-in-rising-water",
        "title": "Swim in Rising Water",
        "difficulty": "Hard",
        "pattern": "Advanced Graphs",
        "tags": ["Graph", "Heap / Priority Queue", "Binary Search", "Union Find", "Matrix"],
        "companies": {"google": 2, "amazon": 1},
        "description": (
            "You are given an `n x n` grid where `grid[i][j]` is the elevation of that cell; the elevations are a "
            "permutation of `0..n*n-1`. At time `t` the water level is `t`, and you can stand on or move between "
            "4-directionally adjacent cells whose elevation is **at most `t`**. Swimming takes no time.\n\n"
            "Return the least time `t` at which you can travel from the top-left cell to the bottom-right cell."
        ),
        "examples": [
            {"input": "grid = [[0,2],[1,3]]", "output": "3",
             "explanation": "The destination has elevation 3, so no earlier time can work; at t = 3 every cell is reachable."},
            {"input": "grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]", "output": "16",
             "explanation": "Follow the snake 0..16 along the border; the cells above 16 on the second row are never needed."},
        ],
        "constraints": ["1 <= n <= 50", "0 <= grid[i][j] < n*n", "All values are distinct."],
        "hints": [
            "You need the path whose maximum elevation is as small as possible, not the shortest path.",
            "Dijkstra with the heap keyed on 'highest elevation seen so far on this path' does exactly that: the first time you pop the target, its key is the answer.",
            "Alternative: binary search on t with a BFS feasibility check, or union-find adding cells in increasing elevation until the corners connect.",
        ],
        "function": "swimInWater",
        "signature": "def swimInWater(self, grid: List[List[int]]) -> int:",
        "arg_types": {"grid": "List[List[int]]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"grid": [[0, 2], [1, 3]]}, "output": 3},
            {"input": {"grid": [[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16], [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]]}, "output": 16},
            {"input": {"grid": [[0]]}, "output": 0},
            {"input": {"grid": [[3, 2], [0, 1]]}, "output": 3},
            {"input": {"grid": [[0, 3, 8], [7, 4, 5], [1, 2, 6]]}, "output": 6},
            {"input": {"grid": [[(i * 50 + j) * 7 % 2500 for j in range(50)] for i in range(50)]}, "output": 2493},
        ],
        "solution": (
            "class Solution:\n"
            "    def swimInWater(self, grid: List[List[int]]) -> int:\n"
            "        n = len(grid)\n"
            "        heap = [(grid[0][0], 0, 0)]  # (max elevation on path so far, r, c)\n"
            "        seen = {(0, 0)}\n"
            "        while heap:\n"
            "            t, r, c = heapq.heappop(heap)\n"
            "            if r == n - 1 and c == n - 1:\n"
            "                return t\n"
            "            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):\n"
            "                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:\n"
            "                    seen.add((nr, nc))\n"
            "                    heapq.heappush(heap, (max(t, grid[nr][nc]), nr, nc))\n"
            "        return -1\n"
        ),
        "approach": (
            "**Minimise the maximum elevation along the path (a bottleneck shortest path), which is Dijkstra with "
            "`max` in place of `+`.** Key the heap on the highest cell seen so far along the route. Popping a cell "
            "with key `t` means there is a route to it whose cells are all <= `t`, and because the heap is "
            "monotone no later pop can improve it. The first time the bottom-right corner is popped, `t` is the answer.\n\n"
            "Because the key of a neighbour is `max(t, grid[nr][nc])` and never decreases, a cell can be marked "
            "visited the moment it is pushed; there is no need for a decrease-key.\n\n"
            "**Alternatives worth naming:** binary search on `t` with a BFS check, O(n^2 log n^2); union-find "
            "adding cells in increasing elevation and stopping when the two corners share a root, also "
            "O(n^2 log n^2) due to the sort.\n\n"
            "**Common mistakes:** treating it as a plain shortest path (summing elevations), forgetting that the "
            "starting cell itself can be the bottleneck, and allowing revisits which blows up the heap.\n\n"
            "**Interview follow-ups:** Compare the three approaches and their constants. How would you return the "
            "path? (Parent pointers at push time.) What if the water rose by more than one unit per second? "
            "(Return the first time step >= t.)"
        ),
        "complexity": {"time": "O(n^2 log n)", "space": "O(n^2)"},
        "similar": ["network-delay-time", "path-with-minimum-effort", "min-cost-to-connect-all-points"],
    },
    {
        "id": "accounts-merge",
        "title": "Accounts Merge",
        "difficulty": "Medium",
        "pattern": "Advanced Graphs",
        "tags": ["Graph", "Union Find", "Hash Table", "Sorting"],
        "companies": {"google": 3, "apple": 1, "meta": 5, "amazon": 3, "microsoft": 2},
        "description": (
            "Each entry of `accounts` is a list whose first element is a person's name and whose remaining "
            "elements are email addresses belonging to that account.\n\n"
            "Two accounts belong to the same person if they share **at least one** email, even when the names "
            "differ in other accounts of the same person. (Two accounts with the same name but no common email may "
            "be different people.)\n\n"
            "Merge the accounts. Each merged account should list the name first followed by its emails in "
            "**sorted** order. The merged accounts themselves may be returned in any order."
        ),
        "examples": [
            {"input": "accounts = [[\"John\",\"johnsmith@mail.com\",\"john_newyork@mail.com\"],[\"John\",\"johnsmith@mail.com\",\"john00@mail.com\"],[\"Mary\",\"mary@mail.com\"],[\"John\",\"johnnybravo@mail.com\"]]",
             "output": "[[\"John\",\"john00@mail.com\",\"john_newyork@mail.com\",\"johnsmith@mail.com\"],[\"Mary\",\"mary@mail.com\"],[\"John\",\"johnnybravo@mail.com\"]]",
             "explanation": "The first two John accounts share johnsmith@mail.com and merge. The third John has no email in common and stays separate."},
            {"input": "accounts = [[\"Ann\",\"a@x.com\"],[\"Ann\",\"b@x.com\"],[\"Ann\",\"a@x.com\",\"b@x.com\"]]",
             "output": "[[\"Ann\",\"a@x.com\",\"b@x.com\"]]",
             "explanation": "The first two accounts share nothing directly, but the third account bridges them, so all three collapse into one."},
        ],
        "constraints": ["1 <= accounts.length <= 1000", "2 <= accounts[i].length <= 10", "Names and emails are non-empty ASCII strings.",
                        "The first element is a name; the others are valid emails."],
        "hints": [
            "Model it as connectivity: accounts that share an email are in the same component.",
            "Union-find over account indices: map each email to the first account index that had it; when another account has the same email, union the two indices.",
            "Afterwards, group emails by the root of their account and sort each group. Use the name from the root (any account in the group has the same person's name).",
        ],
        "function": "accountsMerge",
        "signature": "def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:",
        "arg_types": {"accounts": "List[List[str]]"},
        "return_type": "List[List[str]]",
        "compare": "unordered",
        "tests": [
            {"input": {"accounts": [["John", "johnsmith@mail.com", "john_newyork@mail.com"], ["John", "johnsmith@mail.com", "john00@mail.com"], ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]]},
             "output": [["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"], ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]]},
            {"input": {"accounts": [["Ann", "a@x.com"], ["Ann", "b@x.com"], ["Ann", "a@x.com", "b@x.com"]]},
             "output": [["Ann", "a@x.com", "b@x.com"]]},
            {"input": {"accounts": [["Solo", "solo@x.com"]]}, "output": [["Solo", "solo@x.com"]]},
            {"input": {"accounts": [["Gabe", "Gabe0@m.co", "Gabe3@m.co", "Gabe1@m.co"], ["Kevin", "Kevin3@m.co", "Kevin5@m.co", "Kevin0@m.co"], ["Ethan", "Ethan5@m.co", "Ethan4@m.co", "Ethan0@m.co"], ["Hanzo", "Hanzo3@m.co", "Hanzo1@m.co", "Hanzo0@m.co"], ["Fern", "Fern5@m.co", "Fern1@m.co", "Fern0@m.co"]]},
             "output": [["Ethan", "Ethan0@m.co", "Ethan4@m.co", "Ethan5@m.co"], ["Gabe", "Gabe0@m.co", "Gabe1@m.co", "Gabe3@m.co"], ["Hanzo", "Hanzo0@m.co", "Hanzo1@m.co", "Hanzo3@m.co"], ["Kevin", "Kevin0@m.co", "Kevin3@m.co", "Kevin5@m.co"], ["Fern", "Fern0@m.co", "Fern1@m.co", "Fern5@m.co"]]},
            {"input": {"accounts": [["Dup", "d@x.com", "d@x.com"], ["Dup", "e@x.com", "d@x.com"]]},
             "output": [["Dup", "d@x.com", "e@x.com"]]},
            {"input": {"accounts": [["User", "e%d@m.com" % i, "e%d@m.com" % (i + 1)] for i in range(3000)]
                                    + [["Other", "o%d@m.com" % i] for i in range(1000)]},
             "output": [["User"] + sorted("e%d@m.com" % i for i in range(3001))] + [["Other", "o%d@m.com" % i] for i in range(1000)]},
        ],
        "solution": (
            "class Solution:\n"
            "    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:\n"
            "        parent = list(range(len(accounts)))\n\n"
            "        def find(x):\n"
            "            while parent[x] != x:\n"
            "                parent[x] = parent[parent[x]]  # path halving\n"
            "                x = parent[x]\n"
            "            return x\n\n"
            "        def union(a, b):\n"
            "            ra, rb = find(a), find(b)\n"
            "            if ra != rb:\n"
            "                parent[rb] = ra\n\n"
            "        owner = {}  # email -> index of first account that listed it\n"
            "        for i, acc in enumerate(accounts):\n"
            "            for email in acc[1:]:\n"
            "                if email in owner:\n"
            "                    union(i, owner[email])\n"
            "                else:\n"
            "                    owner[email] = i\n\n"
            "        groups = defaultdict(set)\n"
            "        for email, i in owner.items():\n"
            "            groups[find(i)].add(email)\n"
            "        return [[accounts[root][0]] + sorted(emails) for root, emails in groups.items()]\n"
        ),
        "approach": (
            "**Shared emails define connected components over account indices; union-find finds them in near-linear "
            "time.** Keep `owner[email]`, the first account index seen with that email. Scanning each account, "
            "an email already in `owner` means this account and the owner are the same person, so `union` them. "
            "After one pass every account's root identifies its person.\n\n"
            "Then bucket emails by `find(owner[email])`, sort each bucket, and prepend the name of the root "
            "account. Any account in the component carries the same person's name, so the root's name is fine.\n\n"
            "**Why union-find rather than DFS:** DFS over an email graph also works (build adjacency between the "
            "first email of an account and each other email, then traverse), but union-find needs no explicit "
            "graph and is shorter. With path compression and union by rank (or the path-halving shown), each "
            "operation is effectively O(1) amortised, so the sort dominates.\n\n"
            "**Common mistakes:** unioning on names (wrong: different people may share a name), forgetting to "
            "sort emails, letting duplicate emails inside a single account create duplicates in the output "
            "(using a set per group avoids this), and recursive `find` without compression degrading to O(n).\n\n"
            "**Interview follow-ups:** How would you do this with DFS and what is the memory cost? How does "
            "union by rank differ from path compression and why do you want both? If accounts arrive as a stream, "
            "how do you answer 'same person?' queries online? (Union-find handles that naturally.)"
        ),
        "complexity": {"time": "O(N * K log(N * K)) for N accounts with up to K emails (the sort dominates)", "space": "O(N * K)"},
        "similar": ["number-of-provinces", "redundant-connection", "min-cost-to-connect-all-points"],
    },
]
