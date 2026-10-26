"""Linked List pattern problems. See SCHEMA.md for the dict format.

reverse-linked-list lives in bank/seed.py and is intentionally not repeated here.
"""

PROBLEMS = [
    {
        "id": "merge-two-sorted-lists",
        "title": "Merge Two Sorted Lists",
        "difficulty": "Easy",
        "pattern": "Linked List",
        "tags": ["Linked List", "Recursion"],
        "companies": {"google": 2, "apple": 4, "meta": 2, "amazon": 4, "microsoft": 4},
        "description": (
            "You are given the heads of two singly linked lists, `list1` and `list2`, each sorted in non-decreasing order. "
            "Merge them into one sorted list by **splicing the existing nodes together** (do not allocate new value nodes) "
            "and return the head of the merged list."
        ),
        "examples": [
            {"input": "list1 = [1,2,4], list2 = [1,3,4]", "output": "[1,1,2,3,4,4]"},
            {"input": "list1 = [], list2 = []", "output": "[]"},
            {"input": "list1 = [], list2 = [0]", "output": "[0]"},
        ],
        "constraints": ["0 <= nodes in each list <= 50", "-100 <= Node.val <= 100", "Both lists are sorted in non-decreasing order"],
        "hints": [
            "At every step the next node of the result is the smaller of the two current heads.",
            "A dummy head node removes the special case of choosing the first node; keep a tail pointer and append to it.",
            "When one list runs out, attach the remainder of the other list in one step rather than node by node.",
        ],
        "function": "mergeTwoLists",
        "signature": "def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:",
        "arg_types": {"list1": "ListNode", "list2": "ListNode"},
        "return_type": "ListNode",
        "compare": "exact",
        "tests": [
            {"input": {"list1": [1, 2, 4], "list2": [1, 3, 4]}, "output": [1, 1, 2, 3, 4, 4]},
            {"input": {"list1": [], "list2": []}, "output": []},
            {"input": {"list1": [], "list2": [0]}, "output": [0]},
            {"input": {"list1": [5], "list2": []}, "output": [5]},
            {"input": {"list1": [-3, -1], "list2": [-2, 0]}, "output": [-3, -2, -1, 0]},
            {"input": {"list1": [1], "list2": [1]}, "output": [1, 1]},
            {"input": {"list1": [1, 2, 3], "list2": [4, 5, 6]}, "output": [1, 2, 3, 4, 5, 6]},
            {"input": {"list1": list(range(0, 6000, 2)), "list2": list(range(1, 6000, 2))}, "output": list(range(6000))},
            {"input": {"list1": list(range(3000)), "list2": list(range(3000, 6000))}, "output": list(range(6000))},
        ],
        "solution": '''\
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy
        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        tail.next = list1 if list1 else list2
        return dummy.next
''',
        "approach": (
            "**Key insight: this is the merge step of merge sort, done on nodes instead of array slots.** The smaller "
            "current head is always the next element of the output, and because we reuse the nodes no extra memory is needed.\n\n"
            "**Algorithm.** Create a dummy node and a `tail` pointer at it. While both lists are non-empty, link `tail.next` "
            "to the smaller head, advance that list, and advance `tail`. When one list is exhausted, link the remainder of the "
            "other. Return `dummy.next`.\n\n"
            "**Why it works.** Invariant: everything hanging off `dummy` is sorted and consists of the smallest elements seen "
            "so far; both remaining lists contain only elements >= the tail. Attaching the smaller head preserves it.\n\n"
            "**Common mistakes.** Forgetting to attach the leftover list. Returning `dummy` instead of `dummy.next`. Creating "
            "new nodes (allowed but wasteful, and the interviewer may ask for in-place). Using `<` instead of `<=`, which is "
            "still correct but not stable (nodes from `list2` jump ahead of equal nodes from `list1`).\n\n"
            "**Interview follow-ups.** (1) Write it recursively and discuss the O(n + m) stack cost. (2) Merge k sorted lists "
            "(heap or divide and conquer). (3) Merge two sorted arrays in place when the first has enough trailing space "
            "(fill from the back). (4) Merge descending lists, or remove duplicates while merging."
        ),
        "complexity": {"time": "O(n + m)", "space": "O(1)"},
        "similar": ["merge-k-sorted-lists", "sort-list", "merge-sorted-array"],
        "followups": ["Recursive version and its stack cost.", "Merge k lists."],
    },
    {
        "id": "reorder-list",
        "title": "Reorder List",
        "difficulty": "Medium",
        "pattern": "Linked List",
        "tags": ["Linked List", "Two Pointers", "Stack", "Recursion"],
        "companies": {"google": 1, "meta": 1, "amazon": 2, "microsoft": 1},
        "description": (
            "You are given the head of a singly linked list `L0 -> L1 -> ... -> Ln-1 -> Ln`. Rearrange it **in place** so "
            "that the nodes alternate between the front and the back:\n\n"
            "`L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ...`\n\n"
            "Only the `next` pointers may change; node values must stay where they are. Do not return anything."
        ),
        "examples": [
            {"input": "head = [1,2,3,4]", "output": "[1,4,2,3]"},
            {"input": "head = [1,2,3,4,5]", "output": "[1,5,2,4,3]"},
        ],
        "constraints": ["1 <= number of nodes <= 5 * 10^4", "1 <= Node.val <= 1000"],
        "hints": [
            "The result interleaves the first half with the reversed second half.",
            "Find the middle with slow and fast pointers, cut the list there, reverse the second half.",
            "Then weave: take one node from the first half, one from the reversed second half, repeat. Be careful to detach the first half's tail so the list ends properly.",
        ],
        "function": "reorderList",
        "signature": "def reorderList(self, head: Optional[ListNode]) -> None:",
        "arg_types": {"head": "ListNode"},
        "return_type": "None",
        "output_mode": "arg:head",
        "compare": "exact",
        "tests": [
            {"input": {"head": [1, 2, 3, 4]}, "output": [1, 4, 2, 3]},
            {"input": {"head": [1, 2, 3, 4, 5]}, "output": [1, 5, 2, 4, 3]},
            {"input": {"head": [1]}, "output": [1]},
            {"input": {"head": [1, 2]}, "output": [1, 2]},
            {"input": {"head": [1, 2, 3]}, "output": [1, 3, 2]},
            {"input": {"head": []}, "output": []},
            {"input": {"head": [7, 7, 7, 7, 7, 7]}, "output": [7, 7, 7, 7, 7, 7]},
            {"input": {"head": list(range(4000))}, "output": [v for pair in zip(range(0, 2000), range(3999, 1999, -1)) for v in pair]},
            {"input": {"head": list(range(4001))}, "output": [v for pair in zip(range(0, 2000), range(4000, 2000, -1)) for v in pair] + [2000]},
        ],
        "solution": '''\
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        if not head or not head.next:
            return
        # 1. find the middle (slow ends at the last node of the first half)
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        second = slow.next
        slow.next = None            # cut the list in two
        # 2. reverse the second half
        prev = None
        while second:
            nxt = second.next
            second.next = prev
            prev = second
            second = nxt
        second = prev
        # 3. weave the two halves together
        first = head
        while second:
            f_next, s_next = first.next, second.next
            first.next = second
            second.next = f_next
            first, second = f_next, s_next
''',
        "approach": (
            "**Key insight: the target order is the first half interleaved with the *reversed* second half.** Each of those "
            "three steps (find middle, reverse, merge) is a standard linked-list routine, so the problem is about composing "
            "them cleanly in O(1) extra space.\n\n"
            "**Algorithm.** (1) Use slow/fast pointers to find the end of the first half; starting `fast` at `head.next` puts "
            "the extra node of an odd-length list in the first half. (2) Cut the list and reverse the second half with the "
            "usual three-pointer loop. (3) Walk both halves, alternately linking a node from the first and from the second. "
            "The second half is never longer than the first, so looping while `second` exists is enough.\n\n"
            "**Why it works.** After the cut, the first half holds `L0..Lmid` and the reversed second half holds "
            "`Ln..Lmid+1`. Zipping them produces exactly `L0, Ln, L1, Ln-1, ...`, and the first half's last node (which "
            "now points at `None` or at the final second-half node) terminates the list.\n\n"
            "**Common mistakes.** Not cutting the first half (`slow.next = None`), which creates a cycle. Choosing the "
            "midpoint so the second half is longer, causing the weave to drop a node. Returning a new head when the problem "
            "expects in-place mutation. Using an array of nodes or a stack: correct and O(n) time, but O(n) space, and the "
            "interviewer will ask for the pointer version.\n\n"
            "**Interview follow-ups.** (1) Do it with O(n) extra space first (array of nodes, two indices), then optimise. "
            "(2) Palindrome Linked List uses the same find-middle + reverse trick. (3) Restore the original order afterwards "
            "(unweave and reverse back). (4) Generalise to `L0 -> Ln -> L1 -> Ln-1` for a doubly linked list."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["palindrome-linked-list", "reverse-linked-list", "middle-of-the-linked-list"],
        "followups": ["O(n) space version with an array.", "Restore the original order."],
    },
    {
        "id": "remove-nth-node-from-end",
        "title": "Remove Nth Node From End of List",
        "difficulty": "Medium",
        "pattern": "Linked List",
        "tags": ["Linked List", "Two Pointers"],
        "companies": {"google": 1, "apple": 2, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "Given the head of a singly linked list and an integer `n`, remove the `n`-th node **counting from the end** "
            "(`n = 1` is the last node) and return the head of the resulting list. `n` is always valid.\n\n"
            "Can you do it in a single pass?"
        ),
        "examples": [
            {"input": "head = [1,2,3,4,5], n = 2", "output": "[1,2,3,5]", "explanation": "The 2nd node from the end is 4."},
            {"input": "head = [1], n = 1", "output": "[]"},
            {"input": "head = [1,2], n = 1", "output": "[1]"},
        ],
        "constraints": ["1 <= number of nodes <= 30", "0 <= Node.val <= 100", "1 <= n <= number of nodes"],
        "hints": [
            "Two passes are easy: count the length, then walk to node length - n. Can you avoid the first pass?",
            "Send a fast pointer n steps ahead, then move fast and slow together. When fast reaches the end, slow is just before the node to delete.",
            "Start both pointers from a dummy node in front of head so that deleting the first node needs no special case.",
        ],
        "function": "removeNthFromEnd",
        "signature": "def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:",
        "arg_types": {"head": "ListNode", "n": "int"},
        "return_type": "ListNode",
        "compare": "exact",
        "tests": [
            {"input": {"head": [1, 2, 3, 4, 5], "n": 2}, "output": [1, 2, 3, 5]},
            {"input": {"head": [1], "n": 1}, "output": []},
            {"input": {"head": [1, 2], "n": 1}, "output": [1]},
            {"input": {"head": [1, 2], "n": 2}, "output": [2]},
            {"input": {"head": [1, 2, 3], "n": 3}, "output": [2, 3]},
            {"input": {"head": [1, 2, 3, 4, 5], "n": 5}, "output": [2, 3, 4, 5]},
            {"input": {"head": list(range(5000)), "n": 1}, "output": list(range(4999))},
            {"input": {"head": list(range(5000)), "n": 5000}, "output": list(range(1, 5000))},
            {"input": {"head": list(range(5000)), "n": 2500}, "output": list(range(2500)) + list(range(2501, 5000))},
        ],
        "solution": '''\
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        fast = slow = dummy
        for _ in range(n):
            fast = fast.next
        while fast.next:            # stop when fast is on the last node
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next  # slow is just before the target
        return dummy.next
''',
        "approach": (
            "**Key insight: two pointers kept exactly `n` nodes apart.** When the leading pointer reaches the last node, the "
            "trailing pointer is on the node *before* the one to remove, which is what you need to unlink it.\n\n"
            "**Algorithm.** Put a dummy node in front of `head`. Advance `fast` by `n` steps. Then advance `fast` and `slow` "
            "together until `fast.next` is `None`. Now `slow.next` is the target; set `slow.next = slow.next.next`. Return "
            "`dummy.next`, which handles the case where the original head was removed.\n\n"
            "**Why it works.** The gap between the pointers is constant, so when `fast` is at position `L` (last node), "
            "`slow` is at position `L - n`, exactly one before the node at `L - n + 1`, which is the `n`-th from the end.\n\n"
            "**Common mistakes.** Starting from `head` instead of a dummy and crashing or mishandling `n == length`. "
            "Advancing `fast` `n + 1` steps and then checking `fast` instead of `fast.next` (or vice versa); pick one "
            "convention and trace it on a 2-node list. Returning `head` when the head itself was removed.\n\n"
            "**Interview follow-ups.** (1) What if `n` can exceed the length? Return the list unchanged or raise, and detect "
            "it while advancing `fast`. (2) Remove the n-th node from the end of a doubly linked list or a circular list. "
            "(3) Return the removed node's value, or remove all nodes with a given value."
        ),
        "complexity": {"time": "O(L)", "space": "O(1)"},
        "similar": ["middle-of-the-linked-list", "swap-nodes-in-pairs", "delete-node-in-a-linked-list"],
        "followups": ["Validate n against the length.", "Doubly linked list variant."],
    },
    {
        "id": "add-two-numbers",
        "title": "Add Two Numbers",
        "difficulty": "Medium",
        "pattern": "Linked List",
        "tags": ["Linked List", "Math", "Recursion"],
        "companies": {"google": 2, "apple": 3, "meta": 3, "amazon": 4, "microsoft": 4},
        "description": (
            "Two non-negative integers are stored as linked lists in **reverse order**: each node holds one digit and the "
            "head is the least significant digit. Neither number has leading zeros except the number 0 itself.\n\n"
            "Add the two numbers and return the sum as a linked list in the same format."
        ),
        "examples": [
            {"input": "l1 = [2,4,3], l2 = [5,6,4]", "output": "[7,0,8]", "explanation": "342 + 465 = 807."},
            {"input": "l1 = [0], l2 = [0]", "output": "[0]"},
            {"input": "l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]", "output": "[8,9,9,9,0,0,0,1]", "explanation": "9999999 + 9999 = 10009998."},
        ],
        "constraints": ["1 <= nodes in each list <= 100", "0 <= Node.val <= 9", "No leading zeros except for 0 itself"],
        "hints": [
            "The lists are already least-significant-digit first, which is exactly the order you add digits by hand.",
            "Walk both lists together, summing the two digits plus a carry. Emit sum % 10 and carry sum // 10.",
            "Treat a missing node as digit 0 so you can run one loop until both lists and the carry are exhausted. Do not forget a final carry node.",
        ],
        "function": "addTwoNumbers",
        "signature": "def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:",
        "arg_types": {"l1": "ListNode", "l2": "ListNode"},
        "return_type": "ListNode",
        "compare": "exact",
        "tests": [
            {"input": {"l1": [2, 4, 3], "l2": [5, 6, 4]}, "output": [7, 0, 8]},
            {"input": {"l1": [0], "l2": [0]}, "output": [0]},
            {"input": {"l1": [9, 9, 9, 9, 9, 9, 9], "l2": [9, 9, 9, 9]}, "output": [8, 9, 9, 9, 0, 0, 0, 1]},
            {"input": {"l1": [5], "l2": [5]}, "output": [0, 1]},
            {"input": {"l1": [1, 8], "l2": [0]}, "output": [1, 8]},
            {"input": {"l1": [9], "l2": [1, 9, 9]}, "output": [0, 0, 0, 1]},
            {"input": {"l1": [9] * 5000, "l2": [1]}, "output": [0] * 5000 + [1]},
            {"input": {"l1": [1, 2, 3] * 1000, "l2": [4, 5, 6] * 1000}, "output": [5, 7, 9] * 1000},
        ],
        "solution": '''\
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy
        carry = 0
        while l1 or l2 or carry:
            total = carry
            if l1:
                total += l1.val
                l1 = l1.next
            if l2:
                total += l2.val
                l2 = l2.next
            carry, digit = divmod(total, 10)
            tail.next = ListNode(digit)
            tail = tail.next
        return dummy.next
''',
        "approach": (
            "**Key insight: the reversed storage order makes this grade-school addition.** Start at the least significant "
            "digit, add, keep the carry, move on. No conversion to integers is needed (and converting would fail for numbers "
            "longer than a machine word).\n\n"
            "**Algorithm.** Keep a dummy head, a tail pointer and `carry = 0`. Loop while either list has nodes *or* the carry "
            "is non-zero. Sum the available digits plus the carry, append `total % 10`, set `carry = total // 10`. Return "
            "`dummy.next`.\n\n"
            "**Why it works.** Each iteration produces exactly one output digit in the correct position and forwards the carry, "
            "which is the definition of positional addition. Including `carry` in the loop condition emits the extra leading "
            "digit when the sum is longer than both inputs.\n\n"
            "**Common mistakes.** Stopping when the lists end and dropping a final carry (`[5] + [5]` must give `[0,1]`). "
            "Writing separate loops for the common prefix and for each leftover list, which triples the chance of a bug. "
            "Converting to Python ints, which works here but misses the point of the question.\n\n"
            "**Interview follow-ups.** (1) Add Two Numbers II: digits stored most-significant first; reverse the lists, or "
            "use two stacks, or recurse after padding to equal length. (2) Multiply two numbers stored as lists. "
            "(3) Subtract (handle sign and borrow), or add numbers in base b."
        ),
        "complexity": {"time": "O(max(n, m))", "space": "O(max(n, m)) for the output"},
        "similar": ["add-two-numbers-ii", "add-binary", "multiply-strings"],
        "followups": ["Most-significant-digit-first variant.", "Multiplication."],
    },
    {
        "id": "find-the-duplicate-number",
        "title": "Find the Duplicate Number",
        "difficulty": "Medium",
        "pattern": "Linked List",
        "tags": ["Array", "Two Pointers", "Binary Search", "Bit Manipulation"],
        "companies": {"google": 2, "apple": 1, "meta": 1, "amazon": 3, "microsoft": 2},
        "description": (
            "You are given an array `nums` of `n + 1` integers, each in the range `[1, n]`. Exactly one value appears more "
            "than once (possibly many times); every other value appears exactly once.\n\n"
            "Return the repeated value **without modifying the array** and using only **O(1) extra space**."
        ),
        "examples": [
            {"input": "nums = [1,3,4,2,2]", "output": "2"},
            {"input": "nums = [3,1,3,4,2]", "output": "3"},
            {"input": "nums = [3,3,3,3,3]", "output": "3"},
        ],
        "constraints": ["1 <= n <= 10^5", "nums.length == n + 1", "1 <= nums[i] <= n", "Exactly one value is repeated"],
        "hints": [
            "Sorting or a hash set breaks the no-modification / O(1) space rules. Think of each index as a node and nums[i] as a pointer to the next node.",
            "Values are in [1, n] and there are n + 1 indices, so starting at index 0 you get a linked list that must contain a cycle. The duplicate value is the node two different indices point to, i.e. the cycle entrance.",
            "Use Floyd's algorithm: slow/fast pointers to meet inside the cycle, then restart one pointer from 0 and move both one step at a time; they meet at the entrance.",
        ],
        "function": "findDuplicate",
        "signature": "def findDuplicate(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [1, 3, 4, 2, 2]}, "output": 2},
            {"input": {"nums": [3, 1, 3, 4, 2]}, "output": 3},
            {"input": {"nums": [3, 3, 3, 3, 3]}, "output": 3},
            {"input": {"nums": [1, 1]}, "output": 1},
            {"input": {"nums": [2, 2, 2, 2]}, "output": 2},
            {"input": {"nums": [1, 4, 4, 2, 3]}, "output": 4},
            {"input": {"nums": [2, 5, 9, 6, 9, 3, 8, 9, 7, 1]}, "output": 9},
            {"input": {"nums": list(range(1, 5001)) + [2500]}, "output": 2500},
            {"input": {"nums": list(range(5000, 0, -1)) + [777]}, "output": 777},
            {"input": {"nums": [1] + list(range(1, 6000))}, "output": 1},
        ],
        "solution": '''\
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        # Phase 1: find a meeting point inside the cycle.
        slow = fast = nums[0]
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        # Phase 2: find the cycle entrance, which is the duplicate value.
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        return slow
''',
        "approach": (
            "**Key insight: interpret the array as a linked list where index `i` points to index `nums[i]`.** Since values are "
            "in `[1, n]`, index 0 is never pointed to, so the walk from 0 never returns to its start, yet with only `n + 1` "
            "nodes it must eventually repeat: there is a cycle. The duplicate value is the only index with two incoming "
            "edges, which makes it the **entrance of the cycle**. So the problem *is* Linked List Cycle II in disguise.\n\n"
            "**Algorithm (Floyd).** Phase 1: `slow` moves one step (`nums[slow]`), `fast` two steps, until they meet. "
            "Phase 2: reset `slow` to the start (`nums[0]`), keep `fast` where it met, move both one step at a time; the index "
            "where they meet is the cycle entrance, i.e. the duplicate.\n\n"
            "**Why it works.** Let the tail before the cycle have length `F` and the cycle length `C`. When the pointers first "
            "meet, `slow` has taken `F + a` steps and `fast` `2(F + a)`, so `F + a` is a multiple of `C`. Walking `F` more steps "
            "from the meeting point lands exactly at the entrance, and so does walking `F` steps from the start.\n\n"
            "**Common mistakes.** Starting `slow` and `fast` at index 0 instead of at `nums[0]` and then using a `while slow != "
            "fast` loop that exits immediately; the do-while structure matters. Treating `nums[i]` as a value to compare rather "
            "than as a pointer. Mutating the array (negation marking) when the problem forbids it.\n\n"
            "**Interview follow-ups.** (1) Binary search on the value range: count how many numbers are <= mid; O(n log n) "
            "time, also O(1) space and read-only. (2) Bitwise counting per bit position. (3) Relax the constraints: if you "
            "may modify the array, mark visited indices by negating; if you may use O(n) space, use a set. "
            "(4) Why can a value be repeated many times and the algorithm still work?"
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["linked-list-cycle-ii", "missing-number", "first-missing-positive"],
        "followups": ["Binary search on the value range.", "Marking approach when mutation is allowed."],
    },
    {
        "id": "merge-k-sorted-lists",
        "title": "Merge k Sorted Lists",
        "difficulty": "Hard",
        "pattern": "Linked List",
        "tags": ["Linked List", "Heap / Priority Queue", "Divide and Conquer", "Merge Sort"],
        "companies": {"google": 3, "apple": 2, "meta": 4, "amazon": 4, "microsoft": 3},
        "description": (
            "You are given `lists`, an array of `k` singly linked lists, each sorted in ascending order. Merge them all into "
            "one sorted linked list and return its head.\n\n"
            "Some of the lists, or the whole array, may be empty."
        ),
        "examples": [
            {"input": "lists = [[1,4,5],[1,3,4],[2,6]]", "output": "[1,1,2,3,4,4,5,6]"},
            {"input": "lists = []", "output": "[]"},
            {"input": "lists = [[]]", "output": "[]"},
        ],
        "constraints": ["0 <= k <= 10^4", "0 <= length of each list <= 500", "-10^4 <= Node.val <= 10^4", "Total nodes <= 10^4"],
        "hints": [
            "Merging the lists one after another is O(k * N). Can you pick the global minimum faster than scanning k heads?",
            "A min-heap holding the current head of each list gives the smallest in O(log k). Pop it, append to the result, push its successor.",
            "Python heaps need a tie-breaker because ListNode is not comparable: push (val, list_index, node). Divide and conquer (pairwise merging) is the other O(N log k) solution.",
        ],
        "function": "mergeKLists",
        "signature": "def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:",
        "arg_types": {"lists": "List[ListNode]"},
        "return_type": "ListNode",
        "compare": "exact",
        "tests": [
            {"input": {"lists": [[1, 4, 5], [1, 3, 4], [2, 6]]}, "output": [1, 1, 2, 3, 4, 4, 5, 6]},
            {"input": {"lists": []}, "output": []},
            {"input": {"lists": [[]]}, "output": []},
            {"input": {"lists": [[], [1]]}, "output": [1]},
            {"input": {"lists": [[-2, 0], [-3], [-1, 1]]}, "output": [-3, -2, -1, 0, 1]},
            {"input": {"lists": [[2, 2], [2], [2, 2, 2]]}, "output": [2, 2, 2, 2, 2, 2]},
            {"input": {"lists": [[5]]}, "output": [5]},
            {"input": {"lists": [list(range(i, 10000, 100)) for i in range(100)]}, "output": list(range(10000))},
            {"input": {"lists": [[i] for i in range(3000, 0, -1)]}, "output": list(range(1, 3001))},
        ],
        "solution": '''\
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        heap = []
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(heap, (node.val, i, node))   # i breaks ties; nodes are not comparable
        dummy = ListNode()
        tail = dummy
        while heap:
            val, i, node = heapq.heappop(heap)
            tail.next = node
            tail = node
            if node.next:
                heapq.heappush(heap, (node.next.val, i, node.next))
        return dummy.next
''',
        "approach": (
            "**Key insight: at any moment the next output node is the smallest among the k current heads, and a min-heap "
            "answers that query in O(log k) instead of O(k).** Every node enters and leaves the heap exactly once.\n\n"
            "**Algorithm.** Push the head of each non-empty list as `(val, list_index, node)`. Repeatedly pop the minimum, "
            "append its node to the result tail, and push that node's successor if it exists. The `list_index` is only there "
            "so that ties on `val` never force Python to compare two `ListNode` objects.\n\n"
            "**Why it works.** The heap always contains exactly the frontier of unconsumed nodes, one per non-exhausted list. "
            "Since each list is sorted, the minimum of the frontier is the global minimum of all remaining nodes.\n\n"
            "**Common mistakes.** Pushing bare nodes and getting a `TypeError` on equal values. Forgetting that `lists` may "
            "contain `None` entries or be empty. Merging lists one by one into an accumulator: O(k * N) and the interviewer "
            "will call it out. Concatenating everything and sorting: O(N log N), simple, but ignores the sorted input.\n\n"
            "**Interview follow-ups.** (1) Divide and conquer: merge pairs of lists in rounds, `log k` rounds of O(N) each, "
            "O(1) extra space beyond recursion. Compare it with the heap. (2) The lists are huge files on disk: this is "
            "external merge sort, and the heap is exactly the k-way merge step. (3) Return the k smallest elements only, or "
            "merge k sorted arrays / iterators instead of linked lists."
        ),
        "complexity": {"time": "O(N log k)", "space": "O(k)"},
        "similar": ["merge-two-sorted-lists", "sort-list", "kth-smallest-element-in-a-sorted-matrix"],
        "followups": ["Divide-and-conquer pairwise merge.", "External k-way merge."],
    },
    {
        "id": "reverse-nodes-in-k-group",
        "title": "Reverse Nodes in k-Group",
        "difficulty": "Hard",
        "pattern": "Linked List",
        "tags": ["Linked List", "Recursion"],
        "companies": {"google": 1, "apple": 1, "meta": 2, "amazon": 3, "microsoft": 3},
        "description": (
            "Given the head of a linked list and a positive integer `k`, reverse the nodes **k at a time** and return the new "
            "head. Groups are taken from the front; if fewer than `k` nodes remain at the end, leave them in their original order.\n\n"
            "Only `next` pointers may be changed; do not swap values between nodes."
        ),
        "examples": [
            {"input": "head = [1,2,3,4,5], k = 2", "output": "[2,1,4,3,5]"},
            {"input": "head = [1,2,3,4,5], k = 3", "output": "[3,2,1,4,5]", "explanation": "Only one full group of 3 exists; 4 and 5 are left alone."},
        ],
        "constraints": ["1 <= number of nodes <= 5000", "0 <= Node.val <= 1000", "1 <= k <= number of nodes"],
        "hints": [
            "First make sure k nodes are actually available from the current position; if not, you are done.",
            "Reverse exactly k nodes with the usual prev/cur loop, then reconnect: the node before the group must point to the group's new head, and the group's new tail must point to the next group.",
            "A dummy node before head makes the first group look like every other. Keep a `group_prev` pointer and advance it to the group's new tail after each reversal.",
        ],
        "function": "reverseKGroup",
        "signature": "def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:",
        "arg_types": {"head": "ListNode", "k": "int"},
        "return_type": "ListNode",
        "compare": "exact",
        "tests": [
            {"input": {"head": [1, 2, 3, 4, 5], "k": 2}, "output": [2, 1, 4, 3, 5]},
            {"input": {"head": [1, 2, 3, 4, 5], "k": 3}, "output": [3, 2, 1, 4, 5]},
            {"input": {"head": [1, 2, 3, 4, 5], "k": 1}, "output": [1, 2, 3, 4, 5]},
            {"input": {"head": [1], "k": 1}, "output": [1]},
            {"input": {"head": [1, 2, 3, 4, 5, 6], "k": 3}, "output": [3, 2, 1, 6, 5, 4]},
            {"input": {"head": [1, 2], "k": 3}, "output": [1, 2]},
            {"input": {"head": [], "k": 2}, "output": []},
            {"input": {"head": [1, 2, 3, 4, 5], "k": 5}, "output": [5, 4, 3, 2, 1]},
            {"input": {"head": list(range(6000)), "k": 3}, "output": [v for g in range(0, 6000, 3) for v in (g + 2, g + 1, g)]},
            {"input": {"head": list(range(5000)), "k": 5000}, "output": list(range(4999, -1, -1))},
            {"input": {"head": list(range(5001)), "k": 2}, "output": [v for g in range(0, 5000, 2) for v in (g + 1, g)] + [5000]},
        ],
        "solution": '''\
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        group_prev = dummy
        while True:
            # find the k-th node of the current group; stop if there are fewer than k
            kth = group_prev
            for _ in range(k):
                kth = kth.next
                if kth is None:
                    return dummy.next
            group_next = kth.next
            # reverse the k nodes
            prev, cur = group_next, group_prev.next
            while cur is not group_next:
                nxt = cur.next
                cur.next = prev
                prev = cur
                cur = nxt
            # reconnect: old first node is now the group's tail
            new_tail = group_prev.next
            group_prev.next = kth
            group_prev = new_tail
''',
        "approach": (
            "**Key insight: the problem is `reverse-linked-list` applied repeatedly to windows of exactly `k` nodes, with "
            "careful reconnection between windows.** The hard part is bookkeeping, not the reversal itself.\n\n"
            "**Algorithm.** Use a dummy node and a `group_prev` pointer to the node before the current group. For each group: "
            "walk `k` steps to find the k-th node; if you run out of nodes, return. Remember `group_next = kth.next`. Reverse the "
            "nodes from `group_prev.next` up to `kth`, seeding `prev` with `group_next` so the reversed group's tail already "
            "points at the rest of the list. Finally set `group_prev.next = kth` (new head of the group) and move `group_prev` "
            "to the old first node, now the group's tail.\n\n"
            "**Why it works.** Seeding `prev = group_next` means no dangling pointer is ever created: after the loop the group "
            "is reversed in place and already attached to its right neighbour; the single assignment `group_prev.next = kth` "
            "attaches it on the left. The leftover partial group is never touched because the `k`-step scan fails first.\n\n"
            "**Common mistakes.** Reversing a partial final group. Losing `group_next` before reversing. Forgetting to advance "
            "`group_prev` to the new tail, which reverses the same nodes forever. Swapping values instead of nodes (fails the "
            "spirit of the question and is often explicitly forbidden). An O(n) recursion depth of `n / k` is acceptable but "
            "mention the iterative version.\n\n"
            "**Interview follow-ups.** (1) Reverse Linked List II (reverse a single range `[left, right]`), the same reconnection "
            "logic once. (2) Swap Nodes in Pairs is `k = 2`. (3) Reverse the *last* partial group too, or reverse alternate "
            "groups. (4) Recursive solution and its stack usage."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["reverse-linked-list", "swap-nodes-in-pairs", "reverse-linked-list-ii"],
        "followups": ["Reverse a single sub-range.", "Alternate-group reversal."],
    },
    {
        "id": "palindrome-linked-list",
        "title": "Palindrome Linked List",
        "difficulty": "Easy",
        "pattern": "Linked List",
        "tags": ["Linked List", "Two Pointers", "Stack", "Recursion"],
        "companies": {"google": 2, "apple": 3, "meta": 3, "amazon": 4, "microsoft": 3},
        "description": (
            "Given the head of a singly linked list, return `true` if the sequence of values reads the same forwards and "
            "backwards, and `false` otherwise.\n\n"
            "Can you do it in **O(n) time and O(1) extra space**?"
        ),
        "examples": [
            {"input": "head = [1,2,2,1]", "output": "true"},
            {"input": "head = [1,2]", "output": "false"},
        ],
        "constraints": ["1 <= number of nodes <= 10^5", "0 <= Node.val <= 9"],
        "hints": [
            "Copying the values into an array and comparing from both ends is O(n) space. You cannot walk a singly linked list backwards, but you can change which way it points.",
            "Find the middle with slow/fast pointers, reverse the second half in place, then compare the first half against the reversed second half node by node.",
            "For an odd length the middle node belongs to neither half; comparing only while the second-half pointer exists handles it. Optionally restore the list afterwards.",
        ],
        "function": "isPalindrome",
        "signature": "def isPalindrome(self, head: Optional[ListNode]) -> bool:",
        "arg_types": {"head": "ListNode"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"head": [1, 2, 2, 1]}, "output": True},
            {"input": {"head": [1, 2]}, "output": False},
            {"input": {"head": [1]}, "output": True},
            {"input": {"head": [1, 2, 3, 2, 1]}, "output": True},
            {"input": {"head": [1, 2, 3, 3, 1]}, "output": False},
            {"input": {"head": [1, 1]}, "output": True},
            {"input": {"head": [1, 2, 1, 1]}, "output": False},
            {"input": {"head": list(range(3000)) + list(range(2999, -1, -1))}, "output": True},
            {"input": {"head": list(range(3000)) + [42] + list(range(2999, -1, -1))}, "output": True},
            {"input": {"head": list(range(6000))}, "output": False},
            {"input": {"head": list(range(3000)) + list(range(2999, 0, -1)) + [1]}, "output": False},
        ],
        "solution": '''\
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        # 1. find the middle: slow ends at the start of the second half
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        # 2. reverse the second half
        prev = None
        while slow:
            nxt = slow.next
            slow.next = prev
            prev = slow
            slow = nxt
        # 3. compare the halves (the middle node of an odd list is harmlessly compared with itself)
        left, right = head, prev
        while right:
            if left.val != right.val:
                return False
            left = left.next
            right = right.next
        return True
''',
        "approach": (
            "**Key insight: a singly linked list cannot be read backwards, but half of it can be *made* to point backwards.** "
            "Reverse the second half in place and then compare it with the first half walking forwards.\n\n"
            "**Algorithm.** (1) Slow/fast pointers: when `fast` falls off the end, `slow` is at the start of the second half "
            "(for odd lengths, at the middle node). (2) Reverse the list from `slow` onwards. (3) Walk from `head` and from the "
            "reversed half's head together, comparing values, until the reversed half is exhausted. Optionally reverse again to "
            "restore the input.\n\n"
            "**Why it works.** The reversed second half yields the values from the end toward the middle, exactly the mirror "
            "of the first half. For odd lengths the middle node ends up as the last node of the reversed half and is compared "
            "with itself, which is always equal, so no special case is needed.\n\n"
            "**Common mistakes.** Comparing while `left` exists instead of `right`, which overruns for odd lengths. Off-by-one "
            "in the midpoint search when `fast` starts at `head.next` versus `head`. Reaching for an array or a stack and "
            "calling it O(1) space. Forgetting that mutating the input may be unacceptable in production code; mention "
            "restoring the list.\n\n"
            "**Interview follow-ups.** (1) Restore the list after the check. (2) Recursive solution with an outer pointer "
            "(O(n) stack). (3) Longest palindromic sublist, or check a doubly linked list where two-pointer comparison is trivial."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["reverse-linked-list", "reorder-list", "middle-of-the-linked-list"],
        "followups": ["Restore the original list.", "Recursive approach."],
    },
    {
        "id": "middle-of-the-linked-list",
        "title": "Middle of the Linked List",
        "difficulty": "Easy",
        "pattern": "Linked List",
        "tags": ["Linked List", "Two Pointers"],
        "companies": {"google": 1, "apple": 2, "amazon": 2, "microsoft": 2},
        "description": (
            "Given the head of a singly linked list, return the **middle node**. If the list has an even number of nodes "
            "there are two middle nodes; return the **second** one.\n\n"
            "The returned node still points at the rest of the list, so the answer is shown as the sublist from the middle to the end."
        ),
        "examples": [
            {"input": "head = [1,2,3,4,5]", "output": "[3,4,5]", "explanation": "Node 3 is the middle."},
            {"input": "head = [1,2,3,4,5,6]", "output": "[4,5,6]", "explanation": "Two middles, 3 and 4; the second one is returned."},
        ],
        "constraints": ["1 <= number of nodes <= 100", "1 <= Node.val <= 100"],
        "hints": [
            "Counting the length and walking length // 2 steps works in two passes. Can you do one pass?",
            "Move a slow pointer one step and a fast pointer two steps. When fast runs off the end, slow is in the middle.",
            "Loop while fast and fast.next are both non-null; this naturally picks the second middle for even lengths.",
        ],
        "function": "middleNode",
        "signature": "def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:",
        "arg_types": {"head": "ListNode"},
        "return_type": "ListNode",
        "compare": "exact",
        "tests": [
            {"input": {"head": [1, 2, 3, 4, 5]}, "output": [3, 4, 5]},
            {"input": {"head": [1, 2, 3, 4, 5, 6]}, "output": [4, 5, 6]},
            {"input": {"head": [1]}, "output": [1]},
            {"input": {"head": [1, 2]}, "output": [2]},
            {"input": {"head": [1, 2, 3]}, "output": [2, 3]},
            {"input": {"head": [9, 9, 9, 9]}, "output": [9, 9]},
            {"input": {"head": list(range(5000))}, "output": list(range(2500, 5000))},
            {"input": {"head": list(range(5001))}, "output": list(range(2500, 5001))},
        ],
        "solution": '''\
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow
''',
        "approach": (
            "**Key insight: a pointer moving twice as fast covers the list in the time the slow pointer covers half of it.** "
            "This is the tortoise-and-hare technique that also powers cycle detection and palindrome checks.\n\n"
            "**Algorithm.** Start `slow` and `fast` at `head`. While `fast` and `fast.next` exist, advance `slow` by one and "
            "`fast` by two. Return `slow`.\n\n"
            "**Why it works.** After `t` iterations `slow` is at index `t` and `fast` at `2t`. The loop stops when `2t` is the "
            "last index (odd length, `slow` at the exact middle) or `2t` is one past the last index (even length, `slow` at "
            "index `n / 2`, the second middle).\n\n"
            "**Common mistakes.** Checking only `fast.next` (crashes when `fast` is `None`). Wanting the *first* middle for even "
            "lengths: start `fast` at `head.next` instead, or stop one step earlier; know both variants. Overcomplicating with a "
            "length count when one pass is expected.\n\n"
            "**Interview follow-ups.** (1) Return the first middle instead. (2) Use this as a building block: Palindrome Linked "
            "List, Reorder List, and splitting a list for merge sort. (3) Find the node one third of the way along "
            "(pointers moving at ratio 1:3)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["remove-nth-node-from-end", "palindrome-linked-list", "linked-list-cycle"],
        "followups": ["First middle for even lengths.", "Generalise the speed ratio."],
    },
    {
        "id": "swap-nodes-in-pairs",
        "title": "Swap Nodes in Pairs",
        "difficulty": "Medium",
        "pattern": "Linked List",
        "tags": ["Linked List", "Recursion"],
        "companies": {"google": 1, "apple": 2, "meta": 2, "amazon": 2, "microsoft": 3},
        "description": (
            "Given the head of a linked list, swap every two adjacent nodes and return the new head. If the list has an odd "
            "number of nodes, the last node stays in place.\n\n"
            "You must rewire the nodes themselves; changing the values stored in the nodes is not allowed."
        ),
        "examples": [
            {"input": "head = [1,2,3,4]", "output": "[2,1,4,3]"},
            {"input": "head = []", "output": "[]"},
            {"input": "head = [1]", "output": "[1]"},
        ],
        "constraints": ["0 <= number of nodes <= 100", "0 <= Node.val <= 100"],
        "hints": [
            "To swap nodes a and b you also need the node before a, so that it can be pointed at b.",
            "Use a dummy node before head and a prev pointer. While prev.next and prev.next.next exist, swap that pair and move prev two nodes forward.",
            "Write the three pointer assignments carefully: prev.next = b, a.next = b.next, b.next = a. A recursive version is also short and worth knowing.",
        ],
        "function": "swapPairs",
        "signature": "def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:",
        "arg_types": {"head": "ListNode"},
        "return_type": "ListNode",
        "compare": "exact",
        "tests": [
            {"input": {"head": [1, 2, 3, 4]}, "output": [2, 1, 4, 3]},
            {"input": {"head": []}, "output": []},
            {"input": {"head": [1]}, "output": [1]},
            {"input": {"head": [1, 2, 3]}, "output": [2, 1, 3]},
            {"input": {"head": [1, 2]}, "output": [2, 1]},
            {"input": {"head": [5, 5, 5, 5, 5]}, "output": [5, 5, 5, 5, 5]},
            {"input": {"head": list(range(6000))}, "output": [v for i in range(0, 6000, 2) for v in (i + 1, i)]},
            {"input": {"head": list(range(6001))}, "output": [v for i in range(0, 6000, 2) for v in (i + 1, i)] + [6000]},
        ],
        "solution": '''\
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next and prev.next.next:
            a, b = prev.next, prev.next.next
            prev.next = b
            a.next = b.next
            b.next = a
            prev = a                # a is now the second node of the swapped pair
        return dummy.next
''',
        "approach": (
            "**Key insight: swapping two adjacent nodes is three pointer assignments, provided you hold a reference to the node "
            "*before* the pair.** A dummy node gives you that reference even for the very first pair.\n\n"
            "**Algorithm.** `prev` starts at the dummy. While a full pair `a = prev.next`, `b = a.next` exists: point `prev` at "
            "`b`, point `a` at whatever followed `b`, point `b` at `a`. Then advance `prev` to `a`, which is now the second node "
            "of the swapped pair. Return `dummy.next`.\n\n"
            "**Why it works.** Each iteration leaves everything before `prev` correctly swapped and `prev.next` pointing at the "
            "first unswapped node. The loop condition guarantees a pair exists, so an odd trailing node is left untouched.\n\n"
            "**Common mistakes.** Doing the assignments in an order that loses `b.next` before saving it. Advancing `prev` to `b` "
            "instead of `a`. Handling the first pair separately instead of using a dummy. Swapping values, which the problem "
            "explicitly forbids.\n\n"
            "**Interview follow-ups.** (1) Recursive version: `second = head.next; head.next = swapPairs(second.next); "
            "second.next = head`, and its O(n) stack. (2) Generalise to Reverse Nodes in k-Group. (3) Swap the k-th node from "
            "the start with the k-th from the end."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["reverse-nodes-in-k-group", "reverse-linked-list", "swapping-nodes-in-a-linked-list"],
        "followups": ["Recursive version.", "Generalise to k-groups."],
    },
    {
        "id": "sort-list",
        "title": "Sort List",
        "difficulty": "Medium",
        "pattern": "Linked List",
        "tags": ["Linked List", "Two Pointers", "Divide and Conquer", "Merge Sort"],
        "companies": {"google": 2, "apple": 2, "meta": 2, "amazon": 2, "microsoft": 3},
        "description": (
            "Given the head of a singly linked list, sort it in ascending order and return the head of the sorted list.\n\n"
            "Aim for **O(n log n)** time. Rearrange the nodes themselves rather than copying values into an array."
        ),
        "examples": [
            {"input": "head = [4,2,1,3]", "output": "[1,2,3,4]"},
            {"input": "head = [-1,5,3,4,0]", "output": "[-1,0,3,4,5]"},
            {"input": "head = []", "output": "[]"},
        ],
        "constraints": ["0 <= number of nodes <= 5 * 10^4", "-10^5 <= Node.val <= 10^5"],
        "hints": [
            "Quick sort and heap sort rely on random access. Which O(n log n) sort only ever needs sequential access and merging?",
            "Merge sort: split the list in half (slow/fast pointers), sort each half recursively, merge the two sorted halves.",
            "Cut the list at the midpoint by setting the previous node's next to None, otherwise the recursion never terminates. Reuse your Merge Two Sorted Lists routine.",
        ],
        "function": "sortList",
        "signature": "def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:",
        "arg_types": {"head": "ListNode"},
        "return_type": "ListNode",
        "compare": "exact",
        "tests": [
            {"input": {"head": [4, 2, 1, 3]}, "output": [1, 2, 3, 4]},
            {"input": {"head": [-1, 5, 3, 4, 0]}, "output": [-1, 0, 3, 4, 5]},
            {"input": {"head": []}, "output": []},
            {"input": {"head": [1]}, "output": [1]},
            {"input": {"head": [2, 2, 1, 1]}, "output": [1, 1, 2, 2]},
            {"input": {"head": [3, 3, 3]}, "output": [3, 3, 3]},
            {"input": {"head": [1, 2, 3, 4, 5]}, "output": [1, 2, 3, 4, 5]},
            {"input": {"head": list(range(6000, 0, -1))}, "output": list(range(1, 6001))},
            {"input": {"head": [(i * 7919) % 6007 for i in range(6007)]}, "output": sorted((i * 7919) % 6007 for i in range(6007))},
            {"input": {"head": [(i * 31) % 97 - 48 for i in range(5000)]}, "output": sorted((i * 31) % 97 - 48 for i in range(5000))},
        ],
        "solution": '''\
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        # split: slow stops at the last node of the first half
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        second = slow.next
        slow.next = None
        left = self.sortList(head)
        right = self.sortList(second)
        return self._merge(left, right)

    def _merge(self, a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy
        while a and b:
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a or b
        return dummy.next
''',
        "approach": (
            "**Key insight: merge sort is the natural O(n log n) sort for linked lists.** Splitting a list in half and merging "
            "two sorted lists both need only sequential access and pointer rewiring, with no random access and no extra arrays.\n\n"
            "**Algorithm.** Base case: zero or one node is already sorted. Otherwise find the middle with slow/fast pointers "
            "(start `fast` at `head.next` so a two-node list splits 1/1), cut the list by setting `slow.next = None`, sort both "
            "halves recursively, and merge them with the standard dummy-head merge.\n\n"
            "**Why it works.** The recursion depth is O(log n) because each level halves the list, and each level does O(n) "
            "work in splitting and merging. Correctness is the usual merge-sort argument: merging two sorted lists produces a "
            "sorted list containing all nodes.\n\n"
            "**Common mistakes.** Forgetting to cut the list (infinite recursion). Starting `fast` at `head` so a two-node "
            "list splits 0/2 and never shrinks. Copying values into a Python list and calling `sort()`: correct and O(n log n), "
            "but O(n) extra space and not what the question tests. Quadratic insertion sort on the list.\n\n"
            "**Interview follow-ups.** (1) Achieve O(1) extra space (beyond the output) with **bottom-up** merge sort: merge runs "
            "of length 1, 2, 4, ... iteratively, avoiding recursion. (2) Why is quick sort a poor fit for linked lists? "
            "(3) Insertion Sort List and when it is acceptable (nearly sorted input). (4) Stability: why `<=` in the merge matters."
        ),
        "complexity": {"time": "O(n log n)", "space": "O(log n) recursion stack"},
        "similar": ["merge-two-sorted-lists", "merge-k-sorted-lists", "insertion-sort-list"],
        "followups": ["Bottom-up merge sort with O(1) space.", "Stability of the merge."],
    },
]
