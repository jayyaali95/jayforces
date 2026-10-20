import time

import numpy as np

from check import close, eq, raises, table


def brute(y, s):
    y, s = np.asarray(y), np.asarray(s)
    p, n = s[y == 1], s[y == 0]
    return float(np.mean([(a > b) + 0.5 * (a == b) for a in p for b in n]))


rng = np.random.default_rng(11)
YR = rng.integers(0, 2, 300)
SR = np.round(rng.random(300) + 0.3 * YR, 1)

table(globals(), 1, lambda s, y, sc: s.roc_auc(y, sc), [
    ("perfect", ([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9]), 1.0),
    ("inverted", ([1, 1, 0, 0], [0.1, 0.2, 0.8, 0.9]), 0.0),
    ("all tied", ([0, 1, 0, 1], [0.5] * 4), 0.5),
    ("classic", ([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8]), 0.75),
    ("ties counted half", ([0, 1, 1], [0.3, 0.3, 0.9]), 0.75),
    ("no negatives", ([1, 1], [0.1, 0.2]), ValueError),
    ("no positives", ([0, 0], [0.1, 0.2]), ValueError),
])


def test_p1_matches_brute(sol):
    close(sol.roc_auc(YR, SR), brute(YR, SR))


def test_p1_fast(sol):
    y = np.random.default_rng(0).integers(0, 2, 200000)
    s = np.random.default_rng(1).random(200000)
    t0 = time.perf_counter()
    sol.roc_auc(y, s)
    eq(time.perf_counter() - t0 < 2, True, msg="should be O(n log n)")


def test_p2_curve_small(sol):
    fpr, tpr, th = sol.roc_curve([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8])
    close((fpr, tpr), (np.array([0, 0, 0.5, 0.5, 1]), np.array([0, 0.5, 0.5, 1, 1])))
    eq(th, np.array([np.inf, 0.8, 0.4, 0.35, 0.1]))


def test_p2_curve_ties_one_point(sol):
    fpr, tpr, th = sol.roc_curve([0, 1, 1], [0.3, 0.3, 0.9])
    eq(len(th), 3)


def test_p2_curve_ends(sol):
    fpr, tpr, _ = sol.roc_curve(YR, SR)
    eq((fpr[0], tpr[0], fpr[-1], tpr[-1]), (0.0, 0.0, 1.0, 1.0))


def test_p2_curve_monotone(sol):
    fpr, tpr, _ = sol.roc_curve(YR, SR)
    eq(bool((np.diff(fpr) >= 0).all() and (np.diff(tpr) >= 0).all()), True)


def test_p2_trapezoid_matches_auc(sol):
    fpr, tpr, _ = sol.roc_curve(YR, SR)
    close(sol.auc_trapezoid(fpr, tpr), brute(YR, SR))


def test_p2_trapezoid_square(sol):
    close(sol.auc_trapezoid([0, 0, 1], [0, 1, 1]), 1.0)


def test_p2_trapezoid_diagonal(sol):
    close(sol.auc_trapezoid([0, 1], [0, 1]), 0.5)
