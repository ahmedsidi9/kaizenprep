"""Graph problems: grid flood fill, multi-source BFS, topological sort, union-find, shortest paths."""

import itertools

INF = 2147483647

PROBLEMS = [
    # ---------------------------------------------------------- number-of-islands
    {
        "id": "number-of-islands",
        "title": "Number of Islands",
        "difficulty": "Medium",
        "pattern": "Graphs",
        "tags": ["Array", "DFS", "BFS", "Union Find", "Matrix"],
        "companies": {"google": 5, "apple": 4, "meta": 4, "amazon": 5, "microsoft": 4},
        "description": (
            "You are given an `m x n` grid of characters where `\"1\"` is land and `\"0\"` is water. An island is "
            "a maximal group of land cells connected **horizontally or vertically** (not diagonally). Everything "
            "outside the grid is water.\n\n"
            "Return how many islands the grid contains."
        ),
        "examples": [
            {"input": "grid = [[\"1\",\"1\",\"0\"],[\"0\",\"1\",\"0\"],[\"0\",\"0\",\"1\"]]", "output": "2",
             "explanation": "The three 1s in the top-left are connected; the 1 at the bottom-right is only diagonally adjacent, so it is a separate island."},
            {"input": "grid = [[\"1\",\"0\",\"1\"],[\"0\",\"0\",\"0\"],[\"1\",\"0\",\"1\"]]", "output": "4"},
            {"input": "grid = [[\"0\",\"0\"],[\"0\",\"0\"]]", "output": "0"},
        ],
        "constraints": ["0 <= m, n <= 300", "grid[i][j] is \"0\" or \"1\""],
        "hints": [
            "Each time you meet a land cell you have not seen before, you have found a new island. What should you do before continuing the scan?",
            "Flood-fill from that cell (DFS or BFS) and sink every reachable land cell to \"0\" so it is never counted again.",
            "Mutating the grid doubles as the visited set. If mutation is not allowed, keep a separate boolean matrix.",
        ],
        "function": "numIslands",
        "signature": "def numIslands(self, grid: List[List[str]]) -> int:",
        "arg_types": {"grid": "List[List[str]]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"grid": [["1", "1", "0"], ["0", "1", "0"], ["0", "0", "1"]]}, "output": 2},
            {"input": {"grid": [["1", "0", "1"], ["0", "0", "0"], ["1", "0", "1"]]}, "output": 4},
            {"input": {"grid": [["0", "0"], ["0", "0"]]}, "output": 0},
            {"input": {"grid": []}, "output": 0},
            {"input": {"grid": [["1"]]}, "output": 1},
            {"input": {"grid": [["0"]]}, "output": 0},
            {"input": {"grid": [["1", "1", "1", "1"], ["1", "0", "0", "1"], ["1", "1", "1", "1"]]}, "output": 1},
            {"input": {"grid": [["1" if (r + c) % 2 == 0 else "0" for c in range(60)] for r in range(60)]}, "output": 1800},
            {"input": {"grid": [["1"] * 50 for _ in range(50)]}, "output": 1},
        ],
        "solution": '''class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0
        m, n = len(grid), len(grid[0])
        count = 0

        def sink(r: int, c: int) -> None:
            stack = [(r, c)]
            grid[r][c] = "0"
            while stack:
                x, y = stack.pop()
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == "1":
                        grid[nx][ny] = "0"
                        stack.append((nx, ny))

        for r in range(m):
            for c in range(n):
                if grid[r][c] == "1":
                    count += 1
                    sink(r, c)
        return count
''',
        "approach": (
            "**Key insight: the grid is an implicit graph whose vertices are land cells and whose edges join "
            "4-adjacent land cells; islands are its connected components.** Counting components is one traversal "
            "from each unvisited vertex.\n\n"
            "**Algorithm.** Scan every cell. When you hit a `\"1\"`, increment the counter and flood-fill from it, "
            "turning every reachable `\"1\"` into `\"0\"`. The fill can be recursive DFS, an explicit stack, or a "
            "BFS queue; marking cells on push (not on pop) keeps the stack from growing with duplicates.\n\n"
            "**Why it works.** Flood fill visits exactly one connected component and removes it, so the next "
            "`\"1\"` encountered is guaranteed to start a different island. Each cell is pushed at most once.\n\n"
            "**Common mistakes:** marking a cell visited when popping instead of when pushing (correct but can "
            "blow up memory); counting diagonal neighbours; recursive DFS on a 300x300 all-land grid overflows "
            "Python's default recursion limit, so prefer an explicit stack or raise the limit deliberately.\n\n"
            "**Interview follow-ups:** The grid is read-only? (separate visited matrix, O(mn) extra space.) The "
            "grid is huge and streams row by row? (union-find over the current and previous row, or a row-based "
            "component labelling.) Count islands as cells are added one by one (Number of Islands II)? (union-find "
            "with incremental merges, near O(1) per operation.) Return the island sizes or the largest one? "
            "(Max Area of Island: count cells during the fill.)"
        ),
        "complexity": {"time": "O(m * n)", "space": "O(m * n) worst-case stack"},
        "similar": ["max-area-of-island", "surrounded-regions", "number-of-connected-components-in-an-undirected-graph"],
    },
    # ---------------------------------------------------------------- clone-graph
    {
        "id": "clone-graph",
        "title": "Clone Graph",
        "difficulty": "Medium",
        "pattern": "Graphs",
        "tags": ["Hash Table", "DFS", "BFS", "Graph"],
        "companies": {"google": 3, "apple": 2, "meta": 4, "amazon": 3, "microsoft": 2},
        "description": (
            "You are handed a reference to one node of a **connected undirected graph**. Each node has an "
            "integer `val` and a list `neighbors` of adjacent nodes. Return a **deep copy** of the whole graph: "
            "brand-new node objects with the same values and the same connections, sharing nothing with the "
            "original.\n\n"
            "In the tests the graph is encoded as an adjacency list where entry `i` (1-indexed) lists the "
            "neighbours of the node with value `i`; you receive the node with value 1 and must return the copy of "
            "that node. An empty list means the input is `None`."
        ),
        "examples": [
            {"input": "adjList = [[2,4],[1,3],[2,4],[1,3]]", "output": "[[2,4],[1,3],[2,4],[1,3]]",
             "explanation": "A 4-cycle 1-2-3-4-1. The clone must have the same shape, with the neighbour order preserved."},
            {"input": "adjList = [[]]", "output": "[[]]", "explanation": "A single node with no neighbours."},
            {"input": "adjList = []", "output": "[]", "explanation": "Empty input gives an empty clone."},
        ],
        "constraints": ["0 <= number of nodes <= 2000", "1 <= Node.val <= 2000, all distinct", "No self-loops or repeated edges", "The graph is connected"],
        "hints": [
            "Copying nodes one by one is easy; the difficulty is cycles. How do you avoid cloning the same node twice?",
            "Keep a map from original node to its clone. Before creating a clone, check the map.",
            "DFS: clone(node) returns the mapped copy if present, otherwise creates it, stores it in the map *before* recursing, then appends clone(nb) for each neighbour.",
        ],
        "function": "cloneGraph",
        "signature": "def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:",
        "arg_types": {"node": "GraphNode"},
        "return_type": "GraphNode",
        "compare": "exact",
        "tests": [
            {"input": {"node": [[2, 4], [1, 3], [2, 4], [1, 3]]}, "output": [[2, 4], [1, 3], [2, 4], [1, 3]]},
            {"input": {"node": [[]]}, "output": [[]]},
            {"input": {"node": []}, "output": []},
            {"input": {"node": [[2, 3], [1, 3], [1, 2]]}, "output": [[2, 3], [1, 3], [1, 2]]},
            {"input": {"node": [[2], [1, 3], [2]]}, "output": [[2], [1, 3], [2]]},
            {"input": {"node": [[2, 3, 4, 5], [1], [1], [1], [1]]}, "output": [[2, 3, 4, 5], [1], [1], [1], [1]]},
            {"input": {"node": [[2000 if i == 1 else i - 1, 1 if i == 2000 else i + 1] for i in range(1, 2001)]},
             "output": [[2000 if i == 1 else i - 1, 1 if i == 2000 else i + 1] for i in range(1, 2001)]},
        ],
        "solution": '''class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if node is None:
            return None
        clones = {}

        def clone(orig: 'Node') -> 'Node':
            if orig in clones:
                return clones[orig]
            copy = Node(orig.val)
            clones[orig] = copy
            for nb in orig.neighbors:
                copy.neighbors.append(clone(nb))
            return copy

        return clone(node)
''',
        "approach": (
            "**Key insight: a hash map from original node to its copy both prevents duplicate clones and "
            "breaks cycles.** Register the copy in the map before visiting neighbours so a back-edge finds it.\n\n"
            "**Algorithm.** `clone(orig)`: if `orig` is in the map return the stored copy. Otherwise create "
            "`Node(orig.val)`, store it, then for each neighbour append `clone(nb)` to the copy's neighbour list. "
            "Return `clone(start)`. Keying the map by node object (or by `val`, since values are unique) both work.\n\n"
            "**Why it works.** Every node is created exactly once (first visit) and each edge is traversed once "
            "per endpoint, so the copy has the same vertex set and the same adjacency lists in the same order. "
            "The connectivity guarantee ensures the DFS from the given node reaches everything.\n\n"
            "**Common mistakes:** storing the copy in the map *after* recursing (infinite recursion on any "
            "cycle); appending the original neighbour instead of its clone (a shallow copy that fails the deep-copy "
            "requirement); forgetting the `None` input.\n\n"
            "**Interview follow-ups:** Iterative version to avoid deep recursion on a long path? (BFS with a "
            "queue; clone a node when first seen, wire edges when it is dequeued.) Disconnected graph? (you would "
            "need a list of all nodes, then clone each component.) Directed graph or extra pointers like "
            "Copy List with Random Pointer? (same map technique.) How would you verify the copy is truly deep? "
            "(assert no clone object is identical to any original.)"
        ),
        "complexity": {"time": "O(V + E)", "space": "O(V) for the map and recursion"},
        "similar": ["copy-list-with-random-pointer", "number-of-connected-components-in-an-undirected-graph"],
    },
    # --------------------------------------------------------- max-area-of-island
    {
        "id": "max-area-of-island",
        "title": "Max Area of Island",
        "difficulty": "Medium",
        "pattern": "Graphs",
        "tags": ["Array", "DFS", "BFS", "Union Find", "Matrix"],
        "companies": {"google": 4, "apple": 2, "meta": 3, "amazon": 3, "microsoft": 2},
        "description": (
            "You are given an `m x n` binary grid where `1` is land and `0` is water. An island is a group of "
            "land cells connected horizontally or vertically; its area is the number of cells in it.\n\n"
            "Return the area of the largest island, or `0` if there is no land at all."
        ),
        "examples": [
            {"input": "grid = [[0,0,1,0,0],[0,1,1,0,0],[0,0,0,1,1]]", "output": "3",
             "explanation": "The island covering (0,2), (1,1), (1,2) has area 3; the one at (2,3), (2,4) has area 2."},
            {"input": "grid = [[0,0,0],[0,0,0]]", "output": "0"},
        ],
        "constraints": ["0 <= m, n <= 50", "grid[i][j] is 0 or 1"],
        "hints": [
            "Same scan as Number of Islands, but the flood fill should return how many cells it visited.",
            "Recursive DFS: return 0 for out-of-bounds or water; otherwise sink the cell and return 1 plus the sum of the four neighbour calls.",
            "Take the max over all starting cells. Sinking cells to 0 is the visited marker, so each cell is counted once.",
        ],
        "function": "maxAreaOfIsland",
        "signature": "def maxAreaOfIsland(self, grid: List[List[int]]) -> int:",
        "arg_types": {"grid": "List[List[int]]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"grid": [[0, 0, 1, 0, 0], [0, 1, 1, 0, 0], [0, 0, 0, 1, 1]]}, "output": 3},
            {"input": {"grid": [[0, 0, 0], [0, 0, 0]]}, "output": 0},
            {"input": {"grid": []}, "output": 0},
            {"input": {"grid": [[1]]}, "output": 1},
            {"input": {"grid": [[0]]}, "output": 0},
            {"input": {"grid": [[1, 1], [1, 1]]}, "output": 4},
            {"input": {"grid": [[1, 0, 1, 1], [0, 0, 1, 0], [1, 1, 0, 1]]}, "output": 3},
            {"input": {"grid": [[1 if 10 <= r < 50 and 10 <= c < 50 else 0 for c in range(60)] for r in range(60)]}, "output": 1600},
            {"input": {"grid": [[1 if (r + c) % 2 == 0 else 0 for c in range(60)] for r in range(60)]}, "output": 1},
        ],
        "solution": '''class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0
        m, n = len(grid), len(grid[0])

        def area(r: int, c: int) -> int:
            if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] == 0:
                return 0
            grid[r][c] = 0
            return 1 + area(r + 1, c) + area(r - 1, c) + area(r, c + 1) + area(r, c - 1)

        best = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 1:
                    best = max(best, area(r, c))
        return best
''',
        "approach": (
            "**Key insight: flood fill naturally counts the component it visits; return that count and take "
            "the maximum.** Nothing else changes from counting islands.\n\n"
            "**Algorithm.** For each land cell start `area(r, c)`: out of bounds or water returns 0; otherwise set "
            "the cell to 0 and return `1 + area(neighbours)`. Track the maximum over all starts.\n\n"
            "**Why it works.** Every cell of an island is visited exactly once because it is zeroed on entry, so "
            "the recursive sum equals the component size. Distinct starts always hit distinct islands.\n\n"
            "**Common mistakes:** zeroing the cell *after* the recursive calls (infinite recursion between two "
            "neighbours); checking `grid[r][c]` before the bounds check (IndexError on negative indices wraps in "
            "Python, silently reading the wrong cell); recursion depth on a 50x50 all-land grid is 2500, fine here "
            "but worth mentioning that an explicit stack avoids the issue.\n\n"
            "**Interview follow-ups:** Can you also return the cells of the largest island? (collect them during "
            "the fill.) What if you may flip one water cell to land, what is the largest island you can make "
            "(Making a Large Island)? (label components with their sizes, then for each water cell sum the sizes "
            "of distinct neighbouring labels plus one.) Perimeter instead of area? (count edges that touch water "
            "or the border.)"
        ),
        "complexity": {"time": "O(m * n)", "space": "O(m * n) recursion in the worst case"},
        "similar": ["number-of-islands", "island-perimeter", "making-a-large-island"],
    },
    # ------------------------------------------------------ pacific-atlantic-water-flow
    {
        "id": "pacific-atlantic-water-flow",
        "title": "Pacific Atlantic Water Flow",
        "difficulty": "Medium",
        "pattern": "Graphs",
        "tags": ["Array", "DFS", "BFS", "Matrix"],
        "companies": {"google": 4, "apple": 1, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "A rectangular island is described by an `m x n` matrix `heights`. The Pacific Ocean borders the "
            "**top and left** edges; the Atlantic borders the **bottom and right** edges. Rain on a cell flows to "
            "any 4-adjacent cell whose height is **less than or equal to** the current one, and flows into an ocean "
            "when it leaves the grid along that ocean's edge.\n\n"
            "Return the coordinates `[r, c]` of every cell from which water can reach **both** oceans, in any order."
        ),
        "examples": [
            {"input": "heights = [[1,2,3],[8,9,4],[7,6,5]]", "output": "[[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]",
             "explanation": "Water from (0,0) and (0,1) cannot climb to any Atlantic edge: (0,0) has no lower-or-equal neighbour and (0,1) can only flow into (0,0)."},
            {"input": "heights = [[1,2],[3,4]]", "output": "[[0,1],[1,0],[1,1]]",
             "explanation": "(0,0) is a sink surrounded by taller cells, so it only touches the Pacific."},
            {"input": "heights = [[1]]", "output": "[[0,0]]"},
        ],
        "constraints": ["0 <= m, n <= 200", "0 <= heights[r][c] <= 10^5"],
        "hints": [
            "Simulating flow from every cell is O((mn)^2). Try thinking backwards from the oceans instead.",
            "Start a search from every Pacific border cell and move only to neighbours that are higher or equal (water could have come from there). Do the same for the Atlantic.",
            "Keep two visited sets; the answer is their intersection. Each search is a plain BFS/DFS that visits each cell at most once.",
        ],
        "function": "pacificAtlantic",
        "signature": "def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:",
        "arg_types": {"heights": "List[List[int]]"},
        "return_type": "List[List[int]]",
        "compare": "unordered",
        "tests": [
            {"input": {"heights": [[1, 2, 3], [8, 9, 4], [7, 6, 5]]},
             "output": [[0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]},
            {"input": {"heights": [[1, 2], [3, 4]]}, "output": [[0, 1], [1, 0], [1, 1]]},
            {"input": {"heights": [[1]]}, "output": [[0, 0]]},
            {"input": {"heights": []}, "output": []},
            {"input": {"heights": [[1, 1], [1, 1]]}, "output": [[0, 0], [0, 1], [1, 0], [1, 1]]},
            {"input": {"heights": [[5, 1, 5]]}, "output": [[0, 0], [0, 1], [0, 2]]},
            {"input": {"heights": [[7] * 50 for _ in range(50)]}, "output": [[r, c] for r in range(50) for c in range(50)]},
            {"input": {"heights": [[r + c for c in range(50)] for r in range(50)]},
             "output": [[49, c] for c in range(49)] + [[r, 49] for r in range(50)]},
        ],
        "solution": '''class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights or not heights[0]:
            return []
        m, n = len(heights), len(heights[0])

        def reachable(sources: List[tuple]) -> set:
            seen = set(sources)
            queue = deque(sources)
            while queue:
                r, c = queue.popleft()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen \\
                            and heights[nr][nc] >= heights[r][c]:
                        seen.add((nr, nc))
                        queue.append((nr, nc))
            return seen

        pacific = [(0, c) for c in range(n)] + [(r, 0) for r in range(1, m)]
        atlantic = [(m - 1, c) for c in range(n)] + [(r, n - 1) for r in range(m - 1)]
        both = reachable(pacific) & reachable(atlantic)
        return [[r, c] for r, c in both]
''',
        "approach": (
            "**Key insight: reverse the flow.** Instead of asking \"where can water from this cell go?\" for "
            "every cell, ask \"which cells can send water to this ocean?\" and walk uphill from the coast. Two "
            "multi-source searches replace m*n separate ones.\n\n"
            "**Algorithm.** Seed a BFS with all Pacific edge cells (row 0 and column 0) and expand to neighbours "
            "whose height is >= the current cell's height. Repeat for the Atlantic edge (last row and last column). "
            "Output the intersection of the two visited sets.\n\n"
            "**Why it works.** Water flows from a to b iff `h[a] >= h[b]`, so the reverse search from the ocean "
            "follows edges in the direction `h[next] >= h[cur]`. The set of cells reached is exactly the set that "
            "can drain to that ocean. Each cell is enqueued at most once per search.\n\n"
            "**Common mistakes:** using strictly greater instead of greater-or-equal (equal heights do flow); "
            "seeding the corner cells only once per ocean but forgetting that a corner belongs to both edges of one "
            "ocean (harmless) or to both oceans in a 1-row/1-column grid (also fine, the intersection handles it); "
            "forward simulation from every cell, which is O((mn)^2).\n\n"
            "**Interview follow-ups:** Diagonal flow allowed? (eight neighbours, same idea.) Three or more oceans? "
            "(one search per ocean, intersect all.) Count the cells instead of listing them? (same, return "
            "`len(both)`.) Why BFS rather than DFS here? (either is fine; BFS avoids recursion depth on a 200x200 "
            "grid.)"
        ),
        "complexity": {"time": "O(m * n)", "space": "O(m * n)"},
        "similar": ["number-of-islands", "surrounded-regions", "rotting-oranges"],
    },
    # --------------------------------------------------------- surrounded-regions
    {
        "id": "surrounded-regions",
        "title": "Surrounded Regions",
        "difficulty": "Medium",
        "pattern": "Graphs",
        "tags": ["Array", "DFS", "BFS", "Union Find", "Matrix"],
        "companies": {"google": 3, "apple": 1, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "You are given an `m x n` board of characters `\"X\"` and `\"O\"`. A region is a group of `\"O\"` "
            "cells connected horizontally or vertically. A region is **captured** if it is completely enclosed by "
            "`\"X\"`, meaning none of its cells lies on the border of the board.\n\n"
            "Flip every captured region to `\"X\"` **in place**. Regions that touch the border stay as they are. "
            "Do not return anything."
        ),
        "examples": [
            {"input": "board = [[\"X\",\"X\",\"X\"],[\"X\",\"O\",\"X\"],[\"X\",\"X\",\"X\"]]",
             "output": "[[\"X\",\"X\",\"X\"],[\"X\",\"X\",\"X\"],[\"X\",\"X\",\"X\"]]",
             "explanation": "The single O in the centre is fully enclosed."},
            {"input": "board = [[\"X\",\"O\",\"X\"],[\"X\",\"O\",\"X\"],[\"X\",\"X\",\"X\"]]",
             "output": "[[\"X\",\"O\",\"X\"],[\"X\",\"O\",\"X\"],[\"X\",\"X\",\"X\"]]",
             "explanation": "The O region reaches the top border, so it is not captured."},
            {"input": "board = [[\"O\",\"X\",\"X\",\"X\"],[\"X\",\"O\",\"O\",\"X\"],[\"X\",\"X\",\"O\",\"X\"],[\"X\",\"X\",\"X\",\"X\"]]",
             "output": "[[\"O\",\"X\",\"X\",\"X\"],[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"X\",\"X\",\"X\"]]"},
        ],
        "constraints": ["0 <= m, n <= 200", "board[i][j] is \"X\" or \"O\""],
        "hints": [
            "Deciding whether a region is enclosed while exploring it is awkward. Which regions are definitely NOT captured?",
            "Any O connected to a border O escapes. Flood-fill from every border O and mark what you reach with a temporary symbol.",
            "Afterwards, every remaining O is captured: turn it into X. Then turn the temporary marks back into O.",
        ],
        "function": "solve",
        "signature": "def solve(self, board: List[List[str]]) -> None:",
        "arg_types": {"board": "List[List[str]]"},
        "return_type": "None",
        "output_mode": "arg:board",
        "compare": "exact",
        "tests": [
            {"input": {"board": [["X", "X", "X"], ["X", "O", "X"], ["X", "X", "X"]]},
             "output": [["X", "X", "X"], ["X", "X", "X"], ["X", "X", "X"]]},
            {"input": {"board": [["X", "O", "X"], ["X", "O", "X"], ["X", "X", "X"]]},
             "output": [["X", "O", "X"], ["X", "O", "X"], ["X", "X", "X"]]},
            {"input": {"board": [["O", "X", "X", "X"], ["X", "O", "O", "X"], ["X", "X", "O", "X"], ["X", "X", "X", "X"]]},
             "output": [["O", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "X", "X", "X"]]},
            {"input": {"board": [["O", "O"], ["O", "O"]]}, "output": [["O", "O"], ["O", "O"]]},
            {"input": {"board": []}, "output": []},
            {"input": {"board": [["O"]]}, "output": [["O"]]},
            {"input": {"board": [["X"]]}, "output": [["X"]]},
            {"input": {"board": [["X", "X", "X", "X", "X"], ["X", "O", "X", "O", "X"], ["X", "O", "X", "X", "O"], ["X", "X", "X", "X", "X"]]},
             "output": [["X", "X", "X", "X", "X"], ["X", "X", "X", "X", "X"], ["X", "X", "X", "X", "O"], ["X", "X", "X", "X", "X"]]},
            {"input": {"board": [["X"] * 60 if r % 2 == 0 else ["X"] + ["O"] * 58 + ["X"] for r in range(61)]},
             "output": [["X"] * 60 for _ in range(61)]},
        ],
        "solution": '''class Solution:
    def solve(self, board: List[List[str]]) -> None:
        if not board or not board[0]:
            return
        m, n = len(board), len(board[0])

        def mark_safe(r: int, c: int) -> None:
            stack = [(r, c)]
            board[r][c] = "S"
            while stack:
                x, y = stack.pop()
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < m and 0 <= ny < n and board[nx][ny] == "O":
                        board[nx][ny] = "S"
                        stack.append((nx, ny))

        for r in range(m):
            for c in (0, n - 1):
                if board[r][c] == "O":
                    mark_safe(r, c)
        for c in range(n):
            for r in (0, m - 1):
                if board[r][c] == "O":
                    mark_safe(r, c)

        for r in range(m):
            for c in range(n):
                if board[r][c] == "O":
                    board[r][c] = "X"
                elif board[r][c] == "S":
                    board[r][c] = "O"
''',
        "approach": (
            "**Key insight: invert the question.** It is hard to know while exploring a region whether it will "
            "eventually touch the border, but it is trivial to find the regions that *do*: start from the border "
            "and flood inward. Everything not reached is captured.\n\n"
            "**Algorithm.** For every `O` on the four edges, flood-fill and relabel reachable `O`s with a "
            "sentinel such as `S`. Then sweep the board: `O` -> `X` (captured), `S` -> `O` (restored).\n\n"
            "**Why it works.** A region escapes capture iff it contains a border cell, iff it is reachable from "
            "some border `O` through `O` cells, which is exactly what the flood fill computes. The sentinel lets "
            "us distinguish safe from captured without a separate visited matrix.\n\n"
            "**Common mistakes:** trying to flood from interior cells and bail out when a border is touched "
            "(works but needs careful rollback); flipping to `X` during the border fill; forgetting the 1-row or "
            "1-column board where every cell is a border cell; recursive DFS depth on a 200x200 board of `O`s.\n\n"
            "**Interview follow-ups:** Union-find alternative? (union all adjacent `O`s and a virtual border "
            "node, then flip components not connected to it.) The board must not be modified during computation? "
            "(use a visited set and flip at the end only.) Count the captured cells instead of flipping? (same "
            "traversal, count the `O`s left after marking.)"
        ),
        "complexity": {"time": "O(m * n)", "space": "O(m * n) worst-case stack"},
        "similar": ["number-of-islands", "pacific-atlantic-water-flow", "number-of-enclaves"],
    },
    # ------------------------------------------------------------ rotting-oranges
    {
        "id": "rotting-oranges",
        "title": "Rotting Oranges",
        "difficulty": "Medium",
        "pattern": "Graphs",
        "tags": ["Array", "BFS", "Matrix"],
        "companies": {"google": 3, "apple": 3, "meta": 3, "amazon": 5, "microsoft": 3},
        "description": (
            "An `m x n` grid holds `0` (empty), `1` (fresh orange) or `2` (rotten orange). Every minute, each "
            "fresh orange that is 4-adjacent to a rotten one becomes rotten.\n\n"
            "Return the number of minutes until no fresh orange remains. If some fresh orange can never rot, "
            "return `-1`. A grid with no fresh oranges needs `0` minutes."
        ),
        "examples": [
            {"input": "grid = [[2,1,1],[1,1,0],[0,1,1]]", "output": "4",
             "explanation": "The rot spreads one ring per minute; the orange at (2,2) is the last to turn, after 4 minutes."},
            {"input": "grid = [[2,1,1],[0,1,1],[1,0,1]]", "output": "-1",
             "explanation": "The fresh orange at (2,0) is walled off by empty cells and never rots."},
            {"input": "grid = [[0,2]]", "output": "0", "explanation": "Nothing fresh to begin with."},
        ],
        "constraints": ["0 <= m, n <= 50", "grid[i][j] is 0, 1 or 2"],
        "hints": [
            "All rotten oranges spread simultaneously. Which traversal processes cells in order of distance from a set of sources?",
            "Multi-source BFS: enqueue every rotten orange at time 0, then expand level by level, each level being one minute.",
            "Count the fresh oranges up front; decrement as they rot. If the count is not zero at the end, return -1. The answer is the number of levels that actually rotted something.",
        ],
        "function": "orangesRotting",
        "signature": "def orangesRotting(self, grid: List[List[int]]) -> int:",
        "arg_types": {"grid": "List[List[int]]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"grid": [[2, 1, 1], [1, 1, 0], [0, 1, 1]]}, "output": 4},
            {"input": {"grid": [[2, 1, 1], [0, 1, 1], [1, 0, 1]]}, "output": -1},
            {"input": {"grid": [[0, 2]]}, "output": 0},
            {"input": {"grid": []}, "output": 0},
            {"input": {"grid": [[1]]}, "output": -1},
            {"input": {"grid": [[2]]}, "output": 0},
            {"input": {"grid": [[0]]}, "output": 0},
            {"input": {"grid": [[1, 2, 1]]}, "output": 1},
            {"input": {"grid": [[2, 0, 1]]}, "output": -1},
            {"input": {"grid": [[2] + [1] * 49] + [[1] * 50 for _ in range(49)]}, "output": 98},
            {"input": {"grid": [[2] + [1] * 49] + [[1] * 50 for _ in range(48)] + [[1] * 49 + [2]]}, "output": 49},
        ],
        "solution": '''class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0
        m, n = len(grid), len(grid[0])
        queue = deque()
        fresh = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1

        minutes = 0
        while queue and fresh:
            for _ in range(len(queue)):
                r, c = queue.popleft()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        queue.append((nr, nc))
            minutes += 1
        return minutes if fresh == 0 else -1
''',
        "approach": (
            "**Key insight: the minute an orange rots equals its shortest-path distance to the nearest "
            "initially rotten orange, so the answer is the largest such distance, which multi-source BFS computes "
            "directly.**\n\n"
            "**Algorithm.** Enqueue all rotten cells and count the fresh ones. Process the queue one level at a "
            "time (`for _ in range(len(queue))`), rotting fresh neighbours, decrementing the fresh counter, and "
            "incrementing `minutes` after each non-empty level. Stop when the queue empties or nothing fresh "
            "remains; return `minutes` if `fresh == 0`, else `-1`.\n\n"
            "**Why it works.** BFS from multiple sources explores cells in non-decreasing distance; each level is "
            "exactly one minute of simultaneous spreading. Marking a cell rotten when enqueued prevents double "
            "counting. Guarding the loop with `and fresh` avoids counting a final minute in which nothing changes.\n\n"
            "**Common mistakes:** returning `minutes` without checking for leftover fresh oranges; off-by-one "
            "when the grid has rotten but no fresh oranges (must return 0, not 1); running BFS separately from each "
            "rotten orange and taking a min per cell (correct but O(k * mn)).\n\n"
            "**Interview follow-ups:** Report the exact minute for every cell? (store the level in a distance "
            "grid instead of just the max; this is the Walls and Gates / 01-Matrix pattern.) Rotten oranges "
            "appear over time? (push them with their arrival time; a priority queue or buckets by time.) "
            "Diagonal spreading or a rot that takes different times per cell? (eight neighbours; Dijkstra when "
            "weights differ.)"
        ),
        "complexity": {"time": "O(m * n)", "space": "O(m * n)"},
        "similar": ["walls-and-gates", "01-matrix", "number-of-islands"],
    },
    # ------------------------------------------------------------ walls-and-gates
    {
        "id": "walls-and-gates",
        "title": "Distance to Nearest Gate",
        "difficulty": "Medium",
        "pattern": "Graphs",
        "tags": ["Array", "BFS", "Matrix"],
        "companies": {"google": 4, "meta": 3, "amazon": 2, "microsoft": 1},
        "description": (
            "You are given an `m x n` grid `rooms` with three kinds of cells: `-1` is a wall, `0` is a gate, and "
            "`INF = 2147483647` is an empty room.\n\n"
            "Fill every empty room **in place** with the number of steps to its nearest gate, moving only "
            "horizontally or vertically and never through walls. A room that cannot reach any gate keeps the value "
            "`INF`. Do not return anything."
        ),
        "examples": [
            {"input": "rooms = [[INF,0],[INF,INF]]", "output": "[[1,0],[2,1]]",
             "explanation": "(0,0) and (1,1) are one step from the gate; (1,0) is two steps away."},
            {"input": "rooms = [[0,-1,INF],[INF,INF,INF]]", "output": "[[0,-1,4],[1,2,3]]",
             "explanation": "The wall forces the path to (0,2) to go around through the second row."},
            {"input": "rooms = [[INF,-1],[-1,INF]]", "output": "[[INF,-1],[-1,INF]]",
             "explanation": "No gates at all, so every room keeps INF."},
        ],
        "constraints": ["0 <= m, n <= 250", "rooms[i][j] is -1, 0 or 2147483647"],
        "hints": [
            "Running BFS from every room to find its nearest gate is O((mn)^2). Flip it: where should the search start?",
            "Multi-source BFS from all gates simultaneously. The first time a room is reached, that distance is the minimum.",
            "Use the INF value itself as the 'unvisited' marker: only step into a neighbour whose value is still INF, and set it to current + 1.",
        ],
        "function": "wallsAndGates",
        "signature": "def wallsAndGates(self, rooms: List[List[int]]) -> None:",
        "arg_types": {"rooms": "List[List[int]]"},
        "return_type": "None",
        "output_mode": "arg:rooms",
        "compare": "exact",
        "tests": [
            {"input": {"rooms": [[INF, 0], [INF, INF]]}, "output": [[1, 0], [2, 1]]},
            {"input": {"rooms": [[0, -1, INF], [INF, INF, INF]]}, "output": [[0, -1, 4], [1, 2, 3]]},
            {"input": {"rooms": [[INF, -1], [-1, INF]]}, "output": [[INF, -1], [-1, INF]]},
            {"input": {"rooms": []}, "output": []},
            {"input": {"rooms": [[0]]}, "output": [[0]]},
            {"input": {"rooms": [[INF]]}, "output": [[INF]]},
            {"input": {"rooms": [[INF, INF, INF]]}, "output": [[INF, INF, INF]]},
            {"input": {"rooms": [[0, INF, INF], [INF, -1, INF], [INF, INF, 0]]}, "output": [[0, 1, 2], [1, -1, 1], [2, 1, 0]]},
            {"input": {"rooms": [[INF, -1, 0], [INF, -1, INF], [INF, -1, INF]]}, "output": [[INF, -1, 0], [INF, -1, 1], [INF, -1, 2]]},
            {"input": {"rooms": [[0 if r == c == 0 else INF for c in range(50)] for r in range(50)]},
             "output": [[r + c for c in range(50)] for r in range(50)]},
        ],
        "solution": '''class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        if not rooms or not rooms[0]:
            return
        INF = 2147483647
        m, n = len(rooms), len(rooms[0])
        queue = deque((r, c) for r in range(m) for c in range(n) if rooms[r][c] == 0)
        while queue:
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < m and 0 <= nc < n and rooms[nr][nc] == INF:
                    rooms[nr][nc] = rooms[r][c] + 1
                    queue.append((nr, nc))
''',
        "approach": (
            "**Key insight: a single BFS seeded with every gate computes, for each room, the distance to the "
            "closest gate, because BFS reaches cells in order of distance from the nearest source.**\n\n"
            "**Algorithm.** Put all gate cells in a queue. Pop `(r, c)`; for each neighbour still equal to `INF`, "
            "set it to `rooms[r][c] + 1` and enqueue it. Walls (`-1`) and already-filled rooms are never `INF`, so "
            "they are skipped automatically. No explicit level counter is needed because the distance is stored in "
            "the cell.\n\n"
            "**Why it works.** When a room is first dequeued-into, the popping cell is at the minimum distance d "
            "among all cells processed so far, so d + 1 is the room's true shortest distance. Overwriting `INF` on "
            "first touch doubles as the visited check.\n\n"
            "**Common mistakes:** BFS from each room independently (O((mn)^2)); using `<` comparison updates "
            "(Dijkstra-style) that are unnecessary for unit weights; forgetting walls; mutating `rooms` while "
            "iterating to collect the gates (collect first, then expand).\n\n"
            "**Interview follow-ups:** Same problem with a single gate and obstacles? (ordinary BFS.) The grid "
            "has weighted terrain? (Dijkstra with a heap.) Return, for each room, *which* gate is closest? (store "
            "the source id alongside the distance when enqueueing.) Rotting Oranges and 01 Matrix are the same "
            "template, can you point out the shared structure?"
        ),
        "complexity": {"time": "O(m * n)", "space": "O(m * n)"},
        "similar": ["rotting-oranges", "01-matrix", "shortest-path-in-binary-matrix"],
    },
    # ------------------------------------------------------------ course-schedule
    {
        "id": "course-schedule",
        "title": "Course Schedule",
        "difficulty": "Medium",
        "pattern": "Graphs",
        "tags": ["Graph", "Topological Sort", "DFS", "BFS"],
        "companies": {"google": 4, "apple": 3, "meta": 3, "amazon": 4, "microsoft": 3},
        "description": (
            "There are `numCourses` courses labelled `0` to `numCourses - 1`. The list `prerequisites` contains "
            "pairs `[a, b]` meaning course `b` must be completed **before** course `a`.\n\n"
            "Return `True` if it is possible to finish every course, `False` otherwise."
        ),
        "examples": [
            {"input": "numCourses = 2, prerequisites = [[1,0]]", "output": "true",
             "explanation": "Take 0, then 1."},
            {"input": "numCourses = 2, prerequisites = [[1,0],[0,1]]", "output": "false",
             "explanation": "Each course requires the other first: a cycle."},
        ],
        "constraints": ["1 <= numCourses <= 3000", "0 <= prerequisites.length <= 5000", "prerequisites[i] = [a, b] with a != b, no duplicate pairs"],
        "hints": [
            "Model courses as nodes and each prerequisite as a directed edge b -> a. What property of the graph makes the schedule impossible?",
            "A schedule exists iff the directed graph has no cycle. Detect cycles with DFS using three colours (unvisited / in progress / done) or with Kahn's algorithm.",
            "Kahn's: compute in-degrees, repeatedly remove nodes with in-degree 0. If you removed all numCourses nodes, there is no cycle.",
        ],
        "function": "canFinish",
        "signature": "def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:",
        "arg_types": {"numCourses": "int", "prerequisites": "List[List[int]]"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"numCourses": 2, "prerequisites": [[1, 0]]}, "output": True},
            {"input": {"numCourses": 2, "prerequisites": [[1, 0], [0, 1]]}, "output": False},
            {"input": {"numCourses": 1, "prerequisites": []}, "output": True},
            {"input": {"numCourses": 4, "prerequisites": []}, "output": True},
            {"input": {"numCourses": 3, "prerequisites": [[0, 1], [1, 2], [2, 0]]}, "output": False},
            {"input": {"numCourses": 5, "prerequisites": [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3]]}, "output": True},
            {"input": {"numCourses": 4, "prerequisites": [[1, 0], [2, 1], [3, 2], [1, 3]]}, "output": False},
            {"input": {"numCourses": 3000, "prerequisites": [[i + 1, i] for i in range(2999)]}, "output": True},
            {"input": {"numCourses": 3000, "prerequisites": [[i + 1, i] for i in range(2999)] + [[0, 2999]]}, "output": False},
        ],
        "solution": '''class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for course, prereq in prerequisites:
            graph[prereq].append(course)
            indegree[course] += 1

        queue = deque(i for i in range(numCourses) if indegree[i] == 0)
        taken = 0
        while queue:
            node = queue.popleft()
            taken += 1
            for nxt in graph[node]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
        return taken == numCourses
''',
        "approach": (
            "**Key insight: the courses can all be taken iff the prerequisite graph is a DAG.** A cycle means some "
            "course transitively requires itself; with no cycle a topological order is a valid schedule.\n\n"
            "**Algorithm (Kahn's).** Build adjacency `prereq -> course` and an in-degree array. Enqueue every node "
            "with in-degree 0. Pop a node, count it as taken, and decrement each successor's in-degree, enqueueing it "
            "when it reaches 0. Return whether the number taken equals `numCourses`.\n\n"
            "**Why it works.** A node with in-degree 0 has all prerequisites satisfied. If a cycle exists, none of "
            "its members ever reaches in-degree 0, so they are never counted. Conversely a DAG always has a node of "
            "in-degree 0, and removing it leaves a DAG, so every node is eventually counted.\n\n"
            "**Common mistakes:** reversing the edge direction (still detects cycles, but gives the wrong order "
            "in Course Schedule II); DFS cycle detection with only a boolean visited array (cannot distinguish a "
            "back-edge from a cross-edge; you need the three-state colouring); ignoring courses with no "
            "prerequisites at all.\n\n"
            "**Interview follow-ups:** Return the actual order? (Course Schedule II, record nodes as they are "
            "popped.) Minimum number of semesters if any number of courses can be taken in parallel? (depth of the "
            "DAG, i.e. the number of BFS levels.) Find and print one cycle when the answer is False? (DFS with a "
            "parent stack.) DFS version? (grey/black colouring, return False on hitting a grey node.)"
        ),
        "complexity": {"time": "O(V + E)", "space": "O(V + E)"},
        "similar": ["course-schedule-ii", "graph-valid-tree", "alien-dictionary"],
    },
    # --------------------------------------------------------- course-schedule-ii
    {
        "id": "course-schedule-ii",
        "title": "Course Schedule II",
        "difficulty": "Medium",
        "pattern": "Graphs",
        "tags": ["Graph", "Topological Sort", "DFS", "BFS"],
        "companies": {"google": 4, "apple": 2, "meta": 3, "amazon": 4, "microsoft": 3},
        "description": (
            "There are `numCourses` courses labelled `0` to `numCourses - 1`, and `prerequisites` lists pairs "
            "`[a, b]` meaning `b` must be taken before `a`.\n\n"
            "Return **an order** in which all courses can be taken. If several orders are valid, any one is "
            "accepted. If no valid order exists (the prerequisites contain a cycle), return an empty list."
        ),
        "examples": [
            {"input": "numCourses = 2, prerequisites = [[1,0]]", "output": "[0,1]"},
            {"input": "numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]", "output": "[0,1,2,3]",
             "explanation": "0 first, then 1 and 2 in either order, then 3. [0,2,1,3] is also accepted."},
            {"input": "numCourses = 2, prerequisites = [[1,0],[0,1]]", "output": "[]",
             "explanation": "The two courses require each other."},
        ],
        "constraints": ["1 <= numCourses <= 3000", "0 <= prerequisites.length <= 5000", "prerequisites[i] = [a, b] with a != b, no duplicate pairs"],
        "hints": [
            "This is Course Schedule plus recording the order in which nodes become available.",
            "Kahn's algorithm: nodes leave the queue in a valid topological order. Append each popped node to the result.",
            "If the result is shorter than numCourses at the end, a cycle blocked some courses: return [] instead.",
        ],
        "function": "findOrder",
        "signature": "def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:",
        "arg_types": {"numCourses": "int", "prerequisites": "List[List[int]]"},
        "return_type": "List[int]",
        "compare": "any_of",
        "tests": [
            {"input": {"numCourses": 2, "prerequisites": [[1, 0]]}, "output": [[0, 1]]},
            {"input": {"numCourses": 4, "prerequisites": [[1, 0], [2, 0], [3, 1], [3, 2]]}, "output": [[0, 1, 2, 3], [0, 2, 1, 3]]},
            {"input": {"numCourses": 2, "prerequisites": [[1, 0], [0, 1]]}, "output": [[]]},
            {"input": {"numCourses": 1, "prerequisites": []}, "output": [[0]]},
            {"input": {"numCourses": 3, "prerequisites": []}, "output": [list(p) for p in itertools.permutations(range(3))]},
            {"input": {"numCourses": 3, "prerequisites": [[2, 0], [2, 1]]}, "output": [[0, 1, 2], [1, 0, 2]]},
            {"input": {"numCourses": 3, "prerequisites": [[0, 1], [1, 2], [2, 0]]}, "output": [[]]},
            {"input": {"numCourses": 4, "prerequisites": [[3, 2], [2, 1], [1, 0]]}, "output": [[0, 1, 2, 3]]},
            {"input": {"numCourses": 3000, "prerequisites": [[i + 1, i] for i in range(2999)]}, "output": [list(range(3000))]},
        ],
        "solution": '''class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        graph = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for course, prereq in prerequisites:
            graph[prereq].append(course)
            indegree[course] += 1

        queue = deque(i for i in range(numCourses) if indegree[i] == 0)
        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for nxt in graph[node]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
        return order if len(order) == numCourses else []
''',
        "approach": (
            "**Key insight: a topological order of the prerequisite DAG is exactly a valid schedule, and "
            "Kahn's algorithm produces one while simultaneously detecting cycles.**\n\n"
            "**Algorithm.** Build `prereq -> course` adjacency and in-degrees. Seed a queue with in-degree-0 "
            "nodes. Pop, append to `order`, decrement successors, enqueue those that hit 0. If `len(order) == "
            "numCourses` return it, else return `[]`.\n\n"
            "**Why it works.** A node is appended only after all its predecessors have been appended (its "
            "in-degree reached 0), so every edge points forward in `order`. Nodes on or downstream of a cycle never "
            "reach in-degree 0, which is why a short `order` signals a cycle.\n\n"
            "**Common mistakes:** returning a partial order instead of `[]` on a cycle; building edges in the "
            "wrong direction and then forgetting to reverse the output; using a DFS post-order but forgetting to "
            "reverse it (post-order is the *reverse* of a topological order).\n\n"
            "**Interview follow-ups:** Lexicographically smallest order? (replace the queue with a min-heap.) "
            "Is the order unique? (yes iff the queue never holds more than one node at a time.) Group courses into "
            "the fewest semesters? (each BFS level is a semester.) DFS alternative? (three-colour DFS, push on "
            "finish, reverse at the end.)"
        ),
        "complexity": {"time": "O(V + E)", "space": "O(V + E)"},
        "similar": ["course-schedule", "alien-dictionary", "parallel-courses"],
    },
    # ----------------------------------------------------------- graph-valid-tree
    {
        "id": "graph-valid-tree",
        "title": "Graph Valid Tree",
        "difficulty": "Medium",
        "pattern": "Graphs",
        "tags": ["Graph", "Union Find", "DFS", "BFS"],
        "companies": {"google": 4, "meta": 3, "amazon": 2, "microsoft": 1},
        "description": (
            "You are given `n` nodes labelled `0` to `n - 1` and a list of undirected `edges`. Decide whether "
            "these edges form a **tree**: a graph that is connected and contains no cycle.\n\n"
            "Return `True` if the graph is a valid tree, `False` otherwise."
        ),
        "examples": [
            {"input": "n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]", "output": "true"},
            {"input": "n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]", "output": "false",
             "explanation": "1-2-3-1 is a cycle."},
            {"input": "n = 4, edges = [[0,1],[2,3]]", "output": "false",
             "explanation": "No cycle, but the graph is disconnected."},
        ],
        "constraints": ["1 <= n <= 3000", "0 <= edges.length <= 5000", "No self-loops or duplicate edges"],
        "hints": [
            "A tree on n nodes has exactly n - 1 edges. Is that condition alone sufficient?",
            "With exactly n - 1 edges, the graph is a tree iff it is connected (equivalently, iff it is acyclic). Check one of the two.",
            "Union-find: for each edge, if both endpoints already share a root there is a cycle. Otherwise union. Finish by checking every edge merged two different components, or that one component remains.",
        ],
        "function": "validTree",
        "signature": "def validTree(self, n: int, edges: List[List[int]]) -> bool:",
        "arg_types": {"n": "int", "edges": "List[List[int]]"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"n": 5, "edges": [[0, 1], [0, 2], [0, 3], [1, 4]]}, "output": True},
            {"input": {"n": 5, "edges": [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]}, "output": False},
            {"input": {"n": 4, "edges": [[0, 1], [2, 3]]}, "output": False},
            {"input": {"n": 1, "edges": []}, "output": True},
            {"input": {"n": 2, "edges": []}, "output": False},
            {"input": {"n": 2, "edges": [[0, 1]]}, "output": True},
            {"input": {"n": 3, "edges": [[0, 1], [1, 2], [0, 2]]}, "output": False},
            {"input": {"n": 3000, "edges": [[i, i + 1] for i in range(2999)]}, "output": True},
            {"input": {"n": 3000, "edges": [[i, i + 1] for i in range(2998)] + [[0, 2998]]}, "output": False},
        ],
        "solution": '''class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            parent[ra] = rb
        return True
''',
        "approach": (
            "**Key insight: a graph on n nodes is a tree iff it has exactly n - 1 edges and no cycle (or, "
            "equivalently, n - 1 edges and is connected).** Checking the edge count first lets a single pass of "
            "union-find settle the rest.\n\n"
            "**Algorithm.** If `len(edges) != n - 1` return False. Initialise union-find over `n` nodes. For each "
            "edge, find both roots; if they coincide the edge closes a cycle, return False; otherwise union them. If "
            "all edges are processed, return True.\n\n"
            "**Why it works.** n - 1 edges with no cycle means every edge merged two components, so the component "
            "count went from n to 1: connected and acyclic. Path halving in `find` keeps operations near O(1) "
            "amortised even without union by rank.\n\n"
            "**Common mistakes:** checking connectivity but not the edge count (a connected graph with a cycle "
            "passes); DFS cycle detection on an undirected graph that forgets to ignore the edge back to the parent; "
            "treating `n = 1, edges = []` as invalid.\n\n"
            "**Interview follow-ups:** Which edge, if any, would you remove to make it a tree? (Redundant "
            "Connection.) Count the components instead? (same union-find, stop early.) BFS/DFS version? (traverse "
            "from 0 with a parent pointer, fail on a visited non-parent neighbour, then check all nodes visited.) "
            "How does this change for a directed rooted tree? (every node except the root has in-degree exactly 1, "
            "plus reachability from the root.)"
        ),
        "complexity": {"time": "O(n + E * alpha(n)) ~ O(n + E)", "space": "O(n)"},
        "similar": ["number-of-connected-components-in-an-undirected-graph", "redundant-connection", "course-schedule"],
    },
    # ------------------------------- number-of-connected-components-in-an-undirected-graph
    {
        "id": "number-of-connected-components-in-an-undirected-graph",
        "title": "Number of Connected Components in an Undirected Graph",
        "difficulty": "Medium",
        "pattern": "Graphs",
        "tags": ["Graph", "Union Find", "DFS", "BFS"],
        "companies": {"google": 4, "apple": 1, "meta": 3, "amazon": 3, "microsoft": 2},
        "description": (
            "You are given `n` nodes labelled `0` to `n - 1` and an undirected edge list `edges`. "
            "Return the number of connected components, i.e. the number of groups of nodes that are mutually "
            "reachable. An isolated node counts as its own component."
        ),
        "examples": [
            {"input": "n = 5, edges = [[0,1],[1,2],[3,4]]", "output": "2",
             "explanation": "{0,1,2} and {3,4}."},
            {"input": "n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]", "output": "1"},
            {"input": "n = 4, edges = []", "output": "4"},
        ],
        "constraints": ["1 <= n <= 3000", "0 <= edges.length <= 5000", "No self-loops or duplicate edges"],
        "hints": [
            "Start with n separate components. What happens to the count each time an edge joins two different components?",
            "Union-find: for each edge, if the endpoints have different roots, union them and decrement the count. Edges within a component change nothing.",
            "Alternatively build an adjacency list and run DFS/BFS from each unvisited node, counting the starts.",
        ],
        "function": "countComponents",
        "signature": "def countComponents(self, n: int, edges: List[List[int]]) -> int:",
        "arg_types": {"n": "int", "edges": "List[List[int]]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"n": 5, "edges": [[0, 1], [1, 2], [3, 4]]}, "output": 2},
            {"input": {"n": 5, "edges": [[0, 1], [1, 2], [2, 3], [3, 4]]}, "output": 1},
            {"input": {"n": 4, "edges": []}, "output": 4},
            {"input": {"n": 1, "edges": []}, "output": 1},
            {"input": {"n": 3, "edges": [[0, 1], [1, 2], [0, 2]]}, "output": 1},
            {"input": {"n": 6, "edges": [[0, 1], [2, 3], [4, 5], [1, 3]]}, "output": 2},
            {"input": {"n": 3000, "edges": [[i, i + 1] for i in range(0, 3000, 2)]}, "output": 1500},
            {"input": {"n": 3000, "edges": [[i, (i + 1) % 3000] for i in range(3000)]}, "output": 1},
        ],
        "solution": '''class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        parent = list(range(n))
        size = [1] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        components = n
        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:
                continue
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            components -= 1
        return components
''',
        "approach": (
            "**Key insight: every edge that connects two previously separate components reduces the component "
            "count by exactly one; edges inside a component change nothing.** Union-find tracks this with near "
            "constant work per edge.\n\n"
            "**Algorithm.** Start with `components = n`, each node its own root. For each edge, find both roots; if "
            "different, attach the smaller tree under the larger (union by size), and decrement the count. Return "
            "the count.\n\n"
            "**Why it works.** The invariant \"count equals the number of distinct roots\" holds initially and is "
            "preserved by every union. Path halving plus union by size gives O(alpha(n)) amortised per operation.\n\n"
            "**Common mistakes:** forgetting that nodes without any edge still count; recursive `find` without "
            "compression on a long chain (deep recursion, O(n) per find); counting edges instead of successful "
            "unions.\n\n"
            "**Interview follow-ups:** Edges arrive online and you must answer the count after each? (union-find "
            "is the natural fit; DFS would be O(n) per query.) Also need the size of the largest component? (keep "
            "the size array.) Support edge deletions? (much harder; offline reversal or dynamic connectivity "
            "structures.) DFS version? (adjacency list, count unvisited starts, O(V + E).)"
        ),
        "complexity": {"time": "O(n + E * alpha(n))", "space": "O(n)"},
        "similar": ["graph-valid-tree", "number-of-islands", "redundant-connection"],
    },
    # ------------------------------------------------------- redundant-connection
    {
        "id": "redundant-connection",
        "title": "Redundant Connection",
        "difficulty": "Medium",
        "pattern": "Graphs",
        "tags": ["Graph", "Union Find", "DFS"],
        "companies": {"google": 3, "meta": 2, "amazon": 2, "microsoft": 1},
        "description": (
            "A tree with `n` nodes labelled `1` to `n` had **one extra edge** added between two distinct nodes "
            "that were already connected. You are given the resulting `n` edges in some order.\n\n"
            "Return an edge whose removal turns the graph back into a tree. If more than one edge qualifies, "
            "return the one that appears **last** in the input."
        ),
        "examples": [
            {"input": "edges = [[1,2],[2,3],[1,3]]", "output": "[1,3]",
             "explanation": "All three edges lie on the cycle; the last one listed is [1,3]."},
            {"input": "edges = [[1,2],[1,3],[1,4],[3,4]]", "output": "[3,4]",
             "explanation": "The cycle is 1-3-4-1; of its edges, [3,4] comes last."},
        ],
        "constraints": ["3 <= n <= 3000", "edges.length == n", "1 <= a < b <= n, no duplicate edges"],
        "hints": [
            "Process the edges in the given order. The first edge whose endpoints are already connected closes the cycle.",
            "Because every earlier edge is part of a forest, that edge is on the unique cycle and is the last cycle edge in input order, exactly what is asked for.",
            "Union-find with path compression makes each check near O(1). Nodes are 1-indexed, so allocate n + 1 slots.",
        ],
        "function": "findRedundantConnection",
        "signature": "def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:",
        "arg_types": {"edges": "List[List[int]]"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"edges": [[1, 2], [2, 3], [1, 3]]}, "output": [1, 3]},
            {"input": {"edges": [[1, 2], [1, 3], [1, 4], [3, 4]]}, "output": [3, 4]},
            {"input": {"edges": [[2, 3], [3, 4], [2, 4], [1, 2]]}, "output": [2, 4]},
            {"input": {"edges": [[1, 4], [2, 4], [3, 4], [1, 3]]}, "output": [1, 3]},
            {"input": {"edges": [[1, 2], [2, 3], [3, 4], [4, 5], [1, 5]]}, "output": [1, 5]},
            {"input": {"edges": [[1, 2], [2, 3], [1, 3], [3, 4], [4, 5]]}, "output": [1, 3]},
            {"input": {"edges": [[i, i + 1] for i in range(1, 3000)] + [[1, 3000]]}, "output": [1, 3000]},
        ],
        "solution": '''class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        parent = list(range(len(edges) + 1))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:
                return [a, b]
            parent[ra] = rb
        return []
''',
        "approach": (
            "**Key insight: scanning edges in input order, the first edge that joins two already-connected "
            "nodes is the answer.** Up to that point the edges form a forest; adding this edge creates the one and "
            "only cycle, and every other cycle edge appeared earlier, so this edge is the last cycle edge in the "
            "input, which is precisely the tie-break rule.\n\n"
            "**Algorithm.** Union-find over `1..n`. For each `[a, b]`: if `find(a) == find(b)` return `[a, b]`; "
            "else union. The input guarantees an answer exists.\n\n"
            "**Why it works.** A tree plus one edge has exactly one cycle. The cycle is closed at the moment its "
            "last edge (in input order) is processed, and union-find detects that moment exactly.\n\n"
            "**Common mistakes:** off-by-one from 1-indexed nodes; trying to find the cycle with DFS and then "
            "picking the max-index edge by hand (correct but much more code); returning the first edge of the cycle "
            "rather than the last.\n\n"
            "**Interview follow-ups:** Directed version (Redundant Connection II)? (two cases: a node with two "
            "parents, or a pure cycle; try removing each candidate edge.) Multiple extra edges? (return all edges "
            "that close a cycle during the scan; each is removable, but together they may not be the unique minimal "
            "set.) Why is the expected output well-defined? (because the cycle is unique, the last edge on it is "
            "unique.)"
        ),
        "complexity": {"time": "O(n * alpha(n))", "space": "O(n)"},
        "similar": ["graph-valid-tree", "number-of-connected-components-in-an-undirected-graph", "redundant-connection-ii"],
    },
    # ---------------------------------------------------------------- word-ladder
    {
        "id": "word-ladder",
        "title": "Word Ladder",
        "difficulty": "Hard",
        "pattern": "Graphs",
        "tags": ["Hash Table", "String", "BFS"],
        "companies": {"google": 4, "apple": 2, "meta": 3, "amazon": 4, "microsoft": 3},
        "description": (
            "A transformation sequence from `beginWord` to `endWord` is a list of words "
            "`beginWord -> w1 -> w2 -> ... -> endWord` where consecutive words differ in **exactly one letter** "
            "and every word after `beginWord` belongs to `wordList`.\n\n"
            "Return the **number of words** in the shortest such sequence (counting both ends), or `0` if no "
            "sequence exists. All words have the same length and consist of lowercase letters."
        ),
        "examples": [
            {"input": "beginWord = \"cat\", endWord = \"dog\", wordList = [\"cot\",\"cog\",\"dog\",\"cat\"]",
             "output": "4", "explanation": "cat -> cot -> cog -> dog uses 4 words. No 3-word chain exists because cat and dog differ in all three positions."},
            {"input": "beginWord = \"cat\", endWord = \"dog\", wordList = [\"cot\",\"cog\",\"cat\"]",
             "output": "0", "explanation": "endWord is not in the list, so no sequence can end there."},
            {"input": "beginWord = \"a\", endWord = \"c\", wordList = [\"a\",\"b\",\"c\"]", "output": "2"},
        ],
        "constraints": ["1 <= beginWord.length <= 10", "1 <= wordList.length <= 5000", "beginWord != endWord", "All words have the same length and are lowercase"],
        "hints": [
            "Words are nodes; an edge joins two words differing in one letter. Shortest path in an unweighted graph means BFS.",
            "Generating neighbours by comparing every pair of words is O(N^2 * L). Instead, for the current word try all L * 26 single-letter replacements and look them up in a set.",
            "Remove a word from the set when you enqueue it so it is never visited twice. Count BFS levels starting at 1 for beginWord.",
        ],
        "function": "ladderLength",
        "signature": "def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:",
        "arg_types": {"beginWord": "str", "endWord": "str", "wordList": "List[str]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"beginWord": "cat", "endWord": "dog", "wordList": ["cot", "cog", "dog", "cat"]}, "output": 4},
            {"input": {"beginWord": "cat", "endWord": "dog", "wordList": ["cot", "cog", "cat"]}, "output": 0},
            {"input": {"beginWord": "a", "endWord": "c", "wordList": ["a", "b", "c"]}, "output": 2},
            {"input": {"beginWord": "ab", "endWord": "cd", "wordList": ["ad", "bd", "cd"]}, "output": 3},
            {"input": {"beginWord": "aa", "endWord": "bb", "wordList": ["ab", "bb"]}, "output": 3},
            {"input": {"beginWord": "ab", "endWord": "cd", "wordList": ["cd", "ef"]}, "output": 0},
            {"input": {"beginWord": "red", "endWord": "tax", "wordList": ["ted", "tex", "tad", "tax", "den", "rex", "pee"]}, "output": 4},
            {"input": {"beginWord": "aaa", "endWord": "ppp",
                       "wordList": ["".join(w) for w in itertools.product("abcdefghijklmnop", repeat=3)]}, "output": 4},
            {"input": {"beginWord": "aaa", "endWord": "zzz",
                       "wordList": ["".join(w) for w in itertools.product("abcdefghijklmnop", repeat=3)] + ["zzz"]}, "output": 0},
        ],
        "solution": '''class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        words = set(wordList)
        if endWord not in words:
            return 0
        words.discard(beginWord)
        queue = deque([beginWord])
        steps = 1
        while queue:
            for _ in range(len(queue)):
                word = queue.popleft()
                if word == endWord:
                    return steps
                for i in range(len(word)):
                    for ch in "abcdefghijklmnopqrstuvwxyz":
                        if ch == word[i]:
                            continue
                        candidate = word[:i] + ch + word[i + 1:]
                        if candidate in words:
                            words.remove(candidate)
                            queue.append(candidate)
            steps += 1
        return 0
''',
        "approach": (
            "**Key insight: this is single-source shortest path on an implicit unweighted graph, so BFS gives the "
            "answer, and neighbours are enumerated by mutating one letter at a time rather than by comparing word "
            "pairs.**\n\n"
            "**Algorithm.** Put `wordList` in a set; return 0 if `endWord` is missing. BFS level by level from "
            "`beginWord` with `steps = 1`. For each popped word, if it is `endWord` return `steps`; otherwise for each "
            "position and each of the 25 other letters, form the candidate, and if it is in the set remove it and "
            "enqueue it. Increment `steps` after each level.\n\n"
            "**Why it works.** Each level contains all words reachable in exactly `steps - 1` substitutions and not "
            "earlier, so the first time `endWord` is popped we have the shortest chain. Removing words on enqueue "
            "is the visited set and ensures O(1) work per word per neighbour attempt.\n\n"
            "**Common mistakes:** building the adjacency by comparing all pairs (O(N^2 L), too slow for 5000 "
            "words); checking `endWord` when enqueueing but forgetting the case `beginWord` is one step away; "
            "returning the number of *edges* instead of words; not handling `endWord` absent from the list.\n\n"
            "**Interview follow-ups:** Return all shortest sequences (Word Ladder II)? (BFS recording parents per "
            "level, then DFS backwards.) Speed it up? (bidirectional BFS, expanding the smaller frontier; or "
            "pattern buckets like `h*t` to precompute neighbours in O(N L).) Letters with different costs? "
            "(Dijkstra.) What is the branching factor and how does it bound the complexity? (L * 25 candidates per "
            "word, each O(L) to build and hash, so O(N * L^2) total.)"
        ),
        "complexity": {"time": "O(N * L^2) where N = len(wordList), L = word length", "space": "O(N * L)"},
        "similar": ["word-ladder-ii", "minimum-genetic-mutation", "open-the-lock"],
    },
]
