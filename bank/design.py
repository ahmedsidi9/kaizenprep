"""Design pattern: data-structure design problems (LRU cache lives in seed.py)."""

# ---------------------------------------------------------------------------
# Long op sequences are built here so each test stays readable and the expected
# outputs are derived from the same construction (see comments per block).
# ---------------------------------------------------------------------------

# LFU: fill 100 keys (all freq 1), touch 0..49 (freq 2), then insert 50 more keys.
# Each new insert evicts the least-frequent, least-recently-used key: 50, 51, ..., 99 in order.
_LFU_LONG_OPS = (
    [["LFUCache", [100]]]
    + [["put", [i, i]] for i in range(100)]
    + [["get", [i]] for i in range(50)]
    + [["put", [i, i]] for i in range(100, 150)]
    + [["get", [i]] for i in range(50, 100)]
    + [["get", [i]] for i in range(50)]
    + [["get", [i]] for i in range(100, 150)]
)
_LFU_LONG_OUT = (
    [None]
    + [None] * 100
    + list(range(50))
    + [None] * 50
    + [-1] * 50
    + list(range(50))
    + list(range(100, 150))
)

# TimeMap: one key, values written at odd timestamps 1,3,...,999; query every t in 0..1000.
# The answer at t is the largest odd timestamp <= t (t itself if odd, t-1 if even), "" for t=0.
_TM_LONG_OPS = (
    [["TimeMap", []]]
    + [["set", ["k", str(t), t]] for t in range(1, 1001, 2)]
    + [["get", ["k", t]] for t in range(0, 1001)]
)
_TM_LONG_OUT = [None] + [None] * 500 + [""] + [str(t if t % 2 else t - 1) for t in range(1, 1001)]

# RandomizedSet: insert 0..299, re-insert (all False), remove evens then odds except 299.
_RS_LONG_OPS = (
    [["RandomizedSet", []]]
    + [["insert", [i]] for i in range(300)]
    + [["insert", [i]] for i in range(300)]
    + [["remove", [i]] for i in range(0, 300, 2)]
    + [["remove", [i]] for i in range(1, 299, 2)]
    + [["getRandom", []], ["remove", [299]], ["remove", [299]], ["insert", [7]], ["getRandom", []]]
)
_RS_LONG_OUT = (
    [None]
    + [True] * 300
    + [False] * 300
    + [True] * 150
    + [True] * 149
    + [299, True, False, True, 7]
)

# HitCounter: hit(t) then getHits(t) for t = 1..1000. Hits are at every second, so the
# 300-second window holds min(t, 300) hits.
_HC_LONG_OPS = (
    [["HitCounter", []]]
    + [op for t in range(1, 1001) for op in (["hit", [t]], ["getHits", [t]])]
    + [["getHits", [1299]], ["getHits", [1300]]]
)
_HC_LONG_OUT = [None] + [v for t in range(1, 1001) for v in (None, min(t, 300))] + [1, 0]

# Twitter: user 1 posts 1..200, user 2 posts 201..250, follow/unfollow, then an interleaved
# burst of 200 tweets from users 1 and 2 (1 no longer follows 2, so it sees only its own even ids)
# and a third user who follows both.
_TW_LONG_OPS = (
    [["Twitter", []]]
    + [["postTweet", [1, i]] for i in range(1, 201)]
    + [["getNewsFeed", [1]]]
    + [["postTweet", [2, i]] for i in range(201, 251)]
    + [["follow", [1, 2]], ["getNewsFeed", [1]], ["getNewsFeed", [2]], ["unfollow", [1, 2]], ["getNewsFeed", [1]]]
    + [op for i in range(100) for op in (["postTweet", [1, 1000 + 2 * i]], ["postTweet", [2, 1001 + 2 * i]])]
    + [["getNewsFeed", [1]], ["getNewsFeed", [3]], ["follow", [3, 1]], ["follow", [3, 2]], ["getNewsFeed", [3]]]
)
_TW_LONG_OUT = (
    [None]
    + [None] * 200
    + [list(range(200, 190, -1))]
    + [None] * 50
    + [None, list(range(250, 240, -1)), list(range(250, 240, -1)), None, list(range(200, 190, -1))]
    + [None] * 200
    + [list(range(1198, 1178, -2)), [], None, None, list(range(1199, 1189, -1))]
)

# BrowserHistory: visit p1..p500, step back one page at a time to the homepage,
# then step forward one page at a time to p500 again.
_BH_LONG_OPS = (
    [["BrowserHistory", ["home"]]]
    + [["visit", [f"p{i}"]] for i in range(1, 501)]
    + [["back", [1]] for _ in range(500)]
    + [["forward", [1]] for _ in range(500)]
    + [["forward", [1]], ["back", [1000]]]
)
_BH_LONG_OUT = (
    [None]
    + [None] * 500
    + [f"p{i}" for i in range(499, 0, -1)] + ["home"]
    + [f"p{i}" for i in range(1, 501)]
    + ["p500", "home"]
)

# MyQueue: push 0..499, pop everything in FIFO order, then 300 push/pop pairs on an empty queue.
_MQ_LONG_OPS = (
    [["MyQueue", []]]
    + [["push", [i]] for i in range(500)]
    + [["pop", []] for _ in range(500)]
    + [["empty", []]]
    + [op for i in range(300) for op in (["push", [i]], ["pop", []])]
    + [["empty", []]]
)
_MQ_LONG_OUT = (
    [None]
    + [None] * 500
    + list(range(500))
    + [True]
    + [v for i in range(300) for v in (None, i)]
    + [True]
)

# UndergroundSystem: rider i travels X -> Y in exactly i time units. After rider i checks out,
# the trips are 0,1,...,i, whose mean is i/2 (an integer or a .5, so exact as a float).
_US_LONG_OPS = (
    [["UndergroundSystem", []]]
    + [op for i in range(200) for op in (["checkIn", [i, "X", 0]], ["checkOut", [i, "Y", i]], ["getAverageTime", ["X", "Y"]])]
)
_US_LONG_OUT = [None] + [v for i in range(200) for v in (None, None, i / 2)]

# SnapshotArray: a single cell is set to i and snapped, 300 times; snap i must remember value i.
_SA_LONG_OPS = (
    [["SnapshotArray", [1]]]
    + [op for i in range(300) for op in (["set", [0, i]], ["snap", []])]
    + [["get", [0, s]] for s in range(300)]
)
_SA_LONG_OUT = [None] + [v for i in range(300) for v in (None, i)] + list(range(300))

# SnapshotArray: 500 cells set once, one snap, then every cell read back at snap 0 and snap 1.
_SA_WIDE_OPS = (
    [["SnapshotArray", [500]]]
    + [["set", [i, i]] for i in range(500)]
    + [["snap", []]]
    + [["set", [i, -1]] for i in range(0, 500, 2)]
    + [["snap", []]]
    + [["get", [i, 0]] for i in range(500)]
    + [["get", [i, 1]] for i in range(500)]
)
_SA_WIDE_OUT = (
    [None]
    + [None] * 500
    + [0]
    + [None] * 250
    + [1]
    + list(range(500))
    + [(-1 if i % 2 == 0 else i) for i in range(500)]
)


