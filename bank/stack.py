"""Stack pattern problems. See SCHEMA.md for the dict format."""

PROBLEMS = [
    {
        "id": "valid-parentheses",
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "pattern": "Stack",
        "tags": ["String", "Stack"],
        "companies": {"google": 3, "apple": 4, "meta": 4, "amazon": 5, "microsoft": 4},
        "description": (
            "You are given a string `s` made up only of the characters `(`, `)`, `[`, `]`, `{` and `}`. "
            "Decide whether the brackets are **well formed**.\n\n"
            "A string is well formed when every opening bracket is closed by a bracket of the same type, "
            "and brackets close in the reverse order they were opened (so `([)]` is not allowed). "
            "An empty string counts as well formed."
        ),
        "examples": [
            {"input": "s = \"()\"", "output": "true"},
            {"input": "s = \"()[]{}\"", "output": "true"},
            {"input": "s = \"(]\"", "output": "false", "explanation": "The `(` is closed by `]`, a different type."},
            {"input": "s = \"([)]\"", "output": "false", "explanation": "`[` is still open when `)` arrives."},
        ],
        "constraints": ["1 <= s.length <= 10^4", "s consists only of the six bracket characters"],
        "hints": [
            "The most recently opened bracket is the one that must be closed next. Which data structure gives you the most recent item first?",
            "Push every opening bracket. On a closing bracket, the stack top must be its matching opener; otherwise the string is invalid.",
            "A closing bracket with an empty stack is invalid, and so is a non-empty stack at the end. A dict mapping closer -> opener keeps the code to a few lines.",
        ],
        "function": "isValid",
        "signature": "def isValid(self, s: str) -> bool:",
        "arg_types": {"s": "str"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"s": "()"}, "output": True},
            {"input": {"s": "()[]{}"}, "output": True},
            {"input": {"s": "(]"}, "output": False},
            {"input": {"s": "([)]"}, "output": False},
            {"input": {"s": "{[]}"}, "output": True},
            {"input": {"s": "("}, "output": False},
            {"input": {"s": "]"}, "output": False},
            {"input": {"s": "(" * 5000 + ")" * 5000}, "output": True},
            {"input": {"s": "(" * 5000 + ")" * 4999}, "output": False},
            {"input": {"s": "([{}])" * 1500}, "output": True},
        ],
        "solution": '''\
class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {")": "(", "]": "[", "}": "{"}
        stack = []
        for ch in s:
            if ch in pairs:
                if not stack or stack[-1] != pairs[ch]:
                    return False
                stack.pop()
            else:
                stack.append(ch)
        return not stack
''',
        "approach": (
            "**Key insight: brackets nest, so the last one opened must be the first one closed.** That is exactly "
            "last-in-first-out behaviour, i.e. a stack.\n\n"
            "**Algorithm.** Scan left to right. Push each opening bracket. When you meet a closing bracket, the stack "
            "must be non-empty and its top must be the matching opener; pop it. If either check fails, return false. "
            "At the end the stack must be empty, otherwise some bracket was never closed.\n\n"
            "**Why it works.** At any point the stack holds exactly the brackets that are open, innermost on top. "
            "A closing bracket can only legally close the innermost open bracket, which is the top.\n\n"
            "**Common mistakes.** Forgetting the empty-stack check on a closer (`)` alone crashes or passes). "
            "Returning `True` as soon as the loop finishes without checking the stack is empty (`((` would pass). "
            "Counting brackets instead of matching them (`([)]` has balanced counts but is invalid).\n\n"
            "**Interview follow-ups.** (1) The string also contains letters and digits; ignore them. "
            "(2) Return the minimum number of insertions to make the string valid. "
            "(3) Validate a stream too large to hold in memory: only the stack of open brackets is needed, "
            "but its depth is bounded by the nesting depth, not the input length."
        ),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "similar": ["min-stack", "generate-parentheses", "longest-valid-parentheses"],
        "followups": ["Handle other characters in the string.", "Minimum insertions to make it valid."],
    },
    {
        "id": "min-stack",
        "title": "Min Stack",
        "difficulty": "Medium",
        "pattern": "Stack",
        "tags": ["Stack", "Design"],
        "companies": {"google": 2, "apple": 3, "meta": 2, "amazon": 5, "microsoft": 3},
        "kind": "design",
        "class_name": "MinStack",
        "description": (
            "Design a stack that, in addition to the usual operations, can report its **minimum element** at any time.\n\n"
            "- `MinStack()` creates an empty stack.\n"
            "- `push(val)` pushes `val` on top.\n"
            "- `pop()` removes the top element.\n"
            "- `top()` returns the top element without removing it.\n"
            "- `getMin()` returns the smallest element currently in the stack.\n\n"
            "Every operation must run in **O(1)** time. `pop`, `top` and `getMin` are only called on a non-empty stack."
        ),
        "examples": [
            {"input": "[\"MinStack\",\"push\",\"push\",\"push\",\"getMin\",\"pop\",\"top\",\"getMin\"]\n[[],[-2],[0],[-3],[],[],[],[]]",
             "output": "[null,null,null,null,-3,null,0,-2]",
             "explanation": "After pushing -2, 0, -3 the minimum is -3. Popping it leaves 0 on top and -2 as the minimum."},
        ],
        "constraints": ["-2^31 <= val <= 2^31 - 1", "At most 3 * 10^4 calls in total", "pop, top and getMin are never called on an empty stack"],
        "hints": [
            "Scanning the whole stack in getMin is O(n). Can you remember, for each element, what the minimum was when it was pushed?",
            "Keep a second stack that stores the running minimum. On push, push min(val, current minimum); on pop, pop both.",
            "Alternative: store (value, min_so_far) pairs in one stack. Both versions give O(1) for every operation.",
        ],
        "starter": (
            "class MinStack:\n"
            "    def __init__(self):\n"
            "        pass\n\n"
            "    def push(self, val: int) -> None:\n"
            "        pass\n\n"
            "    def pop(self) -> None:\n"
            "        pass\n\n"
            "    def top(self) -> int:\n"
            "        pass\n\n"
            "    def getMin(self) -> int:\n"
            "        pass\n"
        ),
        "compare": "exact",
        "tests": [
            {"input": {"ops": [["MinStack", []], ["push", [-2]], ["push", [0]], ["push", [-3]], ["getMin", []], ["pop", []], ["top", []], ["getMin", []]]},
             "output": [None, None, None, None, -3, None, 0, -2]},
            {"input": {"ops": [["MinStack", []], ["push", [1]], ["push", [1]], ["getMin", []], ["pop", []], ["getMin", []], ["pop", []], ["push", [2]], ["getMin", []], ["top", []]]},
             "output": [None, None, None, 1, None, 1, None, None, 2, 2]},
            {"input": {"ops": [["MinStack", []], ["push", [5]], ["push", [3]], ["push", [4]], ["getMin", []], ["pop", []], ["getMin", []], ["pop", []], ["getMin", []], ["top", []]]},
             "output": [None, None, None, None, 3, None, 3, None, 5, 5]},
            {"input": {"ops": [["MinStack", []], ["push", [-1]], ["push", [-5]], ["push", [-2]], ["getMin", []], ["top", []], ["pop", []], ["pop", []], ["getMin", []]]},
             "output": [None, None, None, None, -5, -2, None, None, -1]},
            {"input": {"ops": [["MinStack", []], ["push", [2147483647]], ["push", [-2147483648]], ["getMin", []], ["pop", []], ["getMin", []]]},
             "output": [None, None, None, -2147483648, None, 2147483647]},
            {"input": {"ops": [["MinStack", []]] + [["push", [i]] for i in range(5000, 0, -1)] + [["getMin", []]] + [["pop", []]] * 2500 + [["getMin", []], ["top", []]]},
             "output": [None] + [None] * 5000 + [1] + [None] * 2500 + [2501, 2501]},
        ],
        "solution": '''\
class MinStack:
    def __init__(self):
        self.stack = []      # values
        self.mins = []       # mins[i] = min of stack[:i+1]

    def push(self, val: int) -> None:
        self.stack.append(val)
        current_min = val if not self.mins else min(val, self.mins[-1])
        self.mins.append(current_min)

    def pop(self) -> None:
        self.stack.pop()
        self.mins.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.mins[-1]
''',
        "approach": (
            "**Key insight: the minimum of a stack only changes at the top.** Popping removes the most recent element, "
            "so the minimum of what remains is exactly the minimum that existed just before that element was pushed. "
            "If we record the running minimum alongside each push, every query is a lookup.\n\n"
            "**Algorithm.** Keep two parallel stacks: `stack` holds the values, `mins[i]` holds the minimum of `stack[0..i]`. "
            "`push(v)` appends `v` and `min(v, mins[-1])`. `pop` pops both. `top` is `stack[-1]`, `getMin` is `mins[-1]`.\n\n"
            "**Why it works.** `mins[-1]` is always the minimum of the current contents by construction, and popping "
            "restores the previous entry, which was the minimum of the previous contents.\n\n"
            "**Common mistakes.** Using `min(stack)` in `getMin` (O(n)). Keeping only a single `min` variable with no "
            "history, which breaks once the minimum is popped. Pushing to the min stack only when the value is strictly "
            "smaller, then popping it when the popped value *equals* the min; this works but must be `<=` on push or "
            "duplicates break it.\n\n"
            "**Interview follow-ups.** (1) Reduce space: only push to `mins` when `val <= mins[-1]`, and pop from it when "
            "the popped value equals `mins[-1]`. (2) The O(1) extra-space trick that stores `2*val - min` encoded values "
            "(and why it needs unbounded integers). (3) Design a **max stack** with `popMax`, which needs a different "
            "structure (two heaps or a sorted container with lazy deletion)."
        ),
        "complexity": {"time": "O(1) per operation", "space": "O(n)"},
        "similar": ["valid-parentheses", "max-stack", "lru-cache"],
        "followups": ["Only store a new minimum when it changes.", "Support popMax as well."],
    },
    {
        "id": "evaluate-reverse-polish-notation",
        "title": "Evaluate Reverse Polish Notation",
        "difficulty": "Medium",
        "pattern": "Stack",
        "tags": ["Array", "Math", "Stack"],
        "companies": {"google": 2, "apple": 2, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "You are given a list of `tokens` that encodes an arithmetic expression in **postfix (Reverse Polish) notation**. "
            "Each token is either an integer or one of the operators `+`, `-`, `*`, `/`.\n\n"
            "Evaluate the expression and return the result. Division between two integers **truncates toward zero** "
            "(so `-7 / 2` is `-3`). The expression is guaranteed to be valid and no division by zero occurs; "
            "all intermediate values fit in a 32-bit signed integer."
        ),
        "examples": [
            {"input": "tokens = [\"2\",\"1\",\"+\",\"3\",\"*\"]", "output": "9", "explanation": "(2 + 1) * 3 = 9."},
            {"input": "tokens = [\"4\",\"13\",\"5\",\"/\",\"+\"]", "output": "6", "explanation": "4 + (13 / 5) = 4 + 2 = 6."},
            {"input": "tokens = [\"10\",\"6\",\"9\",\"3\",\"+\",\"-11\",\"*\",\"/\",\"*\",\"17\",\"+\",\"5\",\"+\"]", "output": "22"},
        ],
        "constraints": ["1 <= tokens.length <= 10^4", "Each token is an operator or an integer in [-200, 200]"],
        "hints": [
            "In postfix notation an operator applies to the two values that came just before it. What holds those two values?",
            "Push numbers. On an operator, pop the right operand first, then the left, compute, and push the result.",
            "Python's // floors toward negative infinity; use int(a / b) to truncate toward zero as the problem requires.",
        ],
        "function": "evalRPN",
        "signature": "def evalRPN(self, tokens: List[str]) -> int:",
        "arg_types": {"tokens": "List[str]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"tokens": ["2", "1", "+", "3", "*"]}, "output": 9},
            {"input": {"tokens": ["4", "13", "5", "/", "+"]}, "output": 6},
            {"input": {"tokens": ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]}, "output": 22},
            {"input": {"tokens": ["3"]}, "output": 3},
            {"input": {"tokens": ["-7", "2", "/"]}, "output": -3},
            {"input": {"tokens": ["7", "-2", "/"]}, "output": -3},
            {"input": {"tokens": ["5", "-3", "*"]}, "output": -15},
            {"input": {"tokens": ["2", "3", "-"]}, "output": -1},
            {"input": {"tokens": ["1"] + ["1", "+"] * 4999}, "output": 5000},
            {"input": {"tokens": ["0"] + ["2", "-"] * 3000}, "output": -6000},
        ],
        "solution": '''\
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for tok in tokens:
            if tok in ("+", "-", "*", "/"):
                b = stack.pop()
                a = stack.pop()
                if tok == "+":
                    stack.append(a + b)
                elif tok == "-":
                    stack.append(a - b)
                elif tok == "*":
                    stack.append(a * b)
                else:
                    stack.append(int(a / b))  # truncate toward zero
            else:
                stack.append(int(tok))
        return stack[0]
''',
        "approach": (
            "**Key insight: postfix notation needs no precedence rules.** By the time you read an operator, its two "
            "operands are the two most recently produced values, so a stack evaluates the expression in a single pass.\n\n"
            "**Algorithm.** For each token: if it is a number, push it. If it is an operator, pop `b` then `a` (order matters "
            "for `-` and `/`), compute `a op b`, push the result. The single remaining value is the answer.\n\n"
            "**Why it works.** A valid RPN expression is a post-order traversal of its expression tree; the stack holds the "
            "evaluated subtrees whose parent has not been seen yet.\n\n"
            "**Common mistakes.** Popping operands in the wrong order (`b - a` instead of `a - b`). Using `//` for division, "
            "which floors: `-7 // 2` is `-4`, but the problem wants `-3`. Treating `\"-11\"` as an operator because it starts "
            "with `-`; test membership in the operator set, not just the first character.\n\n"
            "**Interview follow-ups.** (1) Convert an infix expression to postfix (shunting-yard) and evaluate it. "
            "(2) Add unary minus or exponentiation. (3) Report an error on malformed input instead of assuming validity."
        ),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "similar": ["basic-calculator-ii", "basic-calculator"],
        "followups": ["Infix to postfix conversion.", "Validate malformed expressions."],
    },
    {
        "id": "daily-temperatures",
        "title": "Daily Temperatures",
        "difficulty": "Medium",
        "pattern": "Stack",
        "tags": ["Array", "Stack", "Monotonic Stack"],
        "companies": {"google": 2, "apple": 1, "meta": 1, "amazon": 3, "microsoft": 2},
        "description": (
            "You are given an array `temperatures` where `temperatures[i]` is the forecast for day `i`. "
            "Return an array `answer` of the same length where `answer[i]` is the number of days you have to wait after "
            "day `i` for a **strictly warmer** temperature. If no warmer day comes, `answer[i]` is `0`."
        ),
        "examples": [
            {"input": "temperatures = [73,74,75,71,69,72,76,73]", "output": "[1,1,4,2,1,1,0,0]",
             "explanation": "Day 2 (75) has to wait 4 days for day 6 (76). The last two days never see a warmer day."},
            {"input": "temperatures = [30,40,50,60]", "output": "[1,1,1,0]"},
            {"input": "temperatures = [30,60,90]", "output": "[1,1,0]"},
        ],
        "constraints": ["1 <= temperatures.length <= 10^5", "30 <= temperatures[i] <= 100"],
        "hints": [
            "The brute force looks ahead from every day: O(n^2). Think about which earlier days are still waiting for an answer.",
            "Keep a stack of indices whose answer is unknown. Their temperatures are decreasing from bottom to top.",
            "When a new day is warmer than the stack top, that day is the answer for the top; pop and repeat, then push the new index.",
        ],
        "function": "dailyTemperatures",
        "signature": "def dailyTemperatures(self, temperatures: List[int]) -> List[int]:",
        "arg_types": {"temperatures": "List[int]"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"temperatures": [73, 74, 75, 71, 69, 72, 76, 73]}, "output": [1, 1, 4, 2, 1, 1, 0, 0]},
            {"input": {"temperatures": [30, 40, 50, 60]}, "output": [1, 1, 1, 0]},
            {"input": {"temperatures": [30, 60, 90]}, "output": [1, 1, 0]},
            {"input": {"temperatures": [50]}, "output": [0]},
            {"input": {"temperatures": [80, 80, 80]}, "output": [0, 0, 0]},
            {"input": {"temperatures": [100, 30, 30, 30, 99]}, "output": [0, 3, 2, 1, 0]},
            {"input": {"temperatures": list(range(10000, 5000, -1))}, "output": [0] * 5000},
            {"input": {"temperatures": [30] * 5000 + [31]}, "output": list(range(5000, 0, -1)) + [0]},
        ],
        "solution": '''\
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        answer = [0] * n
        stack = []  # indices with no warmer day found yet; temps decrease bottom -> top
        for i, t in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < t:
                j = stack.pop()
                answer[j] = i - j
            stack.append(i)
        return answer
''',
        "approach": (
            "**Key insight: a day that is waiting for a warmer day can be resolved the moment one arrives, and the days "
            "still waiting always have decreasing temperatures.** That is a monotonic (decreasing) stack.\n\n"
            "**Algorithm.** Walk the array once with a stack of indices. For the current day `i`, while the stack top "
            "is colder than `temperatures[i]`, pop it and set its answer to `i - j`. Then push `i`. Anything left on the "
            "stack at the end keeps its default `0`.\n\n"
            "**Why it works.** If day `j` is below day `k` in the stack, then `temperatures[j] >= temperatures[k]`, so any "
            "day warmer than `j` is also warmer than `k`; resolving from the top is always correct. Each index is pushed and "
            "popped at most once, hence linear time even though there is a nested loop.\n\n"
            "**Common mistakes.** Storing temperatures instead of indices (you lose the distance). Using `<=` in the pop "
            "condition, which treats equal temperatures as warmer. Believing the nested `while` makes it O(n^2).\n\n"
            "**Interview follow-ups.** (1) Return the next warmer temperature itself (Next Greater Element). "
            "(2) Solve it right-to-left with O(1) extra space using the answer array as jump pointers, exploiting the small "
            "temperature range. (3) Stream version: temperatures arrive one at a time and you must emit answers as soon as they are known."
        ),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "similar": ["next-greater-element-i", "largest-rectangle-in-histogram", "online-stock-span"],
        "followups": ["Right-to-left O(1) space variant.", "Streaming input."],
    },
    {
        "id": "car-fleet",
        "title": "Car Fleet",
        "difficulty": "Medium",
        "pattern": "Stack",
        "tags": ["Array", "Sorting", "Stack", "Monotonic Stack"],
        "companies": {"google": 2, "amazon": 1, "microsoft": 1},
        "description": (
            "`n` cars drive along a single-lane road toward a destination at mile `target`. Car `i` starts at mile "
            "`position[i]` (all starting positions are distinct) and drives at `speed[i]` miles per hour.\n\n"
            "A faster car cannot overtake. When it catches up to a slower car ahead, it slows down and the two travel "
            "together as a **fleet** at the slower speed. A fleet can be a single car. A car that catches another exactly "
            "at the destination is still considered part of the same fleet.\n\n"
            "Return the number of fleets that arrive at the destination."
        ),
        "examples": [
            {"input": "target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]", "output": "3",
             "explanation": "Cars at 10 and 8 meet at mile 12 and form one fleet. The car at 0 never catches anyone. Cars at 5 and 3 meet at mile 6 and arrive together."},
            {"input": "target = 10, position = [3], speed = [3]", "output": "1"},
            {"input": "target = 100, position = [0,2,4], speed = [4,2,1]", "output": "1",
             "explanation": "Everyone catches up to the slow car at position 4 before the destination."},
        ],
        "constraints": ["1 <= n <= 10^5", "0 < target <= 10^6", "0 <= position[i] < target, all distinct", "0 < speed[i] <= 10^6"],
        "hints": [
            "Compute how long each car would take to reach the target on its own: (target - position) / speed.",
            "Sort cars by starting position, closest to the target first. A car behind merges into the car ahead iff its own time is <= the fleet time ahead of it.",
            "Walk from the front. Keep the arrival time of the current fleet leader; a car whose time is larger starts a new fleet. A stack of fleet times or a single variable both work.",
        ],
        "function": "carFleet",
        "signature": "def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:",
        "arg_types": {"target": "int", "position": "List[int]", "speed": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"target": 12, "position": [10, 8, 0, 5, 3], "speed": [2, 4, 1, 1, 3]}, "output": 3},
            {"input": {"target": 10, "position": [3], "speed": [3]}, "output": 1},
            {"input": {"target": 100, "position": [0, 2, 4], "speed": [4, 2, 1]}, "output": 1},
            {"input": {"target": 10, "position": [6, 8], "speed": [3, 2]}, "output": 2},
            {"input": {"target": 10, "position": [0, 4, 2], "speed": [2, 1, 3]}, "output": 1},
            {"input": {"target": 10, "position": [8, 3, 7, 4, 6, 5], "speed": [4, 4, 4, 4, 4, 4]}, "output": 6},
            {"input": {"target": 5000, "position": list(range(5000)), "speed": [1] * 5000}, "output": 5000},
            {"input": {"target": 10000, "position": list(range(5000)), "speed": list(range(5000, 0, -1))}, "output": 1},
        ],
        "solution": '''\
class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        cars = sorted(zip(position, speed), reverse=True)  # closest to target first
        fleets = 0
        leader_time = 0.0
        for pos, spd in cars:
            time = (target - pos) / spd
            if time > leader_time:      # cannot catch the fleet ahead -> new fleet
                fleets += 1
                leader_time = time
        return fleets
''',
        "approach": (
            "**Key insight: a car can only ever be slowed down by cars ahead of it, so process cars from the one nearest "
            "the target backwards.** Each car's unimpeded arrival time `(target - position) / speed` tells you whether it "
            "would catch the fleet directly ahead.\n\n"
            "**Algorithm.** Pair positions with speeds, sort by position descending, compute each car's arrival time. "
            "Keep the arrival time of the current fleet leader (initially 0). If a car's time is strictly greater, it can "
            "never catch the fleet ahead: it becomes a new leader and the fleet count grows. Otherwise it merges and is absorbed.\n\n"
            "**Why it works.** A car that would arrive no later than the fleet ahead must physically catch it before the "
            "target, after which it moves at the fleet's speed; its own time no longer matters. A car that would arrive later "
            "never catches up, and cars behind it compare against *its* time. The leader times therefore form a strictly "
            "increasing stack; counting pushes gives the fleet count.\n\n"
            "**Common mistakes.** Forgetting to sort by position (speeds alone say nothing). Using `>=` instead of `>`: "
            "equal arrival time means they meet exactly at the target and count as one fleet. Integer division of times. "
            "Comparing against the car immediately ahead rather than the fleet leader's time (the leader is slower, so the "
            "leader's time is what matters, and the stack handles this naturally).\n\n"
            "**Interview follow-ups.** (1) Return the arrival time of each fleet. (2) Car Fleet II: for each car, the exact "
            "moment it collides with the car ahead (a harder monotonic-stack problem). (3) Cars can appear online in "
            "arbitrary order: you need a sorted container."
        ),
        "complexity": {"time": "O(n log n)", "space": "O(n)"},
        "similar": ["daily-temperatures", "car-fleet-ii"],
        "followups": ["Return each fleet's arrival time.", "Car Fleet II collision times."],
    },
    {
        "id": "largest-rectangle-in-histogram",
        "title": "Largest Rectangle in Histogram",
        "difficulty": "Hard",
        "pattern": "Stack",
        "tags": ["Array", "Stack", "Monotonic Stack"],
        "companies": {"google": 3, "apple": 1, "meta": 1, "amazon": 3, "microsoft": 2},
        "description": (
            "You are given `heights`, the heights of adjacent bars in a histogram; every bar has width `1`. "
            "Return the area of the largest axis-aligned rectangle that fits entirely inside the histogram."
        ),
        "examples": [
            {"input": "heights = [2,1,5,6,2,3]", "output": "10", "explanation": "The bars 5 and 6 together support a rectangle of height 5 and width 2."},
            {"input": "heights = [2,4]", "output": "4", "explanation": "Either the single bar of height 4, or both bars at height 2."},
        ],
        "constraints": ["1 <= heights.length <= 10^5", "0 <= heights[i] <= 10^4"],
        "hints": [
            "Every maximal rectangle is bounded by the height of some bar. For bar i, how far can a rectangle of height heights[i] extend left and right?",
            "It extends until it meets a strictly shorter bar on each side. Finding the nearest shorter bar on both sides for every i is a monotonic-stack problem.",
            "Keep a stack of indices with increasing heights. When the current bar is shorter than the top, the top's right boundary is found and its left boundary is the new stack top. Append a sentinel 0 to flush the stack.",
        ],
        "function": "largestRectangleArea",
        "signature": "def largestRectangleArea(self, heights: List[int]) -> int:",
        "arg_types": {"heights": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"heights": [2, 1, 5, 6, 2, 3]}, "output": 10},
            {"input": {"heights": [2, 4]}, "output": 4},
            {"input": {"heights": [1]}, "output": 1},
            {"input": {"heights": [0]}, "output": 0},
            {"input": {"heights": [2, 2, 2, 2]}, "output": 8},
            {"input": {"heights": [5, 4, 3, 2, 1]}, "output": 9},
            {"input": {"heights": [3, 0, 3]}, "output": 3},
            {"input": {"heights": list(range(1, 5001))}, "output": max(h * (5001 - h) for h in range(1, 5001))},
            {"input": {"heights": [7] * 6000}, "output": 42000},
        ],
        "solution": '''\
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        best = 0
        stack = []  # indices; heights strictly increasing bottom -> top
        for i, h in enumerate(heights + [0]):   # sentinel 0 pops everything at the end
            while stack and heights[stack[-1]] >= h:
                top = stack.pop()
                height = heights[top]
                left = stack[-1] if stack else -1
                width = i - left - 1
                best = max(best, height * width)
            stack.append(i)
        return best
''',
        "approach": (
            "**Key insight: the best rectangle has the height of some bar `i` and stretches from the nearest shorter bar on "
            "the left to the nearest shorter bar on the right.** So the problem reduces to finding both nearest-shorter "
            "neighbours for every bar, which a monotonic stack does in one pass.\n\n"
            "**Algorithm.** Maintain a stack of indices whose heights increase from bottom to top. For each bar `i` "
            "(plus a trailing sentinel of height 0), while the stack top is at least as tall as `heights[i]`, pop it: "
            "the popped bar's right boundary is `i`, its left boundary is the new stack top (or -1 if empty), so its "
            "width is `i - left - 1`. Update the best area. Then push `i`.\n\n"
            "**Why it works.** When a bar is popped, everything between the new top and `i` is at least as tall as it "
            "(otherwise those bars would have popped it earlier), and both neighbours are shorter, so that is exactly the "
            "maximal rectangle with that bar as the limiting height. Every bar is popped exactly once thanks to the sentinel.\n\n"
            "**Common mistakes.** Width computed as `i - left` instead of `i - left - 1`. Forgetting the sentinel and "
            "writing a separate flush loop with different width logic. Popping on `>` instead of `>=`: both work for the "
            "answer, but `>=` keeps the stack strictly increasing and is easier to reason about. Mixing up whether the "
            "stack stores heights or indices.\n\n"
            "**Interview follow-ups.** (1) Maximal Rectangle in a binary matrix: treat each row as a histogram and run this "
            "per row. (2) Divide and conquer with a segment tree for range-minimum, O(n log n), useful if heights change. "
            "(3) Return the rectangle's coordinates, not just the area."
        ),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "similar": ["maximal-rectangle", "daily-temperatures", "trapping-rain-water"],
        "followups": ["Maximal rectangle in a binary matrix.", "Return the rectangle bounds."],
    },
    {
        "id": "basic-calculator-ii",
        "title": "Basic Calculator II",
        "difficulty": "Medium",
        "pattern": "Stack",
        "tags": ["String", "Math", "Stack"],
        "companies": {"google": 3, "apple": 2, "meta": 5, "amazon": 3, "microsoft": 2},
        "description": (
            "Evaluate the arithmetic expression in the string `s` and return its integer value.\n\n"
            "`s` contains non-negative integers, the operators `+ - * /`, and spaces; there are **no parentheses**. "
            "Multiplication and division bind tighter than addition and subtraction and are evaluated left to right. "
            "Integer division **truncates toward zero**. The expression is valid, never divides by zero, and every "
            "intermediate value fits in a 32-bit signed integer. Do not use `eval`."
        ),
        "examples": [
            {"input": "s = \"3+2*2\"", "output": "7", "explanation": "2*2 is evaluated first: 3 + 4."},
            {"input": "s = \" 3/2 \"", "output": "1"},
            {"input": "s = \" 3+5 / 2 \"", "output": "5", "explanation": "5/2 truncates to 2; 3 + 2 = 5."},
        ],
        "constraints": ["1 <= s.length <= 3 * 10^5", "s consists of digits, '+', '-', '*', '/' and spaces", "All intermediate results fit in a signed 32-bit integer"],
        "hints": [
            "Addition and subtraction can be deferred, but multiplication and division must act on the number immediately before them.",
            "Keep a stack of terms to be summed. On + push the number, on - push its negation, on * or / pop the previous term, combine it with the new number, and push the result.",
            "Parse multi-digit numbers as you go, and apply the pending operator when you hit a non-digit or the end of the string. You can replace the stack with a `last` variable and running `total` for O(1) space.",
        ],
        "function": "calculate",
        "signature": "def calculate(self, s: str) -> int:",
        "arg_types": {"s": "str"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"s": "3+2*2"}, "output": 7},
            {"input": {"s": " 3/2 "}, "output": 1},
            {"input": {"s": " 3+5 / 2 "}, "output": 5},
            {"input": {"s": "14-3/2"}, "output": 13},
            {"input": {"s": "0-2147483647"}, "output": -2147483647},
            {"input": {"s": "1-1+1"}, "output": 1},
            {"input": {"s": "2*3*4"}, "output": 24},
            {"input": {"s": "100"}, "output": 100},
            {"input": {"s": "7-10/3"}, "output": 4},
            {"input": {"s": "1-2*3/4"}, "output": 0},
            {"input": {"s": "+".join(["1"] * 5000)}, "output": 5000},
            {"input": {"s": "10000" + "-1" * 3000}, "output": 7000},
        ],
        "solution": '''\
class Solution:
    def calculate(self, s: str) -> int:
        stack = []
        num = 0
        op = "+"            # operator that applies to the number being read
        for i, ch in enumerate(s):
            if ch.isdigit():
                num = num * 10 + int(ch)
            if (not ch.isdigit() and ch != " ") or i == len(s) - 1:
                if op == "+":
                    stack.append(num)
                elif op == "-":
                    stack.append(-num)
                elif op == "*":
                    stack.append(stack.pop() * num)
                else:
                    prev = stack.pop()
                    stack.append(int(prev / num))   # truncate toward zero
                op = ch
                num = 0
        return sum(stack)
''',
        "approach": (
            "**Key insight: precedence can be handled by deferring `+` and `-` while applying `*` and `/` immediately to "
            "the previous term.** If every term is pushed with its sign, the answer is just the sum of the stack.\n\n"
            "**Algorithm.** Scan the string, accumulating the current number digit by digit. Remember the operator that "
            "precedes that number (initially `+`). When you reach an operator or the end of the string, apply the pending "
            "operator: `+` pushes `num`, `-` pushes `-num`, `*` and `/` pop the last term, combine it with `num`, and push "
            "the result. Then record the new operator and reset `num`. Finally return the sum of the stack.\n\n"
            "**Why it works.** The stack always holds a list of signed terms whose sum equals the value of the prefix "
            "processed so far. `*` and `/` only ever need to modify the most recent term because they bind tighter than "
            "the `+`/`-` that separated it from earlier terms, and they associate left to right.\n\n"
            "**Common mistakes.** Not applying the last pending operation at the end of the string. Treating spaces as "
            "operator boundaries (they must be skipped). Using `//`, which floors negative quotients: `-7 // 2 = -4`, but "
            "the expected result is `-3`. Resetting `num` before using it. Trying to handle `*` and `/` on the fly without "
            "first parsing the complete multi-digit number.\n\n"
            "**Interview follow-ups.** (1) Basic Calculator I/III: add parentheses, usually by recursing or pushing the "
            "running state when you see `(`. (2) O(1) space: replace the stack with `total` and `last`. "
            "(3) Support unary minus or floating-point numbers, and report syntax errors instead of trusting the input."
        ),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "similar": ["evaluate-reverse-polish-notation", "basic-calculator", "basic-calculator-iii"],
        "followups": ["Add parentheses support.", "Reduce to O(1) space."],
    },
    {
        "id": "decode-string",
        "title": "Decode String",
        "difficulty": "Medium",
        "pattern": "Stack",
        "tags": ["String", "Stack", "Recursion"],
        "companies": {"google": 3, "apple": 2, "meta": 2, "amazon": 2, "microsoft": 2},
        "description": (
            "A string is encoded with the rule `k[inner]`, meaning the decoded form of `inner` is repeated exactly `k` times "
            "(`k` is a positive integer). Encoded blocks can be nested and placed next to plain letters.\n\n"
            "Given a valid encoded string `s`, return its decoded form. Digits only ever appear as repeat counts, and the "
            "decoded string contains only lowercase letters."
        ),
        "examples": [
            {"input": "s = \"3[a]2[bc]\"", "output": "\"aaabcbc\""},
            {"input": "s = \"3[a2[c]]\"", "output": "\"accaccacc\"", "explanation": "The inner 2[c] becomes cc, so each copy is acc."},
            {"input": "s = \"2[abc]3[cd]ef\"", "output": "\"abcabccdcdcdef\""},
        ],
        "constraints": ["1 <= s.length <= 30", "s consists of digits, lowercase letters and square brackets", "Repeat counts are in [1, 300]", "The decoded output is at most 10^5 characters"],
        "hints": [
            "When you hit a `]` you need to know the text inside the matching `[` and the number right before it. Nesting means you must remember several such contexts.",
            "Keep a stack. On `[` push the current string and current count, then start fresh. On `]` pop them and set current = previous + count * current.",
            "Counts can be multi-digit, so accumulate digits before the `[`. A recursive descent parser is an equally accepted solution.",
        ],
        "function": "decodeString",
        "signature": "def decodeString(self, s: str) -> str:",
        "arg_types": {"s": "str"},
        "return_type": "str",
        "compare": "exact",
        "tests": [
            {"input": {"s": "3[a]2[bc]"}, "output": "aaabcbc"},
            {"input": {"s": "3[a2[c]]"}, "output": "accaccacc"},
            {"input": {"s": "2[abc]3[cd]ef"}, "output": "abcabccdcdcdef"},
            {"input": {"s": "abc"}, "output": "abc"},
            {"input": {"s": "10[x]"}, "output": "xxxxxxxxxx"},
            {"input": {"s": "2[2[2[y]]]"}, "output": "yyyyyyyy"},
            {"input": {"s": "a2[b3[c]]d"}, "output": "abcccbcccd"},
            {"input": {"s": "3000[q]"}, "output": "q" * 3000},
            {"input": {"s": "1[" * 1000 + "z" + "]" * 1000}, "output": "z"},
            {"input": {"s": "2[ab]" * 1500}, "output": "abab" * 1500},
        ],
        "solution": '''\
class Solution:
    def decodeString(self, s: str) -> str:
        stack = []          # (string_before_bracket, repeat_count)
        current = []        # characters of the string being built
        count = 0
        for ch in s:
            if ch.isdigit():
                count = count * 10 + int(ch)
            elif ch == "[":
                stack.append(("".join(current), count))
                current, count = [], 0
            elif ch == "]":
                prev, k = stack.pop()
                current = [prev + "".join(current) * k]
            else:
                current.append(ch)
        return "".join(current)
''',
        "approach": (
            "**Key insight: every `[` opens a new context that must be finished before the enclosing one can continue.** "
            "Saving the enclosing context on a stack and restoring it at `]` decodes arbitrarily nested input in one pass.\n\n"
            "**Algorithm.** Keep `current` (the string being built) and `count` (digits seen since the last non-digit). "
            "On a digit, extend `count`. On `[`, push `(current, count)` and reset both. On `]`, pop `(prev, k)` and set "
            "`current = prev + current * k`. Letters are appended to `current`. The final `current` is the answer.\n\n"
            "**Why it works.** The stack mirrors the bracket nesting: each level holds the text decoded so far at that depth "
            "and the multiplier waiting for the bracket to close. Because the input is valid, every `]` pops the context "
            "pushed by its matching `[`.\n\n"
            "**Common mistakes.** Taking only one digit for the count (`10[x]`). Forgetting to reset `count` after `[`. "
            "Building strings with repeated `+=` inside deep nesting, which can go quadratic; a list of parts or a single "
            "join per level keeps it linear in the output size. Writing a recursive solution that returns the string but "
            "loses track of the index where the recursion stopped.\n\n"
            "**Interview follow-ups.** (1) Return only the `k`-th character of the decoded string without expanding it "
            "(work with lengths). (2) Decode a stream or a very long string where the output does not fit in memory. "
            "(3) Allow `k` to be omitted (meaning 1) or allow nested counts like `2[3]`."
        ),
        "complexity": {"time": "O(n + m) where m is the output length", "space": "O(n + m)"},
        "similar": ["basic-calculator", "number-of-atoms", "decoded-string-at-index"],
        "followups": ["Return the k-th decoded character without expanding.", "Recursive descent version."],
    },
    {
        "id": "asteroid-collision",
        "title": "Asteroid Collision",
        "difficulty": "Medium",
        "pattern": "Stack",
        "tags": ["Array", "Stack", "Simulation"],
        "companies": {"google": 2, "meta": 1, "amazon": 3, "microsoft": 1},
        "description": (
            "You are given an array `asteroids` describing asteroids in a row. The absolute value is the asteroid's size "
            "and the sign is its direction: positive moves right, negative moves left. All asteroids move at the same speed.\n\n"
            "When two asteroids collide, the smaller one is destroyed; if they are the same size, both are destroyed. "
            "Asteroids moving in the same direction never collide. Return the state of the asteroids after every "
            "possible collision has happened."
        ),
        "examples": [
            {"input": "asteroids = [5,10,-5]", "output": "[5,10]", "explanation": "10 and -5 collide; -5 is destroyed. 5 and 10 move the same way."},
            {"input": "asteroids = [8,-8]", "output": "[]", "explanation": "Equal sizes, both are destroyed."},
            {"input": "asteroids = [10,2,-5]", "output": "[10]", "explanation": "2 and -5 collide leaving -5, which then loses to 10."},
        ],
        "constraints": ["2 <= asteroids.length <= 10^4", "-1000 <= asteroids[i] <= 1000", "asteroids[i] != 0"],
        "hints": [
            "Only a right-moving asteroid followed (somewhere later) by a left-moving one can collide. Everything else is stable.",
            "Keep a stack of survivors. A new positive asteroid is just pushed. A new negative one fights the positive asteroids on top of the stack, from the most recent backwards.",
            "Pop smaller positives while the negative survives. If sizes are equal pop and drop the negative too. If the stack top is negative or empty, the negative asteroid survives and is pushed.",
        ],
        "function": "asteroidCollision",
        "signature": "def asteroidCollision(self, asteroids: List[int]) -> List[int]:",
        "arg_types": {"asteroids": "List[int]"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"asteroids": [5, 10, -5]}, "output": [5, 10]},
            {"input": {"asteroids": [8, -8]}, "output": []},
            {"input": {"asteroids": [10, 2, -5]}, "output": [10]},
            {"input": {"asteroids": [-2, -1, 1, 2]}, "output": [-2, -1, 1, 2]},
            {"input": {"asteroids": [1, -2, -2, -2]}, "output": [-2, -2, -2]},
            {"input": {"asteroids": [3]}, "output": [3]},
            {"input": {"asteroids": [1, 2, 3, -3]}, "output": [1, 2]},
            {"input": {"asteroids": list(range(5000, 0, -1)) + [-5000]}, "output": []},
            {"input": {"asteroids": list(range(1, 5001)) + [-1]}, "output": list(range(1, 5001))},
            {"input": {"asteroids": [1] * 4000 + [-4000]}, "output": [-4000]},
        ],
        "solution": '''\
class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        stack = []
        for a in asteroids:
            alive = True
            while alive and a < 0 and stack and stack[-1] > 0:
                top = stack[-1]
                if top < -a:
                    stack.pop()          # the right-mover is destroyed, keep fighting
                elif top == -a:
                    stack.pop()          # both destroyed
                    alive = False
                else:
                    alive = False        # the new asteroid is destroyed
            if alive:
                stack.append(a)
        return stack
''',
        "approach": (
            "**Key insight: the only collisions are between a right-moving asteroid and a left-moving asteroid that comes "
            "after it, and the left-mover meets the nearest right-movers first.** A stack of survivors models this: the "
            "top is the asteroid a new left-mover hits first.\n\n"
            "**Algorithm.** Iterate once. Positive asteroids are pushed. For a negative asteroid `a`, while the stack top is "
            "positive: if the top is smaller than `|a|`, pop it and continue; if equal, pop it and drop `a`; if larger, drop `a`. "
            "If `a` is still alive after the loop (stack empty or top negative), push it. The stack is the answer.\n\n"
            "**Why it works.** Negative asteroids already on the stack are to the left of everything after them and moving "
            "left, so nothing can reach them; positives on the stack are stable until a negative arrives, and the order they "
            "are hit is top-down. Each asteroid is pushed and popped at most once, so the nested loop is still O(n).\n\n"
            "**Common mistakes.** Forgetting the equal-size case destroys *both*. Pushing the negative asteroid even after it "
            "was destroyed. Breaking out of the `while` without recording whether the new asteroid survived. Simulating "
            "position by position, which is both slow and unnecessary.\n\n"
            "**Interview follow-ups.** (1) Asteroids have different speeds (then it is a simulation / event-queue problem). "
            "(2) Count collisions instead of returning survivors. (3) The row is circular, so a left-mover at the start can "
            "wrap around and hit a right-mover at the end."
        ),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "similar": ["daily-temperatures", "remove-all-adjacent-duplicates-in-string", "car-fleet"],
        "followups": ["Different speeds.", "Circular row."],
    },
]
