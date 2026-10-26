"""Math & Bit Manipulation problems. See SCHEMA.md for the dict format."""

PROBLEMS = [
    {
        "id": "rotate-image",
        "title": "Rotate Image",
        "difficulty": "Medium",
        "pattern": "Math & Bit Manipulation",
        "tags": ["Array", "Matrix", "Math"],
        "companies": {"google": 2, "apple": 3, "meta": 2, "amazon": 3, "microsoft": 3},
        "description": (
            "You are given an `n x n` matrix representing an image. Rotate it **90 degrees clockwise, in place**: you must modify the "
            "given matrix directly rather than allocating a second `n x n` matrix.\n\n"
            "Do not return anything."
        ),
        "examples": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "output": "[[7,4,1],[8,5,2],[9,6,3]]",
             "explanation": "The first column (1,4,7) read bottom-up becomes the first row."},
            {"input": "matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]", "output": "[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]"},
            {"input": "matrix = [[1]]", "output": "[[1]]"},
        ],
        "constraints": ["1 <= n <= 20", "-1000 <= matrix[i][j] <= 1000"],
        "hints": [
            "Where does cell (i, j) end up after a clockwise quarter turn? Row i becomes column n-1-i.",
            "A clockwise rotation is the same as transposing the matrix (swap across the main diagonal) and then reversing each row.",
            "Transpose by swapping matrix[i][j] with matrix[j][i] for j > i only, otherwise you swap everything back.",
        ],
        "function": "rotate",
        "signature": "def rotate(self, matrix: List[List[int]]) -> None:",
        "arg_types": {"matrix": "List[List[int]]"},
        "return_type": "None",
        "output_mode": "arg:matrix",
        "compare": "exact",
        "tests": [
            {"input": {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}, "output": [[7, 4, 1], [8, 5, 2], [9, 6, 3]]},
            {"input": {"matrix": [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]},
             "output": [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]},
            {"input": {"matrix": [[1]]}, "output": [[1]]},
            {"input": {"matrix": [[1, 2], [3, 4]]}, "output": [[3, 1], [4, 2]]},
            {"input": {"matrix": [[-1, 0], [0, -1]]}, "output": [[0, -1], [-1, 0]]},
            {"input": {"matrix": [[i * 300 + j for j in range(300)] for i in range(300)]},
             "output": [[(299 - j) * 300 + i for j in range(300)] for i in range(300)]},
        ],
        "solution": (
            "class Solution:\n"
            "    def rotate(self, matrix: List[List[int]]) -> None:\n"
            "        n = len(matrix)\n"
            "        # 1. transpose: reflect across the main diagonal\n"
            "        for i in range(n):\n"
            "            for j in range(i + 1, n):\n"
            "                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]\n"
            "        # 2. reverse every row\n"
            "        for row in matrix:\n"
            "            row.reverse()\n"
        ),
        "approach": (
            "**Key insight: a 90-degree clockwise rotation decomposes into two reflections that are each trivial to do in place: "
            "transpose, then reverse each row.**\n\n"
            "After transposing, the element originally at `(i, j)` sits at `(j, i)`. Reversing row `j` moves it to `(j, n-1-i)`, which is "
            "exactly where a clockwise rotation sends `(i, j)`. Both steps swap pairs of cells, so no extra matrix is needed.\n\n"
            "**Alternative: four-way cycle.** Process the matrix in concentric rings; for each position on the top edge of a ring, rotate "
            "the four corresponding cells (top, right, bottom, left) with one temporary. Same complexity, more index arithmetic, and the "
            "usual source of off-by-one bugs in interviews. Mention it, but write the transpose version.\n\n"
            "**Common mistakes:** transposing over the full square (every pair swapped twice, matrix unchanged); confusing clockwise with "
            "counter-clockwise (counter-clockwise = transpose then reverse each column, or reverse rows then transpose); returning a new "
            "matrix when the problem demands in place.\n\n"
            "**Interview follow-ups:** (1) Rotate 180 or 270 degrees (compose rotations, or reverse rows and columns for 180). "
            "(2) Rotate a non-square `m x n` matrix (cannot be done in place in the same buffer; return a new `n x m` matrix). "
            "(3) Rotate by an arbitrary angle for real images (interpolation, outside scope but shows you know the limits)."
        ),
        "complexity": {"time": "O(n^2)", "space": "O(1)"},
        "similar": ["set-matrix-zeroes", "spiral-matrix", "transpose-matrix"],
    },
    {
        "id": "set-matrix-zeroes",
        "title": "Set Matrix Zeroes",
        "difficulty": "Medium",
        "pattern": "Math & Bit Manipulation",
        "tags": ["Array", "Matrix", "Hash Table"],
        "companies": {"google": 1, "apple": 1, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "Given an `m x n` integer matrix, for every cell that is `0` in the **original** matrix, set its entire row and entire column "
            "to `0`. Do this in place.\n\n"
            "Zeros created by the operation must not trigger further clearing. Aim for `O(1)` extra space."
        ),
        "examples": [
            {"input": "matrix = [[1,1,1],[1,0,1],[1,1,1]]", "output": "[[1,0,1],[0,0,0],[1,0,1]]"},
            {"input": "matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]", "output": "[[0,0,0,0],[0,4,5,0],[0,3,1,0]]",
             "explanation": "Row 0 and columns 0 and 3 are cleared."},
            {"input": "matrix = [[1,0,3]]", "output": "[[0,0,0]]"},
        ],
        "constraints": ["1 <= m, n <= 200", "-2^31 <= matrix[i][j] <= 2^31 - 1"],
        "hints": [
            "Clearing as soon as you see a zero destroys information: the new zeros look like original ones. Record first, clear second.",
            "Two boolean arrays (rows to clear, columns to clear) give O(m + n) space. To get to O(1), store those flags inside the matrix itself.",
            "Use the first row as the column flags and the first column as the row flags. Those two lines overlap at matrix[0][0], so keep one separate boolean for whether column 0 itself must be cleared. Clear the interior first, then row 0 and column 0 last.",
        ],
        "function": "setZeroes",
        "signature": "def setZeroes(self, matrix: List[List[int]]) -> None:",
        "arg_types": {"matrix": "List[List[int]]"},
        "return_type": "None",
        "output_mode": "arg:matrix",
        "compare": "exact",
        "tests": [
            {"input": {"matrix": [[1, 1, 1], [1, 0, 1], [1, 1, 1]]}, "output": [[1, 0, 1], [0, 0, 0], [1, 0, 1]]},
            {"input": {"matrix": [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]}, "output": [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]},
            {"input": {"matrix": [[1, 0, 3]]}, "output": [[0, 0, 0]]},
            {"input": {"matrix": [[1]]}, "output": [[1]]},
            {"input": {"matrix": [[0]]}, "output": [[0]]},
            {"input": {"matrix": [[1, 2, 3]]}, "output": [[1, 2, 3]]},
            {"input": {"matrix": [[1], [0], [3]]}, "output": [[0], [0], [0]]},
            {"input": {"matrix": [[1, 2], [0, 4]]}, "output": [[0, 2], [0, 0]]},
            {"input": {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 0]]}, "output": [[1, 2, 0], [4, 5, 0], [0, 0, 0]]},
            {"input": {"matrix": [[0 if (i == 150 and j == 150) else 1 for j in range(300)] for i in range(300)]},
             "output": [[0 if (i == 150 or j == 150) else 1 for j in range(300)] for i in range(300)]},
        ],
        "solution": (
            "class Solution:\n"
            "    def setZeroes(self, matrix: List[List[int]]) -> None:\n"
            "        m, n = len(matrix), len(matrix[0])\n"
            "        clear_col0 = False\n"
            "        # 1. record flags: matrix[i][0] marks row i, matrix[0][j] marks column j (j >= 1)\n"
            "        for i in range(m):\n"
            "            if matrix[i][0] == 0:\n"
            "                clear_col0 = True\n"
            "            for j in range(1, n):\n"
            "                if matrix[i][j] == 0:\n"
            "                    matrix[i][0] = 0\n"
            "                    matrix[0][j] = 0\n"
            "        # 2. clear the interior using the flags (bottom-up so row 0 stays intact until last)\n"
            "        for i in range(m - 1, -1, -1):\n"
            "            for j in range(n - 1, 0, -1):\n"
            "                if matrix[i][0] == 0 or matrix[0][j] == 0:\n"
            "                    matrix[i][j] = 0\n"
            "            if clear_col0:\n"
            "                matrix[i][0] = 0\n"
        ),
        "approach": (
            "**Key insight: separate 'which rows and columns need clearing' from the clearing itself, and store those flags inside the "
            "matrix's own first row and first column so no extra arrays are needed.**\n\n"
            "Pass 1 scans every cell. A zero at `(i, j)` sets `matrix[i][0] = 0` (row `i` must be cleared) and `matrix[0][j] = 0` "
            "(column `j` must be cleared). The cell `(0, 0)` would have to serve both as the flag for row 0 and for column 0, so column 0 "
            "gets its own boolean `clear_col0`, and the inner loop starts at `j = 1`.\n\n"
            "Pass 2 walks the matrix from the bottom-right towards the top-left, zeroing `(i, j)` when either flag is set, and finally "
            "zeroing `(i, 0)` if `clear_col0`. Going bottom-up matters: row 0 holds the column flags and must be read for every other row "
            "before it is itself overwritten.\n\n"
            "**Why it is correct:** after pass 1, `matrix[i][0] == 0` iff row `i` originally contained a zero (either it was already zero, "
            "or a zero elsewhere in the row set it), and likewise for `matrix[0][j]`. Pass 2 reads only those flags, never the interior, "
            "so newly created zeros cannot cascade.\n\n"
            "**Simpler alternatives:** two boolean arrays (`O(m + n)` space) are perfectly acceptable as a first answer; a set of rows and "
            "set of columns is the same idea. Replacing zeros with a sentinel value is wrong because every integer is a legal cell value.\n\n"
            "**Common mistakes:** clearing while scanning; letting `(0, 0)` do double duty; iterating pass 2 top-down and wiping row 0's "
            "flags early; forgetting the `j = 1` start so that column 0 flags corrupt row flags.\n\n"
            "**Interview follow-ups:** (1) Clear only the row, or only the column. (2) Count how many cells end up zero without modifying "
            "the matrix (`r*n + c*m - r*c` for `r` rows and `c` columns flagged). (3) The matrix is huge and stored on disk: a two-pass "
            "streaming version with `O(m + n)` memory is the realistic answer."
        ),
        "complexity": {"time": "O(m * n)", "space": "O(1)"},
        "similar": ["rotate-image", "game-of-life", "spiral-matrix"],
    },
    {
        "id": "happy-number",
        "title": "Happy Number",
        "difficulty": "Easy",
        "pattern": "Math & Bit Manipulation",
        "tags": ["Math", "Hash Table", "Two Pointers"],
        "companies": {"google": 1, "apple": 1, "amazon": 1},
        "description": (
            "Starting from a positive integer `n`, repeatedly replace the number by the **sum of the squares of its digits**. "
            "If this process eventually reaches `1`, the number is called happy; otherwise it falls into a cycle that never contains `1`.\n\n"
            "Return `true` if `n` is a happy number, otherwise `false`."
        ),
        "examples": [
            {"input": "n = 19", "output": "true", "explanation": "1^2 + 9^2 = 82, 8^2 + 2^2 = 68, 6^2 + 8^2 = 100, 1^2 + 0 + 0 = 1."},
            {"input": "n = 2", "output": "false", "explanation": "2 -> 4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4, a cycle without 1."},
            {"input": "n = 7", "output": "true", "explanation": "7 -> 49 -> 97 -> 130 -> 10 -> 1."},
        ],
        "constraints": ["1 <= n <= 2^31 - 1"],
        "hints": [
            "Why must the process either reach 1 or repeat? Because the digit-square sum of any number below 10^10 is at most 810, so the values are bounded and must eventually revisit one.",
            "Record every value you have seen in a set. If you see one twice without reaching 1, the answer is false.",
            "For O(1) space, treat the sequence like a linked list and use Floyd's cycle detection: a slow pointer taking one step and a fast pointer taking two meet either at 1 or inside the cycle.",
        ],
        "function": "isHappy",
        "signature": "def isHappy(self, n: int) -> bool:",
        "arg_types": {"n": "int"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"n": 19}, "output": True},
            {"input": {"n": 2}, "output": False},
            {"input": {"n": 7}, "output": True},
            {"input": {"n": 1}, "output": True},
            {"input": {"n": 4}, "output": False},
            {"input": {"n": 1111111}, "output": True},
            {"input": {"n": 999999999}, "output": False},
            {"input": {"n": 2147483647}, "output": False},
        ],
        "solution": (
            "class Solution:\n"
            "    def isHappy(self, n: int) -> bool:\n"
            "        def step(x: int) -> int:\n"
            "            total = 0\n"
            "            while x:\n"
            "                x, d = divmod(x, 10)\n"
            "                total += d * d\n"
            "            return total\n"
            "\n"
            "        slow, fast = n, step(n)\n"
            "        while fast != 1 and slow != fast:\n"
            "            slow = step(slow)\n"
            "            fast = step(step(fast))\n"
            "        return fast == 1\n"
        ),
        "approach": (
            "**Key insight: the digit-square-sum map sends every number into a small bounded range, so the sequence is an implicit "
            "linked list that must terminate at 1 or enter a cycle. Detect the cycle.**\n\n"
            "The bound: a number with `d` digits maps to at most `81 * d`. For `d >= 4`, `81 * d < 10^(d-1)`, so values shrink until they are "
            "below 1000, after which they stay below `81 * 3 = 243`. Finitely many states means repetition is guaranteed.\n\n"
            "**Set-based version:** iterate, storing each value in a set; stop at 1 (true) or at a repeat (false). Simple and `O(k)` space "
            "for `k` distinct values (small in practice).\n\n"
            "**Floyd's tortoise and hare:** advance `slow` one step and `fast` two steps per iteration. If the sequence reaches 1, `fast` gets "
            "there first and we return true (1 maps to 1, so it is a fixed point). Otherwise the two pointers meet inside the cycle and we "
            "return false. This uses `O(1)` extra space.\n\n"
            "**Fun fact for interviews:** every unhappy number falls into the single cycle `4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4`, "
            "so checking `x == 4` is a valid (if cheeky) termination test.\n\n"
            "**Common mistakes:** using string conversion in the hot loop (fine for correctness, slower); forgetting that 1 itself is "
            "happy; in Floyd, starting both pointers at `n` and immediately exiting because they are equal.\n\n"
            "**Interview follow-ups:** (1) Prove the sequence is bounded (the `81 * d` argument). (2) Linked List Cycle uses the same "
            "two-pointer technique. (3) Generalise to sum of cubes or a different base and ask which cycles appear."
        ),
        "complexity": {"time": "O(log n) per step, O(1) steps in practice", "space": "O(1)"},
        "similar": ["linked-list-cycle", "add-digits", "ugly-number"],
    },
    {
        "id": "plus-one",
        "title": "Plus One",
        "difficulty": "Easy",
        "pattern": "Math & Bit Manipulation",
        "tags": ["Array", "Math"],
        "companies": {"google": 3, "apple": 2, "meta": 1, "amazon": 2, "microsoft": 1},
        "description": (
            "A non-negative integer is given as an array `digits`, most significant digit first, with no leading zeros except for the "
            "number `0` itself.\n\n"
            "Add one to the integer and return the resulting digit array."
        ),
        "examples": [
            {"input": "digits = [1,2,3]", "output": "[1,2,4]"},
            {"input": "digits = [9,9,9]", "output": "[1,0,0,0]", "explanation": "999 + 1 = 1000; the array grows by one digit."},
            {"input": "digits = [0]", "output": "[1]"},
        ],
        "constraints": ["1 <= digits.length <= 100", "0 <= digits[i] <= 9", "No leading zeros unless the number is 0."],
        "hints": [
            "Simulate the addition you learned in school, starting from the rightmost digit.",
            "Walk from the end. If the digit is below 9, increment it and stop. If it is 9, set it to 0 and keep carrying.",
            "If you run off the front of the array, every digit was 9: the answer is a 1 followed by all zeros.",
        ],
        "function": "plusOne",
        "signature": "def plusOne(self, digits: List[int]) -> List[int]:",
        "arg_types": {"digits": "List[int]"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"digits": [1, 2, 3]}, "output": [1, 2, 4]},
            {"input": {"digits": [9, 9, 9]}, "output": [1, 0, 0, 0]},
            {"input": {"digits": [0]}, "output": [1]},
            {"input": {"digits": [4, 3, 2, 1]}, "output": [4, 3, 2, 2]},
            {"input": {"digits": [9]}, "output": [1, 0]},
            {"input": {"digits": [1, 9, 9]}, "output": [2, 0, 0]},
            {"input": {"digits": [8, 9]}, "output": [9, 0]},
            {"input": {"digits": [9] * 5000}, "output": [1] + [0] * 5000},
            {"input": {"digits": [1] + [2] * 4999}, "output": [1] + [2] * 4998 + [3]},
        ],
        "solution": (
            "class Solution:\n"
            "    def plusOne(self, digits: List[int]) -> List[int]:\n"
            "        for i in range(len(digits) - 1, -1, -1):\n"
            "            if digits[i] < 9:\n"
            "                digits[i] += 1\n"
            "                return digits\n"
            "            digits[i] = 0   # 9 becomes 0, carry continues\n"
            "        return [1] + digits  # every digit was 9\n"
        ),
        "approach": (
            "**Key insight: adding one only ever produces a carry through a run of trailing 9s. Find the first non-9 from the right, "
            "bump it, and zero everything after it.**\n\n"
            "Scan from the last digit. A digit below 9 absorbs the carry: increment it and return immediately. A 9 becomes 0 and the "
            "carry moves left. If the loop finishes, all digits were 9 and the result is `[1, 0, 0, ..., 0]` with one extra digit.\n\n"
            "**Why it is correct:** this is exactly column addition of `+1`: the carry is 1 while we see 9s and becomes 0 at the first "
            "smaller digit, after which no digit to the left changes.\n\n"
            "**Common mistakes:** converting to an integer and back (defeats the purpose and overflows in fixed-width languages); "
            "handling the all-9 case by inserting at index 0 of a long list in a loop (quadratic); mutating the input when the caller "
            "may not expect it (clarify, or copy).\n\n"
            "**Interview follow-ups:** (1) Add an arbitrary number `k` instead of 1 (carry becomes `k % 10`-style, see Add to Array-Form "
            "of Integer). (2) Add two digit arrays (Add Strings / Add Binary). (3) Digits stored in a linked list, least significant "
            "first or most significant first (Add Two Numbers I/II)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1) extra, O(n) only when the array grows"},
        "similar": ["add-binary", "add-strings", "multiply-strings"],
    },
    {
        "id": "pow-x-n",
        "title": "Pow(x, n)",
        "difficulty": "Medium",
        "pattern": "Math & Bit Manipulation",
        "tags": ["Math", "Recursion", "Divide and Conquer"],
        "companies": {"google": 2, "apple": 1, "meta": 4, "amazon": 2, "microsoft": 1},
        "description": (
            "Implement `pow(x, n)`: raise a floating-point base `x` to an integer exponent `n`, where `n` may be negative. "
            "Do not call the language's built-in power function.\n\n"
            "Return the result as a float."
        ),
        "examples": [
            {"input": "x = 2.0, n = 10", "output": "1024.0"},
            {"input": "x = 2.1, n = 3", "output": "9.261"},
            {"input": "x = 2.0, n = -2", "output": "0.25", "explanation": "2^-2 = 1 / 2^2."},
        ],
        "constraints": ["-100.0 < x < 100.0", "-2^31 <= n <= 2^31 - 1", "n is an integer; x != 0 when n < 0", "-10^4 <= result <= 10^4"],
        "hints": [
            "Multiplying x by itself n times is O(n), far too slow for n near 2^31.",
            "x^n = (x^2)^(n/2) when n is even, and x * (x^2)^((n-1)/2) when n is odd. Each step halves the exponent.",
            "Iterate over the bits of n: keep a running square of x and multiply it into the result whenever the current bit is 1. Handle negative n by inverting x and negating n first.",
        ],
        "function": "myPow",
        "signature": "def myPow(self, x: float, n: int) -> float:",
        "arg_types": {"x": "float", "n": "int"},
        "return_type": "float",
        "compare": "float",
        "tests": [
            {"input": {"x": 2.0, "n": 10}, "output": 1024.0},
            {"input": {"x": 2.1, "n": 3}, "output": 9.261},
            {"input": {"x": 2.0, "n": -2}, "output": 0.25},
            {"input": {"x": 1.0, "n": 2147483647}, "output": 1.0},
            {"input": {"x": -1.0, "n": 2147483647}, "output": -1.0},
            {"input": {"x": 0.5, "n": 4}, "output": 0.0625},
            {"input": {"x": -2.0, "n": 3}, "output": -8.0},
            {"input": {"x": 3.0, "n": 0}, "output": 1.0},
            {"input": {"x": 2.0, "n": -2147483648}, "output": 0.0},
            {"input": {"x": 1.00001, "n": 123456}, "output": 1.00001 ** 123456},
            {"input": {"x": 0.9999999, "n": 2147483647}, "output": 0.9999999 ** 2147483647},
        ],
        "solution": (
            "class Solution:\n"
            "    def myPow(self, x: float, n: int) -> float:\n"
            "        if n < 0:\n"
            "            x, n = 1 / x, -n\n"
            "        result = 1.0\n"
            "        while n:\n"
            "            if n & 1:          # this bit of the exponent is set\n"
            "                result *= x\n"
            "            x *= x             # x^(2^k) for the next bit\n"
            "            n >>= 1\n"
            "        return result\n"
        ),
        "approach": (
            "**Key insight: exponentiation by squaring. Write `n` in binary; `x^n` is the product of `x^(2^k)` over the set bits `k`, and "
            "the successive powers `x, x^2, x^4, ...` come from repeated squaring.**\n\n"
            "Normalise a negative exponent first: `x^-n = (1/x)^n`. Then loop while `n > 0`: if the lowest bit is set multiply the "
            "accumulator by the current power, square the current power, shift `n` right. About 31 iterations for any 32-bit exponent.\n\n"
            "**Recursive form:** `pow(x, n) = pow(x*x, n//2)` if `n` is even, else `x * pow(x*x, n//2)`. Correct and `O(log n)`, but the "
            "naive `pow(x, n//2) * pow(x, n//2)` without caching the half result is `O(n)` again, a classic trap.\n\n"
            "**Why it is correct:** the loop maintains the invariant `answer = result * x^n` for the current `result`, `x` and `n`. "
            "When `n` becomes 0, `result` equals the original `x^n`.\n\n"
            "**Edge cases:** `n = 0` returns 1 for any `x`; `n = -2^31` cannot be negated in 32-bit two's complement (Python is fine, but "
            "say so); `x = 0` with negative `n` is undefined; `x = 1` or `x = -1` with huge `n` should still be fast.\n\n"
            "**Common mistakes:** the un-cached double recursion; forgetting negative exponents; off-by-one when handling odd `n`; "
            "accumulating floating-point error (unavoidable at ~1e-15 relative, acceptable here).\n\n"
            "**Interview follow-ups:** (1) Integer base with a modulus (modular exponentiation, the core of RSA and Fermat primality tests). "
            "(2) Matrix exponentiation for Fibonacci in `O(log n)`. (3) Fractional exponents (Newton's method or `exp(n * log x)`)."
        ),
        "complexity": {"time": "O(log n)", "space": "O(1)"},
        "similar": ["sqrt-x", "super-pow", "fibonacci-number"],
    },
    {
        "id": "multiply-strings",
        "title": "Multiply Strings",
        "difficulty": "Medium",
        "pattern": "Math & Bit Manipulation",
        "tags": ["String", "Math", "Simulation"],
        "companies": {"google": 2, "apple": 1, "meta": 3, "amazon": 2, "microsoft": 2},
        "description": (
            "Given two non-negative integers `num1` and `num2` represented as strings of decimal digits, return their product, also as "
            "a string.\n\n"
            "You may not convert the whole strings to integers with a built-in parser or use big-integer libraries; work with the digits."
        ),
        "examples": [
            {"input": "num1 = \"2\", num2 = \"3\"", "output": "\"6\""},
            {"input": "num1 = \"123\", num2 = \"456\"", "output": "\"56088\""},
            {"input": "num1 = \"0\", num2 = \"12345\"", "output": "\"0\"", "explanation": "No leading zeros in the result."},
        ],
        "constraints": ["1 <= num1.length, num2.length <= 200", "Digits only, no leading zeros except the number 0 itself."],
        "hints": [
            "Long multiplication: the digit at position i of num1 times the digit at position j of num2 contributes to position i + j of the result (counting from the least significant end).",
            "Allocate an integer array of length len(num1) + len(num2), accumulate every digit product into its slot, then do one pass to propagate carries.",
            "Strip leading zeros at the end, but keep a single 0 if the product is zero.",
        ],
        "function": "multiply",
        "signature": "def multiply(self, num1: str, num2: str) -> str:",
        "arg_types": {"num1": "str", "num2": "str"},
        "return_type": "str",
        "compare": "exact",
        "tests": [
            {"input": {"num1": "2", "num2": "3"}, "output": "6"},
            {"input": {"num1": "123", "num2": "456"}, "output": "56088"},
            {"input": {"num1": "0", "num2": "12345"}, "output": "0"},
            {"input": {"num1": "0", "num2": "0"}, "output": "0"},
            {"input": {"num1": "9", "num2": "9"}, "output": "81"},
            {"input": {"num1": "999", "num2": "999"}, "output": "998001"},
            {"input": {"num1": "1", "num2": "98765"}, "output": "98765"},
            {"input": {"num1": "9" * 200, "num2": "9" * 200}, "output": str((10 ** 200 - 1) ** 2)},
            {"input": {"num1": "7" * 150, "num2": "3" * 150}, "output": str(int("7" * 150) * int("3" * 150))},
            {"input": {"num1": "123456789" * 20, "num2": "987654321" * 20}, "output": str(int("123456789" * 20) * int("987654321" * 20))},
        ],
        "solution": (
            "class Solution:\n"
            "    def multiply(self, num1: str, num2: str) -> str:\n"
            "        if num1 == '0' or num2 == '0':\n"
            "            return '0'\n"
            "        m, n = len(num1), len(num2)\n"
            "        slots = [0] * (m + n)   # slots[k] accumulates the coefficient of 10^k\n"
            "        a = [ord(c) - 48 for c in reversed(num1)]   # least significant digit first\n"
            "        b = [ord(c) - 48 for c in reversed(num2)]\n"
            "        for i, da in enumerate(a):\n"
            "            if da == 0:\n"
            "                continue\n"
            "            for j, db in enumerate(b):\n"
            "                slots[i + j] += da * db\n"
            "        carry = 0\n"
            "        for k in range(m + n):\n"
            "            total = slots[k] + carry\n"
            "            slots[k] = total % 10\n"
            "            carry = total // 10\n"
            "        # drop leading zeros (slots is least significant first)\n"
            "        while len(slots) > 1 and slots[-1] == 0:\n"
            "            slots.pop()\n"
            "        return ''.join(str(d) for d in reversed(slots))\n"
        ),
        "approach": (
            "**Key insight: in long multiplication, the product of the digit at power `10^i` and the digit at power `10^j` lands at power "
            "`10^(i+j)`. Accumulate all of those partial products into an array indexed by power, then fix up carries in one pass.**\n\n"
            "Reverse both strings so index equals power of ten. For every pair `(i, j)` add `a[i] * b[j]` into `slots[i + j]`. The slots "
            "temporarily hold values larger than 9, which is fine in Python (in fixed-width languages the maximum is `81 * 200 + carry`, "
            "still tiny). Then sweep from the lowest power upward, keeping `total % 10` and carrying `total // 10`. Finally strip "
            "high-order zeros and reverse back into a string.\n\n"
            "**Why it is correct:** the product of the two numbers is the double sum of `a[i] * b[j] * 10^(i+j)`, which is exactly what the "
            "slot array represents before normalisation; the carry pass converts that representation to canonical base-10 digits without "
            "changing the value. The result has at most `m + n` digits, so the array never overflows.\n\n"
            "**Common mistakes:** doing carries inside the double loop (correct but fiddly and error-prone); forgetting the zero case and "
            "returning `\"000\"`; building the result with string concatenation from the front (quadratic); using `int(num1) * int(num2)`, "
            "which an interviewer will reject.\n\n"
            "**Interview follow-ups:** (1) Add two numeric strings (Add Strings, the carry pass alone). (2) Karatsuba multiplication for "
            "`O(n^1.585)`, and when it is worth it. (3) Negative numbers and a decimal point: strip the sign and the point, multiply, then "
            "reinsert."
        ),
        "complexity": {"time": "O(m * n)", "space": "O(m + n)"},
        "similar": ["add-strings", "plus-one", "add-binary"],
    },
    {
        "id": "single-number",
        "title": "Single Number",
        "difficulty": "Easy",
        "pattern": "Math & Bit Manipulation",
        "tags": ["Array", "Bit Manipulation"],
        "companies": {"google": 1, "apple": 2, "amazon": 2, "microsoft": 1},
        "description": (
            "Every element of the non-empty integer array `nums` appears **exactly twice**, except for one element that appears once. "
            "Find that element.\n\n"
            "Your solution should run in linear time and use only constant extra space."
        ),
        "examples": [
            {"input": "nums = [2,2,1]", "output": "1"},
            {"input": "nums = [4,1,2,1,2]", "output": "4"},
            {"input": "nums = [1]", "output": "1"},
        ],
        "constraints": ["1 <= nums.length <= 3 * 10^4", "-3 * 10^4 <= nums[i] <= 3 * 10^4", "Exactly one element appears once; all others appear twice."],
        "hints": [
            "A hash set works in O(n) space. The constant-space requirement is a hint toward bit tricks.",
            "What operation on two equal numbers gives zero, and on zero and x gives x? XOR.",
            "XOR is commutative and associative, so XOR-ing the whole array cancels every pair and leaves the lone element.",
        ],
        "function": "singleNumber",
        "signature": "def singleNumber(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [2, 2, 1]}, "output": 1},
            {"input": {"nums": [4, 1, 2, 1, 2]}, "output": 4},
            {"input": {"nums": [1]}, "output": 1},
            {"input": {"nums": [-1, -1, 7]}, "output": 7},
            {"input": {"nums": [0, 0, 5]}, "output": 5},
            {"input": {"nums": [3, -3, 3]}, "output": -3},
            {"input": {"nums": [x for i in range(1, 5001) for x in (i, i)] + [123456]}, "output": 123456},
            {"input": {"nums": [-30000] + [x for i in range(-4999, 5000) for x in (i, i)]}, "output": -30000},
        ],
        "solution": (
            "class Solution:\n"
            "    def singleNumber(self, nums: List[int]) -> int:\n"
            "        acc = 0\n"
            "        for x in nums:\n"
            "            acc ^= x\n"
            "        return acc\n"
        ),
        "approach": (
            "**Key insight: `a ^ a = 0` and `a ^ 0 = a`. Because XOR is commutative and associative, XOR-ing every element pairs up the "
            "duplicates (which cancel to 0) regardless of their positions, leaving only the unpaired value.**\n\n"
            "Fold the array with XOR starting from 0 and return the accumulator.\n\n"
            "**Why it is correct:** reorder the XOR so each duplicate pair is adjacent; each pair contributes 0, and `0 ^ ... ^ 0 ^ x = x`. "
            "Negative numbers are fine: XOR acts on the two's-complement bit pattern, and equal numbers have equal patterns.\n\n"
            "**Alternatives to mention:** a hash set (add if absent, remove if present; the survivor is the answer) in `O(n)` space; "
            "`2 * sum(set(nums)) - sum(nums)`, which also uses `O(n)` space and risks overflow elsewhere.\n\n"
            "**Common mistakes:** sorting first (`O(n log n)`); confusing XOR with OR; over-explaining the trick without stating the two "
            "identities that make it work.\n\n"
            "**Interview follow-ups:** (1) Every element appears three times except one (count bits per position mod 3, or the two-mask "
            "state machine). (2) Exactly two elements appear once (XOR everything, split by any set bit of the result, XOR the two groups). "
            "(3) Missing Number is the same trick XOR-ed against `0..n`."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["missing-number", "single-number-ii", "single-number-iii"],
    },
    {
        "id": "number-of-1-bits",
        "title": "Number of 1 Bits",
        "difficulty": "Easy",
        "pattern": "Math & Bit Manipulation",
        "tags": ["Bit Manipulation"],
        "companies": {"google": 1, "apple": 3, "amazon": 1, "microsoft": 2},
        "description": (
            "Given a non-negative integer `n` representing an unsigned 32-bit value, return the number of bits that are set to `1` in its "
            "binary representation. This quantity is also called the Hamming weight or population count.\n\n"
            "Do not rely on a built-in popcount; manipulate the bits yourself."
        ),
        "examples": [
            {"input": "n = 11", "output": "3", "explanation": "11 is 1011 in binary."},
            {"input": "n = 128", "output": "1", "explanation": "128 is 10000000."},
            {"input": "n = 4294967293", "output": "31", "explanation": "All 32 bits set except bit 1."},
        ],
        "constraints": ["0 <= n <= 2^32 - 1"],
        "hints": [
            "Check the lowest bit with n & 1, then shift right. Repeat up to 32 times.",
            "Faster: n & (n - 1) clears the lowest set bit. Count how many times you can do that before reaching zero. This loops once per set bit instead of once per bit.",
        ],
        "function": "hammingWeight",
        "signature": "def hammingWeight(self, n: int) -> int:",
        "arg_types": {"n": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"n": 11}, "output": 3},
            {"input": {"n": 128}, "output": 1},
            {"input": {"n": 4294967293}, "output": 31},
            {"input": {"n": 0}, "output": 0},
            {"input": {"n": 1}, "output": 1},
            {"input": {"n": 4294967295}, "output": 32},
            {"input": {"n": 2147483648}, "output": 1},
            {"input": {"n": 341}, "output": 5},
            {"input": {"n": 2863311530}, "output": 16},
        ],
        "solution": (
            "class Solution:\n"
            "    def hammingWeight(self, n: int) -> int:\n"
            "        count = 0\n"
            "        while n:\n"
            "            n &= n - 1   # drop the lowest set bit\n"
            "            count += 1\n"
            "        return count\n"
        ),
        "approach": (
            "**Key insight: `n & (n - 1)` removes exactly the lowest set bit of `n`. Repeating until `n` is zero therefore takes exactly "
            "as many iterations as there are set bits.**\n\n"
            "Why the identity holds: subtracting 1 flips the lowest set bit to 0 and every bit below it to 1; AND-ing with the original "
            "keeps all higher bits, zeroes the lowest set bit, and the bits below it were already 0.\n\n"
            "**Simpler version:** loop 32 times, add `n & 1`, shift right. Always 32 iterations; fine, but the Brian Kernighan trick above "
            "is what interviewers expect you to know.\n\n"
            "**Branch-free version (worth mentioning):** the SWAR popcount adds bit pairs, then nibbles, then bytes with masks "
            "`0x55555555`, `0x33333333`, `0x0F0F0F0F` and a final multiply; it is what `__builtin_popcount` compiles to without hardware support. "
            "Python's `int.bit_count()` does this natively.\n\n"
            "**Common mistakes:** in Java or C, treating the input as signed and using `>>` (arithmetic shift) on a negative value, which "
            "loops forever; use `>>>` or compare against 0 after the shift. Python has unbounded ints, so no issue, but say you know.\n\n"
            "**Interview follow-ups:** (1) Counting Bits: popcount of every number from 0 to `n` in `O(n)` total. (2) Hamming Distance "
            "between two numbers is popcount of their XOR. (3) Check whether `n` is a power of two: `n > 0 and n & (n - 1) == 0`."
        ),
        "complexity": {"time": "O(k) where k is the number of set bits, at most 32", "space": "O(1)"},
        "similar": ["counting-bits", "reverse-bits", "power-of-two"],
    },
    {
        "id": "counting-bits",
        "title": "Counting Bits",
        "difficulty": "Easy",
        "pattern": "Math & Bit Manipulation",
        "tags": ["Dynamic Programming", "Bit Manipulation"],
        "companies": {"google": 1, "apple": 1, "amazon": 1},
        "description": (
            "Given an integer `n`, return an array `ans` of length `n + 1` where `ans[i]` is the number of `1` bits in the binary "
            "representation of `i`, for every `i` from `0` to `n`.\n\n"
            "Aim for a single linear pass rather than counting the bits of each number independently."
        ),
        "examples": [
            {"input": "n = 2", "output": "[0,1,1]", "explanation": "0 -> 0, 1 -> 1, 10 -> 1."},
            {"input": "n = 5", "output": "[0,1,1,2,1,2]", "explanation": "0, 1, 10, 11, 100, 101."},
            {"input": "n = 0", "output": "[0]"},
        ],
        "constraints": ["0 <= n <= 10^5"],
        "hints": [
            "Calling a popcount on each number is O(n log n). Can the answer for i reuse an answer already computed?",
            "Shifting i right by one drops its lowest bit. So bits(i) = bits(i >> 1) + (i & 1).",
            "Equivalently bits(i) = bits(i & (i - 1)) + 1, since clearing the lowest set bit leaves a smaller number already in the table.",
        ],
        "function": "countBits",
        "signature": "def countBits(self, n: int) -> List[int]:",
        "arg_types": {"n": "int"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"n": 2}, "output": [0, 1, 1]},
            {"input": {"n": 5}, "output": [0, 1, 1, 2, 1, 2]},
            {"input": {"n": 0}, "output": [0]},
            {"input": {"n": 1}, "output": [0, 1]},
            {"input": {"n": 8}, "output": [0, 1, 1, 2, 1, 2, 2, 3, 1]},
            {"input": {"n": 15}, "output": [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4]},
            {"input": {"n": 20000}, "output": [bin(i).count("1") for i in range(20001)]},
        ],
        "solution": (
            "class Solution:\n"
            "    def countBits(self, n: int) -> List[int]:\n"
            "        bits = [0] * (n + 1)\n"
            "        for i in range(1, n + 1):\n"
            "            bits[i] = bits[i >> 1] + (i & 1)\n"
            "        return bits\n"
        ),
        "approach": (
            "**Key insight: the binary representation of `i` is the representation of `i >> 1` with one extra bit appended, so "
            "`bits[i] = bits[i >> 1] + (i & 1)`. Each entry is derived in O(1) from a smaller index already filled in.**\n\n"
            "Allocate `bits[0..n]` with `bits[0] = 0` and fill left to right with that recurrence.\n\n"
            "**Equivalent recurrences:** `bits[i] = bits[i & (i - 1)] + 1` (clear the lowest set bit, which gives a strictly smaller "
            "number), or `bits[i] = bits[i - highest_power_of_two_at_or_below_i] + 1` (the offset form, which resets at each power of two). "
            "All three are O(1) per element; the shift form is the easiest to explain.\n\n"
            "**Why it is correct:** by induction on `i`: `i >> 1 < i` for `i >= 1`, so the referenced entry is already correct, and "
            "appending the bit `i & 1` adds exactly that many set bits.\n\n"
            "**Common mistakes:** calling popcount per element (`O(n log n)`, acceptable but not the point); using `i / 2` with float "
            "division in Python; off-by-one on the array length (`n + 1` entries).\n\n"
            "**Interview follow-ups:** (1) Number of 1 Bits for a single value (Kernighan's trick). (2) Total number of set bits in "
            "`0..n` without the array (count contribution per bit position in `O(log n)`). (3) Same idea for counting trailing zeros or "
            "parity of each number."
        ),
        "complexity": {"time": "O(n)", "space": "O(n) for the output"},
        "similar": ["number-of-1-bits", "single-number", "power-of-two"],
    },
    {
        "id": "reverse-bits",
        "title": "Reverse Bits",
        "difficulty": "Easy",
        "pattern": "Math & Bit Manipulation",
        "tags": ["Bit Manipulation", "Divide and Conquer"],
        "companies": {"google": 1, "apple": 3, "amazon": 1},
        "description": (
            "Given a non-negative integer `n` representing a **32-bit unsigned** value, reverse the order of its 32 bits so that bit 0 "
            "becomes bit 31, bit 1 becomes bit 30, and so on.\n\n"
            "Return the resulting unsigned integer."
        ),
        "examples": [
            {"input": "n = 43261596", "output": "964176192",
             "explanation": "00000010100101000001111010011100 reversed is 00111001011110000010100101000000."},
            {"input": "n = 4294967293", "output": "3221225471",
             "explanation": "11111111111111111111111111111101 reversed is 10111111111111111111111111111111."},
            {"input": "n = 1", "output": "2147483648", "explanation": "The lowest bit moves to the highest position."},
        ],
        "constraints": ["0 <= n <= 2^32 - 1"],
        "hints": [
            "Peel bits off the right of n one at a time and push them onto the right of the result; after 32 iterations the order is reversed.",
            "Remember to run exactly 32 iterations even after n becomes zero, so leading zeros become trailing zeros in the result.",
            "For many calls, reverse bytes with a 256-entry lookup table, or use the divide-and-conquer mask swaps (swap halves, then 8-bit groups, then 4, 2, 1).",
        ],
        "function": "reverseBits",
        "signature": "def reverseBits(self, n: int) -> int:",
        "arg_types": {"n": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"n": 43261596}, "output": 964176192},
            {"input": {"n": 4294967293}, "output": 3221225471},
            {"input": {"n": 1}, "output": 2147483648},
            {"input": {"n": 0}, "output": 0},
            {"input": {"n": 4294967295}, "output": 4294967295},
            {"input": {"n": 2147483648}, "output": 1},
            {"input": {"n": 2863311530}, "output": 1431655765},
            {"input": {"n": 255}, "output": 4278190080},
        ],
        "solution": (
            "class Solution:\n"
            "    def reverseBits(self, n: int) -> int:\n"
            "        result = 0\n"
            "        for _ in range(32):\n"
            "            result = (result << 1) | (n & 1)\n"
            "            n >>= 1\n"
            "        return result\n"
        ),
        "approach": (
            "**Key insight: reading bits off the low end of `n` and appending them to the low end of `result` reverses their order, "
            "exactly like reversing a string by pushing characters onto a stack.**\n\n"
            "Loop 32 times: shift `result` left, OR in `n & 1`, shift `n` right. The fixed iteration count is essential so that high-order "
            "zeros of `n` become low-order zeros of the result.\n\n"
            "**Why it is correct:** after `k` iterations, `result` holds the lowest `k` bits of the original `n` in reversed order. "
            "After 32, it holds all of them.\n\n"
            "**Faster alternatives (follow-up material):** (a) byte-wise lookup: reverse each of the four bytes via a 256-entry table and "
            "place them in swapped positions; (b) divide and conquer with masks: swap the two 16-bit halves, then swap adjacent 8-bit groups "
            "(`0x00FF00FF`), 4-bit (`0x0F0F0F0F`), 2-bit (`0x33333333`) and 1-bit (`0x55555555`) groups, five steps total, no loop.\n\n"
            "**Common mistakes:** stopping when `n` becomes zero (loses the leading zeros); in Java, treating the value as signed and using "
            "`>>` instead of `>>>`; in Python, forgetting that ints are unbounded so you must mask or rely on the 32-step loop to keep the "
            "result within 32 bits.\n\n"
            "**Interview follow-ups:** (1) Optimise for being called millions of times (table or mask method, memoise bytes). "
            "(2) Reverse only the lowest `k` bits. (3) Number of 1 Bits and Counting Bits exercise the same bit-by-bit habits."
        ),
        "complexity": {"time": "O(1) (32 iterations)", "space": "O(1)"},
        "similar": ["number-of-1-bits", "counting-bits", "reverse-integer"],
    },
    {
        "id": "missing-number",
        "title": "Missing Number",
        "difficulty": "Easy",
        "pattern": "Math & Bit Manipulation",
        "tags": ["Array", "Math", "Bit Manipulation"],
        "companies": {"google": 1, "apple": 2, "amazon": 2, "microsoft": 2},
        "description": (
            "The array `nums` contains `n` **distinct** integers drawn from the range `[0, n]`. Since the range has `n + 1` values, exactly "
            "one of them is absent.\n\n"
            "Return the missing value. A solution with linear time and constant extra space is expected."
        ),
        "examples": [
            {"input": "nums = [3,0,1]", "output": "2", "explanation": "n = 3; the range is 0..3 and 2 is absent."},
            {"input": "nums = [0,1]", "output": "2", "explanation": "n = 2; the largest value 2 is the one missing."},
            {"input": "nums = [9,6,4,2,3,5,7,0,1]", "output": "8"},
        ],
        "constraints": ["1 <= n <= 10^4", "0 <= nums[i] <= n", "All values in nums are distinct."],
        "hints": [
            "Sorting or a hash set works but costs O(n log n) time or O(n) space.",
            "The sum of 0..n is n(n+1)/2. Subtract the array's sum.",
            "To avoid any overflow concerns, XOR every index 0..n with every value: the pairs cancel and the missing number remains.",
        ],
        "function": "missingNumber",
        "signature": "def missingNumber(self, nums: List[int]) -> int:",
        "arg_types": {"nums": "List[int]"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"nums": [3, 0, 1]}, "output": 2},
            {"input": {"nums": [0, 1]}, "output": 2},
            {"input": {"nums": [9, 6, 4, 2, 3, 5, 7, 0, 1]}, "output": 8},
            {"input": {"nums": [0]}, "output": 1},
            {"input": {"nums": [1]}, "output": 0},
            {"input": {"nums": [1, 2]}, "output": 0},
            {"input": {"nums": [i for i in range(10001) if i != 4321]}, "output": 4321},
            {"input": {"nums": list(range(10000))}, "output": 10000},
            {"input": {"nums": list(range(1, 10001))}, "output": 0},
        ],
        "solution": (
            "class Solution:\n"
            "    def missingNumber(self, nums: List[int]) -> int:\n"
            "        acc = len(nums)            # start with the index n, which the loop below never visits\n"
            "        for i, x in enumerate(nums):\n"
            "            acc ^= i ^ x\n"
            "        return acc\n"
        ),
        "approach": (
            "**Key insight: XOR-ing all indices `0..n` together with all values `nums[i]` cancels every number that appears in both sets, "
            "leaving only the one that appears as an index but not as a value: the missing number.**\n\n"
            "Initialise the accumulator to `n` (the one index the loop does not produce), then for each position XOR in both `i` and "
            "`nums[i]`. Because XOR is associative and commutative and `a ^ a = 0`, the result is the single unpaired value.\n\n"
            "**Arithmetic alternative:** `n(n+1)/2 - sum(nums)`. Equally valid and often what people say first. In Python there is no "
            "overflow; in a 32-bit language the sum stays within range for `n <= 10^4` but it is worth noting the XOR version never grows.\n\n"
            "**Cyclic-sort alternative:** place each value at its own index by swapping, then the first index whose value does not match is "
            "the answer (`O(n)` time, in-place, generalises to Find All Numbers Disappeared in an Array).\n\n"
            "**Common mistakes:** forgetting that `n` itself may be the missing number (the sum/XOR versions handle it automatically, "
            "a hash-set check against `range(n)` does not); sorting and binary searching, which is correct but `O(n log n)`.\n\n"
            "**Interview follow-ups:** (1) Two numbers missing (sum and sum of squares, or XOR with bit partitioning). (2) One number "
            "missing and one duplicated (Set Mismatch). (3) The array is a read-only stream too large for memory: the running sum or XOR "
            "still works in one pass."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["single-number", "find-the-duplicate-number", "first-missing-positive"],
    },
    {
        "id": "sum-of-two-integers",
        "title": "Sum of Two Integers",
        "difficulty": "Medium",
        "pattern": "Math & Bit Manipulation",
        "tags": ["Math", "Bit Manipulation"],
        "companies": {"apple": 1, "meta": 1, "amazon": 1},
        "description": (
            "Compute `a + b` for two integers **without using the `+` or `-` operators** anywhere in your code. Both inputs may be "
            "negative and lie within the 32-bit signed range.\n\n"
            "Return the sum as a normal (possibly negative) integer."
        ),
        "examples": [
            {"input": "a = 1, b = 2", "output": "3"},
            {"input": "a = -2, b = -3", "output": "-5"},
            {"input": "a = -1, b = 1", "output": "0"},
        ],
        "constraints": ["-1000 <= a, b <= 1000"],
        "hints": [
            "Adding two bits without carry is XOR. The carry out of each position is AND, shifted left by one.",
            "Repeat: sum_without_carry = a ^ b, carry = (a & b) << 1; set a, b to those and loop until the carry is zero.",
            "Python integers have no fixed width, so a negative carry never reaches zero. Mask every intermediate value with 0xFFFFFFFF to simulate 32 bits, then convert the final result back to a signed value if its top bit is set.",
        ],
        "function": "getSum",
        "signature": "def getSum(self, a: int, b: int) -> int:",
        "arg_types": {"a": "int", "b": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"a": 1, "b": 2}, "output": 3},
            {"input": {"a": -2, "b": -3}, "output": -5},
            {"input": {"a": -1, "b": 1}, "output": 0},
            {"input": {"a": 0, "b": 0}, "output": 0},
            {"input": {"a": 1000, "b": -1}, "output": 999},
            {"input": {"a": -1000, "b": 1}, "output": -999},
            {"input": {"a": 1000, "b": 1000}, "output": 2000},
            {"input": {"a": -1000, "b": -1000}, "output": -2000},
            {"input": {"a": 7, "b": -9}, "output": -2},
            {"input": {"a": 999, "b": -1000}, "output": -1},
            {"input": {"a": 2147483647, "b": -2147483648}, "output": -1},
        ],
        "solution": (
            "class Solution:\n"
            "    def getSum(self, a: int, b: int) -> int:\n"
            "        MASK = 0xFFFFFFFF          # keep values to 32 bits\n"
            "        MAX_INT = 0x7FFFFFFF       # largest positive 32-bit value\n"
            "        a &= MASK\n"
            "        b &= MASK\n"
            "        while b:\n"
            "            carry = (a & b) << 1\n"
            "            a = (a ^ b) & MASK     # bitwise sum without carry\n"
            "            b = carry & MASK       # carry becomes the new addend\n"
            "        # a is now an unsigned 32-bit pattern; reinterpret as signed\n"
            "        return a if a <= MAX_INT else ~(a ^ MASK)\n"
        ),
        "approach": (
            "**Key insight: a full adder is XOR for the sum bit and AND for the carry bit. Adding two numbers is repeatedly combining "
            "`a ^ b` (the digits) with `(a & b) << 1` (the carries) until no carry remains.**\n\n"
            "Loop: `carry = (a & b) << 1`, `a = a ^ b`, `b = carry`. Each round pushes the carries one position left, so after at most 32 "
            "rounds (the word width) the carry is zero and `a` is the sum.\n\n"
            "**The Python wrinkle:** Python ints are unbounded, so for negative operands the carry's sign bits propagate forever and "
            "the loop never ends. Mask `a`, `b` and `carry` with `0xFFFFFFFF` to emulate a 32-bit register. At the end `a` is an unsigned "
            "bit pattern; if it exceeds `0x7FFFFFFF` it represents a negative number, which we recover with `~(a ^ MASK)` (flip the bits "
            "within 32 positions, then apply bitwise NOT, which is `-x - 1` without writing a minus sign).\n\n"
            "**Why it is correct:** in two's complement, addition is the same bit operation for signed and unsigned values; only the "
            "interpretation of the top bit differs. So computing the unsigned 32-bit sum and reinterpreting it is exactly what hardware "
            "does.\n\n"
            "**Common mistakes:** forgetting to mask the carry (infinite loop on negatives); converting with `a - 2**32`, which uses the "
            "forbidden minus; swapping the roles of `a` and `b` in the loop and losing the carry; stopping after one round instead of "
            "iterating until the carry is zero.\n\n"
            "**Interview follow-ups:** (1) Subtraction: `a + (~b + 1)`, with the same adder. (2) Multiplication with only shifts and adds "
            "(Russian peasant). (3) Why the loop is bounded by the word width (each round the lowest set carry bit moves strictly left)."
        ),
        "complexity": {"time": "O(1) (at most 32 iterations)", "space": "O(1)"},
        "similar": ["add-binary", "number-of-1-bits", "divide-two-integers"],
    },
    {
        "id": "reverse-integer",
        "title": "Reverse Integer",
        "difficulty": "Medium",
        "pattern": "Math & Bit Manipulation",
        "tags": ["Math"],
        "companies": {"google": 2, "apple": 3, "meta": 1, "amazon": 3, "microsoft": 3},
        "description": (
            "Given a signed 32-bit integer `x`, reverse its decimal digits and return the result. The sign stays with the number.\n\n"
            "If the reversed value does not fit in a signed 32-bit integer (`[-2^31, 2^31 - 1]`), return `0`. Assume you may **not** use "
            "64-bit integers to detect the overflow; check before each multiply-and-add."
        ),
        "examples": [
            {"input": "x = 123", "output": "321"},
            {"input": "x = -123", "output": "-321"},
            {"input": "x = 120", "output": "21", "explanation": "Leading zeros disappear."},
        ],
        "constraints": ["-2^31 <= x <= 2^31 - 1"],
        "hints": [
            "Peel digits off with x % 10 and x // 10, building the result as result * 10 + digit. Work on the absolute value and reapply the sign.",
            "Before computing result * 10 + digit, check whether it would exceed 2^31 - 1: result > 214748364, or result == 214748364 and digit > 7 (digit > 8 for the negative side).",
            "In Python you can simply compare the final value against the bounds, but be ready to explain the pre-check an interviewer expects in C++ or Java.",
        ],
        "function": "reverse",
        "signature": "def reverse(self, x: int) -> int:",
        "arg_types": {"x": "int"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"x": 123}, "output": 321},
            {"input": {"x": -123}, "output": -321},
            {"input": {"x": 120}, "output": 21},
            {"input": {"x": 0}, "output": 0},
            {"input": {"x": 1534236469}, "output": 0},
            {"input": {"x": -2147483648}, "output": 0},
            {"input": {"x": 2147483647}, "output": 0},
            {"input": {"x": 1463847412}, "output": 2147483641},
            {"input": {"x": -1463847412}, "output": -2147483641},
            {"input": {"x": -2147483412}, "output": -2143847412},
            {"input": {"x": 1000000003}, "output": 0},
            {"input": {"x": 1000000000}, "output": 1},
        ],
        "solution": (
            "class Solution:\n"
            "    def reverse(self, x: int) -> int:\n"
            "        INT_MAX = 2**31 - 1\n"
            "        sign = -1 if x < 0 else 1\n"
            "        x = abs(x)\n"
            "        rev = 0\n"
            "        while x:\n"
            "            x, digit = divmod(x, 10)\n"
            "            # would rev * 10 + digit overflow? check before doing it\n"
            "            if rev > INT_MAX // 10 or (rev == INT_MAX // 10 and digit > 7 + (sign < 0)):\n"
            "                return 0\n"
            "            rev = rev * 10 + digit\n"
            "        return sign * rev\n"
        ),
        "approach": (
            "**Key insight: build the reversed number one digit at a time with `rev = rev * 10 + digit`, and detect overflow *before* "
            "performing that step by comparing `rev` with `INT_MAX // 10`.**\n\n"
            "Strip the sign and work on `|x|`. Each iteration takes the last digit with `divmod(x, 10)`. Before appending it, overflow "
            "happens if `rev > 214748364`, or if `rev == 214748364` and the digit would push past the last digit of the limit: `7` for "
            "positive results (`2147483647`), `8` for negative ones (`-2147483648`). Finally reapply the sign.\n\n"
            "**Why the pre-check suffices:** if `rev < 214748364`, then `rev * 10 + 9 <= 2147483639`, safely in range. If `rev > 214748364`, "
            "then `rev * 10 >= 2147483650`, already out of range. Only the boundary value needs the digit comparison. In fact, when "
            "`rev == 214748364` the input had 10 digits and started with 1 or 2, so the final digit is at most 2 and the equality branch "
            "never fires for valid 32-bit inputs; keeping it makes the reasoning complete.\n\n"
            "**Python note:** unbounded ints mean `int(str(abs(x))[::-1])` plus a range check also works. Interviewers at Apple and "
            "Microsoft usually ask for the arithmetic version and the overflow argument, because that is the point of the question.\n\n"
            "**Common mistakes:** checking the range after the multiplication (undefined behaviour in C++, silent wraparound in Java); "
            "forgetting that `-2^31` cannot be negated in 32 bits (handle the sign separately); mishandling trailing zeros (they vanish "
            "naturally with the arithmetic approach).\n\n"
            "**Interview follow-ups:** (1) String to Integer (atoi) uses the same pre-multiplication overflow check. (2) Palindrome Number: "
            "reverse only half the digits. (3) Reverse the bits instead of the decimal digits (Reverse Bits)."
        ),
        "complexity": {"time": "O(log10 x)", "space": "O(1)"},
        "similar": ["string-to-integer-atoi", "palindrome-number", "reverse-bits"],
    },
]
