
import sys, json, time, math, heapq, bisect, itertools, functools, collections, random, string, re
from collections import defaultdict, deque, Counter, OrderedDict
from functools import lru_cache, cache, reduce
from heapq import heappush, heappop, heapify, heappushpop, nlargest, nsmallest
from itertools import permutations, combinations, product, accumulate, groupby
from bisect import bisect_left, bisect_right, insort
from typing import List, Optional, Dict, Set, Tuple, Deque, Any, Iterator
sys.setrecursionlimit(100000)

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def __repr__(self):
        return f"ListNode({self.val})"

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    def __repr__(self):
        return f"TreeNode({self.val})"

class Node:
    """Generic graph / n-ary node (val, neighbors, children)."""
    def __init__(self, val=0, neighbors=None, children=None, next=None, random=None, left=None, right=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
        self.children = children if children is not None else []
        self.next = next
        self.random = random
        self.left = left
        self.right = right

def _to_list_node(arr):
    dummy = ListNode()
    cur = dummy
    for v in arr or []:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

def _from_list_node(node, limit=100000):
    out = []
    while node is not None and len(out) < limit:
        out.append(node.val)
        node = node.next
    return out

def _to_tree_node(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr):
            if arr[i] is not None:
                node.left = TreeNode(arr[i]); q.append(node.left)
            i += 1
        if i < len(arr):
            if arr[i] is not None:
                node.right = TreeNode(arr[i]); q.append(node.right)
            i += 1
    return root

def _from_tree_node(root):
    if root is None:
        return []
    out = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left); q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out

def _to_graph_node(adj):
    """adj: adjacency list, 1-indexed like [[2,4],[1,3],[2,4],[1,3]]."""
    if not adj:
        return None
    nodes = [Node(i + 1) for i in range(len(adj))]
    for i, nb in enumerate(adj):
        nodes[i].neighbors = [nodes[j - 1] for j in nb]
    return nodes[0]

def _from_graph_node(node):
    if node is None:
        return []
    seen = {}
    order = []
    stack = [node]
    while stack:
        n = stack.pop()
        if n.val in seen:
            continue
        seen[n.val] = n
        order.append(n)
        for nb in n.neighbors:
            if nb.val not in seen:
                stack.append(nb)
    size = max(seen) if seen else 0
    out = [[] for _ in range(size)]
    for v, n in seen.items():
        out[v - 1] = [nb.val for nb in n.neighbors]
    return out

def _to_nary(arr):
    """Level order with None separators: [1,null,3,2,4,null,5,6]."""
    if not arr:
        return None
    root = Node(arr[0])
    q = deque([root])
    i = 2
    while q and i < len(arr):
        parent = q.popleft()
        while i < len(arr) and arr[i] is not None:
            child = Node(arr[i]); parent.children.append(child); q.append(child); i += 1
        i += 1
    return root

def _from_nary(root):
    if root is None:
        return []
    out = [root.val, None]
    q = deque([root])
    while q:
        level_nodes = []
        for _ in range(len(q)):
            n = q.popleft()
            for c in n.children:
                out.append(c.val); level_nodes.append(c)
            out.append(None)
            q.extend(n.children)
        # the simple encoding above adds a None after each node's children
    while out and out[-1] is None:
        out.pop()
    return out

def _convert_in(value, typ):
    t = (typ or "").replace("Optional[", "").replace("]", "").strip()
    if t == "ListNode":
        return _to_list_node(value)
    if t == "TreeNode":
        return _to_tree_node(value)
    if t == "GraphNode":
        return _to_graph_node(value)
    if t == "NaryNode":
        return _to_nary(value)
    if t == "List[ListNode":
        return [_to_list_node(v) for v in value]
    if t == "List[TreeNode":
        return [_to_tree_node(v) for v in value]
    return value

def _convert_out(value, typ):
    t = (typ or "").replace("Optional[", "").replace("]", "").strip()
    if t == "ListNode":
        return _from_list_node(value)
    if t == "TreeNode":
        return _from_tree_node(value)
    if t == "GraphNode":
        return _from_graph_node(value)
    if t == "NaryNode":
        return _from_nary(value)
    if t == "List[ListNode":
        return [_from_list_node(v) for v in value]
    if t == "List[TreeNode":
        return [_from_tree_node(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted(value)
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return str(value)
    return value

def _run_function(spec, tests):
    results = []
    fn_name = spec["function"]
    arg_types = spec.get("arg_types", {})
    ret_type = spec.get("return_type", "")
    output_mode = spec.get("output_mode", "return")
    for t in tests:
        res = {"ok": False}
        try:
            sol = Solution()
            fn = getattr(sol, fn_name)
            kwargs = {}
            for k, v in t["input"].items():
                kwargs[k] = _convert_in(json.loads(json.dumps(v)), arg_types.get(k))
            t0 = time.perf_counter()
            out = fn(**kwargs)
            dt = (time.perf_counter() - t0) * 1000
            if output_mode.startswith("arg:"):
                name = output_mode[4:]
                out = _convert_out(kwargs[name], arg_types.get(name))
            elif output_mode.startswith("prefix:"):
                name = output_mode[7:]
                k = out
                out = [k, list(kwargs[name])[:k]]
            else:
                out = _convert_out(out, ret_type)
            res = {"ok": True, "output": out, "ms": round(dt, 3)}
        except Exception as e:  # noqa: BLE001
            import traceback
            res = {"ok": False, "error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-2000:]}
        results.append(res)
    return results

def _run_design(spec, tests):
    """tests: input = {"ops": [["ClassName", [args]], ["method", [args]], ...]}"""
    results = []
    cls_name = spec["class_name"]
    for t in tests:
        res = {"ok": False}
        try:
            ops = t["input"]["ops"]
            outs = []
            obj = None
            t0 = time.perf_counter()
            for name, args in ops:
                if name == cls_name:
                    obj = globals()[cls_name](*args)
                    outs.append(None)
                else:
                    r = getattr(obj, name)(*args)
                    outs.append(_convert_out(r, ""))
            dt = (time.perf_counter() - t0) * 1000
            res = {"ok": True, "output": outs, "ms": round(dt, 3)}
        except Exception as e:  # noqa: BLE001
            import traceback
            res = {"ok": False, "error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-2000:]}
        results.append(res)
    return results

def _main():
    payload = json.loads(sys.stdin.read())
    spec, tests = payload["spec"], payload["tests"]
    if spec.get("kind") == "design":
        out = _run_design(spec, tests)
    else:
        out = _run_function(spec, tests)
    sys.stdout.write("\n__JUDGE_RESULT__\n" + json.dumps(out))


def _run_payload(payload_json):
    payload = json.loads(payload_json)
    spec, tests = payload["spec"], payload["tests"]
    out = _run_design(spec, tests) if spec.get("kind") == "design" else _run_function(spec, tests)
    return json.dumps(out)
