"""ML Coding problems: implement classic ML building blocks from scratch in pure Python.

No numpy: the judge runs with the standard library only. See SCHEMA.md for the dict format.
"""

import math as _math

# ---- deterministic larger inputs shared by a few tests ----
_AUC_BIG_SCORES = [((i * 37) % 101) / 100.0 for i in range(2000)]
_AUC_BIG_LABELS = [1 if (i * 53) % 7 < 3 else 0 for i in range(2000)]
_KM_BIG_POINTS = [[(i * 31 % 100) / 10.0, (i * 17 % 100) / 10.0] for i in range(2000)]
_LR_BIG_X = [[((i * 7) % 13) / 6.0 - 1.0, ((i * 11) % 17) / 8.0 - 1.0] for i in range(300)]
_LR_BIG_Y = [1 if 1.5 * x[0] - 0.8 * x[1] + 0.2 > 0 else 0 for x in _LR_BIG_X]
_AN_BIG_SERIES = [_math.sin(i / 7.0) * 10 for i in range(2000)]
for _i in (500, 1234, 1900):
    _AN_BIG_SERIES[_i] += 80

_KNN_TRAIN = [[0, 0], [1, 0], [0, 1], [5, 5], [6, 5], [5, 6]]
_KNN_LABELS = [0, 0, 0, 1, 1, 1]

