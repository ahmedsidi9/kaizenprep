"""Strings pattern: parsing, formatting and classic string-manipulation problems."""

PROBLEMS = [
    {
        "id": "longest-common-prefix",
        "title": "Longest Common Prefix",
        "difficulty": "Easy",
        "pattern": "Strings",
        "tags": ["String", "Trie"],
        "companies": {"google": 2, "apple": 3, "meta": 1, "amazon": 3, "microsoft": 3},
        "description": (
            "Given a list of strings `strs`, return the longest string that every element starts with. "
            "If the strings share no leading characters, return the empty string `\"\"`."
        ),
        "examples": [
            {"input": "strs = [\"flower\",\"flow\",\"flight\"]", "output": "\"fl\"", "explanation": "All three begin with fl; the third letter differs (o vs i)."},
            {"input": "strs = [\"dog\",\"racecar\",\"car\"]", "output": "\"\"", "explanation": "The first letters already differ."},
            {"input": "strs = [\"abc\",\"ab\",\"\"]", "output": "\"\"", "explanation": "An empty string is a member, so the common prefix is empty."},
        ],
        "constraints": ["1 <= strs.length <= 200", "0 <= strs[i].length <= 200", "strs[i] consists of lowercase English letters"],
        "hints": [
            "The answer can never be longer than the shortest string.",
            "Compare column by column: look at character 0 of every string, then character 1, and stop at the first column that is not uniform.",
            "Python's zip(*strs) yields exactly those columns and stops at the shortest string for free.",
        ],
        "function": "longestCommonPrefix",
        "signature": "def longestCommonPrefix(self, strs: List[str]) -> str:",
        "arg_types": {"strs": "List[str]"},
        "return_type": "str",
        "compare": "exact",
        "tests": [
            {"input": {"strs": ["flower", "flow", "flight"]}, "output": "fl"},
            {"input": {"strs": ["dog", "racecar", "car"]}, "output": ""},
            {"input": {"strs": ["abc", "ab", ""]}, "output": ""},
            {"input": {"strs": ["alone"]}, "output": "alone"},
            {"input": {"strs": ["same", "same", "same"]}, "output": "same"},
            {"input": {"strs": ["interview", "internet", "interval", "intern"]}, "output": "inter"},
            {"input": {"strs": ["ab", "a"]}, "output": "a"},
            {"input": {"strs": ["prefix" + str(i) for i in range(2000)]}, "output": "prefix"},
            {"input": {"strs": ["a" * 1000 + str(i) for i in range(1000)]}, "output": "a" * 1000},
        ],
        "solution": (
            "class Solution:\n"
            "    def longestCommonPrefix(self, strs: List[str]) -> str:\n"
            "        for i, column in enumerate(zip(*strs)):\n"
            "            if len(set(column)) > 1:\n"
            "                return strs[0][:i]\n"
            "        return min(strs, key=len)\n"
        ),
        "approach": (
            "**Key insight: scan vertically.** Look at position 0 of every string, then position 1, and so on. The first "
            "position where the strings disagree, or where the shortest string runs out, ends the prefix. `zip(*strs)` "
            "produces exactly these columns and stops at the shortest string, so if no column disagrees the whole shortest "
            "string is the answer.\n\n"
            "The horizontal alternative (take `strs[0]`, shrink it until every string starts with it) is also O(S) where S is "
            "the total number of characters, but vertical scanning exits early on inputs like `[\"a\"*1000, \"b\"*1000]`.\n\n"
            "**Common mistakes:** indexing past the end of a short string; returning `strs[0]` when the list has one element "
            "without handling the general case; sorting and comparing only first and last string (works, but O(n log n) and "
            "harder to justify).\n\n"
            "**Interview follow-ups:** Many queries against a fixed dictionary? Build a trie; the common prefix of the whole set is "
            "the path from the root while each node has exactly one child and is not a word end. Longest common prefix of two "
            "arbitrary strings among the set (pairwise LCP queries)? Sort the strings; the LCP of any two is the minimum LCP of "
            "adjacent pairs between them, answerable with a sparse table. Divide and conquer is a natural parallel version."
        ),
        "complexity": {"time": "O(S) where S is the total number of characters", "space": "O(1) extra (O(n) for one column)"},
        "similar": ["implement-trie-prefix-tree", "find-the-index-of-the-first-occurrence"],
    },
    {
        "id": "string-to-integer-atoi",
        "title": "String to Integer (atoi)",
        "difficulty": "Medium",
        "pattern": "Strings",
        "tags": ["String"],
        "companies": {"google": 2, "apple": 4, "meta": 3, "amazon": 3, "microsoft": 4},
        "description": (
            "Convert a string to a 32-bit signed integer the way C's `atoi` does:\n\n"
            "1. Skip any leading spaces.\n"
            "2. Read an optional `+` or `-`.\n"
            "3. Read consecutive digits until a non-digit or the end of the string. Leading zeros are fine.\n"
            "4. Anything after the digits is ignored. If no digits were read, the result is `0`.\n"
            "5. Clamp the result to the range `[-2^31, 2^31 - 1]`.\n\n"
            "Only the space character counts as whitespace; a sign must be immediately followed by digits to count."
        ),
        "examples": [
            {"input": "s = \"42\"", "output": "42"},
            {"input": "s = \"   -042\"", "output": "-42", "explanation": "Leading spaces and zeros are skipped, the sign is kept."},
            {"input": "s = \"1337c0d3\"", "output": "1337", "explanation": "Parsing stops at the first non-digit."},
            {"input": "s = \"0-1\"", "output": "0", "explanation": "The digit 0 is read, then parsing stops at the minus sign."},
            {"input": "s = \"words and 987\"", "output": "0", "explanation": "The first non-space character is a letter, so no digits are read."},
        ],
        "constraints": ["0 <= s.length <= 200", "s consists of letters, digits, spaces, '+', '-' and '.'"],
        "hints": [
            "Walk the string with an index and handle the three phases in order: spaces, sign, digits.",
            "Accumulate with `num = num * 10 + digit`. In Python the integer cannot overflow, so clamp once at the end; in other languages check before each multiply.",
            "Watch the corner cases: empty string, only spaces, a bare sign, two signs in a row, and a space between sign and digits.",
        ],
        "function": "myAtoi",
        "signature": "def myAtoi(self, s: str) -> int:",
        "arg_types": {"s": "str"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"s": "42"}, "output": 42},
            {"input": {"s": "   -042"}, "output": -42},
            {"input": {"s": "1337c0d3"}, "output": 1337},
            {"input": {"s": "0-1"}, "output": 0},
            {"input": {"s": "words and 987"}, "output": 0},
            {"input": {"s": ""}, "output": 0},
            {"input": {"s": "   "}, "output": 0},
            {"input": {"s": "-"}, "output": 0},
            {"input": {"s": "+1"}, "output": 1},
            {"input": {"s": "+-12"}, "output": 0},
            {"input": {"s": "  +0 123"}, "output": 0},
            {"input": {"s": "- 5"}, "output": 0},
            {"input": {"s": "3.14159"}, "output": 3},
            {"input": {"s": "2147483647"}, "output": 2147483647},
            {"input": {"s": "2147483648"}, "output": 2147483647},
            {"input": {"s": "-2147483648"}, "output": -2147483648},
            {"input": {"s": "-2147483649"}, "output": -2147483648},
            {"input": {"s": "91283472332"}, "output": 2147483647},
            {"input": {"s": "-91283472332"}, "output": -2147483648},
            {"input": {"s": "00000-42a1234"}, "output": 0},
            {"input": {"s": "9" * 3000}, "output": 2147483647},
            {"input": {"s": "-" + "9" * 3000}, "output": -2147483648},
        ],
        "solution": (
            "class Solution:\n"
            "    def myAtoi(self, s: str) -> int:\n"
            "        INT_MAX, INT_MIN = 2**31 - 1, -2**31\n"
            "        i, n = 0, len(s)\n"
            "        while i < n and s[i] == ' ':\n"
            "            i += 1\n"
            "        sign = 1\n"
            "        if i < n and s[i] in '+-':\n"
            "            sign = -1 if s[i] == '-' else 1\n"
            "            i += 1\n"
            "        num = 0\n"
            "        while i < n and s[i].isdigit():\n"
            "            num = num * 10 + (ord(s[i]) - ord('0'))\n"
            "            if num > INT_MAX + 1:      # already beyond either bound; stop early\n"
            "                break\n"
            "            i += 1\n"
            "        return max(INT_MIN, min(INT_MAX, sign * num))\n"
        ),
        "approach": (
            "**Key insight: this is a tiny state machine, so write it as three sequential loops rather than one clever "
            "regex.** Skip spaces, consume at most one sign, then consume digits while accumulating `num = num*10 + d`. "
            "Everything else is ignored. Finally apply the sign and clamp to the 32-bit range.\n\n"
            "Python integers never overflow, so clamping once at the end is correct. The early `break` once `num` exceeds "
            "`2^31` is what keeps the loop O(1) on absurd inputs and mirrors what you must do in C++/Java, where you check "
            "`num > (INT_MAX - d) / 10` *before* multiplying. Interviewers care about that check more than anything else here.\n\n"
            "**Common mistakes:** accepting `+-12` or `- 5` (a sign must be followed directly by digits); treating tabs or "
            "newlines as skippable whitespace (only spaces are); returning `INT_MIN` for `-2147483648` but overflowing for "
            "`-2147483649`; using `int()` with a try/except, which accepts things like `\"1_000\"` and `\"  12  \"` and fails on "
            "`\"12abc\"`, so it does not match the spec.\n\n"
            "**Interview follow-ups:** Parse floats including exponents (`valid-number`, a bigger state machine). Parse different "
            "bases or digit separators. Unicode digits: `str.isdigit()` is true for characters like superscript two, so a strict "
            "parser should test `'0' <= c <= '9'`. Also discuss error reporting: real `strtol` returns how far it parsed and sets "
            "`errno` on overflow instead of silently clamping."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["reverse-integer", "valid-number", "compare-version-numbers"],
    },
    {
        "id": "roman-to-integer",
        "title": "Roman to Integer",
        "difficulty": "Easy",
        "pattern": "Strings",
        "tags": ["Hash Table", "Math", "String"],
        "companies": {"google": 2, "apple": 3, "meta": 2, "amazon": 3, "microsoft": 3},
        "description": (
            "Roman numerals use seven symbols: `I`=1, `V`=5, `X`=10, `L`=50, `C`=100, `D`=500, `M`=1000. "
            "Symbols are normally written from largest to smallest and added together, but six subtractive pairs exist: "
            "`IV`=4, `IX`=9, `XL`=40, `XC`=90, `CD`=400, `CM`=900, where a smaller symbol placed before a larger one is subtracted.\n\n"
            "Given a valid Roman numeral `s`, return its integer value."
        ),
        "examples": [
            {"input": "s = \"III\"", "output": "3"},
            {"input": "s = \"LVIII\"", "output": "58", "explanation": "L = 50, V = 5, III = 3."},
            {"input": "s = \"MCMXCIV\"", "output": "1994", "explanation": "M = 1000, CM = 900, XC = 90, IV = 4."},
        ],
        "constraints": ["1 <= s.length <= 15", "s contains only the characters I, V, X, L, C, D, M", "s is a valid Roman numeral in the range [1, 3999]"],
        "hints": [
            "Map each symbol to its value and sum them. Where does that go wrong?",
            "A symbol is subtracted exactly when the symbol to its right is larger. Compare each value with its right neighbour.",
            "Scanning right to left, keep the previous value: add the current value if it is >= previous, subtract otherwise.",
        ],
        "function": "romanToInt",
        "signature": "def romanToInt(self, s: str) -> int:",
        "arg_types": {"s": "str"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"s": "III"}, "output": 3},
            {"input": {"s": "LVIII"}, "output": 58},
            {"input": {"s": "MCMXCIV"}, "output": 1994},
            {"input": {"s": "I"}, "output": 1},
            {"input": {"s": "IV"}, "output": 4},
            {"input": {"s": "IX"}, "output": 9},
            {"input": {"s": "XL"}, "output": 40},
            {"input": {"s": "XC"}, "output": 90},
            {"input": {"s": "CDXLIV"}, "output": 444},
            {"input": {"s": "DCCCXC"}, "output": 890},
            {"input": {"s": "MMXXIV"}, "output": 2024},
            {"input": {"s": "MMMCMXCIX"}, "output": 3999},
        ],
        "solution": (
            "class Solution:\n"
            "    def romanToInt(self, s: str) -> int:\n"
            "        value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}\n"
            "        total = 0\n"
            "        for i, ch in enumerate(s):\n"
            "            v = value[ch]\n"
            "            if i + 1 < len(s) and v < value[s[i + 1]]:\n"
            "                total -= v\n"
            "            else:\n"
            "                total += v\n"
            "        return total\n"
        ),
        "approach": (
            "**Key insight: a symbol is subtracted if and only if a bigger symbol follows it.** That single rule covers all six "
            "subtractive pairs, so you never need to special-case `IV`, `IX`, and so on. Walk the string once, look at the "
            "right neighbour, and add or subtract.\n\n"
            "An equivalent formulation scans right to left and tracks the previous (right-hand) value: add when the current "
            "value is at least the previous, subtract when it is smaller. Both are O(n) with a 7-entry table.\n\n"
            "**Common mistakes:** hard-coding the two-character pairs and then skipping an index incorrectly; using a list of pairs "
            "sorted by length and doing repeated `startswith`, which is correct but noisy; forgetting the last character has no "
            "right neighbour.\n\n"
            "**Interview follow-ups:** Validate the numeral as well as parse it (no more than three repeats of I/X/C/M, V/L/D never "
            "repeated, only the six legal subtractive pairs). Write the inverse (`integer-to-roman`). Extend to numbers above 3999 "
            "using the overline notation (multiply by 1000), which breaks the fixed symbol table."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["integer-to-roman", "string-to-integer-atoi"],
    },
    {
        "id": "integer-to-roman",
        "title": "Integer to Roman",
        "difficulty": "Medium",
        "pattern": "Strings",
        "tags": ["Hash Table", "Math", "String"],
        "companies": {"google": 2, "apple": 2, "meta": 2, "amazon": 3, "microsoft": 2},
        "description": (
            "Convert an integer `num` between 1 and 3999 into its Roman numeral.\n\n"
            "Roman numerals use `I`=1, `V`=5, `X`=10, `L`=50, `C`=100, `D`=500, `M`=1000, written largest to smallest, "
            "except that 4, 9, 40, 90, 400 and 900 are written with a subtractive pair (`IV`, `IX`, `XL`, `XC`, `CD`, `CM`) "
            "rather than four repeated symbols. No symbol other than `M` appears more than three times in a row."
        ),
        "examples": [
            {"input": "num = 3", "output": "\"III\""},
            {"input": "num = 58", "output": "\"LVIII\"", "explanation": "50 + 5 + 1 + 1 + 1."},
            {"input": "num = 1994", "output": "\"MCMXCIV\"", "explanation": "1000 + 900 + 90 + 4."},
        ],
        "constraints": ["1 <= num <= 3999"],
        "hints": [
            "This is greedy change-making with a fixed coin set that happens to be canonical.",
            "Treat the six subtractive pairs as extra denominations: 1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1.",
            "Repeatedly take the largest denomination that fits, append its symbol, subtract, and move on when it no longer fits.",
        ],
        "function": "intToRoman",
        "signature": "def intToRoman(self, num: int) -> str:",
        "arg_types": {"num": "int"},
        "return_type": "str",
        "compare": "exact",
        "tests": [
            {"input": {"num": 3}, "output": "III"},
            {"input": {"num": 58}, "output": "LVIII"},
            {"input": {"num": 1994}, "output": "MCMXCIV"},
            {"input": {"num": 1}, "output": "I"},
            {"input": {"num": 4}, "output": "IV"},
            {"input": {"num": 9}, "output": "IX"},
            {"input": {"num": 90}, "output": "XC"},
            {"input": {"num": 444}, "output": "CDXLIV"},
            {"input": {"num": 1000}, "output": "M"},
            {"input": {"num": 2024}, "output": "MMXXIV"},
            {"input": {"num": 3888}, "output": "MMMDCCCLXXXVIII"},
            {"input": {"num": 3999}, "output": "MMMCMXCIX"},
        ],
        "solution": (
            "class Solution:\n"
            "    def intToRoman(self, num: int) -> str:\n"
            "        table = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),\n"
            "                 (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]\n"
            "        out = []\n"
            "        for value, symbol in table:\n"
            "            count, num = divmod(num, value)\n"
            "            out.append(symbol * count)\n"
            "        return ''.join(out)\n"
        ),
        "approach": (
            "**Key insight: once the subtractive pairs are treated as denominations in their own right, the greedy "
            "largest-first choice is always correct.** The 13 denominations (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1) "
            "are exactly the strings a Roman numeral is built from, and each one can only appear a bounded number of times, so "
            "`divmod` per denomination produces the numeral directly.\n\n"
            "Why greedy works: each denomination is more than the sum of what can legally follow it (e.g. after taking as many "
            "900s as fit, the remainder is below 900), so no smaller combination can replace a larger symbol. Because `num <= 3999` "
            "the loop runs at most 13 iterations and the output is at most 15 characters, so the algorithm is effectively constant time.\n\n"
            "A table-driven alternative stores the thousands, hundreds, tens and ones digits as four lookup arrays and concatenates "
            "`thousands[num//1000] + hundreds[num%1000//100] + ...`. It is equally valid and some interviewers prefer it.\n\n"
            "**Common mistakes:** forgetting the subtractive pairs and emitting `IIII`; iterating the table in increasing order; "
            "off-by-one when using `while num >= value` without the `divmod` shortcut.\n\n"
            "**Interview follow-ups:** Round-trip test against `roman-to-integer`. Extend beyond 3999 (overline notation or "
            "repeated `M`). Discuss why greedy fails for arbitrary coin systems (e.g. coins 1, 3, 4 and amount 6) and how this "
            "relates to the `coin-change` DP."
        ),
        "complexity": {"time": "O(1) (at most 13 denominations, 15 output characters)", "space": "O(1)"},
        "similar": ["roman-to-integer", "coin-change"],
    },
    {
        "id": "valid-palindrome-ii",
        "title": "Valid Palindrome II",
        "difficulty": "Easy",
        "pattern": "Strings",
        "tags": ["Two Pointers", "String", "Greedy"],
        "companies": {"google": 2, "apple": 2, "meta": 5, "amazon": 2, "microsoft": 2},
        "description": (
            "Given a string `s`, return `true` if it is a palindrome, or can be turned into one by deleting **at most one** "
            "character. Otherwise return `false`."
        ),
        "examples": [
            {"input": "s = \"aba\"", "output": "true", "explanation": "Already a palindrome; no deletion needed."},
            {"input": "s = \"abca\"", "output": "true", "explanation": "Delete the b (giving aca) or the c (giving aba)."},
            {"input": "s = \"abc\"", "output": "false", "explanation": "Removing any single character leaves a two-letter string with different letters."},
        ],
        "constraints": ["1 <= s.length <= 10^5", "s consists of lowercase English letters"],
        "hints": [
            "Use two pointers from both ends as you would to check an ordinary palindrome.",
            "At the first mismatch you have exactly two choices: drop the left character or drop the right one. Each choice leaves a plain palindrome check on the remaining range.",
            "You never need to branch twice: a second mismatch means that choice failed, so the total work is linear.",
        ],
        "function": "validPalindrome",
        "signature": "def validPalindrome(self, s: str) -> bool:",
        "arg_types": {"s": "str"},
        "return_type": "bool",
        "compare": "exact",
        "tests": [
            {"input": {"s": "aba"}, "output": True},
            {"input": {"s": "abca"}, "output": True},
            {"input": {"s": "abc"}, "output": False},
            {"input": {"s": "a"}, "output": True},
            {"input": {"s": "ab"}, "output": True},
            {"input": {"s": "abcda"}, "output": False},
            {"input": {"s": "deeee"}, "output": True},
            {"input": {"s": "eedede"}, "output": True},
            {"input": {"s": "abcdefdcba"}, "output": True},
            {"input": {"s": "abcdeedcbx"}, "output": False},
            {"input": {"s": "cbbcc"}, "output": True},
            {"input": {"s": "a" * 5000 + "b" + "a" * 4999}, "output": True},
            {"input": {"s": "a" * 3000 + "bcd" + "a" * 3000}, "output": False},
        ],
        "solution": (
            "class Solution:\n"
            "    def validPalindrome(self, s: str) -> bool:\n"
            "        def is_pal(i: int, j: int) -> bool:\n"
            "            while i < j:\n"
            "                if s[i] != s[j]:\n"
            "                    return False\n"
            "                i += 1; j -= 1\n"
            "            return True\n\n"
            "        i, j = 0, len(s) - 1\n"
            "        while i < j:\n"
            "            if s[i] != s[j]:\n"
            "                return is_pal(i + 1, j) or is_pal(i, j - 1)\n"
            "            i += 1; j -= 1\n"
            "        return True\n"
        ),
        "approach": (
            "**Key insight: the first mismatch forces the decision.** Characters that matched from the outside in are already "
            "correct; at the first `s[i] != s[j]`, the only way to fix things with one deletion is to drop `s[i]` or `s[j]`. "
            "Each option reduces to a plain palindrome check on the remaining range, with no further deletions allowed. Try both; "
            "if either succeeds, answer true.\n\n"
            "Two linear scans at most, O(1) extra space. The greedy is sound because deleting a character outside the mismatching "
            "pair cannot help: those outer pairs already matched and would be thrown out of alignment.\n\n"
            "**Common mistakes:** recursing with the deletion budget and re-checking from the very start (O(n^2)); using slicing "
            "like `s[i+1:j+1][::-1]` which is correct but allocates O(n) strings; checking only one of the two options; forgetting "
            "that an already-palindromic string is valid without any deletion.\n\n"
            "**Interview follow-ups:** Generalise to at most k deletions: the two-way branch becomes a DP equal to `n - "
            "longest palindromic subsequence <= k`, O(n^2). Return *which* character to delete. Streaming or very long inputs: "
            "the two-pointer approach needs random access, so discuss what changes if the data only arrives sequentially."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["valid-palindrome", "longest-palindromic-subsequence", "longest-palindrome"],
    },
    {
        "id": "reverse-words-in-a-string",
        "title": "Reverse Words in a String",
        "difficulty": "Medium",
        "pattern": "Strings",
        "tags": ["Two Pointers", "String"],
        "companies": {"google": 2, "apple": 4, "meta": 2, "amazon": 3, "microsoft": 4},
        "description": (
            "Given a string `s` made of words separated by spaces, return the words in **reverse order**, joined by single spaces.\n\n"
            "The input may contain leading, trailing or repeated spaces; the output must contain none of those. A word is a "
            "maximal run of non-space characters, and the characters inside each word keep their order."
        ),
        "examples": [
            {"input": "s = \"the sky is blue\"", "output": "\"blue is sky the\""},
            {"input": "s = \"  hello world  \"", "output": "\"world hello\"", "explanation": "Surrounding spaces are dropped."},
            {"input": "s = \"a good   example\"", "output": "\"example good a\"", "explanation": "Runs of spaces collapse to one."},
        ],
        "constraints": ["1 <= s.length <= 10^4", "s contains English letters, digits and spaces", "s contains at least one word"],
        "hints": [
            "Split on whitespace, reverse the list of tokens, join with one space. Python's split() with no argument already drops empty tokens.",
            "If asked to do it in place (mutable char array, O(1) extra space): reverse the whole array, then reverse each word individually, then squeeze out the extra spaces.",
        ],
        "function": "reverseWords",
        "signature": "def reverseWords(self, s: str) -> str:",
        "arg_types": {"s": "str"},
        "return_type": "str",
        "compare": "exact",
        "tests": [
            {"input": {"s": "the sky is blue"}, "output": "blue is sky the"},
            {"input": {"s": "  hello world  "}, "output": "world hello"},
            {"input": {"s": "a good   example"}, "output": "example good a"},
            {"input": {"s": "a"}, "output": "a"},
            {"input": {"s": "   single   "}, "output": "single"},
            {"input": {"s": "F R I E N D S"}, "output": "S D N E I R F"},
            {"input": {"s": "Alice does not even like bob"}, "output": "bob like even not does Alice"},
            {"input": {"s": "1 22 333  4444"}, "output": "4444 333 22 1"},
            {"input": {"s": " ".join(str(i) for i in range(3000))}, "output": " ".join(str(i) for i in range(2999, -1, -1))},
        ],
        "solution": (
            "class Solution:\n"
            "    def reverseWords(self, s: str) -> str:\n"
            "        return ' '.join(reversed(s.split()))\n"
        ),
        "approach": (
            "**Key insight: tokenise, reverse the tokens, re-join.** `s.split()` with no separator argument treats any run of "
            "whitespace as one delimiter and discards empty tokens, which handles leading, trailing and repeated spaces in one "
            "call. Reversing the list and joining with a single space produces the normalised output. O(n) time and O(n) space.\n\n"
            "The reason this is rated Medium is the follow-up: do it **in place** on a character array with O(1) extra memory. "
            "The trick is **reverse twice**: reverse the entire array (words are now in the right order but each word is "
            "backwards), then reverse every individual word. Space normalisation is a separate two-pointer pass that copies "
            "characters forward, writing a single space between words and truncating the tail. Apple and Microsoft like this "
            "version because it tests careful index handling.\n\n"
            "**Common mistakes:** `split(' ')` (keeps empty strings between consecutive spaces); forgetting to strip the result; "
            "in the in-place version, reversing words before collapsing spaces and losing track of word boundaries.\n\n"
            "**Interview follow-ups:** Reverse the words but keep the original spacing. Reverse only the characters in each word "
            "(`reverse-words-in-a-string-iii`). Handle Unicode: splitting on `str.isspace()` covers non-ASCII spaces, and reversing "
            "a word by code point can break combining characters, so grapheme clusters matter."
        ),
        "complexity": {"time": "O(n)", "space": "O(n) (O(1) extra for the in-place char-array version)"},
        "similar": ["rotate-array", "reverse-words-in-a-string-iii", "reverse-string"],
    },
    {
        "id": "string-compression",
        "title": "String Compression",
        "difficulty": "Medium",
        "pattern": "Strings",
        "tags": ["Two Pointers", "String"],
        "companies": {"google": 3, "apple": 3, "meta": 3, "amazon": 3, "microsoft": 3},
        "description": (
            "Compress a character array `chars` **in place** using run-length encoding.\n\n"
            "Scan the array for maximal runs of identical characters. For each run write the character, followed by the run "
            "length as decimal digits **only if the length is greater than 1** (a length of 1 writes just the character). "
            "Write the result into the front of `chars` and return the new length `k`; only the first `k` elements matter afterwards.\n\n"
            "Lengths of 10 or more take several array slots (one per digit). You must use O(1) extra space, not build a separate string."
        ),
        "examples": [
            {"input": "chars = [\"a\",\"a\",\"b\",\"b\",\"c\",\"c\",\"c\"]", "output": "6, chars = [\"a\",\"2\",\"b\",\"2\",\"c\",\"3\"]"},
            {"input": "chars = [\"a\"]", "output": "1, chars = [\"a\"]", "explanation": "A run of length 1 is written without a count."},
            {"input": "chars = [\"a\",\"b\",\"b\",\"b\",\"b\",\"b\",\"b\",\"b\",\"b\",\"b\",\"b\",\"b\",\"b\"]", "output": "4, chars = [\"a\",\"b\",\"1\",\"2\"]", "explanation": "Twelve b's compress to b12, which takes three slots."},
        ],
        "constraints": ["1 <= chars.length <= 2000", "chars[i] is a lowercase or uppercase English letter, digit or symbol"],
        "hints": [
            "Use a read pointer that walks runs and a write pointer that lags behind. The write pointer never overtakes the read pointer, so writing in place is safe.",
            "For each run, record the character, advance the read pointer to the end of the run, then write the character and, if the run is longer than 1, the digits of its length.",
            "str(count) gives the digits; write them one per slot. The compressed form of a run is never longer than the run itself, which is why in-place works.",
        ],
        "function": "compress",
        "signature": "def compress(self, chars: List[str]) -> int:",
        "arg_types": {"chars": "List[str]"},
        "return_type": "int",
        "output_mode": "prefix:chars",
        "compare": "exact",
        "tests": [
            {"input": {"chars": ["a", "a", "b", "b", "c", "c", "c"]}, "output": [6, ["a", "2", "b", "2", "c", "3"]]},
            {"input": {"chars": ["a"]}, "output": [1, ["a"]]},
            {"input": {"chars": ["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]}, "output": [4, ["a", "b", "1", "2"]]},
            {"input": {"chars": ["a", "a", "a", "b", "b", "a", "a"]}, "output": [6, ["a", "3", "b", "2", "a", "2"]]},
            {"input": {"chars": ["a", "b", "c"]}, "output": [3, ["a", "b", "c"]]},
            {"input": {"chars": ["a", "a"]}, "output": [2, ["a", "2"]]},
            {"input": {"chars": ["x"] * 2000}, "output": [5, ["x", "2", "0", "0", "0"]]},
            {"input": {"chars": ["a"] * 1000 + ["b"] + ["c"] * 100}, "output": [10, ["a", "1", "0", "0", "0", "b", "c", "1", "0", "0"]]},
            {"input": {"chars": ["a", "b"] * 500}, "output": [1000, ["a", "b"] * 500]},
        ],
        "solution": (
            "class Solution:\n"
            "    def compress(self, chars: List[str]) -> int:\n"
            "        write = read = 0\n"
            "        n = len(chars)\n"
            "        while read < n:\n"
            "            ch = chars[read]\n"
            "            start = read\n"
            "            while read < n and chars[read] == ch:\n"
            "                read += 1\n"
            "            chars[write] = ch\n"
            "            write += 1\n"
            "            run = read - start\n"
            "            if run > 1:\n"
            "                for d in str(run):\n"
            "                    chars[write] = d\n"
            "                    write += 1\n"
            "        return write\n"
        ),
        "approach": (
            "**Key insight: two pointers, read ahead and write behind.** The read pointer walks to the end of the current run; "
            "the write pointer emits the character and the digits of the run length. Because a run of length L compresses to "
            "at most `1 + digits(L) <= L` characters for `L >= 2` (and to exactly 1 for `L = 1`), the write index can never pass "
            "the read index, so overwriting the array as you go is safe. That invariant is the thing to say out loud in the interview.\n\n"
            "O(n) time, O(1) extra space apart from the tiny digit string.\n\n"
            "**Common mistakes:** writing a count of `1` (the spec says omit it); writing the count as a single element `\"12\"` "
            "instead of two slots; building a new list and copying it back (works but violates the space requirement); mishandling "
            "the final run when the loop ends.\n\n"
            "**Interview follow-ups:** Decompress the result and discuss ambiguity when the input itself contains digits (a real RLE "
            "format needs an escape or a fixed-width count). What if the compressed form could be longer than the input (e.g. "
            "`\"abc\"` with counts always written)? Then in-place is impossible without first measuring the output length. Streaming "
            "compression: emit a run when the character changes, carrying only (char, count) state."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["count-and-say", "encode-and-decode-strings", "remove-duplicates-from-sorted-array"],
    },
    {
        "id": "find-the-index-of-the-first-occurrence",
        "title": "Find the Index of the First Occurrence in a String",
        "difficulty": "Easy",
        "pattern": "Strings",
        "tags": ["Two Pointers", "String", "String Matching"],
        "companies": {"google": 2, "apple": 3, "meta": 2, "amazon": 3, "microsoft": 3},
        "description": (
            "Given two strings `haystack` and `needle`, return the index of the first position in `haystack` where `needle` "
            "begins, or `-1` if `needle` does not occur. This is the classic `strStr` / `indexOf` routine.\n\n"
            "You may not call the language's built-in substring search; the point is to implement it."
        ),
        "examples": [
            {"input": "haystack = \"sadbutsad\", needle = \"sad\"", "output": "0", "explanation": "sad occurs at 0 and 6; the first is 0."},
            {"input": "haystack = \"leetcode\", needle = \"leeto\"", "output": "-1"},
            {"input": "haystack = \"mississippi\", needle = \"issip\"", "output": "4", "explanation": "The earlier partial match at index 1 (issis) fails on the fifth character."},
        ],
        "constraints": ["1 <= haystack.length, needle.length <= 10^4", "Both strings consist of lowercase English letters"],
        "hints": [
            "The direct approach tries every start index i and compares needle against haystack[i:i+m]. Worst case O(n*m) but fine for small inputs.",
            "To guarantee O(n+m), use KMP: precompute, for each prefix of needle, the length of its longest proper prefix that is also a suffix (the failure table).",
            "While scanning the haystack, on a mismatch fall back to the failure table instead of restarting at the next haystack index; the haystack pointer never moves backwards.",
        ],
        "function": "strStr",
        "signature": "def strStr(self, haystack: str, needle: str) -> int:",
        "arg_types": {"haystack": "str", "needle": "str"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"haystack": "sadbutsad", "needle": "sad"}, "output": 0},
            {"input": {"haystack": "leetcode", "needle": "leeto"}, "output": -1},
            {"input": {"haystack": "mississippi", "needle": "issip"}, "output": 4},
            {"input": {"haystack": "hello", "needle": "ll"}, "output": 2},
            {"input": {"haystack": "aaaaa", "needle": "bba"}, "output": -1},
            {"input": {"haystack": "a", "needle": "a"}, "output": 0},
            {"input": {"haystack": "abc", "needle": "c"}, "output": 2},
            {"input": {"haystack": "ab", "needle": "abc"}, "output": -1},
            {"input": {"haystack": "aabaaabaaac", "needle": "aabaaac"}, "output": 4},
            {"input": {"haystack": "a" * 5000 + "b", "needle": "a" * 2000 + "b"}, "output": 3000},
            {"input": {"haystack": "a" * 3000, "needle": "a" * 1000 + "b"}, "output": -1},
            {"input": {"haystack": "ab" * 2500 + "c", "needle": "ab" * 1000 + "c"}, "output": 3000},
        ],
        "solution": (
            "class Solution:\n"
            "    def strStr(self, haystack: str, needle: str) -> int:\n"
            "        n, m = len(haystack), len(needle)\n"
            "        if m == 0:\n"
            "            return 0\n"
            "        # failure[i] = length of the longest proper prefix of needle[:i+1] that is also its suffix\n"
            "        failure = [0] * m\n"
            "        k = 0\n"
            "        for i in range(1, m):\n"
            "            while k and needle[i] != needle[k]:\n"
            "                k = failure[k - 1]\n"
            "            if needle[i] == needle[k]:\n"
            "                k += 1\n"
            "            failure[i] = k\n"
            "        # scan the haystack; j is how many needle chars are currently matched\n"
            "        j = 0\n"
            "        for i, ch in enumerate(haystack):\n"
            "            while j and ch != needle[j]:\n"
            "                j = failure[j - 1]\n"
            "            if ch == needle[j]:\n"
            "                j += 1\n"
            "                if j == m:\n"
            "                    return i - m + 1\n"
            "        return -1\n"
        ),
        "approach": (
            "**Key insight (KMP): after a mismatch, the characters you just matched tell you exactly how far the pattern can "
            "slide, so the text pointer never goes back.** Precompute `failure[i]`, the length of the longest proper prefix of "
            "`needle[:i+1]` that is also a suffix of it. When the match of length `j` breaks, the best next alignment keeps the "
            "first `failure[j-1]` characters matched. The same loop structure builds the table (pattern against itself) and runs "
            "the search (pattern against text).\n\n"
            "Each step either advances the text pointer or shrinks `j`, and `j` grows at most once per text character, so the "
            "search is O(n) after an O(m) preprocessing pass: O(n + m) total with O(m) space.\n\n"
            "The naive sliding comparison is O((n - m + 1) * m) in the worst case (text `aaa...a`, pattern `aa...ab`) but is the right "
            "first answer in an interview; implement it, then explain where it degrades and offer KMP. In Python, slicing "
            "`haystack[i:i+m] == needle` is fast in practice because the comparison runs in C.\n\n"
            "**Common mistakes:** off-by-one in the return index (`i - m + 1`); forgetting to fall back repeatedly (the inner `while`, "
            "not a single `if`); comparing `needle[j]` after `j` already equals `m`; handling an empty needle.\n\n"
            "**Interview follow-ups:** Rabin-Karp (rolling hash) for searching many patterns of the same length or for 2-D matching; "
            "Boyer-Moore for long alphabets and long patterns (sublinear on average); Aho-Corasick for many patterns at once. "
            "Also ask what a production `indexOf` does: most libraries use a tuned two-way or Boyer-Moore-Horspool variant rather than plain KMP."
        ),
        "complexity": {"time": "O(n + m)", "space": "O(m)"},
        "similar": ["repeated-substring-pattern", "longest-common-prefix", "shortest-palindrome"],
    },
    {
        "id": "text-justification",
        "title": "Text Justification",
        "difficulty": "Hard",
        "pattern": "Strings",
        "tags": ["Array", "String", "Simulation"],
        "companies": {"google": 3, "apple": 2, "meta": 3, "amazon": 2, "microsoft": 2},
        "description": (
            "Lay out a list of `words` into lines of exactly `maxWidth` characters, fully justified.\n\n"
            "Fill each line greedily with as many words as fit (words separated by at least one space). Then pad the line "
            "with spaces so that it is exactly `maxWidth` wide:\n\n"
            "- Distribute the extra spaces as evenly as possible between words. If they do not divide evenly, the gaps on the "
            "**left** get one more space than the gaps on the right.\n"
            "- A line containing a **single word**, and the **last line** of the text, are left-justified instead: words "
            "separated by one space, then spaces appended to reach `maxWidth`.\n\n"
            "Every word is at most `maxWidth` characters long. Return the list of lines."
        ),
        "examples": [
            {
                "input": "words = [\"This\",\"is\",\"an\",\"example\",\"of\",\"text\",\"justification.\"], maxWidth = 16",
                "output": "[\"This    is    an\",\"example  of text\",\"justification.  \"]",
                "explanation": "Line 1 holds 8 letters and must spread 8 spaces over 2 gaps. Line 2 spreads 3 spaces over 2 gaps, so the left gap gets 2. The last line is left-justified.",
            },
            {
                "input": "words = [\"What\",\"must\",\"be\",\"acknowledgment\",\"shall\",\"be\"], maxWidth = 16",
                "output": "[\"What   must   be\",\"acknowledgment  \",\"shall be        \"]",
                "explanation": "acknowledgment is alone on its line, so it is left-justified even though it is not the last line.",
            },
        ],
        "constraints": ["1 <= words.length <= 300", "1 <= words[i].length <= 20", "words[i] contains only non-space characters", "1 <= maxWidth <= 100", "words[i].length <= maxWidth"],
        "hints": [
            "Separate the two problems: first decide which words go on each line, then format each line.",
            "A word fits on the current line if current_letters + current_word_count (minimum spaces) + len(word) <= maxWidth.",
            "For a full-justified line with g gaps and S spaces to distribute, every gap gets S // g spaces and the first S % g gaps get one extra. Handle the one-word line and the last line separately with ljust.",
        ],
        "function": "fullJustify",
        "signature": "def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:",
        "arg_types": {"words": "List[str]", "maxWidth": "int"},
        "return_type": "List[str]",
        "compare": "exact",
        "tests": [
            {"input": {"words": ["This", "is", "an", "example", "of", "text", "justification."], "maxWidth": 16},
             "output": ["This    is    an", "example  of text", "justification.  "]},
            {"input": {"words": ["What", "must", "be", "acknowledgment", "shall", "be"], "maxWidth": 16},
             "output": ["What   must   be", "acknowledgment  ", "shall be        "]},
            {"input": {"words": ["Science", "is", "what", "we", "understand", "well", "enough", "to", "explain", "to", "a", "computer.",
                                 "Art", "is", "everything", "else", "we", "do"], "maxWidth": 20},
             "output": ["Science  is  what we", "understand      well", "enough to explain to", "a  computer.  Art is",
                        "everything  else  we", "do                  "]},
            {"input": {"words": ["a"], "maxWidth": 1}, "output": ["a"]},
            {"input": {"words": ["hello"], "maxWidth": 10}, "output": ["hello     "]},
            {"input": {"words": ["a", "b", "c"], "maxWidth": 5}, "output": ["a b c"]},
            {"input": {"words": ["a", "b", "c", "d"], "maxWidth": 5}, "output": ["a b c", "d    "]},
            {"input": {"words": ["a"] * 7, "maxWidth": 3}, "output": ["a a", "a a", "a a", "a  "]},
            {"input": {"words": ["ab", "cde", "f", "ghij"], "maxWidth": 7}, "output": ["ab  cde", "f ghij "]},
            {"input": {"words": ["ab"] * 600, "maxWidth": 11}, "output": ["ab ab ab ab"] * 150},
        ],
        "solution": (
            "class Solution:\n"
            "    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:\n"
            "        lines = []\n"
            "        i, n = 0, len(words)\n"
            "        while i < n:\n"
            "            # greedily collect words for this line\n"
            "            j, letters = i, 0\n"
            "            while j < n and letters + len(words[j]) + (j - i) <= maxWidth:\n"
            "                letters += len(words[j])\n"
            "                j += 1\n"
            "            line_words = words[i:j]\n"
            "            gaps = j - i - 1\n"
            "            if j == n or gaps == 0:\n"
            "                lines.append(' '.join(line_words).ljust(maxWidth))\n"
            "            else:\n"
            "                spaces = maxWidth - letters\n"
            "                base, extra = divmod(spaces, gaps)\n"
            "                parts = []\n"
            "                for k, w in enumerate(line_words[:-1]):\n"
            "                    parts.append(w)\n"
            "                    parts.append(' ' * (base + (1 if k < extra else 0)))\n"
            "                parts.append(line_words[-1])\n"
            "                lines.append(''.join(parts))\n"
            "            i = j\n"
            "        return lines\n"
        ),
        "approach": (
            "**Key insight: this is a simulation problem; the difficulty is purely in keeping the cases straight.** Split it "
            "into (1) choosing the words for each line and (2) rendering a line.\n\n"
            "Choosing: starting at index `i`, keep adding words while `letters + len(word) + gaps_so_far <= maxWidth`, where "
            "`gaps_so_far = j - i` is the minimum number of spaces needed if we add this word. Greedy packing is what the spec "
            "asks for (it is *not* the optimal line-breaking of TeX, which minimises raggedness with DP).\n\n"
            "Rendering: with `g` gaps and `S = maxWidth - letters` spaces, each gap gets `S // g` and the first `S % g` gaps "
            "get one extra, which is exactly `divmod`. Two cases are left-justified instead: a single-word line (`g == 0`, so there "
            "is nothing to divide by) and the final line (`j == n`). `' '.join(...).ljust(maxWidth)` handles both.\n\n"
            "O(total characters) time, O(maxWidth) working space per line.\n\n"
            "**Common mistakes:** dividing by zero on one-word lines; treating the last line like the others; counting spaces "
            "as part of `letters` when checking fit; putting the extra spaces on the right instead of the left; forgetting to pad "
            "the last line to full width.\n\n"
            "**Interview follow-ups:** Minimise raggedness instead of greedy packing (the classic DP over break points, O(n^2)). "
            "Support hyphenation of words longer than the width. Right-justify or centre instead. Proportional fonts: the width "
            "function changes from `len` to a lookup, but the algorithm stays the same, which is a nice point to make about separating "
            "measurement from layout."
        ),
        "complexity": {"time": "O(total characters)", "space": "O(maxWidth) extra beyond the output"},
        "similar": ["reverse-words-in-a-string", "string-compression"],
    },
    {
        "id": "compare-version-numbers",
        "title": "Compare Version Numbers",
        "difficulty": "Medium",
        "pattern": "Strings",
        "tags": ["Two Pointers", "String"],
        "companies": {"google": 2, "apple": 4, "meta": 2, "amazon": 3, "microsoft": 3},
        "description": (
            "Two version strings `version1` and `version2` consist of numeric revisions separated by dots, such as `\"1.0.3\"`. "
            "Compare them revision by revision from left to right, treating each revision as an integer (so leading zeros are "
            "ignored: `\"01\"` and `\"1\"` are equal). If one version has fewer revisions, its missing revisions count as `0`.\n\n"
            "Return `-1` if `version1 < version2`, `1` if `version1 > version2`, and `0` if they are equal."
        ),
        "examples": [
            {"input": "version1 = \"1.2\", version2 = \"1.10\"", "output": "-1", "explanation": "The second revision compares 2 against 10 numerically, not as strings."},
            {"input": "version1 = \"1.01\", version2 = \"1.001\"", "output": "0", "explanation": "01 and 001 are both the integer 1."},
            {"input": "version1 = \"1.0\", version2 = \"1.0.0.0\"", "output": "0", "explanation": "Missing trailing revisions are treated as 0."},
        ],
        "constraints": ["1 <= version1.length, version2.length <= 500", "Both contain only digits and dots", "Neither starts or ends with a dot, and dots are never adjacent", "Each revision fits in a 32-bit integer"],
        "hints": [
            "Split both strings on '.', convert each chunk with int(), and compare position by position.",
            "Pad the shorter list with zeros (or use itertools.zip_longest with fillvalue=0) so trailing zeros compare as equal.",
            "To avoid allocating the split lists, walk both strings with two pointers and parse one revision at a time.",
        ],
        "function": "compareVersion",
        "signature": "def compareVersion(self, version1: str, version2: str) -> int:",
        "arg_types": {"version1": "str", "version2": "str"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"version1": "1.2", "version2": "1.10"}, "output": -1},
            {"input": {"version1": "1.01", "version2": "1.001"}, "output": 0},
            {"input": {"version1": "1.0", "version2": "1.0.0.0"}, "output": 0},
            {"input": {"version1": "0.1", "version2": "1.1"}, "output": -1},
            {"input": {"version1": "1.0.1", "version2": "1"}, "output": 1},
            {"input": {"version1": "7.5.2.4", "version2": "7.5.3"}, "output": -1},
            {"input": {"version1": "1", "version2": "1.0.0.0.0"}, "output": 0},
            {"input": {"version1": "0000000001", "version2": "1"}, "output": 0},
            {"input": {"version1": "2", "version2": "1.9.9.9.9.9"}, "output": 1},
            {"input": {"version1": "1.0.0.0.1", "version2": "1"}, "output": 1},
            {"input": {"version1": ".".join(["1"] * 2000), "version2": ".".join(["1"] * 1999 + ["2"])}, "output": -1},
            {"input": {"version1": ".".join(["3"] * 1500), "version2": ".".join(["3"] * 1500)}, "output": 0},
        ],
        "solution": (
            "class Solution:\n"
            "    def compareVersion(self, version1: str, version2: str) -> int:\n"
            "        a = [int(x) for x in version1.split('.')]\n"
            "        b = [int(x) for x in version2.split('.')]\n"
            "        for x, y in itertools.zip_longest(a, b, fillvalue=0):\n"
            "            if x != y:\n"
            "                return -1 if x < y else 1\n"
            "        return 0\n"
        ),
        "approach": (
            "**Key insight: compare revisions as integers, and treat a missing revision as zero.** Splitting on `.` and "
            "converting each chunk with `int()` removes leading zeros for free. `zip_longest(..., fillvalue=0)` pads the shorter "
            "list so `\"1.0\"` and `\"1.0.0.0\"` compare equal. The first differing revision decides the result.\n\n"
            "This is O(n + m) time and space. The two-pointer variant parses one revision at a time from each string without "
            "allocating the lists, which is the O(1)-extra-space answer interviewers sometimes push for; the logic is identical, just "
            "with an inner loop that accumulates digits until the next dot or the end.\n\n"
            "**Common mistakes:** comparing the strings lexicographically (`\"1.2\" > \"1.10\"` as strings); comparing chunk strings "
            "instead of integers, so `\"01\"` and `\"1\"` differ; stopping when the shorter version runs out and declaring it smaller, "
            "which is wrong when the remaining revisions are all zero; returning the raw difference instead of -1/0/1.\n\n"
            "**Interview follow-ups:** Semantic versioning adds pre-release tags (`1.0.0-beta.2 < 1.0.0`) and build metadata that is "
            "ignored, so the comparison needs a tokenizer that distinguishes numeric and alphanumeric identifiers. Sort a list of "
            "versions: convert each to a tuple of ints and sort (padding is unnecessary for sorting only if you strip trailing zeros). "
            "Very long revisions that overflow a 32-bit int: compare lengths after stripping zeros, then compare lexicographically."
        ),
        "complexity": {"time": "O(n + m)", "space": "O(n + m) (O(1) with the two-pointer variant)"},
        "similar": ["string-to-integer-atoi", "simplify-path"],
    },
    {
        "id": "longest-palindrome",
        "title": "Longest Palindrome",
        "difficulty": "Easy",
        "pattern": "Strings",
        "tags": ["Hash Table", "String", "Greedy"],
        "companies": {"google": 2, "apple": 1, "meta": 3, "amazon": 2, "microsoft": 1},
        "description": (
            "Given a string `s` of upper- and lowercase letters, return the length of the longest palindrome that can be "
            "built by **rearranging a subset** of its characters.\n\n"
            "Letters are case sensitive: `\"A\"` and `\"a\"` are different characters."
        ),
        "examples": [
            {"input": "s = \"abccccdd\"", "output": "7", "explanation": "One longest palindrome is dccaccd. The lone b cannot be paired, but a single unpaired letter may sit in the middle."},
            {"input": "s = \"a\"", "output": "1"},
            {"input": "s = \"Aa\"", "output": "1", "explanation": "A and a are different letters, so neither can be paired."},
        ],
        "constraints": ["1 <= s.length <= 2000", "s consists of lowercase and/or uppercase English letters"],
        "hints": [
            "A palindrome is made of matched pairs mirrored around the centre, plus at most one unpaired character in the middle.",
            "Count each character. Every pair contributes 2 to the length. Any character with an odd count leaves one letter over.",
            "If at least one count is odd, you can place exactly one leftover letter in the centre: add 1.",
        ],
        "function": "longestPalindrome",
        "signature": "def longestPalindrome(self, s: str) -> int:",
        "arg_types": {"s": "str"},
        "return_type": "int",
        "compare": "exact",
        "tests": [
            {"input": {"s": "abccccdd"}, "output": 7},
            {"input": {"s": "a"}, "output": 1},
            {"input": {"s": "Aa"}, "output": 1},
            {"input": {"s": "bb"}, "output": 2},
            {"input": {"s": "abc"}, "output": 1},
            {"input": {"s": "aaabbbccc"}, "output": 7},
            {"input": {"s": "abcdefg"}, "output": 1},
            {"input": {"s": "aabbcc"}, "output": 6},
            {"input": {"s": "ab" * 1000 + "c"}, "output": 2001},
            {"input": {"s": "z" * 1999}, "output": 1999},
        ],
        "solution": (
            "class Solution:\n"
            "    def longestPalindrome(self, s: str) -> int:\n"
            "        counts = Counter(s)\n"
            "        length = sum(c // 2 * 2 for c in counts.values())\n"
            "        return length + 1 if length < len(s) else length\n"
        ),
        "approach": (
            "**Key insight: a palindrome is pairs plus an optional centre.** Every character with count `c` contributes "
            "`c // 2` pairs, i.e. `c // 2 * 2` characters, to the mirrored part. If any character had an odd count, one leftover "
            "letter exists and can be placed in the middle, adding 1. Checking `length < len(s)` is a compact way to detect that at "
            "least one character was left unpaired.\n\n"
            "Counting is a single pass, O(n) time with O(1) space because the alphabet is bounded at 52 letters. An even more "
            "space-conscious version keeps a set of characters seen an odd number of times: toggle membership per character; the "
            "answer is `n - len(odd_set) + (1 if odd_set else 0)`.\n\n"
            "**Common mistakes:** adding 1 whenever there is *any* odd count without capping it at one centre; treating upper and "
            "lower case as equal; trying to actually build the palindrome (unnecessary, only the length is asked); confusing this "
            "with `longest-palindromic-substring`, which is about contiguous substrings and is a different problem entirely.\n\n"
            "**Interview follow-ups:** Return one such palindrome (build the left half from pairs, put a leftover in the middle, "
            "mirror). Count how many distinct palindromes can be formed (multinomial over the half). Streaming input: maintain the "
            "odd-count set incrementally and answer in O(1) per query."
        ),
        "complexity": {"time": "O(n)", "space": "O(1) (bounded alphabet)"},
        "similar": ["valid-palindrome-ii", "palindrome-permutation", "longest-palindromic-substring"],
    },
    {
        "id": "minimum-remove-to-make-valid-parentheses",
        "title": "Minimum Remove to Make Valid Parentheses",
        "difficulty": "Medium",
        "pattern": "Strings",
        "tags": ["String", "Stack"],
        "companies": {"google": 2, "apple": 2, "meta": 5, "amazon": 3, "microsoft": 2},
        "description": (
            "Given a string `s` of lowercase letters and the characters `(` and `)`, delete the **minimum** number of "
            "parentheses so that the result is balanced, and return the resulting string.\n\n"
            "A string is balanced if it contains no parentheses, or every `(` is closed by a later `)` and the pairs nest "
            "properly. Letters are never removed. When several answers use the minimum number of deletions, any of them is accepted."
        ),
        "examples": [
            {"input": "s = \"lee(t(c)o)de)\"", "output": "\"lee(t(c)o)de\"", "explanation": "One closing parenthesis has no partner. Removing any one of the three closers works, e.g. lee(t(co)de) is also accepted."},
            {"input": "s = \"a)b(c)d\"", "output": "\"ab(c)d\"", "explanation": "The first ) can never be matched."},
            {"input": "s = \"))((\"", "output": "\"\"", "explanation": "Nothing can be matched, so every parenthesis goes."},
        ],
        "constraints": ["1 <= s.length <= 10^5", "s[i] is '(', ')' or a lowercase English letter"],
        "hints": [
            "A ) is removable exactly when no unmatched ( precedes it. A ( is removable exactly when no unmatched ) follows it.",
            "Scan left to right with a stack of indices of unmatched (. On ), pop if possible; otherwise mark that ) for removal.",
            "Whatever indices remain on the stack at the end are unmatched ( and must also be removed. Build the result skipping all marked indices.",
        ],
        "function": "minRemoveToMakeValid",
        "signature": "def minRemoveToMakeValid(self, s: str) -> str:",
        "arg_types": {"s": "str"},
        "return_type": "str",
        "compare": "any_of",
        "tests": [
            {"input": {"s": "lee(t(c)o)de)"}, "output": ["lee(t(c)o)de", "lee(t(co)de)", "lee(t(c)ode)"]},
            {"input": {"s": "a)b(c)d"}, "output": ["ab(c)d"]},
            {"input": {"s": "))(("}, "output": [""]},
            {"input": {"s": "(a(b(c)d)"}, "output": ["a(b(c)d)", "(ab(c)d)", "(a(bc)d)"]},
            {"input": {"s": "((("}, "output": [""]},
            {"input": {"s": "abc"}, "output": ["abc"]},
            {"input": {"s": "()"}, "output": ["()"]},
            {"input": {"s": ")("}, "output": [""]},
            {"input": {"s": "(()"}, "output": ["()"]},
            {"input": {"s": "(" * 1000 + ")" * 1000}, "output": ["(" * 1000 + ")" * 1000]},
            {"input": {"s": "(" * 1000 + ")" * 1500}, "output": ["(" * 1000 + ")" * 1000]},
            {"input": {"s": ")" * 500 + "(" * 1000 + ")" * 1000 + "(" * 300}, "output": ["(" * 1000 + ")" * 1000]},
        ],
        "solution": (
            "class Solution:\n"
            "    def minRemoveToMakeValid(self, s: str) -> str:\n"
            "        remove = set()\n"
            "        stack = []\n"
            "        for i, ch in enumerate(s):\n"
            "            if ch == '(':\n"
            "                stack.append(i)\n"
            "            elif ch == ')':\n"
            "                if stack:\n"
            "                    stack.pop()\n"
            "                else:\n"
            "                    remove.add(i)\n"
            "        remove.update(stack)\n"
            "        return ''.join(ch for i, ch in enumerate(s) if i not in remove)\n"
        ),
        "approach": (
            "**Key insight: a parenthesis must be deleted exactly when it can never be matched, and a single left-to-right "
            "pass with a stack identifies all of them.** Push the index of every `(`. On `)`, pop a partner if one exists; "
            "otherwise this `)` has nothing to its left to match and is doomed. After the scan, every index still on the stack is a "
            "`(` with nothing to its right and is doomed too. Deleting exactly those indices is minimal because each doomed "
            "character is unmatched in *every* valid subsequence of the original string.\n\n"
            "Two passes, O(n) time, O(n) space for the stack and the removal set. Because you only ever need to know how many "
            "`(` are open, the stack can be replaced by a counter for the `)` pass, followed by a right-to-left pass that drops the "
            "surplus `(`; that gives O(1) extra space beyond the output.\n\n"
            "**Common mistakes:** removing letters; deleting the *first* surplus `(` instead of any unmatched one (both are valid, "
            "but the stack naturally keeps the right ones); using `str.replace` or repeated deletion, which is O(n^2); forgetting "
            "the leftover `(` on the stack.\n\n"
            "**Interview follow-ups:** Return the number of removals only (just count). Produce *all* minimal results "
            "(`remove-invalid-parentheses`, BFS or backtracking, exponential). Multiple bracket types: the stack must store the "
            "bracket kind and a mismatched closer invalidates in a more complex way. Validate on a stream: the counter version works online."
        ),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "similar": ["valid-parentheses", "remove-invalid-parentheses", "minimum-add-to-make-parentheses-valid"],
    },
    {
        "id": "simplify-path",
        "title": "Simplify Path",
        "difficulty": "Medium",
        "pattern": "Strings",
        "tags": ["String", "Stack"],
        "companies": {"google": 2, "apple": 2, "meta": 4, "amazon": 2, "microsoft": 3},
        "description": (
            "Given an absolute Unix-style file `path` (it always starts with `/`), return its **canonical** form:\n\n"
            "- A single `.` component means the current directory and is dropped.\n"
            "- A `..` component goes up one directory; going up from the root stays at the root.\n"
            "- Runs of consecutive slashes collapse into one.\n"
            "- The result starts with `/`, has exactly one `/` between directories and no trailing `/` (except for the root itself, which is just `/`).\n\n"
            "Any other sequence of characters, including names like `...` or `.hidden`, is an ordinary directory name."
        ),
        "examples": [
            {"input": "path = \"/home/\"", "output": "\"/home\"", "explanation": "Trailing slash removed."},
            {"input": "path = \"/home//foo/\"", "output": "\"/home/foo\"", "explanation": "Repeated slashes collapse."},
            {"input": "path = \"/home/user/Documents/../Pictures\"", "output": "\"/home/user/Pictures\"", "explanation": ".. cancels Documents."},
            {"input": "path = \"/../\"", "output": "\"/\"", "explanation": "You cannot go above the root."},
            {"input": "path = \"/.../a/../b/c/../d/./\"", "output": "\"/.../b/d\"", "explanation": "... is a normal directory name; . is dropped; each .. removes the previous name."},
        ],
        "constraints": ["1 <= path.length <= 3000", "path consists of letters, digits, '.', '/' and '_'", "path is a valid absolute Unix path"],
        "hints": [
            "Split on '/' and look at each component; empty strings and '.' do nothing.",
            "Keep a stack of directory names. '..' pops (if the stack is non-empty); any other non-empty component is pushed.",
            "The answer is '/' + '/'.join(stack).",
        ],
        "function": "simplifyPath",
        "signature": "def simplifyPath(self, path: str) -> str:",
        "arg_types": {"path": "str"},
        "return_type": "str",
        "compare": "exact",
        "tests": [
            {"input": {"path": "/home/"}, "output": "/home"},
            {"input": {"path": "/home//foo/"}, "output": "/home/foo"},
            {"input": {"path": "/home/user/Documents/../Pictures"}, "output": "/home/user/Pictures"},
            {"input": {"path": "/../"}, "output": "/"},
            {"input": {"path": "/.../a/../b/c/../d/./"}, "output": "/.../b/d"},
            {"input": {"path": "/"}, "output": "/"},
            {"input": {"path": "/a/./b/../../c/"}, "output": "/c"},
            {"input": {"path": "/a//b////c/d//././/.."}, "output": "/a/b/c"},
            {"input": {"path": "/.hidden/..a/a.."}, "output": "/.hidden/..a/a.."},
            {"input": {"path": "/a/../../../b"}, "output": "/b"},
            {"input": {"path": "/" + "/".join(["x"] * 1500) + "/" + "/".join([".."] * 1500)}, "output": "/"},
            {"input": {"path": "/" + "/".join(f"d{i}" for i in range(1000))}, "output": "/" + "/".join(f"d{i}" for i in range(1000))},
        ],
        "solution": (
            "class Solution:\n"
            "    def simplifyPath(self, path: str) -> str:\n"
            "        stack = []\n"
            "        for part in path.split('/'):\n"
            "            if part == '' or part == '.':\n"
            "                continue\n"
            "            if part == '..':\n"
            "                if stack:\n"
            "                    stack.pop()\n"
            "            else:\n"
            "                stack.append(part)\n"
            "        return '/' + '/'.join(stack)\n"
        ),
        "approach": (
            "**Key insight: a path is a sequence of directory operations, and a stack models the current directory "
            "chain exactly.** Splitting on `/` turns repeated slashes into empty components, which are skipped along with `.`. "
            "A `..` pops the most recent directory if there is one (popping an empty stack is the \"stay at root\" rule). Anything "
            "else, including `...` and names with dots, is pushed. Finally join the stack with `/` and prepend the root slash; "
            "when the stack is empty this yields exactly `/`.\n\n"
            "O(n) time and space. The only subtlety is that the output format falls out of the join naturally: no trailing slash, "
            "no double slashes, root handled without a special case.\n\n"
            "**Common mistakes:** treating `...` as a special token; forgetting the empty-stack check on `..`; returning an empty "
            "string instead of `/` for the root; using `os.path.normpath`, which the interviewer will reject and which also behaves "
            "differently on Windows-style paths.\n\n"
            "**Interview follow-ups:** Relative paths (`..` beyond the start must be kept, so the stack can accumulate leading `..`). "
            "Symbolic links (resolution needs the filesystem, and `..` after a symlink is not the parent of the link's name, which is "
            "why `realpath` is different from `normpath`). Streaming or very long paths: the stack approach already processes one "
            "component at a time, so it works on an iterator of components."
        ),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "similar": ["minimum-remove-to-make-valid-parentheses", "compare-version-numbers", "valid-parentheses"],
    },
]
