"""Trees pattern. See SCHEMA.md for the dict format."""
from collections import deque


# ---------------------------------------------------------------------------
# Helpers used only to build large test inputs / expected outputs.
# ---------------------------------------------------------------------------

def _left_chain(vals):
    """Level-order array of a tree where every node has only a left child."""
    vals = list(vals)
    out = [vals[0]] + [x for v in vals[1:] for x in (v, None)]
    while out and out[-1] is None:
        out.pop()
    return out


def _right_chain(vals):
    """Level-order array of a tree where every node has only a right child."""
    vals = list(vals)
    return [vals[0]] + [x for v in vals[1:] for x in (None, v)]


def _balanced_bst(vals):
    """Level-order array of a height-balanced BST holding the sorted values `vals`.

    Built by always taking the middle element as the root, so for range(4095)
    the root is 2047 and the tree is perfect."""
    vals = list(vals)

    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        return [vals[mid], build(lo, mid - 1), build(mid + 1, hi)]

    root = build(0, len(vals) - 1)
    out, q = [], deque([root])
    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node[0])
        q.append(node[1])
        q.append(node[2])
    while out and out[-1] is None:
        out.pop()
    return out


def _complete_order(n, kind):
    """Preorder / inorder of the complete tree whose level-order is list(range(n))."""
    out = []

    def go(i):
        if i >= n:
            return
        if kind == "pre":
            out.append(i)
        go(2 * i + 1)
        if kind == "in":
            out.append(i)
        go(2 * i + 2)

    go(0)
    return out


_FULL_12 = list(range(4095))          # perfect binary tree, depth 12
_LEVELS_12 = [list(range(2 ** d - 1, 2 ** (d + 1) - 1)) for d in range(12)]


