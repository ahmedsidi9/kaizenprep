# Problem bank schema

Every file `bank/<name>.py` defines `PROBLEMS: list[dict]`. Run
`python3 validate.py <name>` from the `prepcode` folder; it must print `0 failures`.
`bank/seed.py` is the reference and demonstrates every feature below.

## Fields (all required unless marked optional)

| Field | Type | Notes |
|---|---|---|
| `id` | str | kebab-case slug, unique across the bank |
| `title` | str | |
| `difficulty` | `"Easy" \| "Medium" \| "Hard"` | |
| `pattern` | str | one of `bank.PATTERN_ORDER` exactly |
| `tags` | list[str] | topic tags, e.g. `["Array", "Hash Table"]` |
| `companies` | dict | keys from `google, apple, meta, amazon, microsoft`; values 0-5 = how often this problem (or a close variant) is reported in interviews at that company, from public interview reports and your own knowledge. Omit a company rather than writing 0. |
| `description` | str (markdown) | **Your own wording.** Do not copy LeetCode's text. Inline code with backticks, bold with `**`. |
| `examples` | list[{input, output, explanation?}] | strings, shown verbatim |
| `constraints` | list[str] | |
| `hints` | list[str] | at least 2, progressive: nudge, then approach, then detail |
| `function` | str | method name on `class Solution` (function problems) |
| `signature` | str | the full `def ...:` line, with type hints, e.g. `def twoSum(self, nums: List[int], target: int) -> List[int]:` |
| `arg_types` | dict | param -> type string. Special values: `ListNode`, `TreeNode`, `GraphNode` (adjacency list, 1-indexed), `NaryNode`, `List[ListNode]`, `List[TreeNode]`. Plain JSON types can be anything (`List[int]`, `str`...). |
| `return_type` | str | same special values apply, else anything |
| `output_mode` | str, optional | `"return"` (default) \| `"arg:<name>"` (check an in-place-mutated argument) \| `"prefix:<name>"` (function returns k; judge compares `[k, arg[:k]]`) |
| `compare` | str | `"exact"` \| `"unordered"` (outer list order ignored) \| `"unordered_nested"` (inner and outer order ignored) \| `"any_of"` (expected is a list of acceptable outputs) \| `"float"` (tolerance 1e-5, or set `tolerance`; applies recursively inside lists and dicts) |
| `tests` | list[{input: dict, output}] | at least 4; the first 2-3 should match `examples`; include edge cases (empty, single element, duplicates, negatives) and one larger case (n in the thousands) to catch O(n^2) where O(n log n) is expected. Inputs are JSON values keyed by parameter name. Linked lists are arrays, trees are level-order arrays with `None` for missing children. |
| `solution` | str | complete Python source defining `class Solution` with the method. May define helper classes/functions at module level. Must pass every test. The harness already imports `List, Optional, deque, defaultdict, Counter, heapq, bisect, math, itertools, functools, lru_cache, cache` and defines `ListNode`, `TreeNode`, `Node`. |
| `approach` | str (markdown) | the editorial: the key insight in bold, the algorithm, why it is correct, common mistakes, and **interview follow-ups** the interviewer is likely to ask |
| `complexity` | `{time, space}` | |
| `similar` | list[str], optional | ids of related problems (can reference ids in other modules) |
| `followups` | list[str], optional | |

## Design problems

Set `"kind": "design"`, `"class_name": "LRUCache"`, and `"starter"` (the class skeleton shown in the editor).
Tests use `{"input": {"ops": [["LRUCache", [2]], ["put", [1, 1]], ["get", [1]]]}, "output": [None, None, 1]}`.
The first op must be the constructor. Methods returning nothing produce `None`.

## Rules

- Descriptions, examples, hints, and editorials are written by you from your understanding of the problem. Never paste text from leetcode.com.
- Solutions must be the canonical optimal approach an interviewer expects, with clean readable code.
- Every test's expected output must be correct; the validator runs your solution and only checks self-consistency, so double-check expected values by hand for the small cases.
- Keep each problem self-contained; no imports beyond what the prelude provides unless you add them inside `solution`.
