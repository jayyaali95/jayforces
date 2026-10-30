from check import eq, table

table(globals(), 1, lambda s, n, k: s.kfold_indices(n, k), [
    ("example", (7, 3), [[0, 1, 2], [3, 4], [5, 6]]),
    ("even", (6, 3), [[0, 1], [2, 3], [4, 5]]),
    ("k equals n", (3, 3), [[0], [1], [2]]),
    ("two folds odd", (5, 2), [[0, 1, 2], [3, 4]]),
    ("many extras", (10, 4), [[0, 1, 2], [3, 4, 5], [6, 7], [8, 9]]),
    ("k too small", (5, 1), ValueError),
    ("k too big", (3, 4), ValueError),
])


def test_p1_covers_everything_once(sol):
    folds = sol.kfold_indices(103, 7)
    eq(sorted(i for f in folds for i in f), list(range(103)))


def test_p1_sizes_differ_by_at_most_one(sol):
    sizes = [len(f) for f in sol.kfold_indices(103, 7)]
    eq(max(sizes) - min(sizes) <= 1 and sizes == sorted(sizes, reverse=True), True)


table(globals(), 2, lambda s, n, k: s.kfold_splits(n, k), [
    ("splits", (5, 2), [([3, 4], [0, 1, 2]), ([0, 1, 2], [3, 4])]),
    ("three way", (3, 3), [([1, 2], [0]), ([0, 2], [1]), ([0, 1], [2])]),
    ("invalid split", (2, 5), ValueError),
])


def test_p2_train_val_disjoint(sol):
    for train, val in sol.kfold_splits(50, 6):
        eq((set(train) & set(val), sorted(train + val)), (set(), list(range(50))))


def test_p2_train_sorted(sol):
    eq(all(t == sorted(t) for t, _ in sol.kfold_splits(20, 3)), True)


def test_p2_each_index_validated_once(sol):
    eq(sorted(i for _, v in sol.kfold_splits(31, 4) for i in v), list(range(31)))