PROBLEMS = [
    # ------------------------------------------------------------------ 1
    {
        "id": "maximum-depth-of-binary-tree",
        "title": "Maximum Depth of Binary Tree",
        "difficulty": "Easy",
        "pattern": "Trees",
        "tags": ["Tree", "DFS", "BFS", "Recursion"],
        "companies": {"google": 3, "apple": 3, "meta": 3, "amazon": 4, "microsoft": 3},
        "description": (
            "Given the root of a binary tree, return its **maximum depth**: the number of nodes on the "
            "longest path from the root down to a leaf.\n\n"
            "An empty tree has depth `0`; a single node has depth `1`."
        ),
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "3",
             "explanation": "The path 3 -> 20 -> 15 (or 3 -> 20 -> 7) has three nodes."},
            {"input": "root = [1,null,2]", "output": "2"},
            {"input": "root = []", "output": "0"},
        ],
        "constraints": ["0 <= number of nodes <= 10^4", "-100 <= Node.val <= 100"],
        "hints": [
            "The depth of a tree is defined in terms of the depth of its subtrees.",
            "depth(node) = 1 + max(depth(left), depth(right)), and depth(None) = 0.",
            "An iterative BFS that counts levels avoids recursion entirely and is worth mentioning for very deep trees.",
        ],
        "function": "maxDepth",
        "signature": "def maxDepth(self, root: Optional[TreeNode]) -> int:",
        "arg_types": {"root": "TreeNode"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"root": [3, 9, 20, None, None, 15, 7]}, "output": 3},
            {"input": {"root": [1, None, 2]}, "output": 2},
            {"input": {"root": []}, "output": 0},
            {"input": {"root": [1]}, "output": 1},
            {"input": {"root": [1, 2, 3, 4, None, None, None, 5]}, "output": 4},
            {"input": {"root": _left_chain(range(3000))}, "output": 3000},
            {"input": {"root": _FULL_12}, "output": 12},
        ],
        "solution": '''class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
''',
        "approach": (
            "**The depth of a node is one more than the deeper of its two subtrees.** That single sentence is the "
            "whole recursion: an empty subtree contributes 0, and every real node adds 1 on top of "
            "`max(depth(left), depth(right))`.\n\n"
            "**Why it works:** every root-to-leaf path passes through exactly one child of the root, so the longest "
            "path is the longest path in one of the subtrees plus the root itself.\n\n"
            "**Iterative alternative:** BFS with a queue, processing one whole level per outer iteration and counting "
            "levels. This is the version to offer if the interviewer worries about recursion depth on a skewed tree "
            "with 10^4+ nodes.\n\n"
            "**Common mistakes:** returning `max(left, right)` without the `+ 1`; counting edges instead of nodes "
            "(depth of a single node is 1, not 0).\n\n"
            "**Interview follow-ups:** minimum depth (careful: a node with one child is not a leaf); "
            "doing it iteratively with an explicit stack of `(node, depth)` pairs; "
            "depth of an n-ary tree (take the max over all children)."
        ),
        "complexity": {"time": "O(n)", "space": "O(h) recursion stack, O(n) worst case for a skewed tree"},
        "similar": ["balanced-binary-tree", "diameter-of-binary-tree", "minimum-depth-of-binary-tree"],
    },
    # ------------------------------------------------------------------ 2
    {
        "id": "diameter-of-binary-tree",
        "title": "Diameter of Binary Tree",
        "difficulty": "Easy",
        "pattern": "Trees",
        "tags": ["Tree", "DFS", "Recursion"],
        "companies": {"google": 3, "apple": 2, "meta": 4, "amazon": 3, "microsoft": 2},
        "description": (
            "Given the root of a binary tree, return the length of its **diameter**: the number of edges on the "
            "longest path between any two nodes. The path does not have to pass through the root.\n\n"
            "A single node has diameter `0`."
        ),
        "examples": [
            {"input": "root = [1,2,3,4,5]", "output": "3",
             "explanation": "The longest path is 4 -> 2 -> 1 -> 3 (or 5 -> 2 -> 1 -> 3), which has 3 edges."},
            {"input": "root = [1,2]", "output": "1"},
        ],
        "constraints": ["1 <= number of nodes <= 10^4", "-100 <= Node.val <= 100"],
        "hints": [
            "The longest path through a given node goes down into its left subtree and down into its right subtree.",
            "For each node, that path has length height(left) + height(right). The answer is the maximum of this over all nodes.",
            "Compute heights bottom-up in one post-order pass and update a running maximum as a side effect.",
        ],
        "function": "diameterOfBinaryTree",
        "signature": "def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:",
        "arg_types": {"root": "TreeNode"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"root": [1, 2, 3, 4, 5]}, "output": 3},
            {"input": {"root": [1, 2]}, "output": 1},
            {"input": {"root": [1]}, "output": 0},
            {"input": {"root": []}, "output": 0},
            {"input": {"root": [1, 2, None, 3, 4, 5, None, None, 6]}, "output": 4},
            {"input": {"root": _left_chain(range(3000))}, "output": 2999},
            {"input": {"root": _FULL_12}, "output": 22},
        ],
        "solution": '''class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        best = 0

        def height(node):
            nonlocal best
            if not node:
                return 0
            left, right = height(node.left), height(node.right)
            best = max(best, left + right)
            return 1 + max(left, right)

        height(root)
        return best
''',
        "approach": (
            "**Every path has a unique highest node; at that node the path is left-height + right-height edges "
            "long.** So compute the height of every subtree bottom-up and, while doing so, record "
            "`height(left) + height(right)` at each node. The largest value seen is the diameter.\n\n"
            "**Algorithm:** a post-order DFS that returns the height of the subtree (0 for None) and updates a "
            "nonlocal maximum. One pass, every node visited once.\n\n"
            "**Common mistakes:** calling a separate `height()` from inside the diameter recursion, which makes "
            "the solution O(n^2) on a skewed tree (the 3000-node chain test catches this); returning the diameter "
            "from the recursion instead of the height; off-by-one between edges and nodes.\n\n"
            "**Interview follow-ups:** return the actual path, not just its length (track the argmax child at each "
            "node); diameter of an n-ary tree (keep the two largest child heights); the same shape of recursion "
            "solves binary-tree-maximum-path-sum and longest univalue path."
        ),
        "complexity": {"time": "O(n)", "space": "O(h)"},
        "similar": ["maximum-depth-of-binary-tree", "binary-tree-maximum-path-sum", "longest-univalue-path"],
    },
    # ------------------------------------------------------------------ 3
    {
        "id": "balanced-binary-tree",
        "title": "Balanced Binary Tree",
        "difficulty": "Easy",
        "pattern": "Trees",
        "tags": ["Tree", "DFS", "Recursion"],
        "companies": {"google": 3, "apple": 2, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "A binary tree is **height-balanced** when, for every node, the heights of its left and right "
            "subtrees differ by at most one.\n\n"
            "Given the root of a binary tree, return `true` if it is height-balanced and `false` otherwise. "
            "The empty tree is balanced."
        ),
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "true"},
            {"input": "root = [1,2,2,3,3,null,null,4,4]", "output": "false",
             "explanation": "The left subtree of the root has height 3 while the right has height 1."},
            {"input": "root = []", "output": "true"},
        ],
        "constraints": ["0 <= number of nodes <= 5000", "-10^4 <= Node.val <= 10^4"],
        "hints": [
            "You need the height of each subtree, and the check must hold at every node, not only at the root.",
            "Compute heights bottom-up. As soon as any node fails the check, the whole answer is false.",
            "Use a sentinel: have the height function return -1 to mean 'unbalanced below here' and short-circuit upward.",
        ],
        "function": "isBalanced",
        "signature": "def isBalanced(self, root: Optional[TreeNode]) -> bool:",
        "arg_types": {"root": "TreeNode"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"root": [3, 9, 20, None, None, 15, 7]}, "output": True},
            {"input": {"root": [1, 2, 2, 3, 3, None, None, 4, 4]}, "output": False},
            {"input": {"root": []}, "output": True},
            {"input": {"root": [1]}, "output": True},
            {"input": {"root": [1, 2, None, 3]}, "output": False},
            {"input": {"root": [1, 2, 3, 4, None, None, None]}, "output": True},
            {"input": {"root": _FULL_12}, "output": True},
            {"input": {"root": _FULL_12 + [4095]}, "output": True},
            {"input": {"root": _left_chain(range(3000))}, "output": False},
        ],
        "solution": '''class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def height(node):
            """Height of the subtree, or -1 if anything below is unbalanced."""
            if not node:
                return 0
            left = height(node.left)
            if left < 0:
                return -1
            right = height(node.right)
            if right < 0 or abs(left - right) > 1:
                return -1
            return 1 + max(left, right)

        return height(root) >= 0
''',
        "approach": (
            "**Fold the balance check into the height computation.** A naive solution computes `height()` for both "
            "children at every node and recurses, which is O(n^2) on a skewed tree. Instead, do a single post-order "
            "pass that returns the height of each subtree but returns the sentinel `-1` the moment an imbalance is "
            "detected. Any caller that sees `-1` propagates it immediately.\n\n"
            "**Why it works:** the height of a node depends only on its children's heights, which we have just "
            "computed, so the balance condition can be checked for free on the way back up.\n\n"
            "**Common mistakes:** only checking the root; forgetting that an empty subtree has height 0 (so a node "
            "with one leaf child is still balanced); forgetting to short-circuit when a child returns -1.\n\n"
            "**Interview follow-ups:** return the *first* unbalanced node instead of a boolean; what changes for an "
            "AVL tree (rotations to restore the invariant after insert); how would you check balance for a very "
            "deep tree without recursion (post-order with an explicit stack and a height map)."
        ),
        "complexity": {"time": "O(n)", "space": "O(h)"},
        "similar": ["maximum-depth-of-binary-tree", "diameter-of-binary-tree"],
    },
    # ------------------------------------------------------------------ 4
    {
        "id": "same-tree",
        "title": "Same Tree",
        "difficulty": "Easy",
        "pattern": "Trees",
        "tags": ["Tree", "DFS", "BFS", "Recursion"],
        "companies": {"google": 3, "apple": 2, "meta": 2, "amazon": 3, "microsoft": 3},
        "description": (
            "Given the roots of two binary trees `p` and `q`, return `true` if the trees are identical: the same "
            "shape **and** the same value at every corresponding node.\n\n"
            "Two empty trees are identical."
        ),
        "examples": [
            {"input": "p = [1,2,3], q = [1,2,3]", "output": "true"},
            {"input": "p = [1,2], q = [1,null,2]", "output": "false",
             "explanation": "Same values, but the 2 is a left child in p and a right child in q."},
            {"input": "p = [1,2,1], q = [1,1,2]", "output": "false"},
        ],
        "constraints": ["0 <= number of nodes in each tree <= 100", "-10^4 <= Node.val <= 10^4"],
        "hints": [
            "Compare the two roots, then compare left with left and right with right.",
            "Handle the three base cases first: both None (true), exactly one None (false), different values (false).",
        ],
        "function": "isSameTree",
        "signature": "def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:",
        "arg_types": {"p": "TreeNode", "q": "TreeNode"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"p": [1, 2, 3], "q": [1, 2, 3]}, "output": True},
            {"input": {"p": [1, 2], "q": [1, None, 2]}, "output": False},
            {"input": {"p": [1, 2, 1], "q": [1, 1, 2]}, "output": False},
            {"input": {"p": [], "q": []}, "output": True},
            {"input": {"p": [1], "q": []}, "output": False},
            {"input": {"p": [-5, None, 7], "q": [-5, None, 7]}, "output": True},
            {"input": {"p": _FULL_12, "q": _FULL_12}, "output": True},
            {"input": {"p": _FULL_12, "q": list(range(4094)) + [-1]}, "output": False},
            {"input": {"p": _left_chain(range(3000)), "q": _left_chain(range(3000))}, "output": True},
        ],
        "solution": '''class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q:
            return True
        if not p or not q or p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
''',
        "approach": (
            "**Walk both trees in lockstep.** Two trees are identical exactly when their roots agree and their left "
            "subtrees are identical and their right subtrees are identical. The recursion mirrors that definition.\n\n"
            "**Base cases:** both nodes missing is a match; one missing or a value mismatch is a failure. Order the "
            "checks so you never dereference None.\n\n"
            "**Iterative alternative:** a queue (or stack) of node pairs. Pop a pair, apply the same three checks, "
            "push `(p.left, q.left)` and `(p.right, q.right)`.\n\n"
            "**Common mistakes:** comparing only values with a traversal of each tree separately (two different "
            "shapes can produce the same inorder sequence); using `and` short-circuit incorrectly so the right "
            "subtree is skipped when the left fails is actually fine, but forgetting one of the two recursive calls is not.\n\n"
            "**Interview follow-ups:** symmetric tree (compare a tree with its own mirror: left with right); "
            "subtree-of-another-tree (run this check at every node); how to compare trees structurally in O(1) "
            "space (Morris traversal or serialising to a string, noting the pitfalls)."
        ),
        "complexity": {"time": "O(min(n, m))", "space": "O(min(h_p, h_q))"},
        "similar": ["subtree-of-another-tree", "symmetric-tree", "invert-binary-tree"],
    },
    # ------------------------------------------------------------------ 5
    {
        "id": "subtree-of-another-tree",
        "title": "Subtree of Another Tree",
        "difficulty": "Easy",
        "pattern": "Trees",
        "tags": ["Tree", "DFS", "String Matching", "Hash Function"],
        "companies": {"google": 2, "apple": 2, "meta": 3, "amazon": 4, "microsoft": 2},
        "description": (
            "Given the roots of two binary trees `root` and `subRoot`, return `true` if some node of `root`, "
            "together with **all** of its descendants, forms a tree identical to `subRoot`.\n\n"
            "The whole of `root` counts as a subtree of itself. Identical means same shape and same values."
        ),
        "examples": [
            {"input": "root = [3,4,5,1,2], subRoot = [4,1,2]", "output": "true",
             "explanation": "The node 4 and its children 1 and 2 match subRoot exactly."},
            {"input": "root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]", "output": "false",
             "explanation": "The node 2 in root has an extra child 0, so the subtree rooted at 4 is not identical."},
        ],
        "constraints": [
            "1 <= number of nodes in root <= 2000",
            "1 <= number of nodes in subRoot <= 1000",
            "-10^4 <= Node.val <= 10^4",
        ],
        "hints": [
            "You already know how to test whether two trees are identical. Where could the matching subtree start?",
            "Try every node of root as a candidate start and run the identical-tree check from there.",
            "To go faster, serialise both trees (with markers for null children) and use substring search or hashing.",
        ],
        "function": "isSubtree",
        "signature": "def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:",
        "arg_types": {"root": "TreeNode", "subRoot": "TreeNode"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"root": [3, 4, 5, 1, 2], "subRoot": [4, 1, 2]}, "output": True},
            {"input": {"root": [3, 4, 5, 1, 2, None, None, None, None, 0], "subRoot": [4, 1, 2]}, "output": False},
            {"input": {"root": [1, 1], "subRoot": [1]}, "output": True},
            {"input": {"root": [1], "subRoot": [1]}, "output": True},
            {"input": {"root": [1, 2, 3], "subRoot": [2, 3]}, "output": False},
            {"input": {"root": [1, 2, 3], "subRoot": [1, 2, 3]}, "output": True},
            {"input": {"root": _FULL_12,
                       "subRoot": [i for d in range(11) for i in range(2 ** (d + 1) - 1, 2 ** (d + 1) - 1 + 2 ** d)]},
             "output": True},
            {"input": {"root": _FULL_12, "subRoot": _FULL_12 + [4095]}, "output": False},
            {"input": {"root": _left_chain(range(3000)), "subRoot": _left_chain(range(1000, 3000))}, "output": True},
        ],
        "solution": '''class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def same(a, b):
            if not a and not b:
                return True
            if not a or not b or a.val != b.val:
                return False
            return same(a.left, b.left) and same(a.right, b.right)

        def walk(node):
            if not node:
                return False
            return same(node, subRoot) or walk(node.left) or walk(node.right)

        if not subRoot:
            return True
        return walk(root)
''',
        "approach": (
            "**Try every node of `root` as the place where `subRoot` could start, and reuse the identical-tree "
            "check.** `walk` visits each node; at each one, `same(node, subRoot)` verifies a full structural match. "
            "The `same` check usually fails on the first value comparison, so in practice this runs close to O(n).\n\n"
            "**Worst case** is O(n * m) when many nodes share the value of `subRoot`'s root and the mismatch is deep. "
            "The linear-time alternative is to serialise both trees in preorder with explicit null markers and a "
            "delimiter before each value (for example `,3,4,1,#,#,2,#,#,5,#,#` so that `2` does not match `12`), "
            "then check whether the pattern string occurs in the text string with KMP or Python's `in`. "
            "Merkle hashing of subtrees is another O(n + m) approach.\n\n"
            "**Common mistakes:** matching values only and ignoring structure; forgetting null markers in the "
            "serialised form (different shapes collapse to the same string); forgetting the delimiter so that "
            "`2` matches inside `12`.\n\n"
            "**Interview follow-ups:** make it O(n + m) (serialisation + KMP, or subtree hashing); "
            "what if node values are not unique and the tree is huge (hashing with collision checks); "
            "count how many times `subRoot` appears."
        ),
        "complexity": {"time": "O(n * m) worst case, O(n + m) with serialisation + KMP", "space": "O(h)"},
        "similar": ["same-tree", "find-duplicate-subtrees", "serialize-and-deserialize-binary-tree"],
    },
    # ------------------------------------------------------------------ 6
    {
        "id": "lowest-common-ancestor-of-bst",
        "title": "Lowest Common Ancestor of a Binary Search Tree",
        "difficulty": "Medium",
        "pattern": "Trees",
        "tags": ["Tree", "Binary Search Tree", "DFS"],
        "companies": {"google": 3, "apple": 3, "meta": 4, "amazon": 4, "microsoft": 3},
        "description": (
            "You are given the root of a **binary search tree** and the values `p` and `q` of two nodes that are "
            "both present in the tree. Return the **value** of their lowest common ancestor.\n\n"
            "The lowest common ancestor is the deepest node that has both `p` and `q` as descendants, where a node "
            "counts as a descendant of itself. For this problem return the ancestor's integer value rather than the "
            "node object."
        ),
        "examples": [
            {"input": "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8", "output": "6",
             "explanation": "2 is in the left subtree of 6 and 8 is in the right subtree, so 6 is the split point."},
            {"input": "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4", "output": "2",
             "explanation": "4 is a descendant of 2, and a node is its own ancestor."},
            {"input": "root = [2,1], p = 2, q = 1", "output": "2"},
        ],
        "constraints": [
            "2 <= number of nodes <= 10^5",
            "-10^9 <= Node.val <= 10^9",
            "All values are unique; p != q; both p and q exist in the tree.",
        ],
        "hints": [
            "What does the BST ordering tell you about where p and q live relative to the current node?",
            "If both are smaller than the current value, the answer is in the left subtree; if both are larger, in the right.",
            "The first node where p and q are on different sides (or equal to the node) is the LCA. No recursion or parent pointers needed.",
        ],
        "function": "lowestCommonAncestor",
        "signature": "def lowestCommonAncestor(self, root: Optional[TreeNode], p: int, q: int) -> int:",
        "arg_types": {"root": "TreeNode", "p": "int", "q": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 2, "q": 8}, "output": 6},
            {"input": {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 2, "q": 4}, "output": 2},
            {"input": {"root": [2, 1], "p": 2, "q": 1}, "output": 2},
            {"input": {"root": [5, 3, 8, 1, 4, 7, 9], "p": 1, "q": 4}, "output": 3},
            {"input": {"root": [5, 3, 8, 1, 4, 7, 9], "p": 7, "q": 9}, "output": 8},
            {"input": {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 3, "q": 5}, "output": 4},
            {"input": {"root": [0, -10, 10, -20, -5], "p": -20, "q": -5}, "output": -10},
            {"input": {"root": _balanced_bst(range(4095)), "p": 0, "q": 4094}, "output": 2047},
            {"input": {"root": _balanced_bst(range(4095)), "p": 0, "q": 1}, "output": 1},
            {"input": {"root": _balanced_bst(range(4095)), "p": 1024, "q": 2046}, "output": 1535},
            {"input": {"root": _right_chain(range(3000)), "p": 1500, "q": 2999}, "output": 1500},
            {"input": {"root": _left_chain(range(2999, -1, -1)), "p": 10, "q": 20}, "output": 20},
        ],
        "solution": '''class Solution:
    def lowestCommonAncestor(self, root: Optional[TreeNode], p: int, q: int) -> int:
        node = root
        while node:
            if p < node.val and q < node.val:
                node = node.left
            elif p > node.val and q > node.val:
                node = node.right
            else:
                return node.val
        return -1  # unreachable when p and q are guaranteed to exist
''',
        "approach": (
            "**Use the BST ordering to decide which way to go without ever searching for p or q.** Starting at the "
            "root: if both targets are smaller than the current value they are both in the left subtree, so move "
            "left; if both are larger, move right. The first node where they split (one on each side) or where the "
            "node equals one of them is the lowest common ancestor.\n\n"
            "**Why it works:** every ancestor of both p and q lies on the root-to-LCA path, and along that path the "
            "two targets are on the same side at every step until the LCA. Below the LCA they diverge, so no deeper "
            "node can contain both.\n\n"
            "**Common mistakes:** applying the general binary-tree LCA (post-order search for both nodes), which is "
            "correct but ignores the O(h) opportunity; using `<=` and `>=` so that a node equal to p or q is "
            "skipped.\n\n"
            "**Interview follow-ups:** LCA in a plain binary tree without the BST property (post-order: return the "
            "node if both sides found something); LCA with parent pointers (walk up and use a set, or align depths); "
            "LCA of k nodes (take min and max of the k values and run the same loop)."
        ),
        "complexity": {"time": "O(h)", "space": "O(1)"},
        "similar": ["lowest-common-ancestor-of-a-binary-tree", "validate-binary-search-tree", "kth-smallest-element-in-bst"],
    },
    # ------------------------------------------------------------------ 7
    {
        "id": "binary-tree-level-order-traversal",
        "title": "Binary Tree Level Order Traversal",
        "difficulty": "Medium",
        "pattern": "Trees",
        "tags": ["Tree", "BFS"],
        "companies": {"google": 3, "apple": 3, "meta": 4, "amazon": 5, "microsoft": 4},
        "description": (
            "Given the root of a binary tree, return the values of its nodes grouped **level by level**, from the "
            "root down, with each level listed left to right.\n\n"
            "Return a list of lists; the empty tree gives an empty list."
        ),
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]"},
            {"input": "root = [1]", "output": "[[1]]"},
            {"input": "root = []", "output": "[]"},
        ],
        "constraints": ["0 <= number of nodes <= 2000", "-1000 <= Node.val <= 1000"],
        "hints": [
            "A queue visits nodes in the order you want. The trick is knowing where one level ends and the next begins.",
            "At the start of each round, the queue holds exactly one level. Record its length and pop exactly that many nodes.",
            "Alternatively, DFS with a depth parameter and append to result[depth], creating the list when first reached.",
        ],
        "function": "levelOrder",
        "signature": "def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:",
        "arg_types": {"root": "TreeNode"},
        "return_type": "List[List[int]]",
        "compare": "exact",
        "tests": [
            {"input": {"root": [3, 9, 20, None, None, 15, 7]}, "output": [[3], [9, 20], [15, 7]]},
            {"input": {"root": [1]}, "output": [[1]]},
            {"input": {"root": []}, "output": []},
            {"input": {"root": [1, 2, None, 3, None, 4]}, "output": [[1], [2], [3], [4]]},
            {"input": {"root": [1, None, 2, None, 3]}, "output": [[1], [2], [3]]},
            {"input": {"root": [1, 2, 3, None, 4, 5, None, 6]}, "output": [[1], [2, 3], [4, 5], [6]]},
            {"input": {"root": _FULL_12}, "output": _LEVELS_12},
            {"input": {"root": _left_chain(range(3000))}, "output": [[i] for i in range(3000)]},
        ],
        "solution": '''class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        result, queue = [], deque([root])
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)
        return result
''',
        "approach": (
            "**BFS with a level boundary.** A plain queue already produces nodes in level order; the only addition "
            "is to snapshot `len(queue)` at the start of each round so that exactly one level is popped before the "
            "next list is started. Children enqueued during the round form the next level.\n\n"
            "**Why it works:** by induction, when a round begins the queue contains precisely the nodes at one depth, "
            "in left-to-right order, because the previous round pushed children in that order.\n\n"
            "**DFS variant:** recurse with `(node, depth)`; if `depth == len(result)` start a new list; append the "
            "value to `result[depth]`. Visiting left before right keeps each level ordered.\n\n"
            "**Common mistakes:** using `while len(queue)` as the inner loop condition instead of a fixed count "
            "(the length changes as you push); pushing None children and then having to filter them.\n\n"
            "**Interview follow-ups:** bottom-up level order (reverse the result); zigzag order; average of each "
            "level; right side view (last element of each level); connect next-right pointers in O(1) extra space."
        ),
        "complexity": {"time": "O(n)", "space": "O(w) for the widest level, O(n) worst case"},
        "similar": ["binary-tree-zigzag-level-order-traversal", "binary-tree-right-side-view", "n-ary-tree-level-order-traversal"],
    },
    # ------------------------------------------------------------------ 8
    {
        "id": "binary-tree-right-side-view",
        "title": "Binary Tree Right Side View",
        "difficulty": "Medium",
        "pattern": "Trees",
        "tags": ["Tree", "BFS", "DFS"],
        "companies": {"google": 2, "apple": 2, "meta": 5, "amazon": 3, "microsoft": 2},
        "description": (
            "Imagine standing to the right of a binary tree and looking at it sideways. Return the values you can "
            "see, listed from top to bottom.\n\n"
            "In other words, return the **rightmost node of every level**. Note that a left child can be visible if "
            "the level has no nodes further to the right."
        ),
        "examples": [
            {"input": "root = [1,2,3,null,5,null,4]", "output": "[1,3,4]"},
            {"input": "root = [1,2,3,4]", "output": "[1,3,4]",
             "explanation": "4 is a left child, but it is the only node on its level so it is visible from the right."},
            {"input": "root = []", "output": "[]"},
        ],
        "constraints": ["0 <= number of nodes <= 100", "-100 <= Node.val <= 100"],
        "hints": [
            "It is not just 'always go right'. A deep left branch can stick out below the right branch.",
            "Level order traversal: take the last node of each level.",
            "DFS alternative: visit right child first and record the first node you reach at each new depth.",
        ],
        "function": "rightSideView",
        "signature": "def rightSideView(self, root: Optional[TreeNode]) -> List[int]:",
        "arg_types": {"root": "TreeNode"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"root": [1, 2, 3, None, 5, None, 4]}, "output": [1, 3, 4]},
            {"input": {"root": [1, 2, 3, 4]}, "output": [1, 3, 4]},
            {"input": {"root": []}, "output": []},
            {"input": {"root": [1, None, 3]}, "output": [1, 3]},
            {"input": {"root": [1, 2]}, "output": [1, 2]},
            {"input": {"root": [1, 2, 3, 4, None, None, None, 5]}, "output": [1, 3, 4, 5]},
            {"input": {"root": _FULL_12}, "output": [2 ** (d + 1) - 2 for d in range(12)]},
            {"input": {"root": _left_chain(range(3000))}, "output": list(range(3000))},
        ],
        "solution": '''class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        view, queue = [], deque([root])
        while queue:
            view.append(queue[-1].val)
            for _ in range(len(queue)):
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        return view
''',
        "approach": (
            "**The right side view is the last node of every level.** Run a level-order BFS; before consuming a "
            "level, the back of the queue is its rightmost node, so record `queue[-1].val` once per level.\n\n"
            "**DFS alternative (often preferred in interviews):** recurse right child first, carrying the depth. "
            "The first time you reach a given depth, that node is the one visible from the right; "
            "`if depth == len(view): view.append(node.val)`.\n\n"
            "**Common mistakes:** following only right pointers (misses deeper left branches, as in example 2); "
            "in the DFS version, recursing left first and then overwriting.\n\n"
            "**Interview follow-ups:** left side view (symmetric); top view / bottom view (track horizontal "
            "distance); return the nodes themselves rather than values; boundary of a binary tree."
        ),
        "complexity": {"time": "O(n)", "space": "O(w) for BFS, O(h) for DFS"},
        "similar": ["binary-tree-level-order-traversal", "binary-tree-zigzag-level-order-traversal", "boundary-of-binary-tree"],
    },
    # ------------------------------------------------------------------ 9
    {
        "id": "count-good-nodes-in-binary-tree",
        "title": "Count Good Nodes in Binary Tree",
        "difficulty": "Medium",
        "pattern": "Trees",
        "tags": ["Tree", "DFS"],
        "companies": {"google": 1, "apple": 1, "meta": 2, "amazon": 3, "microsoft": 3},
        "description": (
            "A node in a binary tree is **good** if no node on the path from the root to it (excluding itself) has "
            "a value strictly greater than its own. The root is always good.\n\n"
            "Given the root, return the number of good nodes."
        ),
        "examples": [
            {"input": "root = [3,1,4,3,null,1,5]", "output": "4",
             "explanation": "Good nodes: 3 (root), 4 (path max 3), 3 (path max 3, equal is fine), 5 (path max 4). "
                            "The two 1s are not good because a 3 or 4 appears above them."},
            {"input": "root = [3,3,null,4,2]", "output": "3",
             "explanation": "Root 3, the left 3, and 4 are good; 2 is not because 3 is above it."},
            {"input": "root = [1]", "output": "1"},
        ],
        "constraints": ["1 <= number of nodes <= 10^5", "-10^4 <= Node.val <= 10^4"],
        "hints": [
            "Whether a node is good depends only on the largest value above it.",
            "Pass the maximum seen so far down the recursion. A node is good when node.val >= that maximum.",
            "Update the maximum before recursing into children, and start with negative infinity for the root.",
        ],
        "function": "goodNodes",
        "signature": "def goodNodes(self, root: TreeNode) -> int:",
        "arg_types": {"root": "TreeNode"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"root": [3, 1, 4, 3, None, 1, 5]}, "output": 4},
            {"input": {"root": [3, 3, None, 4, 2]}, "output": 3},
            {"input": {"root": [1]}, "output": 1},
            {"input": {"root": []}, "output": 0},
            {"input": {"root": [-1, -2, -3]}, "output": 1},
            {"input": {"root": [5, 4, 6, 3, None, None, 7]}, "output": 3},
            {"input": {"root": _left_chain(range(3000))}, "output": 3000},
            {"input": {"root": _left_chain(range(2999, -1, -1))}, "output": 1},
            {"input": {"root": _FULL_12}, "output": 4095},
        ],
        "solution": '''class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node, path_max):
            if not node:
                return 0
            good = 1 if node.val >= path_max else 0
            path_max = max(path_max, node.val)
            return good + dfs(node.left, path_max) + dfs(node.right, path_max)

        return dfs(root, float("-inf"))
''',
        "approach": (
            "**Carry the running maximum of the root-to-node path down the recursion.** A node is good exactly "
            "when its value is at least that maximum, so each node is decided in O(1) and contributes 0 or 1 to the "
            "count returned from its subtree.\n\n"
            "**Why it works:** the only information the definition needs about the ancestors is their maximum, "
            "and that maximum changes only when the current node is itself a new record, so updating it before "
            "recursing is sufficient.\n\n"
            "**Common mistakes:** using strict `>` instead of `>=` (a node equal to the path maximum is good); "
            "initialising the maximum to 0 instead of negative infinity, which breaks trees with negative values "
            "(see the `[-1,-2,-3]` test); recomputing the path maximum by walking up each time (O(n * h)).\n\n"
            "**Interview follow-ups:** iterative version with a stack of `(node, path_max)` pairs; count nodes "
            "that are the *minimum* on their path; return the good nodes' values; what if you also need the count "
            "of good nodes in each subtree (return a tuple)."
        ),
        "complexity": {"time": "O(n)", "space": "O(h)"},
        "similar": ["path-sum-ii", "maximum-depth-of-binary-tree", "validate-binary-search-tree"],
    },
    # ------------------------------------------------------------------ 10
    {
        "id": "validate-binary-search-tree",
        "title": "Validate Binary Search Tree",
        "difficulty": "Medium",
        "pattern": "Trees",
        "tags": ["Tree", "Binary Search Tree", "DFS"],
        "companies": {"google": 3, "apple": 3, "meta": 4, "amazon": 5, "microsoft": 4},
        "description": (
            "Given the root of a binary tree, decide whether it is a valid **binary search tree**.\n\n"
            "A valid BST requires that for every node, **all** values in its left subtree are strictly smaller "
            "and **all** values in its right subtree are strictly larger. Duplicate values are not allowed. "
            "The empty tree is valid."
        ),
        "examples": [
            {"input": "root = [2,1,3]", "output": "true"},
            {"input": "root = [5,1,4,null,null,3,6]", "output": "false",
             "explanation": "The right child of 5 is 4, which is not larger than 5."},
            {"input": "root = [5,4,6,null,null,3,7]", "output": "false",
             "explanation": "3 < 6 looks fine locally, but 3 sits in the right subtree of 5, so it must also be "
                            "greater than 5. Checking only parent-child pairs misses this."},
        ],
        "constraints": ["0 <= number of nodes <= 10^4", "-2^31 <= Node.val <= 2^31 - 1"],
        "hints": [
            "Comparing each node with only its direct children is not enough. What range of values is allowed at each node?",
            "Pass down an open interval (low, high). Going left tightens high to the node's value; going right tightens low.",
            "Alternatively, an inorder traversal of a valid BST is strictly increasing; check consecutive values.",
        ],
        "function": "isValidBST",
        "signature": "def isValidBST(self, root: Optional[TreeNode]) -> bool:",
        "arg_types": {"root": "TreeNode"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"root": [2, 1, 3]}, "output": True},
            {"input": {"root": [5, 1, 4, None, None, 3, 6]}, "output": False},
            {"input": {"root": [5, 4, 6, None, None, 3, 7]}, "output": False},
            {"input": {"root": [1]}, "output": True},
            {"input": {"root": []}, "output": True},
            {"input": {"root": [2, 2, 2]}, "output": False},
            {"input": {"root": [0, -1]}, "output": True},
            {"input": {"root": [2147483647]}, "output": True},
            {"input": {"root": _balanced_bst(range(4095))}, "output": True},
            {"input": {"root": _balanced_bst(range(4095))[:-2] + [4090, 4094]}, "output": False},
            {"input": {"root": _right_chain(range(3000))}, "output": True},
        ],
        "solution": '''class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def valid(node, low, high):
            if not node:
                return True
            if not (low < node.val < high):
                return False
            return valid(node.left, low, node.val) and valid(node.right, node.val, high)

        return valid(root, float("-inf"), float("inf"))
''',
        "approach": (
            "**Every node must lie inside an open interval determined by its ancestors, not just by its parent.** "
            "Recurse with `(low, high)`: the root may be anything, the left child must be below the parent's value "
            "(so `high` becomes `node.val`), the right child above it (`low` becomes `node.val`). A node outside "
            "its interval invalidates the tree.\n\n"
            "**Why it works:** the interval at a node is exactly the intersection of all constraints imposed by its "
            "ancestors, each of which says 'you are in my left subtree so be smaller' or 'in my right subtree so be "
            "larger'. The tightest of each kind is the nearest such ancestor, which is precisely what the recursion "
            "passes down.\n\n"
            "**Inorder alternative:** an inorder walk of a BST yields a strictly increasing sequence. Keep the "
            "previous value and fail if the current one is not larger. Works iteratively with a stack, O(h) space.\n\n"
            "**Common mistakes:** checking only `left.val < node.val < right.val` (fails on the third example and "
            "the large test, where the bad node is deep and locally fine); using `<=` which accepts duplicates; "
            "initialising bounds to fixed 32-bit limits in a way that rejects a legal node equal to the limit "
            "(use infinity or None).\n\n"
            "**Interview follow-ups:** do it iteratively (stack of `(node, low, high)` or inorder with a stack); "
            "recover a BST where two nodes were swapped; find the largest BST subtree; validate with duplicates "
            "allowed on one side."
        ),
        "complexity": {"time": "O(n)", "space": "O(h)"},
        "similar": ["kth-smallest-element-in-bst", "lowest-common-ancestor-of-bst", "recover-binary-search-tree"],
    },
    # ------------------------------------------------------------------ 11
    {
        "id": "kth-smallest-element-in-bst",
        "title": "Kth Smallest Element in a BST",
        "difficulty": "Medium",
        "pattern": "Trees",
        "tags": ["Tree", "Binary Search Tree", "DFS", "Inorder"],
        "companies": {"google": 2, "apple": 2, "meta": 3, "amazon": 4, "microsoft": 3},
        "description": (
            "Given the root of a binary search tree and an integer `k`, return the `k`-th smallest value in the "
            "tree (1-indexed).\n\n"
            "All values are distinct and `k` is guaranteed to be valid."
        ),
        "examples": [
            {"input": "root = [3,1,4,null,2], k = 1", "output": "1"},
            {"input": "root = [5,3,6,2,4,null,null,1], k = 3", "output": "3",
             "explanation": "Sorted order is 1, 2, 3, 4, 5, 6; the third is 3."},
        ],
        "constraints": ["1 <= k <= number of nodes <= 10^4", "0 <= Node.val <= 10^4"],
        "hints": [
            "In which traversal order does a BST produce its values sorted?",
            "Inorder traversal visits values in ascending order. The k-th node visited is the answer.",
            "Do it iteratively with a stack so you can stop as soon as k nodes have been popped, instead of building the whole list.",
        ],
        "function": "kthSmallest",
        "signature": "def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:",
        "arg_types": {"root": "TreeNode", "k": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"root": [3, 1, 4, None, 2], "k": 1}, "output": 1},
            {"input": {"root": [5, 3, 6, 2, 4, None, None, 1], "k": 3}, "output": 3},
            {"input": {"root": [1], "k": 1}, "output": 1},
            {"input": {"root": [2, 1, 3], "k": 3}, "output": 3},
            {"input": {"root": [2, 1, 3], "k": 2}, "output": 2},
            {"input": {"root": _balanced_bst(range(-10, 10)), "k": 1}, "output": -10},
            {"input": {"root": _balanced_bst(range(4095)), "k": 1}, "output": 0},
            {"input": {"root": _balanced_bst(range(4095)), "k": 4095}, "output": 4094},
            {"input": {"root": _balanced_bst(range(4095)), "k": 2048}, "output": 2047},
            {"input": {"root": _right_chain(range(3000)), "k": 1500}, "output": 1499},
        ],
        "solution": '''class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack, node = [], root
        while True:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            k -= 1
            if k == 0:
                return node.val
            node = node.right
''',
        "approach": (
            "**Inorder traversal of a BST visits values in sorted order, so the k-th node popped is the answer.** "
            "The iterative version with an explicit stack lets you stop early: push the whole left spine, pop a "
            "node (that is the next smallest), then move to its right child and repeat.\n\n"
            "**Why it works:** the left spine contains everything smaller than the current node; popping returns "
            "the smallest unvisited value; everything in its right subtree is larger than it but smaller than its "
            "ancestors still on the stack, which is exactly the next range of values.\n\n"
            "**Common mistakes:** collecting all values into a list and indexing (correct but O(n) always, and "
            "O(n) space); confusing 0-indexed and 1-indexed k; recursing without a way to stop, so the recursion "
            "always visits the whole tree.\n\n"
            "**Interview follow-ups:** the BST is modified often and k-th smallest is queried often: augment each "
            "node with the size of its subtree, then answer in O(h) by comparing k with the left subtree size "
            "(order-statistic tree); k-th largest (reverse inorder); the k-th smallest in a stream of BST insertions."
        ),
        "complexity": {"time": "O(h + k)", "space": "O(h)"},
        "similar": ["validate-binary-search-tree", "binary-search-tree-iterator", "lowest-common-ancestor-of-bst"],
    },
    # ------------------------------------------------------------------ 12
    {
        "id": "construct-binary-tree-from-preorder-and-inorder",
        "title": "Construct Binary Tree from Preorder and Inorder Traversal",
        "difficulty": "Medium",
        "pattern": "Trees",
        "tags": ["Tree", "Hash Table", "Divide and Conquer", "Recursion"],
        "companies": {"google": 3, "apple": 2, "meta": 3, "amazon": 3, "microsoft": 4},
        "description": (
            "You are given two integer arrays, `preorder` and `inorder`, which are the preorder and inorder "
            "traversals of the same binary tree. All values are distinct.\n\n"
            "Rebuild the tree and return its root."
        ),
        "examples": [
            {"input": "preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]", "output": "[3,9,20,null,null,15,7]",
             "explanation": "3 is first in preorder so it is the root. In inorder, everything before 3 ([9]) is the "
                            "left subtree and everything after ([15,20,7]) is the right subtree."},
            {"input": "preorder = [-1], inorder = [-1]", "output": "[-1]"},
        ],
        "constraints": [
            "1 <= preorder.length <= 3000",
            "inorder.length == preorder.length",
            "-3000 <= values <= 3000",
            "All values are unique and the traversals describe the same tree.",
        ],
        "hints": [
            "The first element of preorder is always the root of the current subtree.",
            "Find that root in inorder: elements to its left form the left subtree, elements to its right form the right subtree.",
            "Slicing arrays and calling index() each time is O(n^2). Store value -> inorder index in a hash map and recurse on index ranges with a single moving preorder pointer.",
        ],
        "function": "buildTree",
        "signature": "def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:",
        "arg_types": {"preorder": "List[int]", "inorder": "List[int]"},
        "return_type": "TreeNode",
        "compare": "exact",
        "tests": [
            {"input": {"preorder": [3, 9, 20, 15, 7], "inorder": [9, 3, 15, 20, 7]}, "output": [3, 9, 20, None, None, 15, 7]},
            {"input": {"preorder": [-1], "inorder": [-1]}, "output": [-1]},
            {"input": {"preorder": [1, 2], "inorder": [2, 1]}, "output": [1, 2]},
            {"input": {"preorder": [1, 2], "inorder": [1, 2]}, "output": [1, None, 2]},
            {"input": {"preorder": [1, 2, 3], "inorder": [3, 2, 1]}, "output": [1, 2, None, 3]},
            {"input": {"preorder": [1, 2, 4, 5, 3, 6, 7], "inorder": [4, 2, 5, 1, 6, 3, 7]}, "output": [1, 2, 3, 4, 5, 6, 7]},
            {"input": {"preorder": list(range(3000)), "inorder": list(range(2999, -1, -1))}, "output": _left_chain(range(3000))},
            {"input": {"preorder": list(range(3000)), "inorder": list(range(3000))}, "output": _right_chain(range(3000))},
            {"input": {"preorder": _complete_order(4095, "pre"), "inorder": _complete_order(4095, "in")}, "output": _FULL_12},
        ],
        "solution": '''class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        pos = {val: i for i, val in enumerate(inorder)}
        self.next = 0  # index of the next root to consume from preorder

        def build(lo, hi):
            """Build the subtree whose inorder values are inorder[lo..hi]."""
            if lo > hi:
                return None
            val = preorder[self.next]
            self.next += 1
            node = TreeNode(val)
            mid = pos[val]
            node.left = build(lo, mid - 1)
            node.right = build(mid + 1, hi)
            return node

        return build(0, len(inorder) - 1)
''',
        "approach": (
            "**Preorder tells you the root; inorder tells you how many nodes go left of it.** The first unused "
            "preorder value is the root of the current subtree. Its position `mid` in inorder splits the current "
            "inorder range into the left subtree `[lo, mid-1]` and the right subtree `[mid+1, hi]`. Because "
            "preorder lists the entire left subtree before the right one, consuming preorder values with a single "
            "forward pointer while recursing left-then-right hands every subtree exactly its own root.\n\n"
            "**Making it linear:** a hash map from value to inorder index replaces the O(n) `index()` lookup, "
            "and passing index bounds instead of slicing avoids copying. The result is O(n) time and O(n) space. "
            "The 3000-node chain test is where the slicing version turns quadratic.\n\n"
            "**Common mistakes:** slicing `preorder[1:mid+1]` and `inorder[:mid]` at every level (O(n^2) in both "
            "time and memory); building the right subtree before the left while sharing the preorder pointer; "
            "off-by-one on the inorder bounds.\n\n"
            "**Interview follow-ups:** inorder + postorder (same idea, consume postorder from the back and build "
            "right first); preorder + postorder (not unique in general, show why); do it iteratively with a stack; "
            "what if values are not unique (the reconstruction is ambiguous)."
        ),
        "complexity": {"time": "O(n)", "space": "O(n) for the index map plus O(h) recursion"},
        "similar": ["construct-binary-tree-from-inorder-and-postorder", "serialize-and-deserialize-binary-tree", "maximum-binary-tree"],
    },
    # ------------------------------------------------------------------ 13
    {
        "id": "binary-tree-maximum-path-sum",
        "title": "Binary Tree Maximum Path Sum",
        "difficulty": "Hard",
        "pattern": "Trees",
        "tags": ["Tree", "DFS", "Dynamic Programming"],
        "companies": {"google": 3, "apple": 2, "meta": 4, "amazon": 4, "microsoft": 3},
        "description": (
            "A **path** in a binary tree is any sequence of nodes where each consecutive pair is connected by an "
            "edge and no node appears twice. A path does not need to go through the root and may consist of a "
            "single node.\n\n"
            "Given the root, return the largest possible sum of node values along any path. Values may be negative."
        ),
        "examples": [
            {"input": "root = [1,2,3]", "output": "6", "explanation": "The path 2 -> 1 -> 3 sums to 6."},
            {"input": "root = [-10,9,20,null,null,15,7]", "output": "42",
             "explanation": "The path 15 -> 20 -> 7 sums to 42; including -10 would only hurt."},
            {"input": "root = [-3]", "output": "-3", "explanation": "A path must contain at least one node."},
        ],
        "constraints": ["1 <= number of nodes <= 3 * 10^4", "-1000 <= Node.val <= 1000"],
        "hints": [
            "Every path has a unique topmost node. Think about the best path that 'bends' at a given node.",
            "At node x the best bending path is x.val + (best downward path from the left) + (best downward path from the right), where a negative downward contribution is replaced by 0.",
            "The recursion must return something different from what it records: return the best single downward branch (for the parent to extend), but record the bending sum in a global maximum.",
        ],
        "function": "maxPathSum",
        "signature": "def maxPathSum(self, root: Optional[TreeNode]) -> int:",
        "arg_types": {"root": "TreeNode"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"root": [1, 2, 3]}, "output": 6},
            {"input": {"root": [-10, 9, 20, None, None, 15, 7]}, "output": 42},
            {"input": {"root": [-3]}, "output": -3},
            {"input": {"root": [2, -1]}, "output": 2},
            {"input": {"root": [-1, -2, -3]}, "output": -1},
            {"input": {"root": [1, -2, -3, 1, 3, -2, None, -1]}, "output": 3},
            {"input": {"root": [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]}, "output": 48},
            {"input": {"root": _left_chain(range(3000))}, "output": 2999 * 3000 // 2},
            {"input": {"root": [1] * 4095}, "output": 23},
            {"input": {"root": [-1] * 4095}, "output": -1},
        ],
        "solution": '''class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        best = float("-inf")

        def gain(node):
            """Largest sum of a path that starts at node and goes straight down."""
            nonlocal best
            if not node:
                return 0
            left = max(gain(node.left), 0)
            right = max(gain(node.right), 0)
            best = max(best, node.val + left + right)
            return node.val + max(left, right)

        gain(root)
        return best
''',
        "approach": (
            "**Separate what a node reports to its parent from what it records for the answer.** For each node "
            "compute `gain(node)`: the best sum of a path that starts at the node and goes down one side. A parent "
            "can only extend one side, so that is the value returned. But the best path *through* the node may use "
            "both sides: `node.val + gain(left) + gain(right)`. Record that in a global maximum. Negative gains are "
            "clamped to 0 because you are always free to not extend into a subtree.\n\n"
            "**Why it works:** every path has a unique highest node, and at that node the path is exactly the node "
            "plus at most one downward chain on each side. Enumerating the best such combination at every node "
            "covers every possible path.\n\n"
            "**Common mistakes:** returning the two-sided sum to the parent (produces paths that fork, which are not "
            "paths); initialising `best` to 0 instead of negative infinity (fails when all values are negative, "
            "see `[-1,-2,-3]`); forgetting to clamp negative gains at 0.\n\n"
            "**Interview follow-ups:** return the path itself (store the argmax node and rebuild from the recorded "
            "best children); longest path with all equal values (same skeleton); maximum sum path from root to "
            "leaf (simpler: no bending); the n-ary version (keep the top two child gains)."
        ),
        "complexity": {"time": "O(n)", "space": "O(h)"},
        "similar": ["diameter-of-binary-tree", "path-sum-ii", "longest-univalue-path"],
    },
    # ------------------------------------------------------------------ 14
    {
        "id": "binary-tree-zigzag-level-order-traversal",
        "title": "Binary Tree Zigzag Level Order Traversal",
        "difficulty": "Medium",
        "pattern": "Trees",
        "tags": ["Tree", "BFS"],
        "companies": {"google": 2, "apple": 2, "meta": 3, "amazon": 4, "microsoft": 4},
        "description": (
            "Return the values of a binary tree level by level, but **alternate direction** on each level: the "
            "first level left to right, the second right to left, the third left to right, and so on.\n\n"
            "Return a list of lists; the empty tree gives an empty list."
        ),
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[20,9],[15,7]]"},
            {"input": "root = [1]", "output": "[[1]]"},
            {"input": "root = []", "output": "[]"},
        ],
        "constraints": ["0 <= number of nodes <= 2000", "-100 <= Node.val <= 100"],
        "hints": [
            "Start from ordinary level order traversal.",
            "Odd-numbered levels (0-indexed) just need to be reversed before being added to the result.",
            "To avoid the reverse, fill a preallocated list from the back on odd levels, or use a deque and appendleft.",
        ],
        "function": "zigzagLevelOrder",
        "signature": "def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:",
        "arg_types": {"root": "TreeNode"},
        "return_type": "List[List[int]]",
        "compare": "exact",
        "tests": [
            {"input": {"root": [3, 9, 20, None, None, 15, 7]}, "output": [[3], [20, 9], [15, 7]]},
            {"input": {"root": [1]}, "output": [[1]]},
            {"input": {"root": []}, "output": []},
            {"input": {"root": [1, 2, 3, 4, 5, 6, 7]}, "output": [[1], [3, 2], [4, 5, 6, 7]]},
            {"input": {"root": [1, 2, 3, 4, None, None, 5]}, "output": [[1], [3, 2], [4, 5]]},
            {"input": {"root": [1, 2, None, 3, None, 4]}, "output": [[1], [2], [3], [4]]},
            {"input": {"root": _FULL_12},
             "output": [lvl[::-1] if d % 2 else lvl for d, lvl in enumerate(_LEVELS_12)]},
            {"input": {"root": _left_chain(range(3000))}, "output": [[i] for i in range(3000)]},
        ],
        "solution": '''class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        result, queue, left_to_right = [], deque([root]), True
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level if left_to_right else level[::-1])
            left_to_right = not left_to_right
        return result
''',
        "approach": (
            "**It is level order traversal with every other level reversed.** Keep the BFS exactly as in "
            "binary-tree-level-order-traversal and flip a boolean after each level; when the flag says right-to-left, "
            "append the reversed level. The traversal order of the queue never changes, which keeps the children "
            "correctly ordered for the next level.\n\n"
            "**Without the reverse:** allocate `level = [0] * size` and write to index `size - 1 - i` on odd levels, "
            "or use a deque and `appendleft`. Same asymptotic cost, but it shows awareness of the extra pass.\n\n"
            "**Common mistakes:** trying to alternate the order in which children are *enqueued* (this corrupts "
            "later levels); forgetting to flip the flag when a level is empty (not possible here but a sign of "
            "fragile logic); off-by-one on which parity is reversed (level 0 is left to right).\n\n"
            "**Interview follow-ups:** do it with two stacks instead of a queue plus reverse; spiral order of a "
            "matrix (same alternate-direction idea); vertical order traversal."
        ),
        "complexity": {"time": "O(n)", "space": "O(w)"},
        "similar": ["binary-tree-level-order-traversal", "binary-tree-right-side-view"],
    },
    # ------------------------------------------------------------------ 15
    {
        "id": "path-sum-ii",
        "title": "Path Sum II",
        "difficulty": "Medium",
        "pattern": "Trees",
        "tags": ["Tree", "DFS", "Backtracking"],
        "companies": {"google": 2, "apple": 2, "meta": 3, "amazon": 4, "microsoft": 2},
        "description": (
            "Given the root of a binary tree and an integer `targetSum`, return **every root-to-leaf path** whose "
            "node values add up to `targetSum`. Each path is a list of values from the root down to the leaf.\n\n"
            "A leaf is a node with no children; a path must end at a leaf. Paths may be returned in any order."
        ),
        "examples": [
            {"input": "root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22",
             "output": "[[5,4,11,2],[5,8,4,5]]",
             "explanation": "5+4+11+2 = 22 and 5+8+4+5 = 22. The path 5 -> 8 -> 4 -> 1 sums to 18 and does not count."},
            {"input": "root = [1,2,3], targetSum = 5", "output": "[]",
             "explanation": "1+2 = 3 and 1+3 = 4. There is no path of sum 5 because 2 -> 1 -> 3 is not root-to-leaf."},
            {"input": "root = [1,2], targetSum = 0", "output": "[]"},
        ],
        "constraints": ["0 <= number of nodes <= 5000", "-1000 <= Node.val <= 1000", "-1000 <= targetSum <= 1000"],
        "hints": [
            "Walk from the root to each leaf while keeping the current path.",
            "Pass the remaining sum down; at a leaf, if the remaining sum equals the leaf's value, copy the path into the answer.",
            "Append the node on the way down and pop it on the way back (backtracking) so a single shared list serves every branch.",
        ],
        "function": "pathSum",
        "signature": "def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:",
        "arg_types": {"root": "TreeNode", "targetSum": "int"},
        "return_type": "List[List[int]]",
        "compare": "unordered",
        "tests": [
            {"input": {"root": [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], "targetSum": 22},
             "output": [[5, 4, 11, 2], [5, 8, 4, 5]]},
            {"input": {"root": [1, 2, 3], "targetSum": 5}, "output": []},
            {"input": {"root": [1, 2], "targetSum": 0}, "output": []},
            {"input": {"root": [], "targetSum": 0}, "output": []},
            {"input": {"root": [1], "targetSum": 1}, "output": [[1]]},
            {"input": {"root": [-2, None, -3], "targetSum": -5}, "output": [[-2, -3]]},
            {"input": {"root": [0, 1, 1], "targetSum": 1}, "output": [[0, 1], [0, 1]]},
            {"input": {"root": [1, -1, 2, 3, None, None, None], "targetSum": 3}, "output": [[1, -1, 3], [1, 2]]},
            {"input": {"root": _left_chain(range(3000)), "targetSum": 2999 * 3000 // 2}, "output": [list(range(3000))]},
            {"input": {"root": [1] * 4095, "targetSum": 12}, "output": [[1] * 12] * 2048},
            {"input": {"root": _FULL_12, "targetSum": -1}, "output": []},
        ],
        "solution": '''class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        result, path = [], []

        def dfs(node, remaining):
            if not node:
                return
            path.append(node.val)
            remaining -= node.val
            if not node.left and not node.right:
                if remaining == 0:
                    result.append(path[:])
            else:
                dfs(node.left, remaining)
                dfs(node.right, remaining)
            path.pop()

        dfs(root, targetSum)
        return result
''',
        "approach": (
            "**DFS with backtracking on a single shared path.** Descend from the root, appending each value to "
            "`path` and subtracting it from the remaining target. At a leaf, if the remaining target is exactly 0, "
            "copy the current path into the result. On the way back up, pop the value so the list is correct for "
            "the sibling branch.\n\n"
            "**Why it works:** every root-to-leaf path is visited exactly once by the DFS, and `path` always holds "
            "exactly the nodes from the root to the current node because every append is matched by a pop.\n\n"
            "**Common mistakes:** appending `path` itself instead of a copy (`path[:]`), so every stored answer "
            "later mutates to empty; treating a node with one child as a leaf; stopping early when the remaining "
            "sum becomes negative (invalid here because values can be negative, see the `[-2,null,-3]` test); "
            "checking `remaining == 0` at internal nodes.\n\n"
            "**Interview follow-ups:** Path Sum I (just a boolean, no path storage); Path Sum III (paths may start "
            "and end anywhere: prefix sums with a hash map); return only the count; memory discussion: the output "
            "itself can be O(n * h) in the worst case, as the 2048-path test shows."
        ),
        "complexity": {"time": "O(n * h) worst case for copying paths, O(n) if no path matches", "space": "O(h) beyond the output"},
        "similar": ["path-sum", "path-sum-iii", "binary-tree-maximum-path-sum", "count-good-nodes-in-binary-tree"],
    },
]