PROBLEMS = [
    # ------------------------------------------------------------------ 1
    {
        "id": "softmax",
        "title": "Numerically Stable Softmax",
        "difficulty": "Easy",
        "pattern": "ML Coding",
        "tags": ["Math", "Numerical Stability", "Neural Networks"],
        "companies": {"apple": 5, "google": 3, "meta": 3, "amazon": 2, "microsoft": 2},
        "description": (
            "Implement the **softmax** function. Given a list of real-valued logits `x`, return a list of the same "
            "length where entry `i` equals `exp(x[i]) / sum_j exp(x[j])`.\n\n"
            "Your implementation must be **numerically stable**: inputs such as `[1000, 1000]` must not overflow. "
            "Return `[]` for an empty input."
        ),
        "examples": [
            {"input": "x = [1.0, 2.0, 3.0]", "output": "[0.090031, 0.244728, 0.665241]",
             "explanation": "exp(1), exp(2), exp(3) are 2.718, 7.389, 20.086; dividing by their sum 30.193 gives the probabilities."},
            {"input": "x = [1000.0, 1000.0]", "output": "[0.5, 0.5]",
             "explanation": "A naive exp(1000) overflows. Subtracting the max first gives exp(0)/2 for both entries."},
            {"input": "x = [0.0]", "output": "[1.0]"},
        ],
        "constraints": ["0 <= len(x) <= 10^4", "-10^4 <= x[i] <= 10^4", "Answers are compared with tolerance 1e-5."],
        "hints": [
            "exp of a large number overflows a float, but softmax is invariant to shifting all inputs by a constant.",
            "Subtract max(x) from every element before exponentiating; the largest term becomes exp(0) = 1 and nothing overflows.",
            "Very negative shifted values underflow to 0.0, which is harmless because the denominator is at least 1.",
        ],
        "function": "softmax",
        "signature": "def softmax(self, x: List[float]) -> List[float]:",
        "arg_types": {"x": "List[float]"},
        "return_type": "List[float]",
        "compare": "float",
        "tests": [
            {"input": {"x": [1.0, 2.0, 3.0]}, "output": [0.090031, 0.244728, 0.665241]},
            {"input": {"x": [1000.0, 1000.0]}, "output": [0.5, 0.5]},
            {"input": {"x": [0.0]}, "output": [1.0]},
            {"input": {"x": [-1000.0, 0.0, 1000.0]}, "output": [0.0, 0.0, 1.0]},
            {"input": {"x": [3.0, 1.0, 0.2]}, "output": [0.836019, 0.113143, 0.050838]},
            {"input": {"x": [5.0, 5.0, 5.0, 5.0]}, "output": [0.25, 0.25, 0.25, 0.25]},
            {"input": {"x": [-2.5, -1.0, -0.5]}, "output": [0.077696, 0.348207, 0.574097]},
            {"input": {"x": []}, "output": []},
        ],
        "solution": (
            "class Solution:\n"
            "    def softmax(self, x: List[float]) -> List[float]:\n"
            "        if not x:\n"
            "            return []\n"
            "        m = max(x)\n"
            "        exps = [math.exp(v - m) for v in x]\n"
            "        total = sum(exps)\n"
            "        return [e / total for e in exps]\n"
        ),
        "approach": (
            "**Shift by the maximum, then exponentiate and normalise.** Softmax is `exp(x_i) / sum_j exp(x_j)`. "
            "Multiplying numerator and denominator by `exp(-c)` for any constant `c` leaves the result unchanged, so we "
            "may choose `c = max(x)`. After the shift every exponent is `<= 0`, the largest term is exactly 1, and the "
            "denominator is at least 1, so neither overflow nor division by zero can occur. Tiny shifted values may "
            "underflow to 0.0; that only changes the answer by amounts far below float precision.\n\n"
            "Common mistakes: forgetting the empty-input case, dividing each term by `sum(x)` instead of the sum of "
            "exponentials, or computing the sum inside the loop (O(n^2)).\n\n"
            "**Interview follow-ups:** Why not just clip the inputs? (clipping changes the answer; the shift does not). "
            "How would you compute log-softmax stably? (`x_i - max - log(sum(exp(x_j - max)))`, the log-sum-exp trick, "
            "avoiding `log(0)` for very negative logits). What does a temperature parameter do? (dividing logits by "
            "T > 1 flattens the distribution, T < 1 sharpens it). How is softmax applied to a batch? (row-wise, with "
            "the max taken per row)."
        ),
        "complexity": {"time": "O(n)", "space": "O(n)"},
        "similar": ["cross-entropy-loss", "scaled-dot-product-attention"],
    },
    # ------------------------------------------------------------------ 2
    {
        "id": "cross-entropy-loss",
        "title": "Mean Cross-Entropy Loss",
        "difficulty": "Medium",
        "pattern": "ML Coding",
        "tags": ["Loss Function", "Numerical Stability", "Classification"],
        "companies": {"apple": 5, "google": 3, "meta": 3, "amazon": 2, "microsoft": 2},
        "description": (
            "Implement the **mean categorical cross-entropy**. You are given `probs`, a list of `n` rows where row `i` holds "
            "the predicted class probabilities for sample `i` (each row sums to 1), and `labels`, a list of `n` integers "
            "where `labels[i]` is the correct class index for sample `i`.\n\n"
            "The loss for one sample is `-ln(p)` where `p` is the probability assigned to the correct class. Before taking "
            "the log, **clip** `p` into the range `[1e-12, 1 - 1e-12]` so that a probability of exactly 0 does not produce "
            "infinity. Return the average loss over all samples."
        ),
        "examples": [
            {"input": "probs = [[0.7, 0.2, 0.1], [0.1, 0.8, 0.1]], labels = [0, 1]", "output": "0.289909",
             "explanation": "-(ln 0.7 + ln 0.8) / 2 = (0.356675 + 0.223144) / 2."},
            {"input": "probs = [[1.0, 0.0]], labels = [0]", "output": "0.0",
             "explanation": "The correct class has probability 1, so the loss is -ln(1) = 0 (clipping to 1 - 1e-12 changes nothing visible)."},
            {"input": "probs = [[0.0, 1.0]], labels = [0]", "output": "27.631021",
             "explanation": "The model gave the true class probability 0. Clipping to 1e-12 yields -ln(1e-12) = 27.631 instead of infinity."},
        ],
        "constraints": ["1 <= n <= 10^4", "2 <= number of classes <= 100", "0 <= labels[i] < number of classes", "Compared with tolerance 1e-5."],
        "hints": [
            "Only one probability per row matters: the one at index labels[i].",
            "ln(0) is -infinity. Clamp the picked probability with min(max(p, 1e-12), 1 - 1e-12) first.",
            "Sum -ln(p_i) over rows and divide by the number of rows.",
        ],
        "function": "crossEntropy",
        "signature": "def crossEntropy(self, probs: List[List[float]], labels: List[int]) -> float:",
        "arg_types": {"probs": "List[List[float]]", "labels": "List[int]"},
        "return_type": "float",
        "compare": "float",
        "tests": [
            {"input": {"probs": [[0.7, 0.2, 0.1], [0.1, 0.8, 0.1]], "labels": [0, 1]}, "output": 0.289909},
            {"input": {"probs": [[1.0, 0.0]], "labels": [0]}, "output": 0.0},
            {"input": {"probs": [[0.0, 1.0]], "labels": [0]}, "output": 27.631021},
            {"input": {"probs": [[0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25]], "labels": [0, 1, 2]}, "output": 1.386294},
            {"input": {"probs": [[0.9, 0.1], [0.4, 0.6], [0.2, 0.8], [0.5, 0.5]], "labels": [0, 0, 1, 1]}, "output": 0.484485},
            {"input": {"probs": [[0.05, 0.9, 0.05], [0.3, 0.3, 0.4], [0.6, 0.3, 0.1]], "labels": [1, 2, 2]}, "output": 1.108079},
        ],
        "solution": (
            "class Solution:\n"
            "    def crossEntropy(self, probs: List[List[float]], labels: List[int]) -> float:\n"
            "        eps = 1e-12\n"
            "        total = 0.0\n"
            "        for row, y in zip(probs, labels):\n"
            "            p = min(max(row[y], eps), 1.0 - eps)\n"
            "            total -= math.log(p)\n"
            "        return total / len(labels)\n"
        ),
        "approach": (
            "**Cross-entropy is the negative log-likelihood of the true class, averaged over samples.** With a one-hot "
            "target only one term of the general sum `-sum_c y_c ln p_c` survives, so per sample we simply look up "
            "`probs[i][labels[i]]`, take `-ln`, and average.\n\n"
            "The numerical pitfall is `ln(0) = -inf`: one confidently wrong prediction would make the mean infinite and "
            "break gradients. Clipping the probability to `[eps, 1 - eps]` bounds the per-sample loss at about 27.6 for "
            "`eps = 1e-12`. In real frameworks the loss is computed from logits with log-softmax instead of clipping, which "
            "is both more stable and more accurate.\n\n"
            "**Interview follow-ups:** Why combine softmax and cross-entropy into one op? (the gradient simplifies to "
            "`p - y`, and log-softmax avoids the clip). What changes for binary cross-entropy? (`-(y ln p + (1-y) ln(1-p))`, "
            "both branches need clipping). What is label smoothing and how does it change this function? (targets become "
            "`(1 - a) * one_hot + a / C`, so every class contributes). How do you weight classes for imbalance?"
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["softmax", "logistic-regression-sgd"],
    },
    # ------------------------------------------------------------------ 3
    {
        "id": "precision-recall-f1",
        "title": "Precision, Recall and F1",
        "difficulty": "Easy",
        "pattern": "ML Coding",
        "tags": ["Metrics", "Classification"],
        "companies": {"apple": 5, "google": 3, "meta": 4, "amazon": 4, "microsoft": 3},
        "description": (
            "Given two equal-length lists of 0/1 values, `y_true` (ground truth) and `y_pred` (model output), compute "
            "the binary classification metrics and return them as `[precision, recall, f1]`.\n\n"
            "- `precision = TP / (TP + FP)`\n"
            "- `recall = TP / (TP + FN)`\n"
            "- `f1 = 2 * precision * recall / (precision + recall)`\n\n"
            "Whenever a denominator is 0, define that metric as `0.0`. Class 1 is the positive class."
        ),
        "examples": [
            {"input": "y_true = [1,0,1,1,0,1], y_pred = [1,0,0,1,1,1]", "output": "[0.75, 0.75, 0.75]",
             "explanation": "TP = 3 (indices 0, 3, 5), FP = 1 (index 4), FN = 1 (index 2). Both ratios are 3/4, so F1 is 3/4 too."},
            {"input": "y_true = [1,1,0], y_pred = [0,0,0]", "output": "[0.0, 0.0, 0.0]",
             "explanation": "No positive predictions, so TP + FP = 0 and precision is defined as 0. Recall is 0/2 = 0 and F1 is then 0."},
            {"input": "y_true = [1,1,1,0], y_pred = [1,0,0,0]", "output": "[1.0, 0.333333, 0.5]"},
        ],
        "constraints": ["0 <= len(y_true) == len(y_pred) <= 10^5", "Values are 0 or 1.", "Compared with tolerance 1e-5."],
        "hints": [
            "Count the four confusion-matrix cells in one pass. Only TP, FP and FN are needed here.",
            "Guard every division: if the denominator is 0 return 0.0 for that metric, including F1 when precision + recall is 0.",
        ],
        "function": "precisionRecallF1",
        "signature": "def precisionRecallF1(self, y_true: List[int], y_pred: List[int]) -> List[float]:",
        "arg_types": {"y_true": "List[int]", "y_pred": "List[int]"},
        "return_type": "List[float]",
        "compare": "float",
        "tests": [
            {"input": {"y_true": [1, 0, 1, 1, 0, 1], "y_pred": [1, 0, 0, 1, 1, 1]}, "output": [0.75, 0.75, 0.75]},
            {"input": {"y_true": [1, 1, 0], "y_pred": [0, 0, 0]}, "output": [0.0, 0.0, 0.0]},
            {"input": {"y_true": [1, 1, 1, 0], "y_pred": [1, 0, 0, 0]}, "output": [1.0, 0.333333, 0.5]},
            {"input": {"y_true": [1, 1, 1], "y_pred": [1, 1, 1]}, "output": [1.0, 1.0, 1.0]},
            {"input": {"y_true": [], "y_pred": []}, "output": [0.0, 0.0, 0.0]},
            {"input": {"y_true": [0, 0, 0], "y_pred": [1, 1, 1]}, "output": [0.0, 0.0, 0.0]},
            {"input": {"y_true": [0, 1, 0, 1, 0, 0, 1, 0], "y_pred": [1, 1, 0, 0, 0, 1, 1, 0]}, "output": [0.5, 0.666667, 0.571429]},
            {"input": {"y_true": [1 if i % 3 == 0 else 0 for i in range(30000)], "y_pred": [1 if i % 2 == 0 else 0 for i in range(30000)]}, "output": [0.333333, 0.5, 0.4]},
        ],
        "solution": (
            "class Solution:\n"
            "    def precisionRecallF1(self, y_true: List[int], y_pred: List[int]) -> List[float]:\n"
            "        tp = fp = fn = 0\n"
            "        for t, p in zip(y_true, y_pred):\n"
            "            if p == 1:\n"
            "                if t == 1:\n"
            "                    tp += 1\n"
            "                else:\n"
            "                    fp += 1\n"
            "            elif t == 1:\n"
            "                fn += 1\n"
            "        precision = tp / (tp + fp) if tp + fp else 0.0\n"
            "        recall = tp / (tp + fn) if tp + fn else 0.0\n"
            "        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0\n"
            "        return [precision, recall, f1]\n"
        ),
        "approach": (
            "**Build the confusion matrix in one pass, then apply the three formulas with zero guards.** Precision answers "
            "\"of what I flagged, how much was right\", recall answers \"of what was really positive, how much did I catch\", "
            "and F1 is their harmonic mean, which is pulled toward the smaller of the two.\n\n"
            "The zero-denominator convention matters in practice: a model that never predicts positive has undefined "
            "precision; sklearn warns and returns 0 by default, which is what this problem asks for. Note that `tp + fn` is "
            "simply the number of true positives in the ground truth.\n\n"
            "**Interview follow-ups:** How do you extend to multi-class? (per-class one-vs-rest, then macro, micro or "
            "weighted averaging; micro-F1 equals accuracy when every sample has one label). How does F-beta trade off the "
            "two? (`beta > 1` favours recall). Why is accuracy misleading on imbalanced data, and how would you pick a "
            "threshold to maximise F1 from predicted probabilities? (sweep thresholds, O(n log n) after sorting)."
        ),
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "similar": ["roc-auc", "cross-entropy-loss"],
    },
    # ------------------------------------------------------------------ 4
    {
        "id": "roc-auc",
        "title": "ROC AUC with Tied Scores",
        "difficulty": "Hard",
        "pattern": "ML Coding",
        "tags": ["Metrics", "Ranking", "Sorting", "Statistics"],
        "companies": {"apple": 4, "google": 3, "meta": 3, "amazon": 3, "microsoft": 2},
        "description": (
            "Compute the **area under the ROC curve** from a list of real-valued `scores` and a list of binary `labels` "
            "(1 = positive, 0 = negative).\n\n"
            "AUC equals the probability that a randomly chosen positive is scored higher than a randomly chosen negative, "
            "with **ties counting one half**. Implement it with the rank-based (Mann-Whitney U) formulation: assign each "
            "score its 1-based rank in ascending order, giving **tied scores the average of the ranks they span**, then\n\n"
            "`AUC = (sum of positive ranks - P * (P + 1) / 2) / (P * N)`\n\n"
            "where `P` and `N` are the numbers of positives and negatives. If either class is absent the metric is "
            "undefined; return `0.5` in that case. Aim for O(n log n)."
        ),
        "examples": [
            {"input": "scores = [0.1, 0.4, 0.35, 0.8], labels = [0, 0, 1, 1]", "output": "0.75",
             "explanation": "Ranks are 0.1->1, 0.35->2, 0.4->3, 0.8->4. Positive ranks sum to 2 + 4 = 6; (6 - 3) / (2 * 2) = 0.75. Equivalently 3 of the 4 positive/negative pairs are ordered correctly."},
            {"input": "scores = [0.3, 0.3, 0.6], labels = [0, 1, 1]", "output": "0.75",
             "explanation": "The two 0.3 scores share rank 1.5. Pairs: (0.3 pos vs 0.3 neg) counts 0.5, (0.6 vs 0.3) counts 1; the mean is 0.75."},
            {"input": "scores = [0.5, 0.5, 0.5, 0.5], labels = [0, 1, 0, 1]", "output": "0.5",
             "explanation": "A constant scorer orders nothing, which is exactly chance level."},
        ],
        "constraints": ["1 <= len(scores) == len(labels) <= 10^5", "labels[i] in {0, 1}", "Compared with tolerance 1e-5."],
        "hints": [
            "The O(P * N) pairwise definition is a fine first answer, but the interviewer wants O(n log n).",
            "Sort indices by score. Walk the sorted list in groups of equal scores; every member of a group gets the average rank of the group.",
            "The sum of positive ranks over-counts the P*(P+1)/2 positive-positive comparisons; subtracting them leaves the number of (positive beats negative) pairs, ties counted as 0.5.",
        ],
        "function": "rocAuc",
        "signature": "def rocAuc(self, scores: List[float], labels: List[int]) -> float:",
        "arg_types": {"scores": "List[float]", "labels": "List[int]"},
        "return_type": "float",
        "compare": "float",
        "tests": [
            {"input": {"scores": [0.1, 0.4, 0.35, 0.8], "labels": [0, 0, 1, 1]}, "output": 0.75},
            {"input": {"scores": [0.3, 0.3, 0.6], "labels": [0, 1, 1]}, "output": 0.75},
            {"input": {"scores": [0.5, 0.5, 0.5, 0.5], "labels": [0, 1, 0, 1]}, "output": 0.5},
            {"input": {"scores": [0.2, 0.9, 0.1, 0.8], "labels": [0, 1, 0, 1]}, "output": 1.0},
            {"input": {"scores": [0.9, 0.1, 0.8, 0.2], "labels": [0, 1, 0, 1]}, "output": 0.0},
            {"input": {"scores": [0.7, 0.2], "labels": [1, 1]}, "output": 0.5},
            {"input": {"scores": [0.2, 0.5, 0.5, 0.5, 0.9, 0.1, 0.5], "labels": [0, 1, 0, 1, 1, 0, 0]}, "output": 0.833333},
            {"input": {"scores": _AUC_BIG_SCORES, "labels": _AUC_BIG_LABELS}, "output": 0.499986},
        ],
        "solution": (
            "class Solution:\n"
            "    def rocAuc(self, scores: List[float], labels: List[int]) -> float:\n"
            "        n = len(scores)\n"
            "        pos = sum(labels)\n"
            "        neg = n - pos\n"
            "        if pos == 0 or neg == 0:\n"
            "            return 0.5\n"
            "        order = sorted(range(n), key=lambda i: scores[i])\n"
            "        rank_sum_pos = 0.0\n"
            "        i = 0\n"
            "        while i < n:\n"
            "            j = i\n"
            "            while j + 1 < n and scores[order[j + 1]] == scores[order[i]]:\n"
            "                j += 1\n"
            "            avg_rank = (i + 1 + j + 1) / 2.0  # 1-based ranks i+1 .. j+1\n"
            "            for k in range(i, j + 1):\n"
            "                if labels[order[k]] == 1:\n"
            "                    rank_sum_pos += avg_rank\n"
            "            i = j + 1\n"
            "        return (rank_sum_pos - pos * (pos + 1) / 2.0) / (pos * neg)\n"
        ),
        "approach": (
            "**AUC is the Mann-Whitney U statistic normalised by P * N.** For every (positive, negative) pair we want 1 if "
            "the positive scores higher, 0.5 on a tie, 0 otherwise. Summing the ranks of the positives counts, for each "
            "positive, how many items lie below it (plus itself); the `P(P+1)/2` term removes the comparisons among "
            "positives themselves, and what remains is exactly the number of won pairs, with average ranks turning each "
            "tie into a half. Sorting once makes this O(n log n) instead of O(P * N).\n\n"
            "Tie handling is where most implementations go wrong: assigning ranks by sorted position alone (no averaging) "
            "makes the result depend on the sort's stability and over- or under-counts tied pairs. Group equal scores and "
            "give every member `(first_rank + last_rank) / 2`. Compare scores for equality after sorting, not via "
            "float arithmetic on differences.\n\n"
            "**Interview follow-ups:** How does this relate to the ROC curve? (sweeping the threshold traces TPR vs FPR; "
            "the trapezoidal area is the same number). Why can AUC look fine under heavy class imbalance while the model "
            "is useless, and why prefer PR-AUC then? (FPR stays tiny when negatives dominate; precision does not). "
            "How would you compute it in a streaming or distributed setting? (histogram the scores into bins, accept "
            "approximation). What does AUC = 0 tell you? (perfectly inverted scores)."
        ),
        "complexity": {"time": "O(n log n)", "space": "O(n)"},
        "similar": ["precision-recall-f1", "ndcg-at-k"],
    },
    # ------------------------------------------------------------------ 5
    {
        "id": "k-means-step",
        "title": "One Iteration of k-Means",
        "difficulty": "Medium",
        "pattern": "ML Coding",
        "tags": ["Clustering", "Geometry", "Unsupervised Learning"],
        "companies": {"apple": 5, "google": 3, "meta": 2, "amazon": 4, "microsoft": 3},
        "description": (
            "Implement a single **Lloyd iteration** of k-means. You are given `points`, a list of `n` points in `d` "
            "dimensions, and `centroids`, the current list of `k` centroids (also `d`-dimensional).\n\n"
            "1. **Assign** each point to the nearest centroid by Euclidean distance. If several centroids are equally "
            "close, pick the one with the **lowest index**.\n"
            "2. **Update** every centroid to the mean of the points assigned to it. A centroid that received no points "
            "**keeps its current position**.\n\n"
            "Return the list of `k` new centroids, in the same order, as lists of floats."
        ),
        "examples": [
            {"input": "points = [[0,0],[0,1],[10,10],[10,11]], centroids = [[0,0],[10,10]]", "output": "[[0.0, 0.5], [10.0, 10.5]]",
             "explanation": "The first two points go to centroid 0 and average to (0, 0.5); the others go to centroid 1."},
            {"input": "points = [[0,0],[0,1],[10,10],[10,11]], centroids = [[0,0],[100,100]]", "output": "[[5.0, 5.5], [100.0, 100.0]]",
             "explanation": "Every point is closer to (0,0). Centroid 1 is empty and stays where it was."},
            {"input": "points = [[5,5],[1,1],[9,9]], centroids = [[0,0],[10,10]]", "output": "[[3.0, 3.0], [9.0, 9.0]]",
             "explanation": "(5,5) is equidistant from both centroids and is assigned to index 0."},
        ],
        "constraints": ["1 <= n <= 10^4", "1 <= k <= 50", "1 <= d <= 10", "Compared with tolerance 1e-5."],
        "hints": [
            "Squared distance is enough for comparing distances; skip the square root.",
            "Scan centroids in index order and only replace the best when the distance is strictly smaller; that gives the lowest-index tie rule for free.",
            "Accumulate per-centroid coordinate sums and counts, then divide; copy the old centroid when the count is 0.",
        ],
        "function": "kmeansStep",
        "signature": "def kmeansStep(self, points: List[List[float]], centroids: List[List[float]]) -> List[List[float]]:",
        "arg_types": {"points": "List[List[float]]", "centroids": "List[List[float]]"},
        "return_type": "List[List[float]]",
        "compare": "float",
        "tests": [
            {"input": {"points": [[0, 0], [0, 1], [10, 10], [10, 11]], "centroids": [[0, 0], [10, 10]]}, "output": [[0.0, 0.5], [10.0, 10.5]]},
            {"input": {"points": [[0, 0], [0, 1], [10, 10], [10, 11]], "centroids": [[0, 0], [100, 100]]}, "output": [[5.0, 5.5], [100.0, 100.0]]},
            {"input": {"points": [[5, 5], [1, 1], [9, 9]], "centroids": [[0, 0], [10, 10]]}, "output": [[3.0, 3.0], [9.0, 9.0]]},
            {"input": {"points": [[1, 2, 3], [3, 2, 1], [10, 10, 10]], "centroids": [[0, 0, 0], [9, 9, 9]]}, "output": [[2.0, 2.0, 2.0], [10.0, 10.0, 10.0]]},
            {"input": {"points": [[2.5, -1.0]], "centroids": [[0.0, 0.0]]}, "output": [[2.5, -1.0]]},
            {"input": {"points": [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]], "centroids": [[2, 2], [4, 4], [2, 2]]}, "output": [[2.0, 2.0], [4.5, 4.5], [2.0, 2.0]]},
            {"input": {"points": _KM_BIG_POINTS, "centroids": [[0, 0], [10, 0], [0, 10], [10, 10]]}, "output": [[2.5, 2.5], [7.5, 2.5], [2.5, 7.5], [7.5, 7.5]]},
        ],
        "solution": (
            "class Solution:\n"
            "    def kmeansStep(self, points: List[List[float]], centroids: List[List[float]]) -> List[List[float]]:\n"
            "        k = len(centroids)\n"
            "        d = len(centroids[0])\n"
            "        sums = [[0.0] * d for _ in range(k)]\n"
            "        counts = [0] * k\n"
            "        for p in points:\n"
            "            best, best_d2 = 0, float('inf')\n"
            "            for j, c in enumerate(centroids):\n"
            "                d2 = 0.0\n"
            "                for a, b in zip(p, c):\n"
            "                    d2 += (a - b) * (a - b)\n"
            "                if d2 < best_d2:\n"
            "                    best, best_d2 = j, d2\n"
            "            counts[best] += 1\n"
            "            for i in range(d):\n"
            "                sums[best][i] += p[i]\n"
            "        new_centroids = []\n"
            "        for j in range(k):\n"
            "            if counts[j] == 0:\n"
            "                new_centroids.append([float(v) for v in centroids[j]])\n"
            "            else:\n"
            "                new_centroids.append([s / counts[j] for s in sums[j]])\n"
            "        return new_centroids\n"
        ),
        "approach": (
            "**Lloyd's algorithm alternates two exact minimisations of the within-cluster sum of squares.** Holding the "
            "centroids fixed, assigning every point to its nearest centroid minimises the objective; holding the "
            "assignments fixed, the mean of each cluster is the point that minimises the summed squared distance. Each "
            "step therefore never increases the objective, which is why k-means converges (to a local optimum).\n\n"
            "Implementation notes: compare squared distances to avoid `sqrt`; use a strict `<` while scanning centroids "
            "in order so ties resolve to the lowest index; keep running sums and counts rather than building lists of "
            "members. The empty-cluster rule (keep the old position) is one common convention; others re-seed the "
            "centroid at the farthest point.\n\n"
            "**Interview follow-ups:** How do you initialise? (random points, or k-means++ which picks seeds with "
            "probability proportional to squared distance from existing seeds, giving an O(log k) approximation "
            "guarantee). How do you decide convergence and choose k? (centroid shift below a tolerance or assignments "
            "unchanged; elbow or silhouette for k). Why does k-means struggle with non-spherical clusters or features on "
            "different scales? What is the per-iteration complexity and how would you speed it up for large n? "
            "(O(n k d); mini-batch k-means, triangle-inequality pruning, KD-trees in low dimension)."
        ),
        "complexity": {"time": "O(n * k * d)", "space": "O(k * d)"},
        "similar": ["knn-classify", "pca-power-iteration"],
    },
    # ------------------------------------------------------------------ 6
    {
        "id": "knn-classify",
        "title": "k-Nearest Neighbours Classifier",
        "difficulty": "Medium",
        "pattern": "ML Coding",
        "tags": ["Classification", "Geometry", "Heap / Priority Queue"],
        "companies": {"apple": 4, "google": 2, "meta": 2, "amazon": 4, "microsoft": 3},
        "description": (
            "Implement **k-nearest-neighbour classification**. You are given `train_points` (a list of `d`-dimensional "
            "points), the matching integer `train_labels`, a list of `queries` (points of the same dimension) and an "
            "integer `k`.\n\n"
            "For each query, find its `k` nearest training points by Euclidean distance and return the label that occurs "
            "most often among them. Tie-break rules:\n\n"
            "- If two training points are at exactly the same distance, the one with the **smaller index** is considered "
            "nearer.\n"
            "- If several labels tie for the most votes, return the **smallest label**.\n\n"
            "Return a list with one predicted label per query (an empty list for no queries)."
        ),
        "examples": [
            {"input": "train_points = [[0,0],[1,0],[0,1],[5,5],[6,5],[5,6]], train_labels = [0,0,0,1,1,1], queries = [[0.5,0.5],[5.5,5.5]], k = 3",
             "output": "[0, 1]", "explanation": "The three closest points to (0.5, 0.5) all carry label 0; the three closest to (5.5, 5.5) carry label 1."},
            {"input": "train_points = [[0,0],[10,0]], train_labels = [7,3], queries = [[4,0]], k = 2", "output": "[3]",
             "explanation": "Both neighbours get one vote each; the smaller label, 3, wins."},
            {"input": "train_points = [[1,1],[1,1],[2,2],[2,2]], train_labels = [4,1,3,2], queries = [[1,1],[2,2]], k = 2", "output": "[1, 2]"},
        ],
        "constraints": ["1 <= len(train_points) <= 10^4", "1 <= k <= len(train_points)", "0 <= len(queries) <= 10^3", "1 <= d <= 10"],
        "hints": [
            "For each query compute the squared distance to every training point; the square root is unnecessary for ordering.",
            "Sort (distance, index) pairs or use heapq.nsmallest with that key, then take the first k.",
            "Count labels among the k neighbours with a Counter and pick max by (count, -label), or sort candidates by (-count, label).",
        ],
        "function": "knnClassify",
        "signature": "def knnClassify(self, train_points: List[List[float]], train_labels: List[int], queries: List[List[float]], k: int) -> List[int]:",
        "arg_types": {"train_points": "List[List[float]]", "train_labels": "List[int]", "queries": "List[List[float]]", "k": "int"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"train_points": _KNN_TRAIN, "train_labels": _KNN_LABELS, "queries": [[0.5, 0.5], [5.5, 5.5]], "k": 3}, "output": [0, 1]},
            {"input": {"train_points": [[0, 0], [10, 0]], "train_labels": [7, 3], "queries": [[4, 0]], "k": 2}, "output": [3]},
            {"input": {"train_points": [[1, 1], [1, 1], [2, 2], [2, 2]], "train_labels": [4, 1, 3, 2], "queries": [[1, 1], [2, 2]], "k": 2}, "output": [1, 2]},
            {"input": {"train_points": _KNN_TRAIN, "train_labels": _KNN_LABELS, "queries": [[2.5, 2.5]], "k": 1}, "output": [0]},
            {"input": {"train_points": _KNN_TRAIN, "train_labels": _KNN_LABELS, "queries": [[100, 100]], "k": 6}, "output": [0]},
            {"input": {"train_points": _KNN_TRAIN, "train_labels": _KNN_LABELS, "queries": [], "k": 3}, "output": []},
            {"input": {"train_points": [[0], [1], [2], [3], [4]], "train_labels": [2, 2, 1, 1, 1], "queries": [[1.2], [3.9], [2.0]], "k": 3}, "output": [2, 1, 1]},
            {"input": {"train_points": [[i % 100, i // 100] for i in range(5000)], "train_labels": [1 if (i % 100) >= 50 else 0 for i in range(5000)],
                       "queries": [[10, 10], [90, 40], [49.4, 25], [50.6, 3]], "k": 5}, "output": [0, 1, 0, 1]},
        ],
        "solution": (
            "class Solution:\n"
            "    def knnClassify(self, train_points: List[List[float]], train_labels: List[int], queries: List[List[float]], k: int) -> List[int]:\n"
            "        preds = []\n"
            "        for q in queries:\n"
            "            dists = []\n"
            "            for idx, p in enumerate(train_points):\n"
            "                d2 = sum((a - b) * (a - b) for a, b in zip(q, p))\n"
            "                dists.append((d2, idx))\n"
            "            nearest = heapq.nsmallest(k, dists)\n"
            "            votes = Counter(train_labels[idx] for _, idx in nearest)\n"
            "            best_label = min(votes, key=lambda lab: (-votes[lab], lab))\n"
            "            preds.append(best_label)\n"
            "        return preds\n"
        ),
        "approach": (
            "**k-NN has no training step: prediction is a distance query followed by a vote.** For each query compute the "
            "squared Euclidean distance to all training points, select the k smallest (sorting is O(n log n); a bounded "
            "heap or `heapq.nsmallest` is O(n log k)), and return the plurality label. Sorting tuples `(distance, index)` "
            "gives the required lowest-index rule for equal distances, and choosing the label with key `(-count, label)` "
            "gives the smallest label on vote ties.\n\n"
            "Pitfalls: computing `sqrt` needlessly, letting Python's `Counter.most_common` break ties by insertion order "
            "instead of by label, and forgetting that features on different scales dominate the distance, so inputs are "
            "normally standardised first.\n\n"
            "**Interview follow-ups:** How do you choose k and why should it be odd for binary problems? What is the "
            "query cost and how do you scale to millions of points? (KD-trees/ball trees in low dimension, locality-"
            "sensitive hashing or approximate indexes such as HNSW in high dimension). How would you weight votes by "
            "inverse distance, and how does k-NN regression differ? (average the neighbours' targets). Why does k-NN "
            "degrade in high dimensions? (distances concentrate, the curse of dimensionality)."
        ),
        "complexity": {"time": "O(q * n * d + q * n log k)", "space": "O(n)"},
        "similar": ["k-means-step", "k-closest-points-to-origin"],
    },
    # ------------------------------------------------------------------ 7
    {
        "id": "logistic-regression-sgd",
        "title": "Logistic Regression by Gradient Descent",
        "difficulty": "Medium",
        "pattern": "ML Coding",
        "tags": ["Optimisation", "Classification", "Gradient Descent"],
        "companies": {"apple": 5, "google": 3, "meta": 3, "amazon": 3, "microsoft": 3},
        "description": (
            "Train a **logistic regression** classifier with full-batch gradient descent.\n\n"
            "You are given `X`, a list of `n` samples each with `d` features, binary targets `y`, a learning rate `lr` and "
            "a number of `epochs`. Starting from **all-zero weights and zero bias**, repeat `epochs` times:\n\n"
            "1. For every sample compute `p_i = sigmoid(w . x_i + b)`.\n"
            "2. Compute the mean gradients of the log-loss: `grad_w = (1/n) * sum_i (p_i - y_i) * x_i` and "
            "`grad_b = (1/n) * sum_i (p_i - y_i)`.\n"
            "3. Update `w -= lr * grad_w` and `b -= lr * grad_b`.\n\n"
            "Return the learned parameters as one flat list `[w_1, ..., w_d, b]`. With `epochs = 0` return all zeros."
        ),
        "examples": [
            {"input": "X = [[1.0],[2.0]], y = [0,1], lr = 1.0, epochs = 1", "output": "[0.25, 0.0]",
             "explanation": "At zero weights every p_i = 0.5. grad_w = ((0.5)(1) + (-0.5)(2)) / 2 = -0.25, grad_b = 0, so w becomes 0.25 and b stays 0."},
            {"input": "X = [[0.0],[1.0],[2.0],[3.0]], y = [0,0,1,1], lr = 0.1, epochs = 100", "output": "[1.186127, -1.195917]",
             "explanation": "The decision boundary w*x + b = 0 settles near x = 1.0, between the two classes."},
            {"input": "X = [[0.5,-1.0],[1.5,2.0]], y = [1,0], lr = 0.1, epochs = 0", "output": "[0.0, 0.0, 0.0]"},
        ],
        "constraints": ["1 <= n <= 1000", "1 <= d <= 5", "0 <= epochs <= 1000", "Compared with tolerance 1e-4."],
        "hints": [
            "The gradient of the mean log-loss with respect to the logit is simply (p - y) / n; chain it through z = w.x + b.",
            "Accumulate the gradients over all samples before applying a single update per epoch (full batch, not per-sample).",
            "Guard sigmoid against overflow for very negative z: branch on the sign of z or clamp z.",
        ],
        "function": "logisticRegressionGD",
        "signature": "def logisticRegressionGD(self, X: List[List[float]], y: List[int], lr: float, epochs: int) -> List[float]:",
        "arg_types": {"X": "List[List[float]]", "y": "List[int]", "lr": "float", "epochs": "int"},
        "return_type": "List[float]",
        "compare": "float",
        "tolerance": 1e-4,
        "tests": [
            {"input": {"X": [[1.0], [2.0]], "y": [0, 1], "lr": 1.0, "epochs": 1}, "output": [0.25, 0.0]},
            {"input": {"X": [[0.0], [1.0], [2.0], [3.0]], "y": [0, 0, 1, 1], "lr": 0.1, "epochs": 100}, "output": [1.186127, -1.195917]},
            {"input": {"X": [[0.5, -1.0], [1.5, 2.0]], "y": [1, 0], "lr": 0.1, "epochs": 0}, "output": [0.0, 0.0, 0.0]},
            {"input": {"X": [[1.0, 2.0], [2.0, 1.0], [3.0, 3.0], [4.0, 5.0]], "y": [0, 0, 1, 1], "lr": 0.05, "epochs": 200}, "output": [0.220181, 0.516701, -1.364467]},
            {"input": {"X": [[-2.0], [-1.0], [1.0], [2.0]], "y": [0, 0, 1, 1], "lr": 0.5, "epochs": 50}, "output": [2.777381, 0.0]},
            {"input": {"X": [[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]], "y": [1, 1, 1], "lr": 0.1, "epochs": 30}, "output": [0.705016, 0.705016, 0.431423]},
            {"input": {"X": _LR_BIG_X, "y": _LR_BIG_Y, "lr": 0.1, "epochs": 300}, "output": [3.002848, -1.388115, 0.407651]},
        ],
        "solution": (
            "def _sigmoid(z: float) -> float:\n"
            "    if z >= 0:\n"
            "        return 1.0 / (1.0 + math.exp(-z))\n"
            "    ez = math.exp(z)\n"
            "    return ez / (1.0 + ez)\n"
            "\n"
            "class Solution:\n"
            "    def logisticRegressionGD(self, X: List[List[float]], y: List[int], lr: float, epochs: int) -> List[float]:\n"
            "        n, d = len(X), len(X[0])\n"
            "        w = [0.0] * d\n"
            "        b = 0.0\n"
            "        for _ in range(epochs):\n"
            "            grad_w = [0.0] * d\n"
            "            grad_b = 0.0\n"
            "            for xi, yi in zip(X, y):\n"
            "                z = b\n"
            "                for j in range(d):\n"
            "                    z += w[j] * xi[j]\n"
            "                err = _sigmoid(z) - yi\n"
            "                for j in range(d):\n"
            "                    grad_w[j] += err * xi[j]\n"
            "                grad_b += err\n"
            "            for j in range(d):\n"
            "                w[j] -= lr * grad_w[j] / n\n"
            "            b -= lr * grad_b / n\n"
            "        return w + [b]\n"
        ),
        "approach": (
            "**The log-loss gradient for a sigmoid output is `(p - y) x`, the same shape as linear regression's.** "
            "Writing the loss as `-(y ln p + (1-y) ln(1-p))` with `p = sigmoid(z)`, the derivative with respect to `z` "
            "collapses to `p - y` because `sigmoid'(z) = p(1-p)` cancels the denominators. Chain through `z = w.x + b` to "
            "get `(p - y) x` for the weights and `(p - y)` for the bias, average over the batch, and step against the "
            "gradient. The loss is convex, so plain gradient descent with a reasonable learning rate converges to the "
            "global optimum.\n\n"
            "Numerical care: `exp(-z)` overflows for `z < -709`, so compute the sigmoid with a sign branch. Keep the "
            "update full-batch (one step per epoch) so results are deterministic and match the reference. Note that on "
            "perfectly separable data the weights grow without bound; regularisation or early stopping fixes that.\n\n"
            "**Interview follow-ups:** How does stochastic or mini-batch SGD change the loop and why is it preferred at "
            "scale? How would you add L2 regularisation? (add `lambda * w` to `grad_w`, not to the bias). Why is the "
            "loss convex and what would Newton's method look like here? (Hessian `X^T diag(p(1-p)) X`, IRLS). How do you "
            "generalise to multi-class? (softmax regression, gradient `(P - Y)^T X`)."
        ),
        "complexity": {"time": "O(epochs * n * d)", "space": "O(d)"},
        "similar": ["linear-regression-normal-equation", "cross-entropy-loss", "softmax"],
    },
    # ------------------------------------------------------------------ 8
    {
        "id": "linear-regression-normal-equation",
        "title": "Linear Regression via the Normal Equations",
        "difficulty": "Hard",
        "pattern": "ML Coding",
        "tags": ["Linear Algebra", "Regression", "Gaussian Elimination"],
        "companies": {"apple": 4, "google": 3, "meta": 2, "amazon": 3, "microsoft": 3},
        "description": (
            "Fit an ordinary least-squares model `y = w . x + b` **in closed form**.\n\n"
            "You are given `X`, a list of `n` samples with `d` features each (`1 <= d <= 3`), and targets `y`. Append a "
            "constant feature 1 to every sample to absorb the bias, form the normal equations "
            "`(A^T A) theta = A^T y` where `A` is the augmented `n x (d+1)` matrix, and solve the `(d+1) x (d+1)` linear "
            "system with **Gaussian elimination that you implement yourself** (partial pivoting recommended).\n\n"
            "Return `[w_1, ..., w_d, b]`. All test systems are well conditioned and have a unique solution."
        ),
        "examples": [
            {"input": "X = [[1],[2],[3]], y = [3,5,7]", "output": "[2.0, 1.0]", "explanation": "The points lie exactly on y = 2x + 1."},
            {"input": "X = [[0],[1],[2]], y = [1,2,2]", "output": "[0.5, 1.166667]",
             "explanation": "Classic simple regression: slope = Sxy/Sxx = 1/2, intercept = mean(y) - slope * mean(x) = 5/3 - 0.5."},
            {"input": "X = [[1,2],[2,1],[3,4],[4,3],[5,5]], y = [8,7,14,13,18]", "output": "[1.0, 2.0, 3.0]",
             "explanation": "The data satisfy y = x1 + 2*x2 + 3 exactly."},
        ],
        "constraints": ["d + 1 <= n <= 10^4", "1 <= d <= 3", "A^T A is invertible for every test.", "Compared with tolerance 1e-4."],
        "hints": [
            "Build the (d+1) x (d+1) Gram matrix G[i][j] = sum_r A[r][i] * A[r][j] and the vector v[i] = sum_r A[r][i] * y[r] in one pass over the data; never materialise A^T A via an n x n product.",
            "Solve G theta = v by forward elimination: for each column pick the row with the largest absolute value as pivot (partial pivoting), swap, and eliminate below.",
            "Back-substitute from the last row upward. The last unknown is the bias because the constant column was appended at the end.",
        ],
        "function": "linearRegression",
        "signature": "def linearRegression(self, X: List[List[float]], y: List[float]) -> List[float]:",
        "arg_types": {"X": "List[List[float]]", "y": "List[float]"},
        "return_type": "List[float]",
        "compare": "float",
        "tolerance": 1e-4,
        "tests": [
            {"input": {"X": [[1], [2], [3]], "y": [3, 5, 7]}, "output": [2.0, 1.0]},
            {"input": {"X": [[0], [1], [2]], "y": [1, 2, 2]}, "output": [0.5, 1.166667]},
            {"input": {"X": [[1, 2], [2, 1], [3, 4], [4, 3], [5, 5]], "y": [8, 7, 14, 13, 18]}, "output": [1.0, 2.0, 3.0]},
            {"input": {"X": [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1], [2, 1, 0]], "y": [3, 4, 5, 10, 7]}, "output": [1.625, 2.875, 4.125, 1.125]},
            {"input": {"X": [[1, 2], [2, 3], [3, 5], [4, 4]], "y": [5, 7, 9, 10]}, "output": [1.388889, 0.388889, 2.916667]},
            {"input": {"X": [[2.0], [4.0]], "y": [1.0, 2.0]}, "output": [0.5, 0.0]},
            {"input": {"X": [[0, 0, 0], [1, 2, 3], [2, 1, 0], [3, 3, 1], [1, 0, 2], [0, 2, 1]], "y": [1, 3, 2, 5, 0, 4]}, "output": [-0.270349, 1.715116, -0.351744, 0.938953]},
            {"input": {"X": [[(i % 17) / 4.0, (i % 23) / 5.0, (i % 29) / 7.0] for i in range(4000)],
                       "y": [2.0 * ((i % 17) / 4.0) - 1.5 * ((i % 23) / 5.0) + 0.5 * ((i % 29) / 7.0) + 4.0 for i in range(4000)]},
             "output": [2.0, -1.5, 0.5, 4.0]},
        ],
        "solution": (
            "class Solution:\n"
            "    def linearRegression(self, X: List[List[float]], y: List[float]) -> List[float]:\n"
            "        m = len(X[0]) + 1  # features plus bias column\n"
            "        G = [[0.0] * m for _ in range(m)]\n"
            "        v = [0.0] * m\n"
            "        for row, target in zip(X, y):\n"
            "            a = list(row) + [1.0]\n"
            "            for i in range(m):\n"
            "                v[i] += a[i] * target\n"
            "                for j in range(m):\n"
            "                    G[i][j] += a[i] * a[j]\n"
            "        return self._solve(G, v)\n"
            "\n"
            "    def _solve(self, G: List[List[float]], v: List[float]) -> List[float]:\n"
            "        m = len(v)\n"
            "        M = [G[i][:] + [v[i]] for i in range(m)]  # augmented matrix\n"
            "        for col in range(m):\n"
            "            pivot = max(range(col, m), key=lambda r: abs(M[r][col]))\n"
            "            M[col], M[pivot] = M[pivot], M[col]\n"
            "            for r in range(col + 1, m):\n"
            "                factor = M[r][col] / M[col][col]\n"
            "                if factor != 0.0:\n"
            "                    for c in range(col, m + 1):\n"
            "                        M[r][c] -= factor * M[col][c]\n"
            "        theta = [0.0] * m\n"
            "        for i in range(m - 1, -1, -1):\n"
            "            s = M[i][m]\n"
            "            for j in range(i + 1, m):\n"
            "                s -= M[i][j] * theta[j]\n"
            "            theta[i] = s / M[i][i]\n"
            "        return theta\n"
        ),
        "approach": (
            "**Setting the gradient of the squared error to zero gives the normal equations `A^T A theta = A^T y`.** "
            "The residual `A theta - y` must be orthogonal to every column of `A`; that is exactly what the equation says. "
            "Appending a constant 1 to each sample folds the bias into `theta`, so one solver handles both weights and "
            "intercept. The Gram matrix is only `(d+1) x (d+1)`, so we accumulate it in a single pass over the data "
            "(O(n d^2)) and then solve a tiny dense system.\n\n"
            "Gaussian elimination with partial pivoting: for each column choose the remaining row with the largest "
            "absolute entry, swap it up, and subtract multiples to zero out the entries below; then back-substitute. "
            "Pivoting keeps the multipliers at most 1 in magnitude, which bounds error growth. Without it a tiny pivot "
            "can destroy precision even on well-conditioned problems.\n\n"
            "**Interview follow-ups:** When is `A^T A` singular or ill conditioned, and what then? (collinear features; "
            "forming `A^T A` squares the condition number, so prefer QR or SVD, or add ridge `lambda I` which also makes "
            "the matrix invertible). Normal equations vs gradient descent: when do you pick each? (closed form is O(n d^2 "
            "+ d^3), ideal for small d; GD for huge d or streaming). How do you compute R^2 and residuals from theta? "
            "How would you add polynomial features or standardise inputs first?"
        ),
        "complexity": {"time": "O(n * d^2 + d^3)", "space": "O(d^2)"},
        "similar": ["logistic-regression-sgd", "pca-power-iteration"],
    },
    # ------------------------------------------------------------------ 9
    {
        "id": "iou-and-nms",
        "title": "IoU and Non-Maximum Suppression",
        "difficulty": "Medium",
        "pattern": "ML Coding",
        "tags": ["Computer Vision", "Geometry", "Greedy", "Sorting"],
        "companies": {"apple": 5, "google": 3, "meta": 3, "amazon": 3, "microsoft": 2},
        "description": (
            "Implement **non-maximum suppression** for object detection.\n\n"
            "You are given `boxes`, where each box is `[x1, y1, x2, y2]` with `x1 < x2` and `y1 < y2`, a parallel list of "
            "confidence `scores`, and `iou_threshold`. Repeatedly take the remaining box with the **highest score** "
            "(lowest index on equal scores), keep it, and discard every remaining box whose **intersection over union** "
            "with it is **strictly greater** than the threshold. Stop when no boxes remain.\n\n"
            "IoU is `intersection_area / (area_a + area_b - intersection_area)`, using continuous areas "
            "`(x2 - x1) * (y2 - y1)`. Return the indices of the kept boxes in the order they were selected "
            "(descending score)."
        ),
        "examples": [
            {"input": "boxes = [[0,0,10,10],[1,1,11,11],[20,20,30,30],[0,0,5,5]], scores = [0.9,0.8,0.7,0.6], iou_threshold = 0.5",
             "output": "[0, 2, 3]",
             "explanation": "Box 0 is kept first. Box 1 overlaps it with IoU 81/119 = 0.68 > 0.5 and is dropped. Box 3 has IoU 25/100 = 0.25 and survives; box 2 does not touch anything."},
            {"input": "boxes = [[0,0,10,10],[1,1,11,11],[20,20,30,30],[0,0,5,5]], scores = [0.9,0.8,0.7,0.6], iou_threshold = 0.0",
             "output": "[0, 2]", "explanation": "With threshold 0 any positive overlap is suppressed, so only disjoint boxes survive."},
            {"input": "boxes = [[0,0,1,1],[0,0,1,1],[0,0,1,1]], scores = [0.5,0.9,0.5], iou_threshold = 0.5", "output": "[1]"},
        ],
        "constraints": ["0 <= len(boxes) <= 2000", "0 <= iou_threshold <= 1", "Coordinates are integers or floats with x1 < x2 and y1 < y2."],
        "hints": [
            "Write an iou(a, b) helper first: the intersection rectangle is [max(x1s), max(y1s), min(x2s), min(y2s)]; clamp negative widths or heights to 0.",
            "Sort indices by (-score, index). Walk that order with a 'suppressed' flag array; each time you keep a box, compare it against the later unsuppressed ones.",
            "Use strict > against the threshold so that touching boxes (IoU 0) are kept when the threshold is 0.",
        ],
        "function": "nms",
        "signature": "def nms(self, boxes: List[List[float]], scores: List[float], iou_threshold: float) -> List[int]:",
        "arg_types": {"boxes": "List[List[float]]", "scores": "List[float]", "iou_threshold": "float"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"boxes": [[0, 0, 10, 10], [1, 1, 11, 11], [20, 20, 30, 30], [0, 0, 5, 5]], "scores": [0.9, 0.8, 0.7, 0.6], "iou_threshold": 0.5}, "output": [0, 2, 3]},
            {"input": {"boxes": [[0, 0, 10, 10], [1, 1, 11, 11], [20, 20, 30, 30], [0, 0, 5, 5]], "scores": [0.9, 0.8, 0.7, 0.6], "iou_threshold": 0.0}, "output": [0, 2]},
            {"input": {"boxes": [[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1]], "scores": [0.5, 0.9, 0.5], "iou_threshold": 0.5}, "output": [1]},
            {"input": {"boxes": [], "scores": [], "iou_threshold": 0.5}, "output": []},
            {"input": {"boxes": [[3, 3, 7, 7]], "scores": [0.1], "iou_threshold": 0.5}, "output": [0]},
            {"input": {"boxes": [[0, 0, 10, 10], [1, 1, 11, 11], [2, 2, 12, 12], [8, 8, 18, 18]], "scores": [0.5, 0.95, 0.6, 0.7], "iou_threshold": 0.3}, "output": [1, 3]},
            {"input": {"boxes": [[0, 0, 4, 4], [2, 2, 6, 6], [4, 4, 8, 8]], "scores": [0.7, 0.9, 0.8], "iou_threshold": 0.1}, "output": [1]},
            {"input": {"boxes": [[i * 10, 0, i * 10 + 10, 10] for i in range(500)] + [[i * 10 + 1, 1, i * 10 + 11, 11] for i in range(500)],
                       "scores": [0.9] * 500 + [0.8] * 500, "iou_threshold": 0.5}, "output": list(range(500))},
        ],
        "solution": (
            "def _iou(a: List[float], b: List[float]) -> float:\n"
            "    ix1, iy1 = max(a[0], b[0]), max(a[1], b[1])\n"
            "    ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])\n"
            "    inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)\n"
            "    area_a = (a[2] - a[0]) * (a[3] - a[1])\n"
            "    area_b = (b[2] - b[0]) * (b[3] - b[1])\n"
            "    union = area_a + area_b - inter\n"
            "    return inter / union if union > 0 else 0.0\n"
            "\n"
            "class Solution:\n"
            "    def nms(self, boxes: List[List[float]], scores: List[float], iou_threshold: float) -> List[int]:\n"
            "        order = sorted(range(len(boxes)), key=lambda i: (-scores[i], i))\n"
            "        suppressed = [False] * len(boxes)\n"
            "        keep = []\n"
            "        for pos, i in enumerate(order):\n"
            "            if suppressed[i]:\n"
            "                continue\n"
            "            keep.append(i)\n"
            "            for j in order[pos + 1:]:\n"
            "                if not suppressed[j] and _iou(boxes[i], boxes[j]) > iou_threshold:\n"
            "                    suppressed[j] = True\n"
            "        return keep\n"
        ),
        "approach": (
            "**Greedy by confidence: keep the best box, drop its near-duplicates, repeat.** Detectors emit many "
            "overlapping boxes for one object; NMS assumes the highest-scoring one is the right localisation and that "
            "any other box overlapping it heavily describes the same object. Sorting by score once and walking the "
            "list with a suppression mask gives O(n^2) IoU evaluations in the worst case, which is fine for the "
            "hundreds of candidates a detector keeps after score thresholding.\n\n"
            "IoU details that interviewers probe: clamp the intersection width and height at 0 for disjoint boxes, "
            "compute the union as `area_a + area_b - inter` (not the bounding rectangle), guard a zero union, and be "
            "explicit about `>` versus `>=` at the threshold. Pixel-indexed boxes sometimes use `+1` in the side "
            "lengths; this problem uses continuous coordinates.\n\n"
            "**Interview follow-ups:** How does NMS handle multiple classes? (run it per class, or offset boxes per class "
            "so one call works). What is Soft-NMS and why might it beat hard suppression for crowded scenes? (decay "
            "neighbours' scores instead of deleting them). How would you vectorise this on a GPU or batch it? What are "
            "GIoU/DIoU and why are they used as losses rather than plain IoU? (non-zero gradient for disjoint boxes)."
        ),
        "complexity": {"time": "O(n^2) worst case after an O(n log n) sort", "space": "O(n)"},
        "similar": ["merge-intervals", "k-means-step"],
    },
    # ------------------------------------------------------------------ 10
    {
        "id": "ndcg-at-k",
        "title": "NDCG@k",
        "difficulty": "Medium",
        "pattern": "ML Coding",
        "tags": ["Metrics", "Ranking", "Information Retrieval"],
        "companies": {"apple": 4, "google": 4, "meta": 3, "amazon": 4, "microsoft": 3},
        "description": (
            "Compute **normalised discounted cumulative gain at k**.\n\n"
            "`ranked` lists the true relevance grades of the items in the order your ranker returned them. `ideal` is the "
            "list of relevance grades of **all** candidate items (in any order); the ideal ranking sorts them in "
            "descending order. Using the linear gain `gain = rel` and the discount `1 / log2(i + 2)` for the item at "
            "0-based position `i`:\n\n"
            "`DCG@k = sum_{i < k} ranked[i] / log2(i + 2)`\n\n"
            "`IDCG@k` is the same sum over the sorted `ideal` list, and `NDCG@k = DCG@k / IDCG@k`. Only the first `k` "
            "positions of each list count (fewer if a list is shorter). Return `0.0` when `IDCG@k` is 0."
        ),
        "examples": [
            {"input": "ranked = [3,2,3,0,1,2], ideal = [3,2,3,0,1,2], k = 6", "output": "0.960808",
             "explanation": "DCG = 3 + 2/log2(3) + 3/2 + 0 + 1/log2(6) + 2/log2(7) = 6.8611. The ideal order [3,3,2,2,1,0] gives IDCG = 7.1411."},
            {"input": "ranked = [3,2,3,0,1,2], ideal = [3,2,3,0,1,2], k = 3", "output": "0.977781",
             "explanation": "Only the first three positions count: DCG = 3 + 1.2619 + 1.5, IDCG = 3 + 1.8928 + 1."},
            {"input": "ranked = [0,3], ideal = [3,0], k = 1", "output": "0.0",
             "explanation": "The only relevant item is at position 2, outside the cut-off."},
        ],
        "constraints": ["0 <= len(ranked), len(ideal) <= 10^4", "1 <= k <= 10^4", "0 <= relevance <= 10", "Compared with tolerance 1e-5."],
        "hints": [
            "Write a helper dcg(rels, k) that sums rels[i] / log2(i + 2) over the first k entries; log2(i + 2) is 1 at position 0 so the top item is undiscounted.",
            "IDCG uses sorted(ideal, reverse=True), truncated to k. Check for IDCG == 0 before dividing.",
        ],
        "function": "ndcgAtK",
        "signature": "def ndcgAtK(self, ranked: List[float], ideal: List[float], k: int) -> float:",
        "arg_types": {"ranked": "List[float]", "ideal": "List[float]", "k": "int"},
        "return_type": "float",
        "compare": "float",
        "tests": [
            {"input": {"ranked": [3, 2, 3, 0, 1, 2], "ideal": [3, 2, 3, 0, 1, 2], "k": 6}, "output": 0.960808},
            {"input": {"ranked": [3, 2, 3, 0, 1, 2], "ideal": [3, 2, 3, 0, 1, 2], "k": 3}, "output": 0.977781},
            {"input": {"ranked": [0, 3], "ideal": [3, 0], "k": 1}, "output": 0.0},
            {"input": {"ranked": [0, 0, 0], "ideal": [0, 0, 0], "k": 3}, "output": 0.0},
            {"input": {"ranked": [3, 3, 2, 1], "ideal": [1, 2, 3, 3], "k": 4}, "output": 1.0},
            {"input": {"ranked": [1, 0], "ideal": [3, 2, 1, 0], "k": 3}, "output": 0.210002},
            {"input": {"ranked": [2, 1, 0, 0], "ideal": [2, 1], "k": 10}, "output": 1.0},
            {"input": {"ranked": [], "ideal": [3, 2], "k": 5}, "output": 0.0},
        ],
        "solution": (
            "class Solution:\n"
            "    def ndcgAtK(self, ranked: List[float], ideal: List[float], k: int) -> float:\n"
            "        def dcg(rels: List[float]) -> float:\n"
            "            total = 0.0\n"
            "            for i, rel in enumerate(rels[:k]):\n"
            "                total += rel / math.log2(i + 2)\n"
            "            return total\n"
            "        idcg = dcg(sorted(ideal, reverse=True))\n"
            "        if idcg == 0:\n"
            "            return 0.0\n"
            "        return dcg(ranked) / idcg\n"
        ),
        "approach": (
            "**DCG rewards relevance placed early; dividing by the best achievable DCG makes queries comparable.** The "
            "logarithmic discount `1 / log2(position + 2)` drops slowly, encoding the assumption that users scan down a "
            "list with gradually decreasing attention. Normalising by IDCG (the DCG of the perfectly sorted list) maps "
            "every query into `[0, 1]`, so the metric can be averaged over queries with different numbers of relevant "
            "items.\n\n"
            "Watch the off-by-one: with 0-based positions the discount is `log2(i + 2)` so the first item has discount 1. "
            "Truncate both lists to k before summing, and handle a query with no relevant items (IDCG 0) explicitly; "
            "conventions vary between returning 0 and skipping the query, so state yours.\n\n"
            "**Interview follow-ups:** Why do many systems use the exponential gain `2^rel - 1` instead of linear gain? "
            "(it emphasises highly relevant items). How does NDCG compare with MAP or MRR, and which suits graded versus "
            "binary relevance? How would you optimise a model for NDCG when it is non-differentiable? (LambdaRank/"
            "LambdaMART, listwise losses). How does the metric behave when `ideal` contains relevant items the ranker "
            "never retrieved?"
        ),
        "complexity": {"time": "O(n log n) for sorting the ideal list", "space": "O(n)"},
        "similar": ["roc-auc", "tf-idf"],
    },
    # ------------------------------------------------------------------ 11
    {
        "id": "tf-idf",
        "title": "TF-IDF Vectoriser",
        "difficulty": "Medium",
        "pattern": "ML Coding",
        "tags": ["NLP", "Hash Table", "Information Retrieval"],
        "companies": {"apple": 4, "google": 3, "meta": 2, "amazon": 4, "microsoft": 3},
        "description": (
            "Implement a **TF-IDF** vectoriser. You are given `docs`, a list of `N` documents (lowercase words separated "
            "by whitespace), and `vocab`, an ordered list of distinct words. For each document return a vector whose "
            "`j`-th entry is the TF-IDF weight of `vocab[j]` in that document:\n\n"
            "- `tf(word, doc) = count of word in doc / number of words in doc` (0 for an empty document)\n"
            "- `idf(word) = ln((1 + N) / (1 + df(word))) + 1`, where `df` is the number of documents containing the word "
            "(sklearn's smoothed form)\n"
            "- `tfidf = tf * idf`\n\n"
            "Do **not** normalise the vectors. Return a list of `N` vectors, each of length `len(vocab)`."
        ),
        "examples": [
            {"input": "docs = [\"the cat sat\", \"the dog sat on the mat\", \"cats and dogs\"], vocab = [\"the\", \"cat\", \"sat\", \"dog\"]",
             "output": "[[0.429227, 0.564382, 0.429227, 0.0], [0.429227, 0.0, 0.214614, 0.282191], [0.0, 0.0, 0.0, 0.0]]",
             "explanation": "N = 3. \"the\" appears in 2 docs: idf = ln(4/3) + 1 = 1.287682; in doc 0 its tf is 1/3, giving 0.429227. \"cat\" is in 1 doc: idf = ln(4/2) + 1 = 1.693147, times 1/3."},
            {"input": "docs = [\"a a b\", \"b c\"], vocab = [\"a\", \"b\", \"c\", \"z\"]",
             "output": "[[0.936977, 0.333333, 0.0, 0.0], [0.0, 0.5, 0.702733, 0.0]]",
             "explanation": "\"b\" is in every document so its idf is ln(3/3) + 1 = 1; \"z\" never appears and gets 0 everywhere."},
            {"input": "docs = [\"hello\"], vocab = [\"hello\", \"world\"]", "output": "[[1.0, 0.0]]"},
        ],
        "constraints": ["1 <= N <= 10^3", "1 <= len(vocab) <= 10^3", "Documents contain only lowercase words and spaces and may be empty.", "Compared with tolerance 1e-5."],
        "hints": [
            "Tokenise each document once with split() and keep a Counter per document; also build df by counting, per word, in how many documents the Counter is non-zero.",
            "Compute idf once per vocabulary word, then the output entry is counts[word] / len(tokens) * idf[word]. Guard the empty document.",
        ],
        "function": "tfIdf",
        "signature": "def tfIdf(self, docs: List[str], vocab: List[str]) -> List[List[float]]:",
        "arg_types": {"docs": "List[str]", "vocab": "List[str]"},
        "return_type": "List[List[float]]",
        "compare": "float",
        "tests": [
            {"input": {"docs": ["the cat sat", "the dog sat on the mat", "cats and dogs"], "vocab": ["the", "cat", "sat", "dog"]},
             "output": [[0.429227, 0.564382, 0.429227, 0.0], [0.429227, 0.0, 0.214614, 0.282191], [0.0, 0.0, 0.0, 0.0]]},
            {"input": {"docs": ["a a b", "b c"], "vocab": ["a", "b", "c", "z"]}, "output": [[0.936977, 0.333333, 0.0, 0.0], [0.0, 0.5, 0.702733, 0.0]]},
            {"input": {"docs": ["hello"], "vocab": ["hello", "world"]}, "output": [[1.0, 0.0]]},
            {"input": {"docs": ["x y", "", "y y y"], "vocab": ["x", "y"]}, "output": [[0.846574, 0.643841], [0.0, 0.0], [0.0, 1.287682]]},
            {"input": {"docs": ["apple", "apple", "apple"], "vocab": ["apple"]}, "output": [[1.0], [1.0], [1.0]]},
            {"input": {"docs": ["red blue", "blue green", "green red", "red red blue"], "vocab": ["red", "green"]},
             "output": [[0.611572, 0.0], [0.0, 0.755413], [0.611572, 0.755413], [0.815429, 0.0]]},
        ],
        "solution": (
            "class Solution:\n"
            "    def tfIdf(self, docs: List[str], vocab: List[str]) -> List[List[float]]:\n"
            "        n_docs = len(docs)\n"
            "        counts = [Counter(doc.split()) for doc in docs]\n"
            "        lengths = [sum(c.values()) for c in counts]\n"
            "        df = Counter()\n"
            "        for c in counts:\n"
            "            for word in c:\n"
            "                df[word] += 1\n"
            "        idf = {w: math.log((1 + n_docs) / (1 + df[w])) + 1.0 for w in vocab}\n"
            "        vectors = []\n"
            "        for c, length in zip(counts, lengths):\n"
            "            if length == 0:\n"
            "                vectors.append([0.0] * len(vocab))\n"
            "                continue\n"
            "            vectors.append([c[w] / length * idf[w] for w in vocab])\n"
            "        return vectors\n"
        ),
        "approach": (
            "**TF measures how much a document is about a word; IDF down-weights words that appear everywhere.** The "
            "product is large only for words that are frequent in this document yet rare across the corpus, which is "
            "what makes TF-IDF a strong baseline for retrieval and text classification. The smoothed IDF "
            "`ln((1+N)/(1+df)) + 1` behaves as if one extra document contained every word: it avoids division by zero "
            "for unseen vocabulary and never produces a zero or negative weight, so a word present in all documents "
            "still has idf 1.\n\n"
            "Implementation: tokenise once, keep a Counter per document, compute document frequency by iterating over "
            "each Counter's distinct keys (not over raw tokens, which would over-count repeats), and precompute idf per "
            "vocabulary word. Guard empty documents to avoid dividing by zero.\n\n"
            "**Interview follow-ups:** Why L2-normalise the vectors before cosine similarity, and why does sklearn do so "
            "by default? What are the alternatives to raw term frequency? (log or binary tf, BM25's saturation and length "
            "normalisation). How do you build this incrementally for a streaming corpus when idf depends on all "
            "documents? How does TF-IDF compare with dense embeddings for search, and when would you still use it?"
        ),
        "complexity": {"time": "O(total tokens + N * |vocab|)", "space": "O(total distinct tokens + N * |vocab|)"},
        "similar": ["ndcg-at-k", "group-anagrams"],
    },
    # ------------------------------------------------------------------ 12
    {
        "id": "pca-power-iteration",
        "title": "First Principal Component by Power Iteration",
        "difficulty": "Hard",
        "pattern": "ML Coding",
        "tags": ["Linear Algebra", "Dimensionality Reduction", "Numerical Methods"],
        "companies": {"apple": 4, "google": 3, "meta": 2, "amazon": 2, "microsoft": 3},
        "description": (
            "Find the **first principal component** of a small dataset without any linear-algebra library.\n\n"
            "Given `points`, a list of `n >= 2` points in `d` dimensions, and a non-zero `start` vector of length `d`:\n\n"
            "1. Subtract the per-feature mean from every point.\n"
            "2. Form the `d x d` sample covariance matrix `C = X^T X / (n - 1)` of the centred data.\n"
            "3. Run **power iteration** for exactly 500 steps from `start`: `v <- C v`, then rescale `v` to unit length.\n"
            "4. Flip the sign if needed so that the **first non-zero component is positive**, and return `v`.\n\n"
            "The start vector is never orthogonal to the dominant eigenvector, and the top eigenvalue is well separated "
            "from the rest (or the covariance is a multiple of the identity, in which case any unit vector is a valid "
            "answer and the normalised start vector is expected)."
        ),
        "examples": [
            {"input": "points = [[1,2],[2,4],[3,6],[4,8]], start = [1,1]", "output": "[0.447214, 0.894427]",
             "explanation": "All points lie on the line y = 2x, so the direction of maximum variance is (1, 2) / sqrt(5)."},
            {"input": "points = [[0,5],[1,4],[2,3],[3,2],[4,1]], start = [1,0]", "output": "[0.707107, -0.707107]",
             "explanation": "The data lie on x + y = 5. The component (1,-1)/sqrt(2) is reported with its first entry positive."},
            {"input": "points = [[1,0],[-1,0],[0,1],[0,-1]], start = [1,1]", "output": "[0.707107, 0.707107]",
             "explanation": "The covariance is isotropic, so power iteration leaves the direction of the start vector unchanged."},
        ],
        "constraints": ["2 <= n <= 10^3", "1 <= d <= 5", "start is not the zero vector.", "Compared with tolerance 1e-3."],
        "hints": [
            "Centre first: PCA is about variance around the mean, and skipping this step finds the direction of the mean instead.",
            "The covariance is symmetric: C[i][j] = sum over points of (x_i - mu_i)(x_j - mu_j) / (n - 1). You only need matrix-vector products afterwards.",
            "Each iteration multiplies by C and normalises; the component along the dominant eigenvector grows fastest and everything else decays. Fix the sign at the end, not during the loop.",
        ],
        "function": "firstPrincipalComponent",
        "signature": "def firstPrincipalComponent(self, points: List[List[float]], start: List[float]) -> List[float]:",
        "arg_types": {"points": "List[List[float]]", "start": "List[float]"},
        "return_type": "List[float]",
        "compare": "float",
        "tolerance": 1e-3,
        "tests": [
            {"input": {"points": [[1, 2], [2, 4], [3, 6], [4, 8]], "start": [1, 1]}, "output": [0.447214, 0.894427]},
            {"input": {"points": [[0, 5], [1, 4], [2, 3], [3, 2], [4, 1]], "start": [1, 0]}, "output": [0.707107, -0.707107]},
            {"input": {"points": [[1, 0], [-1, 0], [0, 1], [0, -1]], "start": [1, 1]}, "output": [0.707107, 0.707107]},
            {"input": {"points": [[2.5, 2.4], [0.5, 0.7], [2.2, 2.9], [1.9, 2.2], [3.1, 3.0], [2.3, 2.7], [2.0, 1.6], [1.0, 1.1], [1.5, 1.6], [1.1, 0.9]], "start": [1, 0]},
             "output": [0.677873, 0.735179]},
            {"input": {"points": [[1, 2, 3], [2, 4, 7], [3, 6, 9], [4, 9, 12], [5, 10, 16], [6, 12, 17]], "start": [1, 1, 1]},
             "output": [0.272436, 0.554276, 0.786484]},
            {"input": {"points": [[0, 0, 1], [0, 0, 3], [0, 0, -2], [0, 0, 5]], "start": [0.3, 0.3, 0.3]}, "output": [0.0, 0.0, 1.0]},
            {"input": {"points": [[1, 2], [2, 4], [3, 6], [4, 8]], "start": [-1, -3]}, "output": [0.447214, 0.894427]},
        ],
        "solution": (
            "class Solution:\n"
            "    def firstPrincipalComponent(self, points: List[List[float]], start: List[float]) -> List[float]:\n"
            "        n, d = len(points), len(points[0])\n"
            "        mean = [sum(p[j] for p in points) / n for j in range(d)]\n"
            "        centred = [[p[j] - mean[j] for j in range(d)] for p in points]\n"
            "        cov = [[0.0] * d for _ in range(d)]\n"
            "        for row in centred:\n"
            "            for i in range(d):\n"
            "                for j in range(i, d):\n"
            "                    cov[i][j] += row[i] * row[j]\n"
            "        for i in range(d):\n"
            "            for j in range(i, d):\n"
            "                cov[i][j] /= (n - 1)\n"
            "                cov[j][i] = cov[i][j]\n"
            "\n"
            "        def normalise(vec: List[float]) -> List[float]:\n"
            "            norm = math.sqrt(sum(x * x for x in vec))\n"
            "            return [x / norm for x in vec]\n"
            "\n"
            "        v = normalise([float(x) for x in start])\n"
            "        for _ in range(500):\n"
            "            w = [sum(cov[i][j] * v[j] for j in range(d)) for i in range(d)]\n"
            "            v = normalise(w)\n"
            "        for x in v:\n"
            "            if abs(x) > 1e-12:\n"
            "                if x < 0:\n"
            "                    v = [-y for y in v]\n"
            "                break\n"
            "        return v\n"
        ),
        "approach": (
            "**The first principal component is the top eigenvector of the covariance matrix, and power iteration "
            "finds it by repeated multiplication.** Write the start vector in the eigenbasis of `C`; each multiplication "
            "scales the component along eigenvector `i` by `lambda_i`, so after `t` steps the ratio of any other "
            "component to the dominant one shrinks like `(lambda_2 / lambda_1)^t`. Normalising each step only prevents "
            "overflow or underflow and does not change the direction. Because a covariance matrix is symmetric positive "
            "semi-definite, all eigenvalues are real and non-negative, so the iterate never oscillates in sign.\n\n"
            "Pitfalls: forgetting to centre (the result then tilts toward the mean), a start vector orthogonal to the "
            "answer (never recovers in exact arithmetic), and the sign ambiguity of eigenvectors, which the "
            "first-non-zero-positive rule resolves. Convergence is slow when `lambda_1` and `lambda_2` are close.\n\n"
            "**Interview follow-ups:** How do you get the second component? (deflate: subtract `lambda_1 v v^T` from `C` "
            "or re-orthogonalise against `v` each step, Gram-Schmidt). Covariance eigen-decomposition versus SVD of the "
            "centred data: which is more stable and why? (SVD avoids squaring the condition number). Should you "
            "standardise features before PCA? What does the top eigenvalue tell you about the explained variance ratio? "
            "How would you handle n << d (use the n x n Gram matrix instead)?"
        ),
        "complexity": {"time": "O(n * d^2 + iterations * d^2)", "space": "O(n * d)"},
        "similar": ["linear-regression-normal-equation", "k-means-step"],
    },
    # ------------------------------------------------------------------ 13
    {
        "id": "scaled-dot-product-attention",
        "title": "Scaled Dot-Product Attention",
        "difficulty": "Medium",
        "pattern": "ML Coding",
        "tags": ["Transformers", "Linear Algebra", "Deep Learning"],
        "companies": {"apple": 5, "google": 4, "meta": 4, "amazon": 3, "microsoft": 3},
        "description": (
            "Implement single-head **scaled dot-product attention**.\n\n"
            "`Q` is a list of `m` query vectors, `K` a list of `n` key vectors (same dimension `d` as the queries) and "
            "`V` a list of `n` value vectors (any dimension). Compute\n\n"
            "`Attention(Q, K, V) = softmax(Q K^T / sqrt(d)) V`\n\n"
            "where softmax is applied to each row of the `m x n` score matrix. If `causal` is true, position `i` may "
            "only attend to keys `j <= i`: set the score of every `j > i` to `-inf` before the softmax so those weights "
            "become exactly 0. Return the `m` output rows."
        ),
        "examples": [
            {"input": "Q = [[1,0],[0,1]], K = [[1,0],[0,1]], V = [[1,2],[3,4]], causal = false",
             "output": "[[1.660477, 2.660477], [2.339523, 3.339523]]",
             "explanation": "Row 0 scores are [1, 0] / sqrt(2) = [0.7071, 0]; softmax gives [0.6698, 0.3302], and 0.6698*[1,2] + 0.3302*[3,4] = [1.6605, 2.6605]."},
            {"input": "Q = [[1,0],[0,1]], K = [[1,0],[0,1]], V = [[1,2],[3,4]], causal = true",
             "output": "[[1.0, 2.0], [2.339523, 3.339523]]",
             "explanation": "Query 0 may only see key 0, so its output is exactly V[0]. Query 1 sees both keys as before."},
            {"input": "Q = [[0,0]], K = [[1,2],[3,4],[5,6]], V = [[1],[2],[3]], causal = false", "output": "[[2.0]]",
             "explanation": "A zero query scores every key equally, so the output is the plain average of the values."},
        ],
        "constraints": ["1 <= m, n <= 512", "1 <= d <= 64", "When causal is true, m == n.", "Compared with tolerance 1e-5."],
        "hints": [
            "Compute one row of scores at a time: dot(q, k_j) / sqrt(d) for every key j; you never need the full matrix in memory.",
            "Apply a numerically stable softmax to the row (subtract the row max). With -inf entries, exp(-inf - max) is 0.0 in Python, so masked keys fall out naturally.",
            "The output row is the weighted sum of value vectors: sum_j w_j * V[j].",
        ],
        "function": "attention",
        "signature": "def attention(self, Q: List[List[float]], K: List[List[float]], V: List[List[float]], causal: bool) -> List[List[float]]:",
        "arg_types": {"Q": "List[List[float]]", "K": "List[List[float]]", "V": "List[List[float]]", "causal": "bool"},
        "return_type": "List[List[float]]",
        "compare": "float",
        "tests": [
            {"input": {"Q": [[1, 0], [0, 1]], "K": [[1, 0], [0, 1]], "V": [[1, 2], [3, 4]], "causal": False}, "output": [[1.660477, 2.660477], [2.339523, 3.339523]]},
            {"input": {"Q": [[1, 0], [0, 1]], "K": [[1, 0], [0, 1]], "V": [[1, 2], [3, 4]], "causal": True}, "output": [[1.0, 2.0], [2.339523, 3.339523]]},
            {"input": {"Q": [[0, 0]], "K": [[1, 2], [3, 4], [5, 6]], "V": [[1], [2], [3]], "causal": False}, "output": [[2.0]]},
            {"input": {"Q": [[1, 1, 1], [2, 0, 1], [0, 3, 1]], "K": [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "V": [[1, 0], [0, 1], [1, 1]], "causal": True},
             "output": [[1.0, 0.0], [0.760368, 0.239632], [0.329792, 0.881426]]},
            {"input": {"Q": [[1, 1, 1], [2, 0, 1], [0, 3, 1]], "K": [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "V": [[1, 0], [0, 1], [1, 1]], "causal": False},
             "output": [[0.666667, 0.666667], [0.832057, 0.467103], [0.329792, 0.881426]]},
            {"input": {"Q": [[10.0]], "K": [[10.0], [-10.0]], "V": [[7.0], [9.0]], "causal": False}, "output": [[7.0]]},
            {"input": {"Q": [[0.5, -0.5], [1.5, 2.0], [-1.0, 0.25]], "K": [[0.3, 0.8], [-0.6, 0.4], [1.2, -0.9]], "V": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "causal": True},
             "output": [[1.0, 2.0, 3.0], [1.538261, 2.538261, 3.538261], [3.421252, 4.421252, 5.421252]]},
        ],
        "solution": (
            "class Solution:\n"
            "    def attention(self, Q: List[List[float]], K: List[List[float]], V: List[List[float]], causal: bool) -> List[List[float]]:\n"
            "        d = len(Q[0])\n"
            "        scale = 1.0 / math.sqrt(d)\n"
            "        out_dim = len(V[0])\n"
            "        outputs = []\n"
            "        for i, q in enumerate(Q):\n"
            "            scores = []\n"
            "            for j, k in enumerate(K):\n"
            "                if causal and j > i:\n"
            "                    scores.append(float('-inf'))\n"
            "                else:\n"
            "                    scores.append(sum(a * b for a, b in zip(q, k)) * scale)\n"
            "            m = max(scores)\n"
            "            weights = [math.exp(s - m) for s in scores]\n"
            "            total = sum(weights)\n"
            "            weights = [w / total for w in weights]\n"
            "            row = [0.0] * out_dim\n"
            "            for w, v in zip(weights, V):\n"
            "                if w:\n"
            "                    for c in range(out_dim):\n"
            "                        row[c] += w * v[c]\n"
            "            outputs.append(row)\n"
            "        return outputs\n"
        ),
        "approach": (
            "**Attention is a soft dictionary lookup: each query compares itself with every key, turns the similarities "
            "into a probability distribution, and returns the matching average of the values.** The `1 / sqrt(d)` scale "
            "keeps the dot products at unit variance when the components are; without it, large `d` pushes the softmax "
            "into saturation where gradients vanish. Masking with `-inf` rather than a large negative number guarantees "
            "weights that are exactly zero and plays well with the max-subtraction trick, because `exp(-inf) = 0.0`.\n\n"
            "Implementation points: process one query row at a time (O(n) memory per row), reuse the stable softmax, "
            "and skip zero-weight values in the weighted sum. The causal mask requires at least one unmasked key per "
            "row (`j = i`), so the row max is always finite.\n\n"
            "**Interview follow-ups:** How does multi-head attention differ? (split `d_model` into `h` heads, run this "
            "per head on projected Q/K/V, concatenate, project again). What are the time and memory costs for sequence "
            "length n? (O(n^2 d) time and O(n^2) score memory, the motivation for FlashAttention's tiling and online "
            "softmax). What is the KV cache in autoregressive decoding and why does it make generation O(n) per token? "
            "How would you add padding masks or relative position information?"
        ),
        "complexity": {"time": "O(m * n * (d + d_v))", "space": "O(n + m * d_v)"},
        "similar": ["softmax", "batch-norm-forward"],
    },
    # ------------------------------------------------------------------ 14
    {
        "id": "batch-norm-forward",
        "title": "Batch Normalisation Forward Pass",
        "difficulty": "Medium",
        "pattern": "ML Coding",
        "tags": ["Deep Learning", "Statistics", "Normalisation"],
        "companies": {"apple": 5, "google": 3, "meta": 3, "amazon": 2, "microsoft": 2},
        "description": (
            "Implement the **training-mode forward pass of batch normalisation** for a 2-D batch.\n\n"
            "`X` has `n` rows (samples) and `d` columns (features). For each column `j` compute the batch mean `mu_j` and "
            "the **biased** variance `var_j = (1/n) * sum_i (X[i][j] - mu_j)^2`, then output\n\n"
            "`Y[i][j] = gamma[j] * (X[i][j] - mu_j) / sqrt(var_j + eps) + beta[j]`\n\n"
            "with `eps = 1e-5`. `gamma` and `beta` are the learnable per-feature scale and shift. Return `Y` with the "
            "same shape as `X`."
        ),
        "examples": [
            {"input": "X = [[1,2],[3,4]], gamma = [1,1], beta = [0,0]", "output": "[[-0.999995, -0.999995], [0.999995, 0.999995]]",
             "explanation": "Column 0 has mean 2 and variance 1; (1 - 2) / sqrt(1 + 1e-5) = -0.999995. The epsilon is what keeps this from being exactly -1."},
            {"input": "X = [[5,5],[5,5],[5,5]], gamma = [1,1], beta = [0.5,-0.5]", "output": "[[0.5, -0.5], [0.5, -0.5], [0.5, -0.5]]",
             "explanation": "Constant columns have zero variance; eps prevents division by zero and the normalised value is 0, so the output is just beta."},
            {"input": "X = [[3.0,-1.0,7.0]], gamma = [1,1,1], beta = [0,0,0]", "output": "[[0.0, 0.0, 0.0]]",
             "explanation": "With a single sample every feature equals its own mean."},
        ],
        "constraints": ["1 <= n <= 10^4", "1 <= d <= 100", "len(gamma) == len(beta) == d", "Compared with tolerance 1e-5."],
        "hints": [
            "Statistics are per feature (per column), not per sample. Loop over columns, gather the column, compute mean then variance.",
            "Use the biased variance (divide by n), which is what training-mode batch norm uses; the unbiased form is only used for the running variance estimate in some frameworks.",
            "Add eps inside the square root before dividing.",
        ],
        "function": "batchNorm",
        "signature": "def batchNorm(self, X: List[List[float]], gamma: List[float], beta: List[float]) -> List[List[float]]:",
        "arg_types": {"X": "List[List[float]]", "gamma": "List[float]", "beta": "List[float]"},
        "return_type": "List[List[float]]",
        "compare": "float",
        "tests": [
            {"input": {"X": [[1, 2], [3, 4]], "gamma": [1, 1], "beta": [0, 0]}, "output": [[-0.999995, -0.999995], [0.999995, 0.999995]]},
            {"input": {"X": [[5, 5], [5, 5], [5, 5]], "gamma": [1, 1], "beta": [0.5, -0.5]}, "output": [[0.5, -0.5], [0.5, -0.5], [0.5, -0.5]]},
            {"input": {"X": [[3.0, -1.0, 7.0]], "gamma": [1, 1, 1], "beta": [0, 0, 0]}, "output": [[0.0, 0.0, 0.0]]},
            {"input": {"X": [[1, 2], [3, 4]], "gamma": [2, 0.5], "beta": [1, -1]}, "output": [[-0.99999, -1.499998], [2.99999, -0.500002]]},
            {"input": {"X": [[1], [2], [3], [4], [5]], "gamma": [1], "beta": [0]}, "output": [[-1.41421], [-0.707105], [0.0], [0.707105], [1.41421]]},
            {"input": {"X": [[1, 10, 100], [2, 20, 200], [3, 30, 300], [4, 40, 400]], "gamma": [1, 0.1, 0.01], "beta": [0, 1, 2]},
             "output": [[-1.341635, 0.865836, 1.986584], [-0.447212, 0.955279, 1.995528], [0.447212, 1.044721, 2.004472], [1.341635, 1.134164, 2.013416]]},
        ],
        "solution": (
            "class Solution:\n"
            "    def batchNorm(self, X: List[List[float]], gamma: List[float], beta: List[float]) -> List[List[float]]:\n"
            "        n, d = len(X), len(X[0])\n"
            "        eps = 1e-5\n"
            "        Y = [[0.0] * d for _ in range(n)]\n"
            "        for j in range(d):\n"
            "            col = [X[i][j] for i in range(n)]\n"
            "            mean = sum(col) / n\n"
            "            var = sum((x - mean) ** 2 for x in col) / n\n"
            "            inv_std = 1.0 / math.sqrt(var + eps)\n"
            "            for i in range(n):\n"
            "                Y[i][j] = gamma[j] * (col[i] - mean) * inv_std + beta[j]\n"
            "        return Y\n"
        ),
        "approach": (
            "**Standardise each feature across the batch, then let the network undo it if it wants to.** Normalising to "
            "zero mean and unit variance keeps activations in a well-scaled range so later layers see stable input "
            "distributions and larger learning rates become usable; the learnable `gamma` and `beta` restore any scale "
            "and shift the model needs, including the identity. The epsilon inside the square root guards constant "
            "features, where the variance is zero.\n\n"
            "Implementation notes: compute statistics per column, use the two-pass mean-then-variance formula (the "
            "one-pass `E[x^2] - E[x]^2` form suffers catastrophic cancellation), and divide by `n` not `n - 1`.\n\n"
            "**Interview follow-ups:** What happens at inference time? (no batch statistics; use running averages of mean "
            "and variance accumulated with momentum during training, which turns the layer into a fixed affine map that "
            "can be folded into the preceding linear layer). How does layer normalisation differ and why do transformers "
            "prefer it? (normalise across features within one sample, so it is independent of batch size and works for "
            "variable-length sequences). What goes wrong with tiny batches? Can you derive the backward pass, "
            "remembering that the mean and variance depend on every sample?"
        ),
        "complexity": {"time": "O(n * d)", "space": "O(n * d)"},
        "similar": ["scaled-dot-product-attention", "softmax"],
    },
    # ------------------------------------------------------------------ 15
    {
        "id": "reservoir-sample-deterministic",
        "title": "Reservoir Sampling with Supplied Randomness",
        "difficulty": "Easy",
        "pattern": "ML Coding",
        "tags": ["Sampling", "Streaming", "Randomised Algorithms"],
        "companies": {"apple": 4, "google": 4, "meta": 3, "amazon": 3, "microsoft": 3},
        "description": (
            "Implement **reservoir sampling** (Algorithm R) to keep a uniform sample of `k` items from a stream whose "
            "length is unknown in advance.\n\n"
            "To make the result checkable, the randomness is supplied: `rand` is a list of the same length as `stream`, "
            "and `rand[i]` plays the role of a uniformly random integer drawn from `0 .. i` when item `i` arrives.\n\n"
            "- The first `k` items (indices `0 .. k-1`) fill the reservoir in order; `rand` is ignored for them.\n"
            "- For every later item `i >= k`: if `rand[i] < k`, item `i` **replaces** reservoir slot `rand[i]`; otherwise "
            "it is discarded.\n\n"
            "Return the final reservoir. If the stream has fewer than `k` items, return all of them in order."
        ),
        "examples": [
            {"input": "stream = [10,20,30,40,50], k = 2, rand = [0,0,1,5,0]", "output": "[50, 30]",
             "explanation": "Reservoir starts as [10, 20]. Item 30 (rand 1) replaces slot 1 -> [10, 30]. Item 40 (rand 5 >= k) is skipped. Item 50 (rand 0) replaces slot 0 -> [50, 30]."},
            {"input": "stream = [1,2,3], k = 5, rand = [0,0,0]", "output": "[1, 2, 3]", "explanation": "Fewer items than k: keep everything."},
            {"input": "stream = [1,2,3,4,5,6], k = 3, rand = [0,0,0,3,4,5]", "output": "[1, 2, 3]", "explanation": "Every later draw is >= k, so nothing is replaced."},
        ],
        "constraints": ["0 <= len(stream) <= 10^5", "1 <= k <= 10^5", "len(rand) == len(stream)", "0 <= rand[i] <= i"],
        "hints": [
            "Process the stream strictly left to right and never look ahead; a reservoir sampler must work on a stream.",
            "Only one comparison per item after the reservoir is full: rand[i] < k decides replacement, and rand[i] is the slot.",
        ],
        "function": "reservoirSample",
        "signature": "def reservoirSample(self, stream: List[int], k: int, rand: List[int]) -> List[int]:",
        "arg_types": {"stream": "List[int]", "k": "int", "rand": "List[int]"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"stream": [10, 20, 30, 40, 50], "k": 2, "rand": [0, 0, 1, 5, 0]}, "output": [50, 30]},
            {"input": {"stream": [1, 2, 3], "k": 5, "rand": [0, 0, 0]}, "output": [1, 2, 3]},
            {"input": {"stream": [1, 2, 3, 4, 5, 6], "k": 3, "rand": [0, 0, 0, 3, 4, 5]}, "output": [1, 2, 3]},
            {"input": {"stream": [1, 2, 3, 4, 5, 6], "k": 3, "rand": [0, 0, 0, 2, 1, 0]}, "output": [6, 5, 4]},
            {"input": {"stream": [], "k": 3, "rand": []}, "output": []},
            {"input": {"stream": [7, 8, 9, 10], "k": 1, "rand": [0, 0, 1, 0]}, "output": [10]},
            {"input": {"stream": list(range(10)), "k": 4, "rand": [0, 1, 2, 3, 2, 9, 0, 7, 3, 1]}, "output": [6, 9, 4, 8]},
            {"input": {"stream": list(range(50000)), "k": 3, "rand": [(i * i * 7919 + 13) % (i + 1) for i in range(50000)]}, "output": [7931, 7930, 7929]},
        ],
        "solution": (
            "class Solution:\n"
            "    def reservoirSample(self, stream: List[int], k: int, rand: List[int]) -> List[int]:\n"
            "        reservoir = []\n"
            "        for i, item in enumerate(stream):\n"
            "            if i < k:\n"
            "                reservoir.append(item)\n"
            "            elif rand[i] < k:\n"
            "                reservoir[rand[i]] = item\n"
            "        return reservoir\n"
        ),
        "approach": (
            "**Keep item `i` with probability `k / (i + 1)` and evict a uniformly chosen slot; by induction every item "
            "ends up in the reservoir with probability `k / n`.** When item `i` arrives (0-based), drawing `r` uniformly "
            "from `0 .. i` and accepting if `r < k` happens with probability `k / (i + 1)`. An item already in the "
            "reservoir survives this step with probability `1 - (k / (i + 1)) * (1 / k) = i / (i + 1)`. Multiplying the "
            "survival probabilities from the moment an item enters to the end of the stream telescopes to `k / n` for "
            "every item, which is exactly uniform sampling without replacement, in one pass and O(k) memory.\n\n"
            "Supplying `rand` externally keeps the output deterministic for the judge; in production you would call "
            "`random.randint(0, i)`. The interview is mostly about the proof, so be ready to walk through the induction.\n\n"
            "**Interview follow-ups:** Prove uniformity for k = 1 and then general k. How do you sample with weights? "
            "(A-Res: key `u^(1/w)` per item, keep the k largest in a heap). How do you parallelise across shards? (each "
            "shard keeps a reservoir plus its count, then merge by weighted sampling). Why is this preferable to shuffling "
            "or to `random.sample` on data that does not fit in memory?"
        ),
        "complexity": {"time": "O(n)", "space": "O(k)"},
        "similar": ["moving-average-anomaly", "kth-largest-element-in-a-stream"],
    },
    # ------------------------------------------------------------------ 16
    {
        "id": "moving-average-anomaly",
        "title": "Moving-Window Z-Score Anomaly Detection",
        "difficulty": "Easy",
        "pattern": "ML Coding",
        "tags": ["Time Series", "Statistics", "Sliding Window"],
        "companies": {"apple": 4, "google": 2, "meta": 2, "amazon": 4, "microsoft": 3},
        "description": (
            "Flag anomalies in a time series with a trailing-window **z-score** test.\n\n"
            "Given `series`, a window size `w` and a threshold `z`, consider each index `i >= w`. Let the window be the "
            "`w` values **immediately before** `i` (`series[i-w : i]`, excluding the current value), with mean `mu` and "
            "**population** standard deviation `sigma` (divide by `w`). Index `i` is anomalous when "
            "`|series[i] - mu| > z * sigma`.\n\n"
            "Indices without a full window are never flagged, and a window with `sigma = 0` never flags its index. "
            "Return the flagged indices in increasing order."
        ),
        "examples": [
            {"input": "series = [1,2,3,2,1,2,3,100,2,1], w = 4, z = 2.0", "output": "[7]",
             "explanation": "The window before index 7 is [2,1,2,3] with mean 2 and sigma 0.7071; |100 - 2| = 98 far exceeds 2 * 0.7071. Index 8's window [1,2,3,100] has a huge sigma, so the value 2 there is not flagged."},
            {"input": "series = [1,1,1,1,10,1,1,1], w = 3, z = 2.0", "output": "[]",
             "explanation": "The window before the 10 is [1,1,1] with sigma 0, so by the rule nothing is flagged; afterwards the windows containing 10 have large sigma."},
            {"input": "series = [1,2], w = 3, z = 1.0", "output": "[]", "explanation": "No index has a full window."},
        ],
        "constraints": ["0 <= len(series) <= 10^5", "1 <= w <= 10^4", "z >= 0", "Values are floats or ints."],
        "hints": [
            "Start the loop at i = w and slice series[i-w:i]; a straightforward O(n * w) solution is acceptable for a first version.",
            "To reach O(n), maintain running sums of the window values and of their squares, then sigma^2 = sum_sq / w - mean^2 (clamp tiny negatives to 0).",
            "Compare with strict > and skip when sigma == 0.",
        ],
        "function": "detectAnomalies",
        "signature": "def detectAnomalies(self, series: List[float], w: int, z: float) -> List[int]:",
        "arg_types": {"series": "List[float]", "w": "int", "z": "float"},
        "return_type": "List[int]",
        "compare": "exact",
        "tests": [
            {"input": {"series": [1, 2, 3, 2, 1, 2, 3, 100, 2, 1], "w": 4, "z": 2.0}, "output": [7]},
            {"input": {"series": [1, 1, 1, 1, 10, 1, 1, 1], "w": 3, "z": 2.0}, "output": []},
            {"input": {"series": [1, 2], "w": 3, "z": 1.0}, "output": []},
            {"input": {"series": [5, 5, 5, 5, 5], "w": 2, "z": 1.0}, "output": []},
            {"input": {"series": [0, 10, 0, 10, 0, 10, 0, 10, 50], "w": 4, "z": 1.5}, "output": [8]},
            {"input": {"series": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "w": 3, "z": 1.0}, "output": [3, 4, 5, 6, 7, 8, 9]},
            {"input": {"series": [2.0, 4.0, 3.0, 9.0, 3.0, 3.5, 2.5, -4.0], "w": 3, "z": 2.0}, "output": [3, 7]},
            {"input": {"series": _AN_BIG_SERIES, "w": 20, "z": 3.0}, "output": [500, 1234, 1900]},
        ],
        "solution": (
            "class Solution:\n"
            "    def detectAnomalies(self, series: List[float], w: int, z: float) -> List[int]:\n"
            "        flagged = []\n"
            "        for i in range(w, len(series)):\n"
            "            window = series[i - w:i]\n"
            "            mean = sum(window) / w\n"
            "            var = sum((v - mean) ** 2 for v in window) / w\n"
            "            sigma = math.sqrt(var)\n"
            "            if sigma > 0 and abs(series[i] - mean) > z * sigma:\n"
            "                flagged.append(i)\n"
            "        return flagged\n"
        ),
        "approach": (
            "**Model the recent past as a Gaussian and flag points that are improbable under it.** The trailing window "
            "estimates the local mean and spread; a value more than `z` standard deviations away is an outlier at that "
            "moment. Excluding the current value from the window matters: including it would inflate `sigma` and hide "
            "the very spike you want to catch. The `sigma = 0` rule is a deliberate design choice: a perfectly flat "
            "history gives no scale, so any deviation would be infinitely many standard deviations away; real systems "
            "add a floor to `sigma` or require a minimum spread instead.\n\n"
            "The direct implementation recomputes each window in O(w). Rolling sums of `x` and `x^2` bring it to O(n), "
            "but `E[x^2] - E[x]^2` loses precision when the mean is large relative to the spread, so prefer Welford's "
            "algorithm or periodically recompute from scratch in production.\n\n"
            "**Interview follow-ups:** How do you prevent a detected spike from poisoning the next `w` windows? (skip "
            "flagged values when updating the statistics, or use a robust median/MAD estimator). How do you handle "
            "trends and seasonality, which this method flags as anomalies? (differencing, exponentially weighted "
            "statistics, seasonal baselines). How do you pick `w` and `z`, and what is the trade-off between detection "
            "delay and false positives?"
        ),
        "complexity": {"time": "O(n * w), or O(n) with rolling sums", "space": "O(1) extra beyond the output"},
        "similar": ["reservoir-sample-deterministic", "sliding-window-maximum"],
    },
]
