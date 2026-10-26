"""Tries pattern. See SCHEMA.md for the dict format."""

# A 6x6 board whose cells spell the alphabet row by row (wrapping after z):
#   a b c d e f
#   g h i j k l
#   m n o p q r
#   s t u v w x
#   y z a b c d
#   e f g h i j
_ALPHA_BOARD = [[chr(97 + (r * 6 + c) % 26) for c in range(6)] for r in range(6)]

_TRIE_WORDS = [f"w{i:04d}" for i in range(2000)]
_DICT_WORDS = [f"w{i:04d}" for i in range(1000)]


PROBLEMS = [
    # ------------------------------------------------------------------ 1
    {
        "id": "implement-trie",
        "title": "Implement Trie (Prefix Tree)",
        "difficulty": "Medium",
        "pattern": "Tries",
        "tags": ["Trie", "Design", "Hash Table", "String"],
        "companies": {"google": 3, "apple": 2, "meta": 3, "amazon": 3, "microsoft": 3},
        "kind": "design",
        "class_name": "Trie",
        "description": (
            "A **trie** (prefix tree) stores a set of strings so that any prefix can be looked up in time "
            "proportional to its length, independent of how many words are stored.\n\n"
            "Implement the class:\n\n"
            "- `Trie()` creates an empty trie.\n"
            "- `insert(word)` adds `word` to the trie.\n"
            "- `search(word)` returns `true` if exactly `word` was inserted earlier.\n"
            "- `startsWith(prefix)` returns `true` if at least one inserted word begins with `prefix`.\n\n"
            "All strings consist of lowercase English letters."
        ),
        "examples": [
            {"input": "[\"Trie\",\"insert\",\"search\",\"search\",\"startsWith\",\"insert\",\"search\"]\n"
                      "[[],[\"apple\"],[\"apple\"],[\"app\"],[\"app\"],[\"app\"],[\"app\"]]",
             "output": "[null,null,true,false,true,null,true]",
             "explanation": "After inserting \"apple\", \"app\" is a prefix but not a stored word, so search(\"app\") is false "
                            "while startsWith(\"app\") is true. Inserting \"app\" makes search(\"app\") true."},
        ],
        "constraints": [
            "1 <= word.length, prefix.length <= 2000",
            "Strings contain only lowercase letters a-z.",
            "At most 3 * 10^4 calls in total to insert, search and startsWith.",
        ],
        "hints": [
            "Each node represents one prefix; its children are the possible next letters.",
            "Walk one character at a time from the root. insert creates missing children; search and startsWith stop and return false at the first missing child.",
            "The only difference between search and startsWith is that search also requires an 'end of word' flag on the final node.",
        ],
        "starter": (
            "class Trie:\n"
            "    def __init__(self):\n"
            "        pass\n\n"
            "    def insert(self, word: str) -> None:\n"
            "        pass\n\n"
            "    def search(self, word: str) -> bool:\n"
            "        pass\n\n"
            "    def startsWith(self, prefix: str) -> bool:\n"
            "        pass\n"
        ),
        "compare": "exact",
        "tests": [
            {"input": {"ops": [["Trie", []], ["insert", ["apple"]], ["search", ["apple"]], ["search", ["app"]],
                               ["startsWith", ["app"]], ["insert", ["app"]], ["search", ["app"]]]},
             "output": [None, None, True, False, True, None, True]},
            {"input": {"ops": [["Trie", []], ["search", ["a"]], ["startsWith", ["a"]]]},
             "output": [None, False, False]},
            {"input": {"ops": [["Trie", []], ["insert", ["ab"]], ["insert", ["abc"]], ["search", ["abc"]], ["search", ["ab"]],
                               ["search", ["abcd"]], ["startsWith", ["abcd"]], ["startsWith", ["abc"]], ["search", ["a"]]]},
             "output": [None, None, None, True, True, False, False, True, False]},
            {"input": {"ops": [["Trie", []], ["insert", ["car"]], ["insert", ["card"]], ["insert", ["care"]],
                               ["search", ["ca"]], ["startsWith", ["ca"]], ["search", ["cart"]], ["search", ["card"]],
                               ["startsWith", ["care"]], ["search", ["careful"]]]},
             "output": [None, None, None, None, False, True, False, True, True, False]},
            {"input": {"ops": [["Trie", []], ["insert", ["a"]], ["insert", ["a"]], ["search", ["a"]], ["startsWith", ["a"]], ["search", ["aa"]]]},
             "output": [None, None, None, True, True, False]},
            {"input": {"ops": [["Trie", []]] + [["insert", [w]] for w in _TRIE_WORDS]
                              + [["search", [w]] for w in _TRIE_WORDS[::100]]
                              + [["search", ["w"]], ["startsWith", ["w19"]], ["startsWith", ["x"]], ["search", ["w2000"]]]},
             "output": [None] + [None] * 2000 + [True] * 20 + [False, True, False, False]},
        ],
        "solution": '''class _TrieNode:
    __slots__ = ("children", "is_word")

    def __init__(self):
        self.children = {}
        self.is_word = False


class Trie:
    def __init__(self):
        self.root = _TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, _TrieNode())
        node.is_word = True

    def _walk(self, s: str):
        """Return the node reached by following s, or None if the path breaks."""
        node = self.root
        for ch in s:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_word

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None
''',
        "approach": (
            "**One node per prefix, one edge per letter.** The root represents the empty string. Each node has a "
            "map from next character to child node and a flag marking whether the path from the root to it spells "
            "a complete inserted word. Every operation is a walk of at most `len(s)` steps.\n\n"
            "- `insert`: walk, creating children as needed; mark the final node as a word.\n"
            "- `startsWith`: walk; succeed if the walk never hits a missing child.\n"
            "- `search`: same walk, but additionally require the end-of-word flag.\n\n"
            "**Why the flag matters:** \"app\" is a prefix of \"apple\", so the node for \"app\" exists after inserting "
            "\"apple\". Without the flag, `search(\"app\")` would wrongly return true.\n\n"
            "**Children as dict vs fixed array:** a dict is simplest and memory-proportional to what is used; an "
            "array of 26 slots is faster and what many interviewers expect you to mention for a fixed alphabet.\n\n"
            "**Common mistakes:** marking every node on the path as a word; sharing a single root-level dict so "
            "that search and startsWith become identical; using a set of all prefixes instead (correct but O(total "
            "length) memory and missing the point of the question).\n\n"
            "**Interview follow-ups:** delete a word (walk down, then prune childless non-word nodes on the way "
            "back up); count words with a given prefix (store a counter on each node); autocomplete the k most "
            "frequent completions (DFS from the prefix node, or cache top-k per node); memory optimisation with a "
            "compressed (radix) trie."
        ),
        "complexity": {"time": "O(L) per operation, L = length of the string", "space": "O(total characters inserted)"},
        "similar": ["design-add-and-search-words", "word-search-ii", "replace-words"],
    },
    # ------------------------------------------------------------------ 2
    {
        "id": "design-add-and-search-words",
        "title": "Design Add and Search Words Data Structure",
        "difficulty": "Medium",
        "pattern": "Tries",
        "tags": ["Trie", "Design", "DFS", "String"],
        "companies": {"google": 2, "apple": 2, "meta": 4, "amazon": 3, "microsoft": 2},
        "kind": "design",
        "class_name": "WordDictionary",
        "description": (
            "Design a data structure that stores words and supports lookups with a **wildcard**.\n\n"
            "- `WordDictionary()` creates an empty structure.\n"
            "- `addWord(word)` stores `word`.\n"
            "- `search(word)` returns `true` if some stored word matches `word`, where the character `.` in the "
            "query matches **any single letter**. A match must have exactly the same length as the query.\n\n"
            "Added words contain only lowercase letters; queries contain lowercase letters and dots."
        ),
        "examples": [
            {"input": "[\"WordDictionary\",\"addWord\",\"addWord\",\"addWord\",\"search\",\"search\",\"search\",\"search\"]\n"
                      "[[],[\"bad\"],[\"dad\"],[\"mad\"],[\"pad\"],[\"bad\"],[\".ad\"],[\"b..\"]]",
             "output": "[null,null,null,null,false,true,true,true]",
             "explanation": "\"pad\" was never added. \".ad\" matches all three stored words; \"b..\" matches \"bad\"."},
        ],
        "constraints": [
            "1 <= word.length <= 25",
            "Words passed to addWord contain only a-z; queries contain a-z and '.'.",
            "At most 2 dots per search query; at most 10^4 calls to addWord and search.",
        ],
        "hints": [
            "Start from a plain trie. A letter in the query follows one child, exactly as before.",
            "A dot has to try every child of the current node. That turns the walk into a depth-first search that can backtrack.",
            "Recurse on (node, index). Return true if any branch reaches the end of the query at a node flagged as a word.",
        ],
        "starter": (
            "class WordDictionary:\n"
            "    def __init__(self):\n"
            "        pass\n\n"
            "    def addWord(self, word: str) -> None:\n"
            "        pass\n\n"
            "    def search(self, word: str) -> bool:\n"
            "        pass\n"
        ),
        "compare": "exact",
        "tests": [
            {"input": {"ops": [["WordDictionary", []], ["addWord", ["bad"]], ["addWord", ["dad"]], ["addWord", ["mad"]],
                               ["search", ["pad"]], ["search", ["bad"]], ["search", [".ad"]], ["search", ["b.."]]]},
             "output": [None, None, None, None, False, True, True, True]},
            {"input": {"ops": [["WordDictionary", []], ["search", ["."]], ["search", ["a"]]]},
             "output": [None, False, False]},
            {"input": {"ops": [["WordDictionary", []], ["addWord", ["a"]], ["addWord", ["ab"]],
                               ["search", ["."]], ["search", [".."]], ["search", ["..."]], ["search", ["a."]],
                               ["search", [".b"]], ["search", ["b."]]]},
             "output": [None, None, None, True, True, False, True, True, False]},
            {"input": {"ops": [["WordDictionary", []], ["addWord", ["abc"]],
                               ["search", ["ab"]], ["search", [".b."]], ["search", ["a.."]], ["search", ["..."]],
                               ["search", ["...."]], ["search", ["..c"]], ["search", ["..d"]]]},
             "output": [None, None, False, True, True, True, False, True, False]},
            {"input": {"ops": [["WordDictionary", []], ["addWord", ["ab"]], ["addWord", ["cd"]],
                               ["search", [".d"]], ["search", [".b"]], ["search", ["a."]], ["search", ["c.b"]], ["search", ["ad"]]]},
             "output": [None, None, None, True, True, True, False, False]},
            {"input": {"ops": [["WordDictionary", []]] + [["addWord", [w]] for w in _DICT_WORDS]
                              + [["search", ["w0999"]], ["search", ["w1000"]], ["search", ["w.5.."]], ["search", ["x...."]],
                                 ["search", ["....."]], ["search", ["w0.3."]], ["search", ["......"]], ["search", ["w099."]]]},
             "output": [None] + [None] * 1000 + [True, False, True, False, True, True, False, True]},
        ],
        "solution": '''class WordDictionary:
    def __init__(self):
        self.root = {}  # char -> child dict; the key "$" marks a complete word

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, word: str) -> bool:
        def dfs(node, i):
            if i == len(word):
                return "$" in node
            ch = word[i]
            if ch == ".":
                return any(dfs(child, i + 1) for key, child in node.items() if key != "$")
            return ch in node and dfs(node[ch], i + 1)

        return dfs(self.root, 0)
''',
        "approach": (
            "**A trie where the wildcard branches into every child.** Storing words is exactly a trie insert. "
            "Searching is a trie walk, except that when the query character is `.` the walk must try every child "
            "of the current node and succeed if any of them leads to a match. That is a depth-first search over "
            "`(node, position)` states.\n\n"
            "**Why it works:** a trie node corresponds to one prefix of a stored word. The DFS explores precisely "
            "the set of stored prefixes consistent with the query so far, and the end-of-word flag at the final "
            "node guarantees the match has the same length as the query rather than merely being a prefix.\n\n"
            "**Complexity:** a letter costs O(1) per level; a dot costs up to 26 branches, so a query with d dots "
            "costs O(26^d * L) in the worst case. With at most 2 dots this is fine, which is why the constraint "
            "exists.\n\n"
            "**Common mistakes:** returning true when the query is exhausted at any node (must check the word flag, "
            "otherwise \"ab\" would match stored \"abc\"); treating the `$` marker as a child when expanding a dot; "
            "storing words in a list and regex-matching each query (O(total words) per search, which the 1000-word "
            "test punishes).\n\n"
            "**Interview follow-ups:** what if the query could contain `*` (zero or more letters) like a glob; how "
            "would you support a huge number of dots (group words by length and, for very dotty queries, scan the "
            "bucket instead); deleting words; returning all matches rather than a boolean."
        ),
        "complexity": {"time": "O(L) for addWord; O(26^d * L) for search with d dots", "space": "O(total characters stored)"},
        "similar": ["implement-trie", "word-search-ii", "wildcard-matching"],
    },
    # ------------------------------------------------------------------ 3
    {
        "id": "word-search-ii",
        "title": "Word Search II",
        "difficulty": "Hard",
        "pattern": "Tries",
        "tags": ["Trie", "Backtracking", "Matrix", "DFS"],
        "companies": {"google": 3, "apple": 2, "meta": 2, "amazon": 4, "microsoft": 4},
        "description": (
            "You are given an `m x n` grid `board` of lowercase letters and a list of distinct `words`. Return "
            "every word that can be traced on the board by starting at any cell and moving to a horizontally or "
            "vertically adjacent cell at each step. A cell may be used **at most once per word**.\n\n"
            "Each found word should appear once in the result, in any order."
        ),
        "examples": [
            {"input": "board = [[\"o\",\"a\",\"a\",\"n\"],[\"e\",\"t\",\"a\",\"e\"],[\"i\",\"h\",\"k\",\"r\"],[\"i\",\"f\",\"l\",\"v\"]], "
                      "words = [\"oath\",\"pea\",\"eat\",\"rain\"]",
             "output": "[\"eat\",\"oath\"]",
             "explanation": "\"oath\" runs o(0,0) a(0,1) t(1,1) h(2,1). \"eat\" runs e(1,3) a(1,2) t(1,1). "
                            "There is no 'p' on the board, and the 'r' is not adjacent to an 'a'."},
            {"input": "board = [[\"a\",\"b\"],[\"c\",\"d\"]], words = [\"abcb\"]", "output": "[]",
             "explanation": "The second 'b' would reuse the cell at (0,1)."},
        ],
        "constraints": [
            "1 <= m, n <= 12",
            "1 <= words.length <= 3 * 10^4",
            "1 <= words[i].length <= 10",
            "All words are distinct; board and words contain only lowercase letters.",
        ],
        "hints": [
            "Running the single-word backtracking search once per word repeats the same board walks over and over.",
            "Put all the words in a trie and do one DFS from each cell, advancing through the trie as you move on the board. Stop as soon as the current prefix is not in the trie.",
            "Record a word when you reach its end node, then remove it from the trie (and prune empty nodes) so it is reported once and dead branches are not re-explored.",
        ],
        "function": "findWords",
        "signature": "def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:",
        "arg_types": {"board": "List[List[str]]", "words": "List[str]"},
        "return_type": "List[str]",
        "compare": "unordered",
        "tests": [
            {"input": {"board": [["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]],
                       "words": ["oath", "pea", "eat", "rain"]},
             "output": ["eat", "oath"]},
            {"input": {"board": [["a", "b"], ["c", "d"]], "words": ["abcb"]}, "output": []},
            {"input": {"board": [["a"]], "words": ["a"]}, "output": ["a"]},
            {"input": {"board": [["a"]], "words": ["aa"]}, "output": []},
            {"input": {"board": [["a", "a"]], "words": ["a", "aa", "aaa"]}, "output": ["a", "aa"]},
            {"input": {"board": [["a", "b"], ["c", "d"]], "words": ["ab", "ac", "bd", "dc", "abdc", "acdb", "abc", "ad"]},
             "output": ["ab", "ac", "bd", "dc", "abdc", "acdb"]},
            {"input": {"board": _ALPHA_BOARD,
                       "words": ["abc", "agm", "fedc", "hnt", "abz", "ihg", "jkl", "hello", "xyz", "bhn"]},
             "output": ["abc", "agm", "fedc", "hnt", "ihg", "jkl", "bhn"]},
            {"input": {"board": [["a"] * 12 for _ in range(12)],
                       "words": ["a" * k for k in range(1, 13)] + ["b", "ab", "ba"]},
             "output": ["a" * k for k in range(1, 13)]},
        ],
        "solution": '''class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        # Build a trie; the key "$" on a node holds the complete word ending there.
        root = {}
        for word in words:
            node = root
            for ch in word:
                node = node.setdefault(ch, {})
            node["$"] = word

        rows, cols = len(board), len(board[0])
        found = []

        def dfs(r, c, parent):
            ch = board[r][c]
            node = parent[ch]
            word = node.pop("$", None)
            if word is not None:
                found.append(word)          # report once; the marker is gone now
            board[r][c] = "#"               # mark the cell as used on this path
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in node:
                    dfs(nr, nc, node)
            board[r][c] = ch
            if not node:                    # prune: nothing below here can match any more
                del parent[ch]

        for r in range(rows):
            for c in range(cols):
                if board[r][c] in root:
                    dfs(r, c, root)
        return found
''',
        "approach": (
            "**Search the board once for all words at the same time by walking a trie alongside the DFS.** Insert "
            "every word into a trie. From each cell, start a backtracking DFS that only continues into a neighbour "
            "whose letter is a child of the current trie node. Whenever the current node carries a complete word, "
            "add it to the output.\n\n"
            "**Two optimisations that make it fast in practice:**\n"
            "1. *Report each word once* by removing its end marker the first time it is reached, instead of using a "
            "result set.\n"
            "2. *Prune the trie* as you backtrack: when a node has no children left (all its words were found), "
            "delete it from its parent. Later DFS calls never enter that subtree. On the all-'a' board this is the "
            "difference between finishing instantly and never finishing.\n\n"
            "**Why it works:** every path on the board that spells a prefix of some word corresponds to a path in "
            "the trie from the root. Walking both together means a board path is abandoned the moment it stops "
            "being a prefix of any remaining word. Marking cells with a sentinel and restoring them on the way back "
            "enforces the use-once rule.\n\n"
            "**Common mistakes:** running Word Search I once per word (O(words * cells * 4^L), times out at 3 * 10^4 "
            "words); forgetting to restore the cell after the DFS; returning duplicate words; forgetting that a "
            "word can be a prefix of another, so you must keep searching past an end node.\n\n"
            "**Interview follow-ups:** why a trie and not a hash set of prefixes (a set works too, but the trie "
            "gives O(1) per step and enables pruning); how to handle diagonal moves or wraparound; estimate the "
            "worst-case complexity and explain what pruning buys; make it incremental when words are added later."
        ),
        "complexity": {"time": "O(m * n * 4 * 3^(L-1)) worst case, L = max word length; far less with pruning", "space": "O(total characters in words)"},
        "similar": ["word-search", "implement-trie", "design-add-and-search-words"],
    },
    # ------------------------------------------------------------------ 4
    {
        "id": "replace-words",
        "title": "Replace Words",
        "difficulty": "Medium",
        "pattern": "Tries",
        "tags": ["Trie", "Hash Table", "String"],
        "companies": {"google": 1, "apple": 1, "meta": 1, "amazon": 2, "microsoft": 2},
        "description": (
            "You are given a `dictionary` of **roots** and a `sentence` of words separated by single spaces. "
            "A root forms a longer word by having letters appended to it: `cat` is a root of `cattle`.\n\n"
            "Replace every word in the sentence that begins with some root by that root. If several roots fit, "
            "use the **shortest** one. Words with no matching root are left unchanged. Return the resulting sentence."
        ),
        "examples": [
            {"input": "dictionary = [\"cat\",\"bat\",\"rat\"], sentence = \"the cattle was rattled by the battery\"",
             "output": "\"the cat was rat by the bat\""},
            {"input": "dictionary = [\"a\",\"b\",\"c\"], sentence = \"aadsfasf absbs bbab cadsfafs\"",
             "output": "\"a a b c\""},
            {"input": "dictionary = [\"catt\",\"cat\"], sentence = \"the cattle\"", "output": "\"the cat\"",
             "explanation": "Both roots fit, and \"cat\" is the shorter."},
        ],
        "constraints": [
            "1 <= dictionary.length <= 1000",
            "1 <= dictionary[i].length <= 100",
            "1 <= sentence.length <= 10^6; words are separated by single spaces with no leading or trailing spaces.",
            "Only lowercase letters.",
        ],
        "hints": [
            "For each word, you want the shortest prefix that is a root. Checking every root against every word is too slow.",
            "Put the roots in a trie. Walk each word down the trie character by character.",
            "Stop at the first node flagged as a root: that prefix is the answer for this word. If you fall off the trie first, keep the word as is.",
        ],
        "function": "replaceWords",
        "signature": "def replaceWords(self, dictionary: List[str], sentence: str) -> str:",
        "arg_types": {"dictionary": "List[str]", "sentence": "str"},
        "return_type": "str",
        "compare": "exact",
        "tests": [
            {"input": {"dictionary": ["cat", "bat", "rat"], "sentence": "the cattle was rattled by the battery"},
             "output": "the cat was rat by the bat"},
            {"input": {"dictionary": ["a", "b", "c"], "sentence": "aadsfasf absbs bbab cadsfafs"}, "output": "a a b c"},
            {"input": {"dictionary": ["catt", "cat"], "sentence": "the cattle"}, "output": "the cat"},
            {"input": {"dictionary": ["a", "aa", "aaa", "aaaa"], "sentence": "a aa a aaaa aaa aaa aaa aaaaaa bbb baba ababa"},
             "output": "a a a a a a a a bbb baba a"},
            {"input": {"dictionary": ["ac", "ab"], "sentence": "it is abnormal that this solution is accepted"},
             "output": "it is ab that this solution is ac"},
            {"input": {"dictionary": ["xyz"], "sentence": "abc def"}, "output": "abc def"},
            {"input": {"dictionary": ["abcd"], "sentence": "abc"}, "output": "abc"},
            {"input": {"dictionary": ["w" + str(i) for i in range(1000)], "sentence": " ".join(f"w{i}x" for i in range(1000))},
             "output": " ".join("w" + str(i)[0] for i in range(1000))},
            {"input": {"dictionary": ["q" + str(i) for i in range(2000)], "sentence": " ".join(f"w{i}" for i in range(3000))},
             "output": " ".join(f"w{i}" for i in range(3000))},
        ],
        "solution": '''class Solution:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        root = {}
        for word in dictionary:
            node = root
            for ch in word:
                node = node.setdefault(ch, {})
            node["$"] = True

        def shortest_root(word):
            node = root
            for i, ch in enumerate(word):
                if ch not in node:
                    return word            # fell off the trie: no root matches
                node = node[ch]
                if "$" in node:
                    return word[:i + 1]    # first root reached is the shortest
            return word

        return " ".join(shortest_root(w) for w in sentence.split(" "))
''',
        "approach": (
            "**A trie of roots turns 'shortest matching prefix' into 'first flagged node on the walk'.** Insert "
            "every root into a trie with an end marker. For each word of the sentence, walk down the trie one "
            "character at a time. The first node that carries an end marker spells the shortest root that is a "
            "prefix of this word, so return that prefix immediately. If a character has no child, no root matches "
            "and the word stays as it is.\n\n"
            "**Why it works:** all roots that are prefixes of a word lie on the same root-to-node path in the trie, "
            "ordered by length. Stopping at the first marker therefore picks the shortest, and never looks at "
            "characters beyond it.\n\n"
            "**Alternatives:** a hash set of roots and, for each word, testing every prefix `word[:k]` for "
            "increasing k. Also correct, O(L^2) per word because of slicing, which is fine for short words but "
            "worse than the trie's O(L).\n\n"
            "**Common mistakes:** checking roots against words in the other direction (looping over roots per word, "
            "O(roots * words)); picking the longest root instead of the shortest; splitting on whitespace in a way "
            "that drops the exact spacing the problem requires (single spaces here, so `split(' ')` and `join` are safe).\n\n"
            "**Interview follow-ups:** what if the sentence is a stream too large to hold (process word by word); "
            "replace with the longest root instead (keep walking and remember the last marker); handle "
            "case-insensitivity or punctuation; count how many words were replaced."
        ),
        "complexity": {"time": "O(total root characters + total sentence characters)", "space": "O(total root characters)"},
        "similar": ["implement-trie", "longest-word-in-dictionary", "design-add-and-search-words"],
    },
]
