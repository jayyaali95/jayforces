import math

import numpy as np

from check import eq, raises

X = np.arange(40).reshape(20, 2)
Y = np.array([0] * 12 + [1] * 8)


def ref(n, ts, seed):
    p = np.random.default_rng(seed).permutation(n)
    k = math.ceil(ts * n)
    return p[k:], p[:k]


def test_p1_sizes(sol):
    Xtr, Xte, ytr, yte = sol.train_test_split(X, Y)
    eq((len(Xtr), len(Xte), len(ytr), len(yte)), (15, 5, 15, 5))


def test_p1_exact_indices(sol):
    tr, te = ref(20, 0.25, 0)
    Xtr, Xte, _, _ = sol.train_test_split(X, Y)
    eq((Xtr, Xte), (X[tr], X[te]))


def test_p1_labels_follow_rows(sol):
    Xtr, _, ytr, _ = sol.train_test_split(X, Y, 0.3, 4)
    eq(ytr, Y[Xtr[:, 0] // 2])


def test_p1_seed_matters(sol):
    a = sol.train_test_split(X, Y, seed=1)[1]
    b = sol.train_test_split(X, Y, seed=2)[1]
    eq(np.array_equal(a, b), False)


def test_p1_reproducible(sol):
    eq(sol.train_test_split(X, Y, seed=5)[1], sol.train_test_split(X, Y, seed=5)[1])


def test_p1_ceil(sol):
    eq(len(sol.train_test_split(X, Y, 0.21)[1]), 5)


def test_p1_lists_ok(sol):
    out = sol.train_test_split(list(range(8)), list(range(8)), 0.5, 3)
    eq(sorted(out[0].tolist() + out[1].tolist()), list(range(8)))


def test_p1_too_small(sol):
    raises(ValueError, sol.train_test_split, X, Y, 0.0)


def test_p1_all_test(sol):
    raises(ValueError, sol.train_test_split, X, Y, 1.0)


def test_p1_length_mismatch(sol):
    raises(ValueError, sol.train_test_split, X, Y[:5])


def ref_strat(y, ts, seed):
    rng = np.random.default_rng(seed)
    tr, te = [], []
    for c in np.unique(y):
        idx = np.flatnonzero(y == c)
        idx = idx[rng.permutation(len(idx))]
        k = round(ts * len(idx))
        te += idx[:k].tolist()
        tr += idx[k:].tolist()
    return tr, te


def test_p2_proportions(sol):
    _, _, ytr, yte = sol.stratified_split(X, Y)
    eq((int((yte == 0).sum()), int((yte == 1).sum())), (3, 2))


def test_p2_exact(sol):
    tr, te = ref_strat(Y, 0.25, 0)
    Xtr, Xte, _, _ = sol.stratified_split(X, Y)
    eq((Xtr, Xte), (X[tr], X[te]))


def test_p2_other_seed(sol):
    tr, te = ref_strat(Y, 0.4, 9)
    _, Xte, _, _ = sol.stratified_split(X, Y, 0.4, 9)
    eq(Xte, X[te])


def test_p2_tiny_class(sol):
    y = np.array([0] * 9 + [1])
    _, _, ytr, yte = sol.stratified_split(np.arange(10), y, 0.2)
    eq((yte.tolist(), int((ytr == 1).sum())), ([0, 0], 1))


def test_p2_string_labels(sol):
    y = np.array(["a", "b"] * 5)
    _, _, _, yte = sol.stratified_split(np.arange(10), y, 0.4)
    eq(sorted(yte.tolist()), ["a", "a", "b", "b"])
