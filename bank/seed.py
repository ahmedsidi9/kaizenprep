"""Seed problems that demonstrate every schema feature. See SCHEMA.md."""

PROBLEMS = [
    {
        "id": "two-sum",
        "title": "Two Sum",
        "difficulty": "Easy",
        "pattern": "Arrays & Hashing",
        "tags": ["Array", "Hash Table"],
        "companies": {"google": 5, "apple": 5, "meta": 4, "amazon": 5, "microsoft": 4},
        "description": (
            "Given an integer array `nums` and an integer `target`, return the **indices** of the two "
            "elements whose values add up to `target`.\n\n"
            "Every input has exactly one valid pair, and you may not use the same index twice. "
            "The indices can be returned in any order."
        ),
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "nums[0] + nums[1] = 2 + 7 = 9."},
            {"input": "nums = [3,2,4], target = 6", "output": "[1,2]", "explanation": "nums[1] + nums[2] = 2 + 4 = 6."},
            {"input": "nums = [3,3], target = 6", "output": "[0,1]"},
        ],
        "constraints": ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9", "Exactly one valid answer exists."],
        "hints": [
            "The brute force checks every pair in O(n^2). Can you remember what you have already seen?",
            "For each number x, the partner you need is target - x. A hash map lets you check for it in O(1).",
            "Store value -> index as you scan. Check for the complement before inserting the current number so you never pair an element with itself.",
        ],
        "function": "twoSum",
        "signature": "def twoSum(self, nums: List[int], target: int) -> List[int]:",
        "arg_types": {"nums": "List[int]", "target": "int"},
        "return_type": "List[int]",
        "compare": "unordered",
        "tests": [
            {"input": {"nums": [2, 7, 11, 15], "target": 9}, "output": [0, 1]},
            {"input": {"nums": [3, 2, 4], "target": 6}, "output": [1, 2]},
            {"input": {"nums": [3, 3], "target": 6}, "output": [0, 1]},
            {"input": {"nums": [-1, -2, -3, -4, -5], "target": -8}, "output": [2, 4]},
            {"input": {"nums": [0, 4, 3, 0], "target": 0}, "output": [0, 3]},
            {"input": {"nums": list(range(0, 20000, 2)) + [1], "target": 19999}, "output": [9999, 10000]},
        ],
        "solution": (
            "class Solution:\n"
            "    def twoSum(self, nums: List[int], target: int) -> List[int]:\n"
            "        seen = {}\n"
            "        for i, x in enumerate(nums):\n"
            "            if target - x in seen:\n"
            "                return [seen[target - x], i]\n"
            "            seen[x] = i\n"
            "        return []\n"
        ),
        "approach": (
            "**One-pass hash map.** Walk the array once. For each value `x`, the partner we need is "
            "`target - x`. If that partner is already in the map we are done; otherwise record `x -> index`.\n\n"
            "Checking before inserting guarantees we never pair an element with itself.\n\n"
            "**Interview follow-ups:** What if the array is sorted? (two pointers, O(1) space). "
            "What if there can be many answers? (collect all pairs, mind duplicates). "
            "What about streaming input? (keep the map, answer per query)."
        ),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "similar": ["3sum", "two-sum-ii-sorted", "subarray-sum-equals-k"],
    },
    {
        "id": "reverse-linked-list",
        "title": "Reverse Linked List",
        "difficulty": "Easy",
        "pattern": "Linked List",
        "tags": ["Linked List", "Recursion"],
        "companies": {"google": 3, "apple": 5, "meta": 3, "amazon": 4, "microsoft": 4},
        "description": "Given the head of a singly linked list, reverse it and return the new head.",
        "examples": [
            {"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]"},
            {"input": "head = [1,2]", "output": "[2,1]"},
            {"input": "head = []", "output": "[]"},
        ],
        "constraints": ["0 <= number of nodes <= 5000", "-5000 <= Node.val <= 5000"],
        "hints": [
            "Keep three pointers: previous, current, next.",
            "At each step point current.next at previous, then advance all three.",
        ],
        "function": "reverseList",
        "signature": "def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:",
        "arg_types": {"head": "ListNode"},
        "return_type": "ListNode",
        "compare": "exact",
        "tests": [
            {"input": {"head": [1, 2, 3, 4, 5]}, "output": [5, 4, 3, 2, 1]},
            {"input": {"head": [1, 2]}, "output": [2, 1]},
            {"input": {"head": []}, "output": []},
            {"input": {"head": [7]}, "output": [7]},
            {"input": {"head": list(range(3000))}, "output": list(range(2999, -1, -1))},
        ],
        "solution": (
            "class Solution:\n"
            "    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:\n"
            "        prev, cur = None, head\n"
            "        while cur:\n"
            "            nxt = cur.next\n"
            "            cur.next = prev\n"
            "            prev, cur = cur, nxt\n"
            "        return prev\n"
        ),
        "approach": (
            "**Iterative pointer flip.** Maintain `prev` and `cur`. Save `cur.next`, redirect `cur.next` to `prev`, "
            "then slide both forward. When `cur` is None, `prev` is the new head.\n\n"
            "The recursive version reverses the tail first then fixes `head.next.next = head`; it uses O(n) stack, "
            "which interviewers at Apple often ask you to point out."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["reverse-linked-list-ii", "reverse-nodes-in-k-group", "palindrome-linked-list"],
    },
    {
        "id": "invert-binary-tree",
        "title": "Invert Binary Tree",
        "difficulty": "Easy",
        "pattern": "Trees",
        "tags": ["Tree", "DFS", "BFS"],
        "companies": {"google": 4, "apple": 3, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": "Given the root of a binary tree, swap the left and right children of every node and return the root.",
        "examples": [
            {"input": "root = [4,2,7,1,3,6,9]", "output": "[4,7,2,9,6,3,1]"},
            {"input": "root = [2,1,3]", "output": "[2,3,1]"},
            {"input": "root = []", "output": "[]"},
        ],
        "constraints": ["0 <= number of nodes <= 100", "-100 <= Node.val <= 100"],
        "hints": ["Swap the children of the current node, then recurse into both subtrees.", "Any traversal order works."],
        "function": "invertTree",
        "signature": "def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:",
        "arg_types": {"root": "TreeNode"},
        "return_type": "TreeNode",
        "compare": "exact",
        "tests": [
            {"input": {"root": [4, 2, 7, 1, 3, 6, 9]}, "output": [4, 7, 2, 9, 6, 3, 1]},
            {"input": {"root": [2, 1, 3]}, "output": [2, 3, 1]},
            {"input": {"root": []}, "output": []},
            {"input": {"root": [1, None, 2]}, "output": [1, 2]},
            {"input": {"root": [1, 2, None, 3]}, "output": [1, None, 2, None, 3]},
        ],
        "solution": (
            "class Solution:\n"
            "    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:\n"
            "        if root:\n"
            "            root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)\n"
            "        return root\n"
        ),
        "approach": "**Recursive swap.** Swap the two subtrees after inverting each. BFS with a queue is the iterative alternative and avoids deep recursion.",
        "complexity": {"time": "O(n)", "space": "O(h)"},
        "similar": ["maximum-depth-of-binary-tree", "symmetric-tree"],
    },
    {
        "id": "rotate-array",
        "title": "Rotate Array",
        "difficulty": "Medium",
        "pattern": "Arrays & Hashing",
        "tags": ["Array", "Math"],
        "companies": {"google": 2, "apple": 4, "meta": 1, "amazon": 3, "microsoft": 4},
        "description": (
            "Rotate the array `nums` to the right by `k` steps, **in place**. `k` is non-negative and may exceed the length.\n\n"
            "Do not return anything; modify `nums` directly."
        ),
        "examples": [
            {"input": "nums = [1,2,3,4,5,6,7], k = 3", "output": "[5,6,7,1,2,3,4]"},
            {"input": "nums = [-1,-100,3,99], k = 2", "output": "[3,99,-1,-100]"},
        ],
        "constraints": ["1 <= nums.length <= 10^5", "0 <= k <= 10^5"],
        "hints": [
            "Reduce k modulo the length first.",
            "Reverse the whole array, then reverse the first k elements, then reverse the rest. Three reversals, O(1) space.",
        ],
        "function": "rotate",
        "signature": "def rotate(self, nums: List[int], k: int) -> None:",
        "arg_types": {"nums": "List[int]", "k": "int"},
        "return_type": "None",
        "output_mode": "arg:nums",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [1, 2, 3, 4, 5, 6, 7], "k": 3}, "output": [5, 6, 7, 1, 2, 3, 4]},
            {"input": {"nums": [-1, -100, 3, 99], "k": 2}, "output": [3, 99, -1, -100]},
            {"input": {"nums": [1], "k": 5}, "output": [1]},
            {"input": {"nums": [1, 2], "k": 0}, "output": [1, 2]},
            {"input": {"nums": [1, 2, 3], "k": 4}, "output": [3, 1, 2]},
        ],
        "solution": (
            "class Solution:\n"
            "    def rotate(self, nums: List[int], k: int) -> None:\n"
            "        n = len(nums)\n"
            "        k %= n\n"
            "        def rev(i, j):\n"
            "            while i < j:\n"
            "                nums[i], nums[j] = nums[j], nums[i]\n"
            "                i += 1; j -= 1\n"
            "        rev(0, n - 1); rev(0, k - 1); rev(k, n - 1)\n"
        ),
        "approach": "**Three reversals.** Reversing the whole array puts the last k elements at the front in reverse order; reversing each half restores their order. O(1) extra space, which is the point of the question.",
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["reverse-words-in-a-string", "rotate-image"],
    },
    {
        "id": "lru-cache",
        "title": "LRU Cache",
        "difficulty": "Medium",
        "pattern": "Design",
        "tags": ["Hash Table", "Linked List", "Design"],
        "companies": {"google": 4, "apple": 5, "meta": 4, "amazon": 5, "microsoft": 5},
        "kind": "design",
        "class_name": "LRUCache",
        "description": (
            "Design a cache with a fixed `capacity` that evicts the **least recently used** key when full.\n\n"
            "- `LRUCache(capacity)` initialises the cache.\n"
            "- `get(key)` returns the value, or `-1` if absent. A successful get counts as a use.\n"
            "- `put(key, value)` inserts or updates the key. If the insert exceeds capacity, evict the least recently used key first.\n\n"
            "Both operations must run in **O(1)** average time."
        ),
        "examples": [
            {"input": "[\"LRUCache\",\"put\",\"put\",\"get\",\"put\",\"get\",\"get\"]\n[[2],[1,1],[2,2],[1],[3,3],[2],[3]]",
             "output": "[null,null,null,1,null,-1,3]",
             "explanation": "After put(3,3) the cache is full, so key 2 (least recently used) is evicted."},
        ],
        "constraints": ["1 <= capacity <= 3000", "0 <= key, value <= 10^5", "Up to 2 * 10^5 calls to get and put."],
        "hints": [
            "A hash map gives O(1) lookup but no ordering. A doubly linked list gives O(1) move-to-front and removal but no lookup. Combine them.",
            "Keep sentinel head and tail nodes so insert and unlink never special-case the ends.",
            "In Python, OrderedDict with move_to_end and popitem(last=False) is an accepted shortcut, but be ready to explain the linked-list version.",
        ],
        "starter": (
            "class LRUCache:\n"
            "    def __init__(self, capacity: int):\n"
            "        pass\n\n"
            "    def get(self, key: int) -> int:\n"
            "        pass\n\n"
            "    def put(self, key: int, value: int) -> None:\n"
            "        pass\n"
        ),
        "compare": "exact",
        "tests": [
            {"input": {"ops": [["LRUCache", [2]], ["put", [1, 1]], ["put", [2, 2]], ["get", [1]], ["put", [3, 3]], ["get", [2]], ["get", [3]]]},
             "output": [None, None, None, 1, None, -1, 3]},
            {"input": {"ops": [["LRUCache", [1]], ["put", [2, 1]], ["get", [2]], ["put", [3, 2]], ["get", [2]], ["get", [3]]]},
             "output": [None, None, 1, None, -1, 2]},
            {"input": {"ops": [["LRUCache", [2]], ["get", [2]], ["put", [2, 6]], ["get", [1]], ["put", [1, 5]], ["put", [1, 2]], ["get", [1]], ["get", [2]]]},
             "output": [None, -1, None, -1, None, None, 2, 6]},
            {"input": {"ops": [["LRUCache", [2]], ["put", [2, 1]], ["put", [1, 1]], ["put", [2, 3]], ["put", [4, 1]], ["get", [1]], ["get", [2]]]},
             "output": [None, None, None, None, None, -1, 3]},
        ],
        "solution": (
            "class _Node:\n"
            "    __slots__ = ('key', 'val', 'prev', 'next')\n"
            "    def __init__(self, key=0, val=0):\n"
            "        self.key, self.val, self.prev, self.next = key, val, None, None\n\n"
            "class LRUCache:\n"
            "    def __init__(self, capacity: int):\n"
            "        self.cap = capacity\n"
            "        self.map = {}\n"
            "        self.head, self.tail = _Node(), _Node()\n"
            "        self.head.next, self.tail.prev = self.tail, self.head\n\n"
            "    def _unlink(self, node):\n"
            "        node.prev.next, node.next.prev = node.next, node.prev\n\n"
            "    def _push_front(self, node):\n"
            "        node.next, node.prev = self.head.next, self.head\n"
            "        self.head.next.prev = node\n"
            "        self.head.next = node\n\n"
            "    def get(self, key: int) -> int:\n"
            "        if key not in self.map:\n"
            "            return -1\n"
            "        node = self.map[key]\n"
            "        self._unlink(node); self._push_front(node)\n"
            "        return node.val\n\n"
            "    def put(self, key: int, value: int) -> None:\n"
            "        if key in self.map:\n"
            "            node = self.map[key]\n"
            "            node.val = value\n"
            "            self._unlink(node); self._push_front(node)\n"
            "            return\n"
            "        if len(self.map) == self.cap:\n"
            "            lru = self.tail.prev\n"
            "            self._unlink(lru)\n"
            "            del self.map[lru.key]\n"
            "        node = _Node(key, value)\n"
            "        self.map[key] = node\n"
            "        self._push_front(node)\n"
        ),
        "approach": (
            "**Hash map + doubly linked list.** The map gives O(1) access to a node; the list keeps recency order "
            "with the most recent at the front. `get` and `put` on an existing key move the node to the front. "
            "Inserting past capacity unlinks the node before the tail sentinel and drops its key from the map.\n\n"
            "**Follow-ups:** LFU cache (frequency buckets), thread safety (a lock around each operation), TTL expiry."
        ),
        "complexity": {"time": "O(1) per operation", "space": "O(capacity)"},
        "similar": ["lfu-cache", "design-hashmap"],
    },
]
