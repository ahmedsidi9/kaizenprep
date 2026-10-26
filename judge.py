"""Local judge: runs a Python solution against a problem's tests in a subprocess.

The user's code is written to a temp file and executed with `python3 -I` with a
wall-clock timeout. Tests are passed over stdin as JSON so the solution never
touches the filesystem. The harness prelude provides ListNode / TreeNode and the
usual typing / collections imports, converts JSON inputs into those structures,
and converts results back to JSON for comparison.
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import tempfile
import time

TIMEOUT_SECONDS = 10

PRELUDE = r'''
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
'''

HARNESS_TAIL = "\n\nif __name__ == '__main__':\n    _main()\n"


def _normalize(value, mode):
    if mode == "unordered":
        return sorted(json.dumps(v, sort_keys=True) for v in (value or []))
    if mode == "unordered_nested":
        return sorted(json.dumps(sorted(v) if isinstance(v, list) else v, sort_keys=True) for v in (value or []))
    return value


def compare(expected, actual, mode="exact", tolerance=1e-5):
    """Return True when actual matches expected under the comparison mode."""
    if mode == "any_of":
        return any(compare(e, actual, "exact", tolerance) for e in expected)
    if mode == "float":
        def close(a, b):
            if isinstance(a, list) or isinstance(b, list):
                return isinstance(a, list) and isinstance(b, list) and len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
            if isinstance(a, dict) or isinstance(b, dict):
                return isinstance(a, dict) and isinstance(b, dict) and a.keys() == b.keys() and all(close(a[k], b[k]) for k in a)
            if isinstance(a, (bool, str)) or isinstance(b, (bool, str)) or a is None or b is None:
                return a == b
            try:
                return abs(float(a) - float(b)) <= tolerance
            except (TypeError, ValueError):
                return False
        return close(expected, actual)
    if mode in ("unordered", "unordered_nested"):
        return _normalize(expected, mode) == _normalize(actual, mode)
    if isinstance(expected, bool) or isinstance(actual, bool):
        return expected == actual and type(expected) is type(actual)
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        return expected == actual
    return expected == actual


def run_code(code: str, problem: dict, tests: list, timeout: float = TIMEOUT_SECONDS) -> dict:
    """Execute `code` against `tests` for `problem`. Returns a result dict."""
    spec = {
        "kind": problem.get("kind", "function"),
        "function": problem.get("function"),
        "class_name": problem.get("class_name"),
        "arg_types": problem.get("arg_types", {}),
        "return_type": problem.get("return_type", ""),
        "output_mode": problem.get("output_mode", "return"),
    }
    source = PRELUDE + "\n# ---- user code ----\n" + code + "\n# ---- end user code ----\n" + HARNESS_TAIL
    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "solution_run.py")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(source)
        t0 = time.perf_counter()
        try:
            proc = subprocess.run(
                [sys.executable, "-I", path],
                input=json.dumps({"spec": spec, "tests": tests}),
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=td,
            )
        except subprocess.TimeoutExpired:
            return {"status": "Time Limit Exceeded", "passed": 0, "total": len(tests), "cases": [],
                    "stderr": f"Execution exceeded {timeout}s. Check for an infinite loop or an exponential algorithm.",
                    "ms": round((time.perf_counter() - t0) * 1000)}
        wall = round((time.perf_counter() - t0) * 1000)
    stdout, stderr = proc.stdout, proc.stderr
    if "__JUDGE_RESULT__" not in stdout:
        return {"status": "Runtime Error" if proc.returncode else "Compile Error", "passed": 0, "total": len(tests),
                "cases": [], "stderr": (stderr or stdout)[-3000:], "ms": wall}
    user_stdout, _, result_json = stdout.rpartition("\n__JUDGE_RESULT__\n")
    try:
        results = json.loads(result_json)
    except json.JSONDecodeError:
        return {"status": "Runtime Error", "passed": 0, "total": len(tests), "cases": [], "stderr": stderr[-3000:], "ms": wall}
    mode = problem.get("compare", "exact")
    cases = []
    passed = 0
    status = "Accepted"
    for t, r in zip(tests, results):
        expected = t["output"]
        if r.get("ok"):
            ok = compare(expected, r["output"], mode, problem.get("tolerance", 1e-5))
            passed += ok
            cases.append({"input": t["input"], "expected": expected, "output": r["output"], "ok": ok, "ms": r.get("ms")})
            if not ok and status == "Accepted":
                status = "Wrong Answer"
        else:
            cases.append({"input": t["input"], "expected": expected, "output": None, "ok": False, "error": r.get("error"), "trace": r.get("trace")})
            status = "Runtime Error"
    return {"status": status, "passed": passed, "total": len(tests), "cases": cases,
            "stdout": user_stdout[-2000:], "stderr": stderr[-2000:], "ms": wall}
