"""Heap / Priority Queue pattern. See SCHEMA.md for the dict format."""

# (i * 7919) % 10007 for i in range(10007) is a permutation of 0..10006 because 10007 is prime.
_PERM_10007 = [(i * 7919) % 10007 for i in range(10007)]
# Likewise 5003 is prime, so this is a permutation of 0..5002.
_PERM_5003 = [(i * 7919) % 5003 for i in range(5003)]

# 3000 words; word w{i} appears (i % 7) + 1 times, so the most frequent (7 times) are i = 6, 13, 20, ...
_FREQ_WORDS = [f"w{i:04d}" for i in range(3000) for _ in range(i % 7 + 1)]


PROBLEMS = [
    # ------------------------------------------------------------------ 1
    {
        "id": "kth-largest-element-in-an-array",
        "title": "Kth Largest Element in an Array",
        "difficulty": "Medium",
        "pattern": "Heap / Priority Queue",
        "tags": ["Array", "Heap", "Quickselect", "Divide and Conquer"],
        "companies": {"google": 3, "apple": 3, "meta": 5, "amazon": 4, "microsoft": 3},
        "description": (
            "Given an integer array `nums` and an integer `k`, return the `k`-th largest element **in sorted "
            "order**, counting duplicates. For `[3,3,1]` and `k = 2` the answer is `3`, not `1`.\n\n"
            "Can you do better than sorting the whole array?"
        ),
        "examples": [
            {"input": "nums = [3,2,1,5,6,4], k = 2", "output": "5", "explanation": "Sorted descending: 6, 5, 4, ... The second is 5."},
            {"input": "nums = [3,2,3,1,2,4,5,5,6], k = 4", "output": "4", "explanation": "Descending: 6, 5, 5, 4, ... The fourth is 4."},
        ],
        "constraints": ["1 <= k <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "hints": [
            "Sorting is O(n log n). You only care about the top k, not the order of the rest.",
            "Keep a min-heap of the k largest values seen so far. Its root is the k-th largest.",
            "For each new value, if it beats the heap root, replace the root. That is O(n log k). Quickselect gives O(n) average.",
        ],
        "function": "findKthLargest",
        "signature": "def findKthLargest(self, nums: List[int], k: int) -> int:",
        "arg_types": {"nums": "List[int]", "k": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [3, 2, 1, 5, 6, 4], "k": 2}, "output": 5},
            {"input": {"nums": [3, 2, 3, 1, 2, 4, 5, 5, 6], "k": 4}, "output": 4},
            {"input": {"nums": [1], "k": 1}, "output": 1},
            {"input": {"nums": [-1, -2, -3], "k": 1}, "output": -1},
            {"input": {"nums": [-1, -2, -3], "k": 3}, "output": -3},
            {"input": {"nums": [2, 2, 2, 2], "k": 3}, "output": 2},
            {"input": {"nums": [5, 1], "k": 2}, "output": 1},
            {"input": {"nums": _PERM_10007, "k": 5}, "output": 10002},
            {"input": {"nums": _PERM_10007, "k": 10007}, "output": 0},
            {"input": {"nums": _PERM_10007, "k": 1}, "output": 10006},
        ],
        "solution": '''class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []  # min-heap holding the k largest values seen so far
        for x in nums:
            if len(heap) < k:
                heappush(heap, x)
            elif x > heap[0]:
                heapq.heapreplace(heap, x)
        return heap[0]
''',
        "approach": (
            "**Keep only the k largest values in a min-heap; its smallest element is the k-th largest overall.** "
            "Scan the array once. While the heap has fewer than k items, push. Afterwards, a new value matters only "
            "if it is bigger than the heap's root (the current k-th largest); if so, replace the root. When the "
            "scan ends the root is the answer.\n\n"
            "**Why it works:** at every moment the heap holds the k largest values seen so far. A value smaller "
            "than or equal to the root cannot enter the top k, and a larger one evicts exactly the one that falls "
            "out. Duplicates are handled naturally because they are stored as separate entries.\n\n"
            "**Quickselect alternative:** partition around a pivot as in quicksort, but recurse into only the side "
            "that contains index `n - k`. Average O(n), worst case O(n^2) unless the pivot is random or "
            "median-of-medians. Interviewers often want this discussed, and a few want it implemented; be ready "
            "for both. With values bounded by 10^4 a counting sort is also O(n + range).\n\n"
            "**Common mistakes:** using a max-heap of all n elements and popping k times (O(n + k log n), correct "
            "but misses the point); confusing k-th largest with k-th distinct; building the heap with "
            "`heapq.nlargest(k, nums)[-1]`, which is fine in Python but should be explained, not hidden behind.\n\n"
            "**Interview follow-ups:** streaming version (kth-largest-element-in-a-stream, same heap); k-th "
            "smallest (max-heap or flip signs); when is quickselect preferable (k close to n/2, data in memory, "
            "mutation allowed); k-th largest in a sorted matrix or across two sorted arrays."
        ),
        "complexity": {"time": "O(n log k)", "space": "O(k)"},
        "similar": ["kth-largest-element-in-a-stream", "top-k-frequent-elements", "k-closest-points-to-origin"],
    },
    # ------------------------------------------------------------------ 2
    {
        "id": "kth-largest-element-in-a-stream",
        "title": "Kth Largest Element in a Stream",
        "difficulty": "Easy",
        "pattern": "Heap / Priority Queue",
        "tags": ["Heap", "Design", "Data Stream"],
        "companies": {"google": 2, "apple": 2, "meta": 2, "amazon": 4, "microsoft": 2},
        "kind": "design",
        "class_name": "KthLargest",
        "description": (
            "Design a class that tracks the `k`-th largest value in a growing stream of integers, counting duplicates.\n\n"
            "- `KthLargest(k, nums)` initialises the structure with the integers already seen (`nums` may be empty "
            "or shorter than `k`).\n"
            "- `add(val)` appends `val` to the stream and returns the current `k`-th largest value.\n\n"
            "It is guaranteed that at least `k` values have been seen by the time `add` returns."
        ),
        "examples": [
            {"input": "[\"KthLargest\",\"add\",\"add\",\"add\",\"add\",\"add\"]\n[[3,[4,5,8,2]],[3],[5],[10],[9],[4]]",
             "output": "[null,4,5,5,8,8]",
             "explanation": "After adding 3 the stream is [4,5,8,2,3]; the three largest are 8,5,4 so the answer is 4. "
                            "Adding 5 makes the top three 8,5,5. Adding 10: 10,8,5. Adding 9: 10,9,8. Adding 4 changes nothing."},
        ],
        "constraints": [
            "1 <= k <= 10^4",
            "0 <= nums.length <= 10^4",
            "-10^4 <= nums[i], val <= 10^4",
            "At most 10^4 calls to add.",
        ],
        "hints": [
            "You never need to remember anything that is not among the k largest.",
            "Keep a min-heap of size k. Its root is the k-th largest.",
            "On add: push the value, then pop the smallest if the heap has grown past k. Return the root.",
        ],
        "starter": (
            "class KthLargest:\n"
            "    def __init__(self, k: int, nums: List[int]):\n"
            "        pass\n\n"
            "    def add(self, val: int) -> int:\n"
            "        pass\n"
        ),
        "compare": "exact",
        "tests": [
            {"input": {"ops": [["KthLargest", [3, [4, 5, 8, 2]]], ["add", [3]], ["add", [5]], ["add", [10]], ["add", [9]], ["add", [4]]]},
             "output": [None, 4, 5, 5, 8, 8]},
            {"input": {"ops": [["KthLargest", [1, []]], ["add", [-3]], ["add", [-2]], ["add", [-4]], ["add", [0]], ["add", [4]]]},
             "output": [None, -3, -2, -2, 0, 4]},
            {"input": {"ops": [["KthLargest", [2, [0]]], ["add", [-1]], ["add", [1]], ["add", [-2]], ["add", [-4]], ["add", [3]]]},
             "output": [None, -1, 0, 0, 0, 1]},
            {"input": {"ops": [["KthLargest", [3, [5, 5, 5]]], ["add", [5]], ["add", [6]], ["add", [7]], ["add", [8]]]},
             "output": [None, 5, 5, 5, 6]},
            {"input": {"ops": [["KthLargest", [2, [9, 1, 8]]], ["add", [0]], ["add", [10]]]},
             "output": [None, 8, 9]},
            {"input": {"ops": [["KthLargest", [100, list(range(5000))]], ["add", [10000]], ["add", [-1]], ["add", [5000]]]
                              + [["add", [-5]]] * 3000},
             "output": [None, 4901, 4901, 4902] + [4902] * 3000},
        ],
        "solution": '''class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = list(nums)       # min-heap of the k largest values seen
        heapify(self.heap)
        while len(self.heap) > k:
            heappop(self.heap)

    def add(self, val: int) -> int:
        if len(self.heap) < self.k:
            heappush(self.heap, val)
        else:
            heappushpop(self.heap, val)  # push val, then pop the smallest
        return self.heap[0]
''',
        "approach": (
            "**A min-heap of exactly k elements whose root is the answer.** Anything smaller than the k largest "
            "values can never become the k-th largest again, because the stream only grows, so it is safe to throw "
            "it away. The constructor heapifies the initial values and pops down to k. Each `add` pushes the new "
            "value and, if the heap exceeds k, pops the minimum; `heappushpop` does both in one step.\n\n"
            "**Why it works:** invariant: the heap contains the k largest values seen so far. Push-then-pop "
            "maintains it: if the new value is smaller than the root it is popped straight back out, otherwise the "
            "old root (no longer in the top k) leaves.\n\n"
            "**Common mistakes:** using a max-heap of everything and peeking k deep (O(n) per query); sorting on "
            "every add (O(n log n) per query, which the 3000-add test exposes); forgetting that `nums` can be "
            "shorter than k so the heap may still be filling up during the first few adds.\n\n"
            "**Interview follow-ups:** k-th smallest in a stream (max-heap or negate); removing values from the "
            "stream (lazy deletion with a counter, or a balanced BST / sorted container); sliding window k-th "
            "largest; the median of a stream, which needs two heaps (find-median-from-data-stream)."
        ),
        "complexity": {"time": "O(n log k) to build, O(log k) per add", "space": "O(k)"},
        "similar": ["kth-largest-element-in-an-array", "find-median-from-data-stream", "top-k-frequent-elements"],
    },
    # ------------------------------------------------------------------ 3
    {
        "id": "last-stone-weight",
        "title": "Last Stone Weight",
        "difficulty": "Easy",
        "pattern": "Heap / Priority Queue",
        "tags": ["Array", "Heap", "Simulation"],
        "companies": {"google": 2, "apple": 1, "meta": 1, "amazon": 3, "microsoft": 1},
        "description": (
            "You have a collection of stones with positive integer weights. Repeatedly take the **two heaviest** "
            "stones and smash them together: if they weigh the same both are destroyed; otherwise the lighter one "
            "is destroyed and the heavier one is left with weight equal to the difference.\n\n"
            "Continue until at most one stone remains. Return its weight, or `0` if no stones are left."
        ),
        "examples": [
            {"input": "stones = [2,7,4,1,8,1]", "output": "1",
             "explanation": "8 and 7 -> 1, stones [2,4,1,1,1]. 4 and 2 -> 2, stones [2,1,1,1]. 2 and 1 -> 1, stones [1,1,1]. "
                            "1 and 1 -> gone, stones [1]. Answer 1."},
            {"input": "stones = [1]", "output": "1"},
            {"input": "stones = [2,2]", "output": "0"},
        ],
        "constraints": ["1 <= stones.length <= 30", "1 <= stones[i] <= 1000"],
        "hints": [
            "Each round needs the two largest remaining values, and the collection changes every round.",
            "A max-heap gives you the largest in O(log n). Python's heapq is a min-heap, so store negated weights.",
            "Pop two, push the difference if it is non-zero, repeat while more than one stone is left.",
        ],
        "function": "lastStoneWeight",
        "signature": "def lastStoneWeight(self, stones: List[int]) -> int:",
        "arg_types": {"stones": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"stones": [2, 7, 4, 1, 8, 1]}, "output": 1},
            {"input": {"stones": [1]}, "output": 1},
            {"input": {"stones": [2, 2]}, "output": 0},
            {"input": {"stones": [3, 7]}, "output": 4},
            {"input": {"stones": [1, 1, 1]}, "output": 1},
            {"input": {"stones": [10, 4, 2, 10]}, "output": 2},
            {"input": {"stones": [1] * 3001}, "output": 1},
            {"input": {"stones": [1] * 3000}, "output": 0},
            {"input": {"stones": list(range(1, 3001))}, "output": 0},
            {"input": {"stones": list(range(1, 3002))}, "output": 1},
        ],
        "solution": '''class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        heap = [-s for s in stones]      # max-heap via negation
        heapify(heap)
        while len(heap) > 1:
            heaviest = -heappop(heap)
            second = -heappop(heap)
            if heaviest != second:
                heappush(heap, -(heaviest - second))
        return -heap[0] if heap else 0
''',
        "approach": (
            "**Simulate the process with a max-heap.** The problem statement is literally an algorithm: repeatedly "
            "extract the two largest, push back their difference if positive. A heap makes each extraction and "
            "insertion O(log n), and the number of rounds is at most n - 1 because every round removes at least "
            "one stone.\n\n"
            "**Python detail:** `heapq` is a min-heap, so store `-weight` and negate on the way out. Say this out "
            "loud in an interview; it is a classic gotcha.\n\n"
            "**Why it is correct:** the simulation is the definition. There is no greedy choice to justify; the "
            "only engineering question is how to find the two maxima quickly. Sorting the list every round is "
            "O(n^2 log n) and noticeably slower on the 3000-stone tests.\n\n"
            "**Common mistakes:** pushing a 0 back when the two stones are equal (harmless for the answer but "
            "wasteful and confusing); returning `heap[0]` without negating; forgetting the empty-heap case.\n\n"
            "**Interview follow-ups:** Last Stone Weight II, where you choose *any* two stones to minimise the "
            "final weight (becomes a subset-sum / partition DP, not a heap problem); what if weights are bounded "
            "and small (bucket counts); prove the number of rounds is at most n - 1."
        ),
        "complexity": {"time": "O(n log n)", "space": "O(n)"},
        "similar": ["last-stone-weight-ii", "kth-largest-element-in-an-array", "task-scheduler"],
    },
    # ------------------------------------------------------------------ 4
    {
        "id": "k-closest-points-to-origin",
        "title": "K Closest Points to Origin",
        "difficulty": "Medium",
        "pattern": "Heap / Priority Queue",
        "tags": ["Array", "Heap", "Geometry", "Quickselect"],
        "companies": {"google": 2, "apple": 2, "meta": 5, "amazon": 5, "microsoft": 2},
        "description": (
            "Given a list of `points` on the plane, each as `[x, y]`, and an integer `k`, return the `k` points "
            "closest to the origin `(0, 0)` by Euclidean distance.\n\n"
            "The answer is guaranteed to be unique (no ties at the boundary) and may be returned in any order."
        ),
        "examples": [
            {"input": "points = [[1,3],[-2,2]], k = 1", "output": "[[-2,2]]",
             "explanation": "Squared distances: 1+9 = 10 and 4+4 = 8. The second point is closer."},
            {"input": "points = [[3,3],[5,-1],[-2,4]], k = 2", "output": "[[3,3],[-2,4]]",
             "explanation": "Squared distances 18, 26, 20. Keep the two smallest."},
        ],
        "constraints": ["1 <= k <= points.length <= 10^4", "-10^4 <= x, y <= 10^4"],
        "hints": [
            "You never need the square root: comparing squared distances gives the same order and avoids floats.",
            "Keep a max-heap of the k closest points seen so far; evict the farthest when a closer one arrives.",
            "In Python, push (-distance, x, y) into heapq and use heappushpop once the heap has k entries.",
        ],
        "function": "kClosest",
        "signature": "def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:",
        "arg_types": {"points": "List[List[int]]", "k": "int"},
        "return_type": "List[List[int]]",
        "compare": "unordered",
        "tests": [
            {"input": {"points": [[1, 3], [-2, 2]], "k": 1}, "output": [[-2, 2]]},
            {"input": {"points": [[3, 3], [5, -1], [-2, 4]], "k": 2}, "output": [[3, 3], [-2, 4]]},
            {"input": {"points": [[0, 0]], "k": 1}, "output": [[0, 0]]},
            {"input": {"points": [[1, 1], [-1, -1], [2, 2]], "k": 2}, "output": [[1, 1], [-1, -1]]},
            {"input": {"points": [[2, 2], [2, 2], [3, 3]], "k": 2}, "output": [[2, 2], [2, 2]]},
            {"input": {"points": [[-5, 0], [0, 4], [3, -3], [1, 1]], "k": 4}, "output": [[-5, 0], [0, 4], [3, -3], [1, 1]]},
            {"input": {"points": [[i, i] for i in range(5000, 0, -1)], "k": 3}, "output": [[1, 1], [2, 2], [3, 3]]},
            {"input": {"points": [[x, 0] for x in _PERM_5003], "k": 4}, "output": [[0, 0], [1, 0], [2, 0], [3, 0]]},
        ],
        "solution": '''class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        heap = []  # max-heap (negated squared distance) of the k closest so far
        for x, y in points:
            entry = (-(x * x + y * y), x, y)
            if len(heap) < k:
                heappush(heap, entry)
            else:
                heappushpop(heap, entry)
        return [[x, y] for _, x, y in heap]
''',
        "approach": (
            "**Keep the k closest points in a max-heap keyed by distance, so the farthest of them is always at the "
            "root and can be evicted in O(log k).** Scan the points once; push until the heap has k entries, then "
            "`heappushpop` each new point: if it is farther than the current worst it bounces straight out, "
            "otherwise it replaces the worst. Squared distance avoids `sqrt` and floating point entirely.\n\n"
            "**Why it works:** the invariant 'heap = k closest points among those seen' holds after every step, so "
            "it holds at the end. The problem guarantees a unique answer, so tie-breaking on x and y in the tuple "
            "never changes the result.\n\n"
            "**Alternatives and when to mention them:** sorting by distance is O(n log n) and the simplest correct "
            "answer. Quickselect on the distance gives O(n) average and is the 'can you do better' follow-up. "
            "Binary search on the distance threshold is O(n log(range)). For a true stream where n is unknown, the "
            "heap is the only one that works online.\n\n"
            "**Common mistakes:** using a min-heap of all points and popping k (O(n + k log n), fine but not the "
            "O(n log k) they asked about); computing `math.sqrt` per point; mixing up which heap type to use "
            "(you want to evict the *farthest*, hence a max-heap).\n\n"
            "**Interview follow-ups:** k closest to an arbitrary query point (shift coordinates); many queries "
            "(k-d tree or grid bucketing); points arriving as a stream; what changes in 3-D."
        ),
        "complexity": {"time": "O(n log k)", "space": "O(k)"},
        "similar": ["kth-largest-element-in-an-array", "top-k-frequent-elements", "find-k-closest-elements"],
    },
    # ------------------------------------------------------------------ 5
    {
        "id": "task-scheduler",
        "title": "Task Scheduler",
        "difficulty": "Medium",
        "pattern": "Heap / Priority Queue",
        "tags": ["Array", "Hash Table", "Greedy", "Heap", "Counting"],
        "companies": {"google": 2, "apple": 2, "meta": 4, "amazon": 3, "microsoft": 3},
        "description": (
            "You are given a list of `tasks`, each a capital letter, and a cooldown `n`. Every unit of time the "
            "CPU either runs one task or idles. Two runs of the **same** letter must be separated by at least `n` "
            "other time units (other tasks or idles). Tasks may be run in any order.\n\n"
            "Return the minimum number of time units needed to finish every task."
        ),
        "examples": [
            {"input": "tasks = [\"A\",\"A\",\"A\",\"B\",\"B\",\"B\"], n = 2", "output": "8",
             "explanation": "One optimal schedule: A B idle A B idle A B."},
            {"input": "tasks = [\"A\",\"C\",\"A\",\"B\",\"D\",\"B\"], n = 1", "output": "6",
             "explanation": "Enough variety to never idle, e.g. A B A B C D."},
            {"input": "tasks = [\"A\",\"A\",\"A\",\"B\",\"B\",\"B\"], n = 3", "output": "10",
             "explanation": "A B idle idle A B idle idle A B."},
        ],
        "constraints": ["1 <= tasks.length <= 10^4", "tasks[i] is an uppercase English letter", "0 <= n <= 100"],
        "hints": [
            "Idle time only appears when the most frequent task runs out of distinct partners. Schedule the most frequent letter first.",
            "Simulate: a max-heap of remaining counts picks the most frequent available task each tick; a queue holds tasks that are cooling down with the time they become available again.",
            "Closed form: with f the max frequency and m letters having that frequency, the answer is max(len(tasks), (f - 1) * (n + 1) + m).",
        ],
        "function": "leastInterval",
        "signature": "def leastInterval(self, tasks: List[str], n: int) -> int:",
        "arg_types": {"tasks": "List[str]", "n": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"tasks": ["A", "A", "A", "B", "B", "B"], "n": 2}, "output": 8},
            {"input": {"tasks": ["A", "C", "A", "B", "D", "B"], "n": 1}, "output": 6},
            {"input": {"tasks": ["A", "A", "A", "B", "B", "B"], "n": 3}, "output": 10},
            {"input": {"tasks": ["A"], "n": 0}, "output": 1},
            {"input": {"tasks": ["A", "A"], "n": 0}, "output": 2},
            {"input": {"tasks": ["A", "A"], "n": 5}, "output": 7},
            {"input": {"tasks": ["A", "A", "A", "A", "B", "C"], "n": 2}, "output": 10},
            {"input": {"tasks": ["A", "A", "A", "B", "B", "B", "C", "C", "C", "D", "D", "E"], "n": 2}, "output": 12},
            {"input": {"tasks": ["A"] * 3000 + ["B"] * 3000, "n": 2}, "output": 8999},
            {"input": {"tasks": [chr(65 + i) for i in range(26) for _ in range(200)], "n": 1}, "output": 5200},
        ],
        "solution": '''class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        heap = [-c for c in Counter(tasks).values()]   # max-heap of remaining counts
        heapify(heap)
        cooling = deque()                              # (time when usable again, remaining count)
        time = 0
        while heap or cooling:
            time += 1
            if heap:
                remaining = heappop(heap) + 1          # run one unit of the most frequent task
                if remaining:
                    cooling.append((time + n, remaining))
            else:
                time = cooling[0][0]                   # nothing runnable: idle until the next release
            while cooling and cooling[0][0] <= time:
                heappush(heap, cooling.popleft()[1])
        return time
''',
        "approach": (
            "**Greedy: at every tick run the available task with the most remaining copies; if nothing is "
            "available, idle.** The task with the most copies is the one that forces idle time, so spending each "
            "slot on it (or, when it is cooling, on the next most frequent) never hurts.\n\n"
            "**Simulation with a heap and a queue:** a max-heap holds remaining counts of tasks that may run now. "
            "After running a task it goes into a FIFO `cooling` queue tagged with the time it becomes available "
            "(`now + n`); because every task waits the same n, the queue stays sorted by release time. When the "
            "heap is empty but the queue is not, jump the clock to the next release instead of ticking one by one.\n\n"
            "**Closed form (the follow-up you should know):** let f be the highest frequency and m the number of "
            "letters with that frequency. Lay out f - 1 frames of length n + 1, each starting with the most frequent "
            "letters, then a final row holding the m top letters: `(f - 1) * (n + 1) + m` slots. If there are more "
            "tasks than that, they fill idle slots and the answer is simply `len(tasks)`. So the answer is "
            "`max(len(tasks), (f - 1) * (n + 1) + m)`. Example 1: f = 3, m = 2, n = 2 gives (2)(3) + 2 = 8.\n\n"
            "**Common mistakes:** releasing a cooled task one tick too early or late (off by one on `time + n`); "
            "ticking one unit at a time during long idle stretches (slow for large n); in the formula, forgetting "
            "the `max` with `len(tasks)` (see the 26-letter test, where variety removes all idling).\n\n"
            "**Interview follow-ups:** return the actual schedule; different cooldowns per task type; tasks have "
            "deadlines or dependencies (becomes topological sort / scheduling theory); prove the formula is a lower "
            "bound and that the greedy achieves it."
        ),
        "complexity": {"time": "O(T log 26) = O(T) for the simulation, T = total time; O(len(tasks)) for the formula", "space": "O(26)"},
        "similar": ["reorganize-string", "rearrange-string-k-distance-apart", "last-stone-weight"],
    },
    # ------------------------------------------------------------------ 6
    {
        "id": "find-median-from-data-stream",
        "title": "Find Median from Data Stream",
        "difficulty": "Hard",
        "pattern": "Heap / Priority Queue",
        "tags": ["Heap", "Design", "Two Heaps", "Data Stream"],
        "companies": {"google": 4, "apple": 3, "meta": 3, "amazon": 5, "microsoft": 4},
        "kind": "design",
        "class_name": "MedianFinder",
        "description": (
            "The **median** of a list of numbers is the middle value when the list is sorted; if the list has even "
            "length it is the mean of the two middle values.\n\n"
            "Design a class that supports:\n\n"
            "- `MedianFinder()` creates an empty structure.\n"
            "- `addNum(num)` adds an integer from the stream.\n"
            "- `findMedian()` returns the median of everything added so far, as a float (for example `2.0` or `1.5`).\n\n"
            "`findMedian` is only called after at least one number has been added."
        ),
        "examples": [
            {"input": "[\"MedianFinder\",\"addNum\",\"addNum\",\"findMedian\",\"addNum\",\"findMedian\"]\n[[],[1],[2],[],[3],[]]",
             "output": "[null,null,null,1.5,null,2.0]",
             "explanation": "After 1 and 2 the median is (1 + 2) / 2 = 1.5. After adding 3 the sorted list is [1,2,3] and the median is 2."},
        ],
        "constraints": ["-10^5 <= num <= 10^5", "At most 5 * 10^4 calls to addNum and findMedian in total."],
        "hints": [
            "Keeping a sorted list costs O(n) per insertion. You only ever need the two middle elements, not the whole order.",
            "Split the numbers into a lower half and an upper half. If you can always reach the largest of the lower half and the smallest of the upper half, the median is one step away.",
            "Use a max-heap for the lower half and a min-heap for the upper half, keeping their sizes equal or with the lower half one larger. Rebalance after each insertion.",
        ],
        "starter": (
            "class MedianFinder:\n"
            "    def __init__(self):\n"
            "        pass\n\n"
            "    def addNum(self, num: int) -> None:\n"
            "        pass\n\n"
            "    def findMedian(self) -> float:\n"
            "        pass\n"
        ),
        "compare": "exact",
        "tests": [
            {"input": {"ops": [["MedianFinder", []], ["addNum", [1]], ["addNum", [2]], ["findMedian", []], ["addNum", [3]], ["findMedian", []]]},
             "output": [None, None, None, 1.5, None, 2.0]},
            {"input": {"ops": [["MedianFinder", []], ["addNum", [-1]], ["findMedian", []], ["addNum", [-2]], ["findMedian", []],
                               ["addNum", [-3]], ["findMedian", []], ["addNum", [-4]], ["findMedian", []], ["addNum", [-5]], ["findMedian", []]]},
             "output": [None, None, -1.0, None, -1.5, None, -2.0, None, -2.5, None, -3.0]},
            {"input": {"ops": [["MedianFinder", []], ["addNum", [5]], ["addNum", [5]], ["addNum", [5]], ["findMedian", []],
                               ["addNum", [6]], ["findMedian", []], ["addNum", [7]], ["findMedian", []], ["addNum", [8]], ["findMedian", []]]},
             "output": [None, None, None, None, 5.0, None, 5.0, None, 5.0, None, 5.5]},
            {"input": {"ops": [["MedianFinder", []], ["addNum", [10]], ["addNum", [1]], ["findMedian", []], ["addNum", [100]], ["findMedian", []],
                               ["addNum", [50]], ["findMedian", []], ["addNum", [0]], ["findMedian", []]]},
             "output": [None, None, None, 5.5, None, 10.0, None, 30.0, None, 10.0]},
            {"input": {"ops": [["MedianFinder", []]] + [["addNum", [i]] for i in range(2000)] + [["findMedian", []], ["addNum", [2000]], ["findMedian", []]]},
             "output": [None] + [None] * 2000 + [999.5, None, 1000.0]},
            {"input": {"ops": [["MedianFinder", []]] + [op for i in range(3000) for op in (["addNum", [i]], ["findMedian", []])]},
             "output": [None] + [x for i in range(3000) for x in (None, i / 2)]},
            {"input": {"ops": [["MedianFinder", []]] + [op for i in range(2999, -1, -1) for op in (["addNum", [i]], ["findMedian", []])]},
             "output": [None] + [x for j in range(3000) for x in (None, (2999 - j + 2999) / 2)]},
        ],
        "solution": '''class MedianFinder:
    def __init__(self):
        self.lower = []   # max-heap (negated) holding the smaller half
        self.upper = []   # min-heap holding the larger half; len(lower) - len(upper) is 0 or 1

    def addNum(self, num: int) -> None:
        heappush(self.lower, -num)
        heappush(self.upper, -heappop(self.lower))       # move the largest of lower up
        if len(self.upper) > len(self.lower):
            heappush(self.lower, -heappop(self.upper))   # restore the size invariant

    def findMedian(self) -> float:
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        return (-self.lower[0] + self.upper[0]) / 2
''',
        "approach": (
            "**Two heaps that meet in the middle.** Keep the smaller half of the numbers in a max-heap and the "
            "larger half in a min-heap, with the invariant that every element of the lower half is <= every element "
            "of the upper half and the lower half has either the same size or exactly one more element. Then the "
            "median is either the top of the lower heap (odd count) or the average of the two tops (even count).\n\n"
            "**Insertion in three moves:** push into the lower heap, move the lower heap's maximum to the upper "
            "heap (this guarantees the ordering invariant regardless of where `num` belonged), and if the upper "
            "heap is now bigger, move its minimum back down. Each step is O(log n) and the invariants are restored "
            "without any case analysis on `num`.\n\n"
            "**Why it works:** after step two the upper heap holds the k largest values for some k, and the lower "
            "heap holds the rest, so the ordering between halves is guaranteed. Step three only fixes sizes. The "
            "median of a sorted sequence is defined by the boundary between the two halves, which is exactly what "
            "the two tops expose.\n\n"
            "**Common mistakes:** comparing `num` with the tops to decide which heap to use and then forgetting to "
            "rebalance; off-by-one on which heap may be larger, which flips the odd-count median; returning an int "
            "for the odd case (callers expect a float); forgetting to negate values stored in the max-heap.\n\n"
            "**Interview follow-ups:** all numbers are in [0, 100]: use a counting array and scan for the median "
            "in O(100). 99% of numbers are in [0, 100]: counting array plus two heaps (or sorted containers) for the "
            "outliers. Sliding window median: two heaps with lazy deletion, or a balanced BST / `SortedList`. "
            "Approximate median over a huge stream: reservoir sampling or t-digest."
        ),
        "complexity": {"time": "O(log n) per addNum, O(1) per findMedian", "space": "O(n)"},
        "similar": ["sliding-window-median", "kth-largest-element-in-a-stream", "ipo"],
    },
    # ------------------------------------------------------------------ 7
    {
        "id": "top-k-frequent-words",
        "title": "Top K Frequent Words",
        "difficulty": "Medium",
        "pattern": "Heap / Priority Queue",
        "tags": ["Array", "Hash Table", "String", "Heap", "Sorting", "Bucket Sort"],
        "companies": {"google": 2, "apple": 2, "meta": 2, "amazon": 4, "microsoft": 2},
        "description": (
            "Given a list of `words` and an integer `k`, return the `k` most frequent words.\n\n"
            "Order the result by **frequency, highest first**; break ties by putting the **alphabetically smaller** "
            "word first. `k` is guaranteed not to exceed the number of distinct words."
        ),
        "examples": [
            {"input": "words = [\"i\",\"love\",\"leetcode\",\"i\",\"love\",\"coding\"], k = 2", "output": "[\"i\",\"love\"]",
             "explanation": "Both appear twice; \"i\" comes before \"love\" alphabetically."},
            {"input": "words = [\"the\",\"day\",\"is\",\"sunny\",\"the\",\"the\",\"the\",\"sunny\",\"is\",\"is\"], k = 4",
             "output": "[\"the\",\"is\",\"sunny\",\"day\"]",
             "explanation": "Counts: the 4, is 3, sunny 2, day 1."},
        ],
        "constraints": ["1 <= words.length <= 500", "1 <= words[i].length <= 10", "words[i] is lowercase letters", "1 <= k <= number of distinct words"],
        "hints": [
            "Count first. Then the problem is 'k smallest under a custom order' on the distinct words.",
            "The custom order is: higher count first, then alphabetical. As a sort key that is (-count, word).",
            "Sorting all distinct words is O(m log m). A heap of size k keyed by (-count, word) gives O(m log k); heapq.nsmallest does exactly this.",
        ],
        "function": "topKFrequent",
        "signature": "def topKFrequent(self, words: List[str], k: int) -> List[str]:",
        "arg_types": {"words": "List[str]", "k": "int"},
        "return_type": "List[str]",
        "compare": "exact",
        "tests": [
            {"input": {"words": ["i", "love", "leetcode", "i", "love", "coding"], "k": 2}, "output": ["i", "love"]},
            {"input": {"words": ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], "k": 4},
             "output": ["the", "is", "sunny", "day"]},
            {"input": {"words": ["a"], "k": 1}, "output": ["a"]},
            {"input": {"words": ["b", "a"], "k": 2}, "output": ["a", "b"]},
            {"input": {"words": ["b", "a", "b", "a", "c"], "k": 1}, "output": ["a"]},
            {"input": {"words": ["apple", "app", "apple", "app", "ap"], "k": 3}, "output": ["app", "apple", "ap"]},
            {"input": {"words": ["z", "y", "x", "x", "y", "z", "y"], "k": 3}, "output": ["y", "x", "z"]},
            {"input": {"words": _FREQ_WORDS, "k": 5}, "output": ["w0006", "w0013", "w0020", "w0027", "w0034"]},
            {"input": {"words": _FREQ_WORDS, "k": 1}, "output": ["w0006"]},
        ],
        "solution": '''class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        counts = Counter(words)
        # "Most frequent, then alphabetical" is the same as "smallest (-count, word)".
        return heapq.nsmallest(k, counts, key=lambda w: (-counts[w], w))
''',
        "approach": (
            "**Count, then select the k best under the composite order (-count, word).** Negating the count turns "
            "'highest frequency first' into 'smallest key first', and the word itself as the second component "
            "gives the alphabetical tie-break for free, because tuples compare lexicographically. The problem is "
            "then 'k smallest elements by key', which a size-k heap solves in O(m log k) over m distinct words. "
            "`heapq.nsmallest` implements exactly that and returns the result already sorted.\n\n"
            "**If asked to write the heap by hand:** maintain a min-heap of size k where the *worst* of the kept "
            "words is at the root. Worst means lowest count, or alphabetically largest among equal counts, so the "
            "heap entry is `(count, ReversedWord)`: either wrap the word in a small class with an inverted `__lt__`, "
            "or push `(-count, word)` into a max-heap. Pop the root whenever the size exceeds k, then pop everything "
            "at the end and reverse.\n\n"
            "**Why it works:** the ordering is a strict total order on distinct words, so the k smallest keys are "
            "well defined and unique, and both sorting and a size-k heap return exactly those in order.\n\n"
            "**Common mistakes:** pushing `(-count, word)` into a min-heap of size k and popping the root (that "
            "evicts the *best* word, not the worst); sorting by count only and ignoring the tie-break; returning in "
            "heap-pop order without reversing.\n\n"
            "**Interview follow-ups:** O(m) with bucket sort by count plus sorting inside buckets (the alphabetical "
            "tie-break makes it O(m log m) in the worst case anyway, which is a good thing to notice); top k in a "
            "stream (count-min sketch plus a heap); top-k-frequent-elements with integers, where bucket sort is "
            "truly linear."
        ),
        "complexity": {"time": "O(n + m log k), n = words, m = distinct words", "space": "O(m)"},
        "similar": ["top-k-frequent-elements", "kth-largest-element-in-an-array", "sort-characters-by-frequency"],
    },
    # ------------------------------------------------------------------ 8
    {
        "id": "reorganize-string",
        "title": "Reorganize String",
        "difficulty": "Medium",
        "pattern": "Heap / Priority Queue",
        "tags": ["Hash Table", "String", "Greedy", "Heap", "Counting"],
        "companies": {"google": 2, "apple": 2, "meta": 3, "amazon": 4, "microsoft": 2},
        "description": (
            "Given a string `s`, rearrange its characters so that **no two adjacent characters are the same**.\n\n"
            "Return any valid rearrangement, or the empty string `\"\"` if none exists."
        ),
        "examples": [
            {"input": "s = \"aab\"", "output": "\"aba\""},
            {"input": "s = \"aaab\"", "output": "\"\"",
             "explanation": "Three a's need at least two separators between them, but there is only one b."},
            {"input": "s = \"aabb\"", "output": "\"abab\"", "explanation": "\"baba\" is also accepted."},
        ],
        "constraints": ["1 <= s.length <= 500", "s consists of lowercase English letters."],
        "hints": [
            "When is it impossible? Think about how many slots the most common character needs.",
            "If any character appears more than ceil(len(s) / 2) times, return \"\". Otherwise a greedy works: always place the most frequent remaining character that differs from the last one placed.",
            "Use a max-heap of (count, char). Pop the top, append it, and hold it back one round before re-inserting it so it cannot be placed twice in a row.",
        ],
        "function": "reorganizeString",
        "signature": "def reorganizeString(self, s: str) -> str:",
        "arg_types": {"s": "str"},
        "return_type": "str",
        "compare": "any_of",
        "tests": [
            {"input": {"s": "aab"}, "output": ["aba"]},
            {"input": {"s": "aaab"}, "output": [""]},
            {"input": {"s": "aabb"}, "output": ["abab", "baba"]},
            {"input": {"s": "a"}, "output": ["a"]},
            {"input": {"s": "ab"}, "output": ["ab", "ba"]},
            {"input": {"s": "aaabb"}, "output": ["ababa"]},
            {"input": {"s": "aaaabb"}, "output": [""]},
            {"input": {"s": "aaabc"}, "output": ["abaca", "acaba"]},
            {"input": {"s": "vvvlo"}, "output": ["vlvov", "vovlv"]},
            {"input": {"s": "a" * 2000 + "b" * 1999}, "output": ["ab" * 1999 + "a"]},
            {"input": {"s": "a" * 2001 + "b" * 1999}, "output": [""]},
            {"input": {"s": "a" * 1500 + "b" * 1500}, "output": ["ab" * 1500, "ba" * 1500]},
        ],
        "solution": '''class Solution:
    def reorganizeString(self, s: str) -> str:
        counts = Counter(s)
        if max(counts.values()) > (len(s) + 1) // 2:
            return ""

        heap = [(-count, ch) for ch, count in counts.items()]   # max-heap by count
        heapify(heap)
        result = []
        held = None   # the character placed last round, kept out of the heap for one turn

        while heap:
            count, ch = heappop(heap)
            result.append(ch)
            if held is not None:
                heappush(heap, held)
            held = (count + 1, ch) if count + 1 < 0 else None

        return "".join(result)
''',
        "approach": (
            "**Feasibility check, then greedy by frequency with a one-round hold-back.** A character with c copies "
            "needs c - 1 gaps, so it fits only if c <= ceil(len(s) / 2). If the most frequent character passes this "
            "test, a valid arrangement always exists and the greedy below finds one.\n\n"
            "**Algorithm:** max-heap of `(-count, char)`. Each round pop the most frequent character, append it, "
            "then push back the character held from the *previous* round (it has now been separated by one "
            "position), and hold the current one if it still has copies left. Because the just-used character is "
            "never in the heap at the next pop, no two adjacent characters are equal.\n\n"
            "**Why it never gets stuck:** suppose the heap becomes empty while a character is still held with "
            "copies remaining. That means every other character ran out while this one still needed slots, which "
            "contradicts the feasibility bound; so with the bound checked up front the loop always consumes "
            "everything. Equivalently, the greedy keeps the gap between the most frequent letter's copies filled "
            "with the next most frequent letters, which is the best possible use of separators.\n\n"
            "**Alternative without a heap:** sort characters by frequency and place them into the even indices "
            "0, 2, 4, ... first, then the odd indices. O(n) after counting, and a nice follow-up to offer.\n\n"
            "**Common mistakes:** pushing the used character straight back (it may be popped again immediately); "
            "popping two characters per round and forgetting the case where only one is left; off-by-one in the "
            "feasibility bound (`(len + 1) // 2`, not `len // 2`); returning a partially built string instead of "
            "\"\" when the input is impossible.\n\n"
            "**Interview follow-ups:** require a distance of at least k between equal characters (same idea with a "
            "queue of k held items, rearrange-string-k-distance-apart); return the lexicographically smallest valid "
            "arrangement; count the number of valid arrangements; the even/odd slot method and why it is correct."
        ),
        "complexity": {"time": "O(n log 26) = O(n)", "space": "O(26) for the heap plus O(n) for the output"},
        "similar": ["task-scheduler", "rearrange-string-k-distance-apart", "sort-characters-by-frequency"],
    },
]