PROBLEMS = [
    {
        "id": "lfu-cache",
        "title": "LFU Cache",
        "difficulty": "Hard",
        "pattern": "Design",
        "tags": ["Hash Table", "Linked List", "Design", "Doubly-Linked List"],
        "companies": {"google": 3, "apple": 3, "meta": 2, "amazon": 4, "microsoft": 2},
        "kind": "design",
        "class_name": "LFUCache",
        "description": (
            "Build a cache with a fixed `capacity` that evicts the **least frequently used** key when it is full.\n\n"
            "- `LFUCache(capacity)` creates an empty cache.\n"
            "- `get(key)` returns the stored value, or `-1` if the key is absent.\n"
            "- `put(key, value)` inserts the key or overwrites its value. If inserting a new key would exceed the "
            "capacity, first evict the key with the smallest use count. If several keys share the smallest count, "
            "evict the one among them that was **least recently** used.\n\n"
            "A key's use count starts at 1 when it is inserted and increases by one on every `get` and every `put` "
            "that touches it. Both operations must run in **O(1)** average time. A capacity of 0 means nothing is ever stored."
        ),
        "examples": [
            {
                "input": "[\"LFUCache\",\"put\",\"put\",\"get\",\"put\",\"get\",\"get\",\"put\",\"get\",\"get\",\"get\"]\n"
                         "[[2],[1,1],[2,2],[1],[3,3],[2],[3],[4,4],[1],[3],[4]]",
                "output": "[null,null,null,1,null,-1,3,null,-1,3,4]",
                "explanation": "put(3,3) evicts key 2 (count 1, while key 1 has count 2). put(4,4) sees keys 1 and 3 both at "
                               "count 2 and evicts key 1 because key 3 was used more recently.",
            },
            {
                "input": "[\"LFUCache\",\"put\",\"get\"]\n[[0],[0,0],[0]]",
                "output": "[null,null,-1]",
                "explanation": "With capacity 0 nothing is stored.",
            },
        ],
        "constraints": ["0 <= capacity <= 10^4", "0 <= key <= 10^5", "0 <= value <= 10^9", "At most 2 * 10^5 calls to get and put."],
        "hints": [
            "You need to find the minimum frequency in O(1) and, within that frequency, the least recently used key in O(1).",
            "Keep one recency-ordered structure per frequency: a map frequency -> OrderedDict (or doubly linked list) of keys.",
            "Track `min_freq`. When a key moves from frequency f to f+1 and bucket f becomes empty, and f was the minimum, "
            "the new minimum is exactly f+1. A fresh insert always resets min_freq to 1.",
        ],
        "starter": (
            "class LFUCache:\n"
            "    def __init__(self, capacity: int):\n"
            "        pass\n\n"
            "    def get(self, key: int) -> int:\n"
            "        pass\n\n"
            "    def put(self, key: int, value: int) -> None:\n"
            "        pass\n"
        ),
        "compare": "exact",
        "tests": [
            {"input": {"ops": [["LFUCache", [2]], ["put", [1, 1]], ["put", [2, 2]], ["get", [1]], ["put", [3, 3]], ["get", [2]],
                               ["get", [3]], ["put", [4, 4]], ["get", [1]], ["get", [3]], ["get", [4]]]},
             "output": [None, None, None, 1, None, -1, 3, None, -1, 3, 4]},
            {"input": {"ops": [["LFUCache", [0]], ["put", [0, 0]], ["get", [0]]]},
             "output": [None, None, -1]},
            {"input": {"ops": [["LFUCache", [2]], ["put", [1, 1]], ["put", [2, 2]], ["put", [1, 10]], ["put", [3, 3]],
                               ["get", [1]], ["get", [2]], ["get", [3]]]},
             "output": [None, None, None, None, None, 10, -1, 3]},
            {"input": {"ops": [["LFUCache", [2]], ["put", [1, 1]], ["put", [2, 2]], ["get", [1]], ["get", [2]], ["put", [3, 3]],
                               ["get", [1]], ["get", [2]], ["get", [3]]]},
             "output": [None, None, None, 1, 2, None, -1, 2, 3]},
            {"input": {"ops": [["LFUCache", [1]], ["put", [1, 1]], ["get", [1]], ["get", [1]], ["put", [2, 2]], ["get", [1]], ["get", [2]]]},
             "output": [None, None, 1, 1, None, -1, 2]},
            {"input": {"ops": _LFU_LONG_OPS}, "output": _LFU_LONG_OUT},
        ],
        "solution": (
            "class LFUCache:\n"
            "    def __init__(self, capacity: int):\n"
            "        self.cap = capacity\n"
            "        self.vals = {}            # key -> value\n"
            "        self.freq = {}            # key -> use count\n"
            "        self.buckets = defaultdict(OrderedDict)  # count -> keys in recency order (oldest first)\n"
            "        self.min_freq = 0\n\n"
            "    def _touch(self, key: int) -> None:\n"
            "        f = self.freq[key]\n"
            "        del self.buckets[f][key]\n"
            "        if not self.buckets[f]:\n"
            "            del self.buckets[f]\n"
            "            if self.min_freq == f:\n"
            "                self.min_freq = f + 1\n"
            "        self.freq[key] = f + 1\n"
            "        self.buckets[f + 1][key] = None\n\n"
            "    def get(self, key: int) -> int:\n"
            "        if key not in self.vals:\n"
            "            return -1\n"
            "        self._touch(key)\n"
            "        return self.vals[key]\n\n"
            "    def put(self, key: int, value: int) -> None:\n"
            "        if self.cap == 0:\n"
            "            return\n"
            "        if key in self.vals:\n"
            "            self.vals[key] = value\n"
            "            self._touch(key)\n"
            "            return\n"
            "        if len(self.vals) == self.cap:\n"
            "            old, _ = self.buckets[self.min_freq].popitem(last=False)\n"
            "            if not self.buckets[self.min_freq]:\n"
            "                del self.buckets[self.min_freq]\n"
            "            del self.vals[old], self.freq[old]\n"
            "        self.vals[key] = value\n"
            "        self.freq[key] = 1\n"
            "        self.buckets[1][key] = None\n"
            "        self.min_freq = 1\n"
        ),
        "approach": (
            "**Key insight: group keys by frequency, and keep each group in recency order.** LRU needs one ordered "
            "list; LFU needs one ordered list *per frequency* plus a pointer to the smallest frequency currently in use.\n\n"
            "Data structures: `vals` (key -> value), `freq` (key -> count), `buckets` (count -> OrderedDict of keys, oldest "
            "first; a hand-rolled doubly linked list works the same way), and `min_freq`. Every touch of a key removes it "
            "from bucket `f` and appends it to bucket `f+1`. If bucket `f` became empty and `f == min_freq`, the minimum is "
            "now `f+1`, because the key we just moved is the only candidate. A brand-new insert always has count 1, so "
            "`min_freq` resets to 1 after any insert.\n\n"
            "Eviction pops the oldest entry of `buckets[min_freq]`. Every step is a dictionary operation, so `get` and "
            "`put` are O(1).\n\n"
            "**Common mistakes:** forgetting that `put` on an existing key also counts as a use; not handling capacity 0; "
            "evicting *before* checking whether the key already exists (which can wrongly evict something when updating); "
            "trying to find `min_freq` by scanning, which makes operations O(number of distinct frequencies).\n\n"
            "**Interview follow-ups:** How would you make this thread safe? (one lock around each public method is simplest; "
            "finer-grained locking is hard because `min_freq` is shared state.) How would you add TTL expiry? (store an "
            "expiry timestamp per key and treat expired keys as misses, lazily deleting them.) What about memory for keys "
            "with huge frequencies? (counts only grow; a decay or aging scheme such as periodically halving all counts keeps "
            "old hot keys from pinning the cache forever, which is what real LFU-style caches like Redis' approximate LFU do.)"
        ),
        "complexity": {"time": "O(1) per operation", "space": "O(capacity)"},
        "similar": ["lru-cache", "design-hit-counter"],
    },
    {
        "id": "time-based-key-value-store",
        "title": "Time Based Key-Value Store",
        "difficulty": "Medium",
        "pattern": "Design",
        "tags": ["Hash Table", "Binary Search", "Design", "String"],
        "companies": {"google": 3, "apple": 2, "meta": 2, "amazon": 3, "microsoft": 1},
        "kind": "design",
        "class_name": "TimeMap",
        "description": (
            "Design a key-value store where every write carries a timestamp and reads ask for the value as of a given time.\n\n"
            "- `TimeMap()` creates an empty store.\n"
            "- `set(key, value, timestamp)` records that `key` had `value` at time `timestamp`.\n"
            "- `get(key, timestamp)` returns the value written to `key` with the **largest timestamp that is "
            "less than or equal to** `timestamp`. If no such write exists, return `\"\"`.\n\n"
            "For a given key, the timestamps passed to `set` are strictly increasing."
        ),
        "examples": [
            {
                "input": "[\"TimeMap\",\"set\",\"get\",\"get\",\"set\",\"get\",\"get\"]\n"
                         "[[],[\"foo\",\"bar\",1],[\"foo\",1],[\"foo\",3],[\"foo\",\"bar2\",4],[\"foo\",4],[\"foo\",5]]",
                "output": "[null,null,\"bar\",\"bar\",null,\"bar2\",\"bar2\"]",
                "explanation": "At time 3 the latest write to foo is still the one from time 1. From time 4 onwards it is bar2.",
            },
            {
                "input": "[\"TimeMap\",\"set\",\"get\",\"get\"]\n[[],[\"a\",\"x\",5],[\"a\",4],[\"b\",5]]",
                "output": "[null,null,\"\",\"\"]",
                "explanation": "Nothing was written to a before time 5, and key b does not exist.",
            },
        ],
        "constraints": [
            "1 <= key.length, value.length <= 100",
            "key and value consist of lowercase letters and digits",
            "1 <= timestamp <= 10^7",
            "Timestamps for set calls on the same key are strictly increasing",
            "At most 2 * 10^5 calls to set and get",
        ],
        "hints": [
            "Each key needs to remember its whole history, not just the latest value.",
            "Because set timestamps are strictly increasing per key, appending to a list keeps that list sorted for free.",
            "On get, binary search the key's timestamp list for the rightmost entry <= timestamp (bisect_right minus one).",
        ],
        "starter": (
            "class TimeMap:\n"
            "    def __init__(self):\n"
            "        pass\n\n"
            "    def set(self, key: str, value: str, timestamp: int) -> None:\n"
            "        pass\n\n"
            "    def get(self, key: str, timestamp: int) -> str:\n"
            "        pass\n"
        ),
        "compare": "exact",
        "tests": [
            {"input": {"ops": [["TimeMap", []], ["set", ["foo", "bar", 1]], ["get", ["foo", 1]], ["get", ["foo", 3]],
                               ["set", ["foo", "bar2", 4]], ["get", ["foo", 4]], ["get", ["foo", 5]]]},
             "output": [None, None, "bar", "bar", None, "bar2", "bar2"]},
            {"input": {"ops": [["TimeMap", []], ["set", ["a", "x", 5]], ["get", ["a", 4]], ["get", ["b", 5]]]},
             "output": [None, None, "", ""]},
            {"input": {"ops": [["TimeMap", []], ["get", ["missing", 1]], ["set", ["k", "v1", 10]], ["set", ["k", "v2", 20]],
                               ["set", ["k", "v3", 30]], ["get", ["k", 9]], ["get", ["k", 10]], ["get", ["k", 19]],
                               ["get", ["k", 25]], ["get", ["k", 30]], ["get", ["k", 10000000]]]},
             "output": [None, "", None, None, None, "", "v1", "v1", "v2", "v3", "v3"]},
            {"input": {"ops": [["TimeMap", []], ["set", ["a", "1", 1]], ["set", ["b", "2", 2]], ["get", ["a", 2]], ["get", ["b", 1]],
                               ["get", ["b", 2]]]},
             "output": [None, None, None, "1", "", "2"]},
            {"input": {"ops": _TM_LONG_OPS}, "output": _TM_LONG_OUT},
        ],
        "solution": (
            "class TimeMap:\n"
            "    def __init__(self):\n"
            "        self.times = defaultdict(list)   # key -> sorted timestamps\n"
            "        self.values = defaultdict(list)  # key -> values, parallel to times\n\n"
            "    def set(self, key: str, value: str, timestamp: int) -> None:\n"
            "        self.times[key].append(timestamp)\n"
            "        self.values[key].append(value)\n\n"
            "    def get(self, key: str, timestamp: int) -> str:\n"
            "        if key not in self.times:\n"
            "            return ''\n"
            "        i = bisect_right(self.times[key], timestamp)\n"
            "        return self.values[key][i - 1] if i else ''\n"
        ),
        "approach": (
            "**Key insight: the history of each key is already sorted, so reads are a binary search.** Writes arrive "
            "with strictly increasing timestamps per key, which means appending to a per-key list keeps it sorted with "
            "no extra work.\n\n"
            "Keep a dictionary from key to two parallel lists (timestamps and values), or a single list of pairs. `set` is "
            "an O(1) append. `get` uses `bisect_right(times, timestamp)`, which returns how many stored timestamps are "
            "<= the query; if that count is zero the key had no value yet, otherwise the answer is at index `count - 1`.\n\n"
            "**Common mistakes:** using `bisect_left`, which returns the wrong index when the query equals a stored timestamp; "
            "returning the most recent value regardless of the query time; linear scans, which are O(n) per get and time out "
            "under 2 * 10^5 calls.\n\n"
            "**Interview follow-ups:** What if timestamps are *not* guaranteed increasing? (use `insort` for O(n) inserts, or a "
            "balanced tree / sorted containers for O(log n).) How would you scale this past one machine? (shard by key; each "
            "shard keeps its own sorted history. This is essentially how versioned KV stores and MVCC work.) How would you bound "
            "memory? (retention policy: drop versions older than a cutoff, or keep only the last k versions per key.)"
        ),
        "complexity": {"time": "O(1) set, O(log n) get where n is the number of writes to that key", "space": "O(total writes)"},
        "similar": ["snapshot-array", "lru-cache"],
    },
    {
        "id": "insert-delete-getrandom-o1",
        "title": "Insert Delete GetRandom O(1)",
        "difficulty": "Medium",
        "pattern": "Design",
        "tags": ["Array", "Hash Table", "Math", "Design", "Randomized"],
        "companies": {"google": 3, "apple": 3, "meta": 4, "amazon": 3, "microsoft": 3},
        "kind": "design",
        "class_name": "RandomizedSet",
        "description": (
            "Implement a set of integers that supports three operations in **average O(1)** time:\n\n"
            "- `RandomizedSet()` creates an empty set.\n"
            "- `insert(val)` adds `val` and returns `true`; returns `false` if it was already present.\n"
            "- `remove(val)` deletes `val` and returns `true`; returns `false` if it was not present.\n"
            "- `getRandom()` returns one of the current elements, each with equal probability. It is only called when "
            "the set is non-empty.\n\n"
            "Because `getRandom` is random, the judge only calls it when the set contains **exactly one element**, so its "
            "output is determined. Your implementation must still be uniformly random in general."
        ),
        "examples": [
            {
                "input": "[\"RandomizedSet\",\"insert\",\"remove\",\"insert\",\"remove\",\"getRandom\",\"insert\",\"remove\",\"insert\",\"getRandom\"]\n"
                         "[[],[1],[2],[2],[1],[],[2],[2],[5],[]]",
                "output": "[null,true,false,true,true,2,false,true,true,5]",
                "explanation": "remove(2) fails before 2 is inserted. After removing 1 the only element is 2, so getRandom returns 2. "
                               "Inserting 2 again fails because it is already present.",
            },
        ],
        "constraints": ["-2^31 <= val <= 2^31 - 1", "At most 2 * 10^5 calls in total", "getRandom is only called on a non-empty set"],
        "hints": [
            "A hash set gives O(1) insert and remove, but picking a uniformly random element from it is not O(1). An array gives O(1) random access but O(n) removal.",
            "Use both: a list of values and a dict from value to its index in the list.",
            "To remove in O(1), swap the element with the last element of the list, fix the dict entry of the moved element, then pop.",
        ],
        "starter": (
            "class RandomizedSet:\n"
            "    def __init__(self):\n"
            "        pass\n\n"
            "    def insert(self, val: int) -> bool:\n"
            "        pass\n\n"
            "    def remove(self, val: int) -> bool:\n"
            "        pass\n\n"
            "    def getRandom(self) -> int:\n"
            "        pass\n"
        ),
        "compare": "exact",
        "tests": [
            {"input": {"ops": [["RandomizedSet", []], ["insert", [1]], ["remove", [2]], ["insert", [2]], ["remove", [1]], ["getRandom", []],
                               ["insert", [2]], ["remove", [2]], ["insert", [5]], ["getRandom", []]]},
             "output": [None, True, False, True, True, 2, False, True, True, 5]},
            {"input": {"ops": [["RandomizedSet", []], ["remove", [0]], ["insert", [0]], ["insert", [0]], ["getRandom", []], ["remove", [0]], ["remove", [0]]]},
             "output": [None, False, True, False, 0, True, False]},
            {"input": {"ops": [["RandomizedSet", []], ["insert", [10]], ["insert", [20]], ["insert", [30]], ["remove", [20]], ["remove", [10]],
                               ["getRandom", []], ["remove", [30]], ["remove", [30]], ["insert", [20]], ["getRandom", []]]},
             "output": [None, True, True, True, True, True, 30, True, False, True, 20]},
            {"input": {"ops": [["RandomizedSet", []], ["insert", [-5]], ["insert", [2147483647]], ["remove", [-5]], ["getRandom", []],
                               ["insert", [-5]], ["remove", [2147483647]], ["getRandom", []]]},
             "output": [None, True, True, True, 2147483647, True, True, -5]},
            {"input": {"ops": [["RandomizedSet", []], ["insert", [1]], ["insert", [2]], ["insert", [3]], ["remove", [1]], ["remove", [3]],
                               ["getRandom", []], ["insert", [1]], ["remove", [2]], ["getRandom", []]]},
             "output": [None, True, True, True, True, True, 2, True, True, 1]},
            {"input": {"ops": _RS_LONG_OPS}, "output": _RS_LONG_OUT},
        ],
        "solution": (
            "class RandomizedSet:\n"
            "    def __init__(self):\n"
            "        self.vals = []      # the elements, in arbitrary order\n"
            "        self.pos = {}       # value -> index in self.vals\n\n"
            "    def insert(self, val: int) -> bool:\n"
            "        if val in self.pos:\n"
            "            return False\n"
            "        self.pos[val] = len(self.vals)\n"
            "        self.vals.append(val)\n"
            "        return True\n\n"
            "    def remove(self, val: int) -> bool:\n"
            "        if val not in self.pos:\n"
            "            return False\n"
            "        i, last = self.pos[val], self.vals[-1]\n"
            "        self.vals[i] = last\n"
            "        self.pos[last] = i\n"
            "        self.vals.pop()\n"
            "        del self.pos[val]\n"
            "        return True\n\n"
            "    def getRandom(self) -> int:\n"
            "        return random.choice(self.vals)\n"
        ),
        "approach": (
            "**Key insight: a dynamic array plus an index map.** Uniform random choice needs O(1) access by position, which "
            "only an array provides. Deleting from the middle of an array is O(n), unless you do not care about order: "
            "overwrite the removed slot with the last element and pop the tail.\n\n"
            "`vals` holds the elements; `pos[v]` is the index of `v` inside `vals`. Insert appends and records the index. "
            "Remove looks up the index `i`, copies the last element into slot `i`, updates that element's index to `i`, pops "
            "the list and deletes the removed value from the map. `getRandom` is `random.choice(vals)`, which is uniform "
            "because every element occupies exactly one slot.\n\n"
            "**Common mistakes:** updating the map for the moved element *after* deleting the removed key when both are the same "
            "value (removing the last element); when `val` is the tail, the swap is a no-op and the code must still work, which "
            "the order above guarantees. Using `list.remove(val)` or `list.index(val)` silently makes remove O(n).\n\n"
            "**Interview follow-ups:** Allow duplicates (`RandomizedCollection`): map each value to a *set* of indices. Weighted "
            "random pick: prefix sums plus binary search, O(log n) per pick. Thread safety: a single lock is fine; lock-free "
            "variants are hard because remove mutates two structures that must stay consistent."
        ),
        "complexity": {"time": "O(1) average per operation", "space": "O(n)"},
        "similar": ["lru-cache", "design-hit-counter"],
    },
    {
        "id": "design-hit-counter",
        "title": "Design Hit Counter",
        "difficulty": "Medium",
        "pattern": "Design",
        "tags": ["Array", "Queue", "Design", "Binary Search", "Data Stream"],
        "companies": {"google": 3, "apple": 3, "meta": 2, "amazon": 3, "microsoft": 2},
        "kind": "design",
        "class_name": "HitCounter",
        "description": (
            "Design a counter that reports how many hits were received in the **last 5 minutes (300 seconds)**.\n\n"
            "- `HitCounter()` creates the counter.\n"
            "- `hit(timestamp)` records one hit at the given second. Several hits may share a timestamp.\n"
            "- `getHits(timestamp)` returns the number of hits in the window `[timestamp - 299, timestamp]`.\n\n"
            "Timestamps are given in seconds and every call, whether `hit` or `getHits`, arrives in chronological "
            "(non-decreasing) order."
        ),
        "examples": [
            {
                "input": "[\"HitCounter\",\"hit\",\"hit\",\"hit\",\"getHits\",\"hit\",\"getHits\",\"getHits\"]\n[[],[1],[2],[3],[4],[300],[300],[301]]",
                "output": "[null,null,null,null,3,null,4,3]",
                "explanation": "At 300 the window is [1, 300] and holds four hits. At 301 the window is [2, 301], so the hit at 1 has expired.",
            },
            {
                "input": "[\"HitCounter\",\"hit\",\"hit\",\"getHits\",\"getHits\"]\n[[],[7],[7],[7],[307]]",
                "output": "[null,null,null,2,0]",
                "explanation": "Two hits at the same second both count. At 307 the window is [8, 307] and is empty.",
            },
        ],
        "constraints": ["1 <= timestamp <= 2 * 10^9", "Calls arrive with non-decreasing timestamps", "At most 300 calls to hit and getHits"],
        "hints": [
            "Only hits from the last 300 seconds ever matter; everything older can be thrown away.",
            "Since timestamps arrive in order, a queue of hit timestamps is naturally sorted. On getHits, pop from the front while the front is too old.",
            "For O(1) memory regardless of hit volume, keep 300 buckets of (timestamp, count) indexed by timestamp % 300 and reset a bucket when its stored timestamp differs.",
        ],
        "starter": (
            "class HitCounter:\n"
            "    def __init__(self):\n"
            "        pass\n\n"
            "    def hit(self, timestamp: int) -> None:\n"
            "        pass\n\n"
            "    def getHits(self, timestamp: int) -> int:\n"
            "        pass\n"
        ),
        "compare": "exact",
        "tests": [
            {"input": {"ops": [["HitCounter", []], ["hit", [1]], ["hit", [2]], ["hit", [3]], ["getHits", [4]], ["hit", [300]], ["getHits", [300]], ["getHits", [301]]]},
             "output": [None, None, None, None, 3, None, 4, 3]},
            {"input": {"ops": [["HitCounter", []], ["hit", [7]], ["hit", [7]], ["getHits", [7]], ["getHits", [307]]]},
             "output": [None, None, None, 2, 0]},
            {"input": {"ops": [["HitCounter", []], ["getHits", [1]], ["getHits", [1000]]]},
             "output": [None, 0, 0]},
            {"input": {"ops": [["HitCounter", []], ["hit", [1]], ["getHits", [300]], ["getHits", [301]], ["hit", [301]], ["getHits", [301]], ["getHits", [600]], ["getHits", [601]]]},
             "output": [None, None, 1, 0, None, 1, 1, 0]},
            {"input": {"ops": [["HitCounter", []], ["hit", [5]], ["hit", [5]], ["hit", [5]], ["hit", [200]], ["getHits", [304]], ["getHits", [305]], ["getHits", [499]], ["getHits", [500]]]},
             "output": [None, None, None, None, None, 4, 1, 1, 0]},
            {"input": {"ops": _HC_LONG_OPS}, "output": _HC_LONG_OUT},
        ],
        "solution": (
            "class HitCounter:\n"
            "    WINDOW = 300\n\n"
            "    def __init__(self):\n"
            "        self.q = deque()   # (timestamp, count) pairs, oldest first\n"
            "        self.total = 0\n\n"
            "    def hit(self, timestamp: int) -> None:\n"
            "        if self.q and self.q[-1][0] == timestamp:\n"
            "            self.q[-1][1] += 1\n"
            "        else:\n"
            "            self.q.append([timestamp, 1])\n"
            "        self.total += 1\n\n"
            "    def getHits(self, timestamp: int) -> int:\n"
            "        while self.q and self.q[0][0] <= timestamp - self.WINDOW:\n"
            "            self.total -= self.q.popleft()[1]\n"
            "        return self.total\n"
        ),
        "approach": (
            "**Key insight: the stream is chronological, so a queue of hits is automatically sorted and expiring old hits "
            "is just popping from the front.** Keep a deque of `(timestamp, count)` pairs and a running total. `hit` either "
            "bumps the count of the last pair (same second) or appends a new pair. `getHits` pops pairs whose timestamp is "
            "`<= timestamp - 300` and returns the total.\n\n"
            "Each hit is pushed once and popped at most once, so the work is amortised O(1) per call. Grouping hits by "
            "second bounds the deque at 300 entries no matter how many hits arrive.\n\n"
            "The classic O(1)-memory alternative is a circular buffer of 300 slots: `times[t % 300]` and `counts[t % 300]`. "
            "On `hit`, if the stored time differs from `t`, reset the slot. On `getHits`, sum the counts of the slots whose "
            "stored time is inside the window, which is 300 additions regardless of volume.\n\n"
            "**Common mistakes:** off-by-one on the window (`timestamp - 300` must be excluded, `timestamp - 299` included); "
            "forgetting to evict inside `getHits` when no `hit` happened recently; popping on `hit` only, which leaves stale "
            "data if `getHits` is called far in the future.\n\n"
            "**Interview follow-ups:** What if hits arrive out of order? (keep a sorted structure or bucket by second and sum.) "
            "What if there are millions of hits per second? (the bucket-per-second array is the answer; counts, not individual "
            "events.) Concurrency: a lock per call, or atomic counters per bucket; for a distributed counter, shard by server "
            "and sum on read, accepting slight staleness."
        ),
        "complexity": {"time": "O(1) amortised per call (O(300) worst case for the bucket variant)", "space": "O(300) = O(1)"},
        "similar": ["moving-average-from-data-stream", "lru-cache"],
    },
    {
        "id": "design-twitter",
        "title": "Design Twitter",
        "difficulty": "Medium",
        "pattern": "Design",
        "tags": ["Hash Table", "Linked List", "Design", "Heap / Priority Queue"],
        "companies": {"google": 2, "apple": 2, "meta": 3, "amazon": 4, "microsoft": 2},
        "kind": "design",
        "class_name": "Twitter",
        "description": (
            "Design a tiny social network with posts, follows and a news feed.\n\n"
            "- `Twitter()` creates the service.\n"
            "- `postTweet(userId, tweetId)` publishes a tweet. Each `tweetId` is unique.\n"
            "- `getNewsFeed(userId)` returns the ids of the **10 most recent** tweets written by the user or by anyone they "
            "follow, newest first. Fewer than 10 are returned if that is all there is.\n"
            "- `follow(followerId, followeeId)` makes the first user follow the second.\n"
            "- `unfollow(followerId, followeeId)` undoes a follow. Unfollowing someone you do not follow does nothing.\n\n"
            "Users always see their own tweets in their feed, and user ids are created implicitly the first time they appear."
        ),
        "examples": [
            {
                "input": "[\"Twitter\",\"postTweet\",\"getNewsFeed\",\"follow\",\"postTweet\",\"getNewsFeed\",\"unfollow\",\"getNewsFeed\"]\n"
                         "[[],[1,5],[1],[1,2],[2,6],[1],[1,2],[1]]",
                "output": "[null,null,[5],null,null,[6,5],null,[5]]",
                "explanation": "After following user 2, user 1 sees tweet 6 (newer) before their own tweet 5. After unfollowing, only tweet 5 remains.",
            },
            {
                "input": "[\"Twitter\",\"getNewsFeed\",\"follow\",\"postTweet\",\"getNewsFeed\"]\n[[],[9],[9,9],[9,1],[9]]",
                "output": "[null,[],null,null,[1]]",
                "explanation": "A brand-new user has an empty feed. Following yourself must not duplicate your own tweets.",
            },
        ],
        "constraints": ["1 <= userId, followerId, followeeId <= 500", "0 <= tweetId <= 10^4", "All tweet ids are distinct", "At most 3 * 10^4 calls in total"],
        "hints": [
            "Stamp every tweet with a global, increasing counter so recency can be compared across users.",
            "Store each user's tweets in a list (newest at the end) and their followees in a set.",
            "The feed is a k-way merge of the followees' tweet lists: push each followee's most recent tweet into a max-heap and pop 10 times, pushing the next tweet of the same user after each pop.",
        ],
        "starter": (
            "class Twitter:\n"
            "    def __init__(self):\n"
            "        pass\n\n"
            "    def postTweet(self, userId: int, tweetId: int) -> None:\n"
            "        pass\n\n"
            "    def getNewsFeed(self, userId: int) -> List[int]:\n"
            "        pass\n\n"
            "    def follow(self, followerId: int, followeeId: int) -> None:\n"
            "        pass\n\n"
            "    def unfollow(self, followerId: int, followeeId: int) -> None:\n"
            "        pass\n"
        ),
        "compare": "exact",
        "tests": [
            {"input": {"ops": [["Twitter", []], ["postTweet", [1, 5]], ["getNewsFeed", [1]], ["follow", [1, 2]], ["postTweet", [2, 6]],
                               ["getNewsFeed", [1]], ["unfollow", [1, 2]], ["getNewsFeed", [1]]]},
             "output": [None, None, [5], None, None, [6, 5], None, [5]]},
            {"input": {"ops": [["Twitter", []], ["getNewsFeed", [9]], ["follow", [9, 9]], ["postTweet", [9, 1]], ["getNewsFeed", [9]]]},
             "output": [None, [], None, None, [1]]},
            {"input": {"ops": [["Twitter", []], ["follow", [1, 1]], ["unfollow", [1, 1]], ["postTweet", [1, 1]], ["unfollow", [1, 2]], ["getNewsFeed", [1]]]},
             "output": [None, None, None, None, None, [1]]},
            {"input": {"ops": [["Twitter", []], ["postTweet", [1, 10]], ["postTweet", [2, 20]], ["postTweet", [3, 30]], ["follow", [1, 2]],
                               ["follow", [1, 3]], ["getNewsFeed", [1]], ["getNewsFeed", [2]], ["unfollow", [1, 3]], ["getNewsFeed", [1]]]},
             "output": [None, None, None, None, None, None, [30, 20, 10], [20], None, [20, 10]]},
            {"input": {"ops": [["Twitter", []]] + [["postTweet", [1, i]] for i in range(12)] + [["getNewsFeed", [1]], ["getNewsFeed", [2]], ["follow", [2, 1]], ["getNewsFeed", [2]]]},
             "output": [None] + [None] * 12 + [list(range(11, 1, -1)), [], None, list(range(11, 1, -1))]},
            {"input": {"ops": _TW_LONG_OPS}, "output": _TW_LONG_OUT},
        ],
        "solution": (
            "class Twitter:\n"
            "    FEED_SIZE = 10\n\n"
            "    def __init__(self):\n"
            "        self.clock = 0\n"
            "        self.tweets = defaultdict(list)     # userId -> [(time, tweetId)], oldest first\n"
            "        self.following = defaultdict(set)   # userId -> set of followee ids\n\n"
            "    def postTweet(self, userId: int, tweetId: int) -> None:\n"
            "        self.tweets[userId].append((self.clock, tweetId))\n"
            "        self.clock += 1\n\n"
            "    def getNewsFeed(self, userId: int) -> List[int]:\n"
            "        heap = []\n"
            "        for uid in self.following[userId] | {userId}:\n"
            "            posts = self.tweets[uid]\n"
            "            if posts:\n"
            "                t, tid = posts[-1]\n"
            "                heap.append((-t, tid, uid, len(posts) - 1))\n"
            "        heapify(heap)\n"
            "        feed = []\n"
            "        while heap and len(feed) < self.FEED_SIZE:\n"
            "            _, tid, uid, idx = heappop(heap)\n"
            "            feed.append(tid)\n"
            "            if idx > 0:\n"
            "                t, nxt = self.tweets[uid][idx - 1]\n"
            "                heappush(heap, (-t, nxt, uid, idx - 1))\n"
            "        return feed\n\n"
            "    def follow(self, followerId: int, followeeId: int) -> None:\n"
            "        if followerId != followeeId:\n"
            "            self.following[followerId].add(followeeId)\n\n"
            "    def unfollow(self, followerId: int, followeeId: int) -> None:\n"
            "        self.following[followerId].discard(followeeId)\n"
        ),
        "approach": (
            "**Key insight: a news feed is a k-way merge of already-sorted per-user timelines.** Each user's tweets are "
            "appended in time order, so the newest tweet of each followee is at the end of their list. A max-heap seeded "
            "with one entry per followee lets you pull the globally newest tweet, then push that user's next-newest, exactly "
            "like merging k sorted lists. Because the feed stops after 10 items, at most 10 pops happen.\n\n"
            "A global counter gives tweets a total order (wall-clock time can collide). `following` is a set per user so "
            "follow and unfollow are O(1) and duplicates are impossible. Guarding `follow(u, u)` prevents a user appearing twice "
            "in the merge; the solution unions `{userId}` in at read time so users always see their own posts.\n\n"
            "**Common mistakes:** returning oldest first; letting a self-follow cause duplicate tweets in the feed; scanning and "
            "sorting *all* tweets of all followees on every feed call, which is O(total tweets log total) instead of O(k + 10 log k); "
            "unfollow raising on a missing followee (use `discard`).\n\n"
            "**Interview follow-ups:** Fan-out on write vs fan-out on read: for users with millions of followers, precomputing feeds "
            "(pushing each tweet into followers' feed caches) explodes; real systems mix both, pushing for normal users and pulling "
            "for celebrities. How would you cap memory? (keep only the last N tweets per user in the hot store.) Pagination: pass "
            "the timestamp of the last item seen and merge from there."
        ),
        "complexity": {"time": "O(1) post/follow/unfollow; O(k + 10 log k) per feed where k is the number of followees", "space": "O(tweets + follow edges)"},
        "similar": ["merge-k-sorted-lists", "lru-cache"],
    },
    {
        "id": "design-browser-history",
        "title": "Design Browser History",
        "difficulty": "Medium",
        "pattern": "Design",
        "tags": ["Array", "Stack", "Design", "Doubly-Linked List"],
        "companies": {"google": 1, "apple": 2, "meta": 1, "amazon": 2, "microsoft": 2},
        "kind": "design",
        "class_name": "BrowserHistory",
        "description": (
            "Model the back and forward buttons of a single browser tab.\n\n"
            "- `BrowserHistory(homepage)` opens the tab on `homepage`.\n"
            "- `visit(url)` navigates to `url` from the current page. Any pages that were ahead in the forward history are discarded.\n"
            "- `back(steps)` moves back up to `steps` pages. If there are fewer than `steps` pages behind, you stop at the oldest page. Returns the current url afterwards.\n"
            "- `forward(steps)` moves forward up to `steps` pages, stopping at the newest page if there are fewer. Returns the current url afterwards."
        ),
        "examples": [
            {
                "input": "[\"BrowserHistory\",\"visit\",\"visit\",\"visit\",\"back\",\"back\",\"forward\",\"visit\",\"forward\",\"back\",\"back\"]\n"
                         "[[\"home.com\"],[\"a.com\"],[\"b.com\"],[\"c.com\"],[1],[1],[1],[\"d.com\"],[2],[2],[7]]",
                "output": "[null,null,null,null,\"b.com\",\"a.com\",\"b.com\",null,\"d.com\",\"a.com\",\"home.com\"]",
                "explanation": "Visiting d.com from b.com throws away c.com, so forward(2) has nowhere to go and stays on d.com. "
                               "back(7) is clamped at the homepage.",
            },
            {
                "input": "[\"BrowserHistory\",\"back\",\"forward\",\"visit\",\"back\",\"forward\"]\n[[\"x\"],[3],[3],[\"y\"],[1],[5]]",
                "output": "[null,\"x\",\"x\",null,\"x\",\"y\"]",
            },
        ],
        "constraints": ["1 <= homepage.length, url.length <= 20", "1 <= steps <= 100", "At most 5000 calls in total"],
        "hints": [
            "Two stacks (back and forward) work: visit pushes onto back and clears forward. But clearing is O(size).",
            "A single array with a `current` index makes back and forward simple index arithmetic clamped to the valid range.",
            "To make visit O(1) too, keep an `end` index marking the last valid page instead of physically truncating the array; visit overwrites position current+1 and sets end to it.",
        ],
        "starter": (
            "class BrowserHistory:\n"
            "    def __init__(self, homepage: str):\n"
            "        pass\n\n"
            "    def visit(self, url: str) -> None:\n"
            "        pass\n\n"
            "    def back(self, steps: int) -> str:\n"
            "        pass\n\n"
            "    def forward(self, steps: int) -> str:\n"
            "        pass\n"
        ),
        "compare": "exact",
        "tests": [
            {"input": {"ops": [["BrowserHistory", ["home.com"]], ["visit", ["a.com"]], ["visit", ["b.com"]], ["visit", ["c.com"]], ["back", [1]],
                               ["back", [1]], ["forward", [1]], ["visit", ["d.com"]], ["forward", [2]], ["back", [2]], ["back", [7]]]},
             "output": [None, None, None, None, "b.com", "a.com", "b.com", None, "d.com", "a.com", "home.com"]},
            {"input": {"ops": [["BrowserHistory", ["x"]], ["back", [3]], ["forward", [3]], ["visit", ["y"]], ["back", [1]], ["forward", [5]]]},
             "output": [None, "x", "x", None, "x", "y"]},
            {"input": {"ops": [["BrowserHistory", ["h"]], ["visit", ["a"]], ["visit", ["b"]], ["back", [2]], ["visit", ["c"]], ["forward", [1]],
                               ["back", [1]], ["forward", [1]], ["visit", ["d"]], ["back", [100]], ["forward", [100]]]},
             "output": [None, None, None, "h", None, "c", "h", "c", None, "h", "d"]},
            {"input": {"ops": [["BrowserHistory", ["h"]], ["visit", ["a"]], ["visit", ["b"]], ["visit", ["c"]], ["back", [3]], ["forward", [2]],
                               ["visit", ["z"]], ["forward", [1]], ["back", [1]], ["back", [1]], ["back", [1]]]},
             "output": [None, None, None, None, "h", "b", None, "z", "b", "a", "h"]},
            {"input": {"ops": _BH_LONG_OPS}, "output": _BH_LONG_OUT},
        ],
        "solution": (
            "class BrowserHistory:\n"
            "    def __init__(self, homepage: str):\n"
            "        self.pages = [homepage]\n"
            "        self.cur = 0     # index of the current page\n"
            "        self.end = 0     # index of the newest valid page\n\n"
            "    def visit(self, url: str) -> None:\n"
            "        self.cur += 1\n"
            "        if self.cur < len(self.pages):\n"
            "            self.pages[self.cur] = url\n"
            "        else:\n"
            "            self.pages.append(url)\n"
            "        self.end = self.cur\n\n"
            "    def back(self, steps: int) -> str:\n"
            "        self.cur = max(0, self.cur - steps)\n"
            "        return self.pages[self.cur]\n\n"
            "    def forward(self, steps: int) -> str:\n"
            "        self.cur = min(self.end, self.cur + steps)\n"
            "        return self.pages[self.cur]\n"
        ),
        "approach": (
            "**Key insight: history is a linear timeline, so an array with a cursor beats two stacks.** `back` and "
            "`forward` become `cur = max(0, cur - steps)` and `cur = min(end, cur + steps)`, both O(1). Visiting writes at "
            "`cur + 1` and marks that as the new end, which logically discards the forward history without touching memory; "
            "later visits simply overwrite those stale slots.\n\n"
            "The two-stack version (back stack, forward stack) is a fine first answer, but `visit` must empty the forward stack "
            "and `back(steps)` moves one element at a time, so it is O(steps) per call. A doubly linked list has the same O(steps) cost. "
            "The array with an `end` pointer is strictly better and just as short.\n\n"
            "**Common mistakes:** truncating the list with slicing on every visit (correct but O(n)); forgetting to clamp at the "
            "homepage or at the newest page; off-by-one when `steps` exceeds the available history.\n\n"
            "**Interview follow-ups:** Memory bound: real browsers cap the history length; use a ring buffer or drop the oldest page "
            "when the array exceeds a limit (shift indices accordingly). Multiple tabs: one instance per tab. Persisting across "
            "restarts: serialise the array and the cursor. What about `back` in O(1) when steps is huge? Already O(1) here, which "
            "is the point of the array approach over stacks."
        ),
        "complexity": {"time": "O(1) per operation", "space": "O(number of pages visited)"},
        "similar": ["min-stack", "implement-queue-using-stacks"],
    },
    {
        "id": "implement-queue-using-stacks",
        "title": "Implement Queue using Stacks",
        "difficulty": "Easy",
        "pattern": "Design",
        "tags": ["Stack", "Queue", "Design"],
        "companies": {"google": 2, "apple": 4, "meta": 2, "amazon": 4, "microsoft": 4},
        "kind": "design",
        "class_name": "MyQueue",
        "description": (
            "Implement a first-in-first-out queue using **only stack operations**: push to top, pop from top, peek at top, "
            "size and is-empty.\n\n"
            "- `MyQueue()` creates an empty queue.\n"
            "- `push(x)` adds `x` to the back of the queue.\n"
            "- `pop()` removes and returns the element at the front.\n"
            "- `peek()` returns the front element without removing it.\n"
            "- `empty()` returns `true` if the queue has no elements.\n\n"
            "`pop` and `peek` are only called on a non-empty queue. Aim for **amortised O(1)** per operation."
        ),
        "examples": [
            {
                "input": "[\"MyQueue\",\"push\",\"push\",\"peek\",\"pop\",\"empty\"]\n[[],[1],[2],[],[],[]]",
                "output": "[null,null,null,1,1,false]",
                "explanation": "1 was pushed first, so it is at the front. After popping it, 2 remains and the queue is not empty.",
            },
            {
                "input": "[\"MyQueue\",\"push\",\"pop\",\"empty\"]\n[[],[7],[],[]]",
                "output": "[null,null,7,true]",
            },
        ],
        "constraints": ["1 <= x <= 10^9", "At most 100 calls to push, pop, peek and empty", "pop and peek are only called when the queue is non-empty"],
        "hints": [
            "Pushing everything onto one stack puts the oldest element at the bottom. Popping the whole stack onto a second stack reverses it, so the oldest ends up on top.",
            "Keep an input stack and an output stack. Push always goes to input. Pop and peek take from output, and only when output is empty do you pour input into it.",
            "Each element is moved from input to output exactly once in its lifetime, so the total work is linear and every operation is amortised O(1).",
        ],
        "starter": (
            "class MyQueue:\n"
            "    def __init__(self):\n"
            "        pass\n\n"
            "    def push(self, x: int) -> None:\n"
            "        pass\n\n"
            "    def pop(self) -> int:\n"
            "        pass\n\n"
            "    def peek(self) -> int:\n"
            "        pass\n\n"
            "    def empty(self) -> bool:\n"
            "        pass\n"
        ),
        "compare": "exact",
        "tests": [
            {"input": {"ops": [["MyQueue", []], ["push", [1]], ["push", [2]], ["peek", []], ["pop", []], ["empty", []]]},
             "output": [None, None, None, 1, 1, False]},
            {"input": {"ops": [["MyQueue", []], ["push", [7]], ["pop", []], ["empty", []]]},
             "output": [None, None, 7, True]},
            {"input": {"ops": [["MyQueue", []], ["empty", []], ["push", [1]], ["push", [2]], ["pop", []], ["push", [3]], ["pop", []], ["peek", []], ["pop", []], ["empty", []]]},
             "output": [None, True, None, None, 1, None, 2, 3, 3, True]},
            {"input": {"ops": [["MyQueue", []]] + [["push", [i]] for i in range(10)] + [["pop", []] for _ in range(5)]
                              + [["push", [i]] for i in range(10, 20)] + [["pop", []] for _ in range(15)] + [["empty", []]]},
             "output": [None] + [None] * 10 + list(range(5)) + [None] * 10 + list(range(5, 20)) + [True]},
            {"input": {"ops": [["MyQueue", []], ["push", [5]], ["peek", []], ["peek", []], ["push", [6]], ["peek", []], ["pop", []], ["peek", []], ["empty", []], ["pop", []], ["empty", []]]},
             "output": [None, None, 5, 5, None, 5, 5, 6, False, 6, True]},
            {"input": {"ops": _MQ_LONG_OPS}, "output": _MQ_LONG_OUT},
        ],
        "solution": (
            "class MyQueue:\n"
            "    def __init__(self):\n"
            "        self.inbox = []    # newest on top\n"
            "        self.outbox = []   # oldest on top\n\n"
            "    def push(self, x: int) -> None:\n"
            "        self.inbox.append(x)\n\n"
            "    def _shift(self) -> None:\n"
            "        if not self.outbox:\n"
            "            while self.inbox:\n"
            "                self.outbox.append(self.inbox.pop())\n\n"
            "    def pop(self) -> int:\n"
            "        self._shift()\n"
            "        return self.outbox.pop()\n\n"
            "    def peek(self) -> int:\n"
            "        self._shift()\n"
            "        return self.outbox[-1]\n\n"
            "    def empty(self) -> bool:\n"
            "        return not self.inbox and not self.outbox\n"
        ),
        "approach": (
            "**Key insight: two stacks, with a lazy transfer.** Pushes go onto `inbox`. When a pop or peek needs the front "
            "and `outbox` is empty, pour all of `inbox` into `outbox`; the reversal puts the oldest element on top. Crucially, "
            "do *not* pour while `outbox` still has elements, because those are older than anything in `inbox`.\n\n"
            "Why amortised O(1): every element is pushed onto `inbox` once, moved to `outbox` once and popped once, so n operations "
            "cost O(n) total even though a single pop may move many elements. This is the standard example interviewers use to "
            "check that you can explain amortised analysis.\n\n"
            "The naive alternative makes `push` O(n) by always moving everything so the front is on top; it is correct but every "
            "push pays the full cost.\n\n"
            "**Common mistakes:** transferring on every pop (destroys the order and the complexity); `empty` checking only one stack; "
            "using Python list operations such as `pop(0)` or `insert(0, x)`, which are not stack operations and defeat the exercise.\n\n"
            "**Interview follow-ups:** Implement a stack with queues (the mirror problem, where push or pop has to rotate the queue). "
            "Thread safety: a lock around the transfer is required because it mutates both stacks; a two-lock queue (Michael-Scott style) "
            "is the classic concurrent design. Bounded capacity: track the total size and block or reject on push."
        ),
        "complexity": {"time": "O(1) amortised per operation", "space": "O(n)"},
        "similar": ["implement-stack-using-queues", "min-stack", "design-browser-history"],
    },
    {
        "id": "design-underground-system",
        "title": "Design Underground System",
        "difficulty": "Medium",
        "pattern": "Design",
        "tags": ["Hash Table", "String", "Design"],
        "companies": {"google": 1, "apple": 1, "amazon": 3},
        "kind": "design",
        "class_name": "UndergroundSystem",
        "description": (
            "Design the back end of a metro system that tracks journeys and reports average travel times between stations.\n\n"
            "- `UndergroundSystem()` creates the system.\n"
            "- `checkIn(id, stationName, t)` records that passenger `id` entered `stationName` at time `t`. A passenger can be checked in at only one station at a time.\n"
            "- `checkOut(id, stationName, t)` records that the same passenger left at `stationName` at time `t`, completing one journey from their check-in station.\n"
            "- `getAverageTime(startStation, endStation)` returns the mean duration, as a float, of **all** completed journeys that started at `startStation` and ended at `endStation`, in the order given. There is always at least one such journey when it is called.\n\n"
            "Journeys from A to B and from B to A are different routes. All times for a given passenger are increasing, and a passenger may travel again after checking out."
        ),
        "examples": [
            {
                "input": "[\"UndergroundSystem\",\"checkIn\",\"checkIn\",\"checkIn\",\"checkOut\",\"checkOut\",\"checkOut\",\"getAverageTime\",\"getAverageTime\",\"checkIn\",\"getAverageTime\",\"checkOut\",\"getAverageTime\"]\n"
                         "[[],[45,\"Central\",3],[32,\"Harbor\",8],[27,\"Central\",10],[45,\"Museum\",15],[27,\"Museum\",20],[32,\"Airport\",22],"
                         "[\"Harbor\",\"Airport\"],[\"Central\",\"Museum\"],[10,\"Central\",24],[\"Central\",\"Museum\"],[10,\"Museum\",38],[\"Central\",\"Museum\"]]",
                "output": "[null,null,null,null,null,null,null,14.0,11.0,null,11.0,null,12.0]",
                "explanation": "Central -> Museum journeys take 12 (passenger 45) and 10 (passenger 27), mean 11.0. Passenger 10 is still "
                               "travelling when the second query happens, so it is unchanged; after their 14-unit trip the mean becomes 36/3 = 12.0.",
            },
            {
                "input": "[\"UndergroundSystem\",\"checkIn\",\"checkOut\",\"getAverageTime\",\"checkIn\",\"checkOut\",\"getAverageTime\",\"getAverageTime\"]\n"
                         "[[],[1,\"A\",0],[1,\"B\",5],[\"A\",\"B\"],[1,\"B\",6],[1,\"A\",14],[\"A\",\"B\"],[\"B\",\"A\"]]",
                "output": "[null,null,null,5.0,null,null,5.0,8.0]",
                "explanation": "The return trip B -> A is a separate route with its own average.",
            },
        ],
        "constraints": [
            "1 <= id, t <= 10^6",
            "1 <= stationName.length, startStation.length, endStation.length <= 10",
            "At most 2 * 10^4 calls in total",
            "getAverageTime is only called for a route with at least one completed journey",
        ],
        "hints": [
            "A check-in is pending state keyed by passenger id; a check-out consumes it.",
            "You never need individual journey durations, only their sum and count per route.",
            "Two maps: id -> (startStation, startTime), and (startStation, endStation) -> (totalTime, trips). The average is total / trips.",
        ],
        "starter": (
            "class UndergroundSystem:\n"
            "    def __init__(self):\n"
            "        pass\n\n"
            "    def checkIn(self, id: int, stationName: str, t: int) -> None:\n"
            "        pass\n\n"
            "    def checkOut(self, id: int, stationName: str, t: int) -> None:\n"
            "        pass\n\n"
            "    def getAverageTime(self, startStation: str, endStation: str) -> float:\n"
            "        pass\n"
        ),
        "compare": "exact",
        "tests": [
            {"input": {"ops": [["UndergroundSystem", []], ["checkIn", [45, "Central", 3]], ["checkIn", [32, "Harbor", 8]], ["checkIn", [27, "Central", 10]],
                               ["checkOut", [45, "Museum", 15]], ["checkOut", [27, "Museum", 20]], ["checkOut", [32, "Airport", 22]],
                               ["getAverageTime", ["Harbor", "Airport"]], ["getAverageTime", ["Central", "Museum"]], ["checkIn", [10, "Central", 24]],
                               ["getAverageTime", ["Central", "Museum"]], ["checkOut", [10, "Museum", 38]], ["getAverageTime", ["Central", "Museum"]]]},
             "output": [None, None, None, None, None, None, None, 14.0, 11.0, None, 11.0, None, 12.0]},
            {"input": {"ops": [["UndergroundSystem", []], ["checkIn", [1, "A", 0]], ["checkOut", [1, "B", 5]], ["getAverageTime", ["A", "B"]],
                               ["checkIn", [1, "B", 6]], ["checkOut", [1, "A", 14]], ["getAverageTime", ["A", "B"]], ["getAverageTime", ["B", "A"]]]},
             "output": [None, None, None, 5.0, None, None, 5.0, 8.0]},
            {"input": {"ops": [["UndergroundSystem", []], ["checkIn", [1, "A", 10]], ["checkOut", [1, "B", 21]], ["checkIn", [2, "A", 30]],
                               ["checkOut", [2, "B", 42]], ["getAverageTime", ["A", "B"]], ["checkIn", [1, "A", 50]], ["checkOut", [1, "B", 60]],
                               ["getAverageTime", ["A", "B"]]]},
             "output": [None, None, None, None, None, 11.5, None, None, 11.0]},
            {"input": {"ops": [["UndergroundSystem", []], ["checkIn", [7, "S", 1]], ["checkOut", [7, "S", 1]], ["getAverageTime", ["S", "S"]],
                               ["checkIn", [8, "S", 2]], ["checkOut", [8, "S", 4]], ["getAverageTime", ["S", "S"]]]},
             "output": [None, None, None, 0.0, None, None, 1.0]},
            {"input": {"ops": [["UndergroundSystem", []], ["checkIn", [1, "A", 0]], ["checkIn", [2, "A", 0]], ["checkIn", [3, "B", 0]],
                               ["checkOut", [3, "A", 7]], ["checkOut", [1, "B", 3]], ["checkOut", [2, "C", 9]],
                               ["getAverageTime", ["A", "B"]], ["getAverageTime", ["A", "C"]], ["getAverageTime", ["B", "A"]]]},
             "output": [None, None, None, None, None, None, None, 3.0, 9.0, 7.0]},
            {"input": {"ops": _US_LONG_OPS}, "output": _US_LONG_OUT},
        ],
        "solution": (
            "class UndergroundSystem:\n"
            "    def __init__(self):\n"
            "        self.active = {}                 # id -> (startStation, startTime)\n"
            "        self.routes = defaultdict(lambda: [0, 0])   # (start, end) -> [totalTime, trips]\n\n"
            "    def checkIn(self, id: int, stationName: str, t: int) -> None:\n"
            "        self.active[id] = (stationName, t)\n\n"
            "    def checkOut(self, id: int, stationName: str, t: int) -> None:\n"
            "        start, t0 = self.active.pop(id)\n"
            "        route = self.routes[(start, stationName)]\n"
            "        route[0] += t - t0\n"
            "        route[1] += 1\n\n"
            "    def getAverageTime(self, startStation: str, endStation: str) -> float:\n"
            "        total, trips = self.routes[(startStation, endStation)]\n"
            "        return total / trips\n"
        ),
        "approach": (
            "**Key insight: an average only needs a running sum and a count, never the individual journeys.** Two hash maps do "
            "the whole job. `active` maps a passenger id to where and when they checked in; `checkOut` pops that entry, computes "
            "the duration and adds it to the `(start, end)` route's `[total, count]`. `getAverageTime` is a division.\n\n"
            "Popping on check-out both frees memory and lets the same passenger travel again. Keying routes by the ordered pair keeps "
            "A -> B separate from B -> A.\n\n"
            "**Common mistakes:** storing a list of durations per route and averaging on every query (O(trips) per query and unbounded "
            "memory); keying routes by an unordered pair; forgetting to remove the active check-in, which would leak memory over "
            "millions of passengers; integer division in languages where that matters.\n\n"
            "**Interview follow-ups:** Floating-point drift over billions of trips: keep the sum as an integer (or use Kahan summation) "
            "and divide only on read. Scaling: routes are independent, so shard by route key; the `active` map can live in a fast "
            "store keyed by passenger. Thread safety: updates to a route's sum and count must be atomic together (lock per route or a "
            "compare-and-swap on a packed struct). Also discuss handling a check-out without a matching check-in (data error) gracefully."
        ),
        "complexity": {"time": "O(1) per operation", "space": "O(active passengers + distinct routes)"},
        "similar": ["design-hit-counter", "lru-cache"],
    },
    {
        "id": "snapshot-array",
        "title": "Snapshot Array",
        "difficulty": "Medium",
        "pattern": "Design",
        "tags": ["Array", "Hash Table", "Binary Search", "Design"],
        "companies": {"google": 4, "apple": 1, "meta": 1, "amazon": 2},
        "kind": "design",
        "class_name": "SnapshotArray",
        "description": (
            "Design an integer array that can be snapshotted, where any element can later be read as it was at any past snapshot.\n\n"
            "- `SnapshotArray(length)` creates an array of the given length with every element equal to `0`.\n"
            "- `set(index, val)` sets the element at `index` to `val`.\n"
            "- `snap()` takes a snapshot and returns its id. Ids start at `0` and increase by one with every call.\n"
            "- `get(index, snap_id)` returns the value at `index` as it was right after snapshot `snap_id` was taken.\n\n"
            "The array can be long and snapshots frequent, so copying the whole array on every `snap` is too slow."
        ),
        "examples": [
            {
                "input": "[\"SnapshotArray\",\"set\",\"snap\",\"set\",\"get\"]\n[[3],[0,5],[],[0,6],[0,0]]",
                "output": "[null,null,0,null,5]",
                "explanation": "Snapshot 0 was taken while index 0 held 5. Setting it to 6 afterwards does not change what snapshot 0 recorded.",
            },
            {
                "input": "[\"SnapshotArray\",\"snap\",\"snap\",\"get\",\"set\",\"snap\",\"get\",\"get\"]\n[[2],[],[],[1,1],[1,9],[],[1,2],[1,0]]",
                "output": "[null,0,1,0,null,2,9,0]",
                "explanation": "Elements that were never set read as 0 in every snapshot.",
            },
        ],
        "constraints": ["1 <= length <= 5 * 10^4", "0 <= index < length", "0 <= val <= 10^9", "0 <= snap_id < number of snaps taken", "At most 5 * 10^4 calls in total"],
        "hints": [
            "Most elements do not change between snapshots, so store changes, not copies.",
            "For each index keep a list of (snap_id, value) pairs recording when the value changed. The list is sorted by snap_id automatically.",
            "On get, binary search that index's list for the last pair with snap_id <= the requested id. If set is called twice in the same snapshot period, overwrite the last pair instead of appending.",
        ],
        "starter": (
            "class SnapshotArray:\n"
            "    def __init__(self, length: int):\n"
            "        pass\n\n"
            "    def set(self, index: int, val: int) -> None:\n"
            "        pass\n\n"
            "    def snap(self) -> int:\n"
            "        pass\n\n"
            "    def get(self, index: int, snap_id: int) -> int:\n"
            "        pass\n"
        ),
        "compare": "exact",
        "tests": [
            {"input": {"ops": [["SnapshotArray", [3]], ["set", [0, 5]], ["snap", []], ["set", [0, 6]], ["get", [0, 0]]]},
             "output": [None, None, 0, None, 5]},
            {"input": {"ops": [["SnapshotArray", [2]], ["snap", []], ["snap", []], ["get", [1, 1]], ["set", [1, 9]], ["snap", []], ["get", [1, 2]], ["get", [1, 0]]]},
             "output": [None, 0, 1, 0, None, 2, 9, 0]},
            {"input": {"ops": [["SnapshotArray", [1]], ["set", [0, 1]], ["set", [0, 2]], ["set", [0, 3]], ["snap", []], ["get", [0, 0]], ["set", [0, 4]],
                               ["snap", []], ["snap", []], ["get", [0, 0]], ["get", [0, 1]], ["get", [0, 2]]]},
             "output": [None, None, None, None, 0, 3, None, 1, 2, 3, 4, 4]},
            {"input": {"ops": [["SnapshotArray", [4]], ["set", [3, 7]], ["snap", []], ["set", [1, 2]], ["snap", []], ["set", [3, 8]], ["snap", []],
                               ["get", [3, 0]], ["get", [3, 1]], ["get", [3, 2]], ["get", [1, 0]], ["get", [1, 2]], ["get", [0, 2]]]},
             "output": [None, None, 0, None, 1, None, 2, 7, 7, 8, 0, 2, 0]},
            {"input": {"ops": _SA_LONG_OPS}, "output": _SA_LONG_OUT},
            {"input": {"ops": _SA_WIDE_OPS}, "output": _SA_WIDE_OUT},
        ],
        "solution": (
            "class SnapshotArray:\n"
            "    def __init__(self, length: int):\n"
            "        self.hist = [[(0, 0)] for _ in range(length)]   # index -> [(snap_id, value)] sorted by snap_id\n"
            "        self.snap_id = 0\n\n"
            "    def set(self, index: int, val: int) -> None:\n"
            "        h = self.hist[index]\n"
            "        if h[-1][0] == self.snap_id:\n"
            "            h[-1] = (self.snap_id, val)\n"
            "        else:\n"
            "            h.append((self.snap_id, val))\n\n"
            "    def snap(self) -> int:\n"
            "        self.snap_id += 1\n"
            "        return self.snap_id - 1\n\n"
            "    def get(self, index: int, snap_id: int) -> int:\n"
            "        h = self.hist[index]\n"
            "        i = bisect_right(h, (snap_id, float('inf'))) - 1\n"
            "        return h[i][1]\n"
        ),
        "approach": (
            "**Key insight: persist the diffs, not the array.** Each index keeps its own change log: a list of "
            "`(snap_id, value)` pairs where `snap_id` is the id the *next* `snap()` call will return, i.e. the snapshot that "
            "will first observe this value. Because the current snap id only grows, every log is sorted, and `get` is a binary "
            "search for the last pair whose id is <= the requested snapshot.\n\n"
            "Seeding every log with `(0, 0)` means an element that was never set reads as 0 at every snapshot, and the search "
            "always finds something. If `set` is called repeatedly between two snaps, only the latest value can ever be observed, "
            "so overwrite the last pair instead of appending; this bounds the log by the number of snaps plus one.\n\n"
            "`snap()` is O(1): it just bumps a counter. Nothing is copied.\n\n"
            "**Common mistakes:** copying the array in `snap` (O(length) per snap, times out); storing the snap id that was "
            "*last* taken instead of the one that will be taken next, which is off by one; using `bisect_left`, which misses an "
            "exact match on the snap id.\n\n"
            "**Interview follow-ups:** This is the simplest persistent data structure; compare with a persistent segment tree or "
            "copy-on-write pages used by databases and filesystems (ZFS, Btrfs) and by MVCC. Memory: logs grow with the number of "
            "distinct writes, so a long-lived system needs snapshot retirement (drop pairs older than the oldest live snapshot). "
            "Concurrency: `snap` must be atomic with respect to `set` so a snapshot sees a consistent state; a reader-writer lock "
            "or a per-snapshot epoch works."
        ),
        "complexity": {"time": "O(1) set and snap, O(log s) get where s is the number of changes to that index", "space": "O(length + number of sets)"},
        "similar": ["time-based-key-value-store", "lru-cache"],
    },
]
