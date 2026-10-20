import numpy as np

from check import close, eq


class Majority:
    instances = 0

    def __init__(self, **kw):
        Majority.instances += 1
        self.fitted = False

    def fit(self, X, y):
        vals, counts = np.unique(y, return_counts=True)
        self.label, self.fitted = vals[counts.argmax()], True

    def predict(self, X):
        assert self.fitted, "predict called before fit"
        return np.full(len(X), self.label)


class Threshold:
    def __init__(self, t=0.0, flip=False):
        self.t, self.flip = t, flip

    def fit(self, X, y):
        pass

    def predict(self, X):
        p = (np.asarray(X)[:, 0] > self.t).astype(int)
        return 1 - p if self.flip else p


X = np.arange(10, dtype=float).reshape(10, 1)
Y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])


def test_p1_length(sol):
    eq(len(sol.cross_val_score(Majority, X, Y, k=5)), 5)


def test_p1_majority_scores(sol):
    close(sol.cross_val_score(Majority, X, Y, k=2), [0.0, 0.0])


def test_p1_fresh_models(sol):
    Majority.instances = 0
    sol.cross_val_score(Majority, X, Y, k=5)
    eq(Majority.instances, 5)


def test_p1_params_passed(sol):
    close(sol.cross_val_score(Threshold, X, Y, k=5, params={"t": 4.5}), [1.0] * 5)


def test_p1_custom_metric(sol):
    errors = lambda t, p: float(np.sum(t != p))
    close(sol.cross_val_score(Threshold, X, Y, k=2, metric=errors, params={"t": 2.5}), [2.0, 0.0])


def test_p1_uneven_folds(sol):
    sizes = []
    sol.cross_val_score(Threshold, X, Y, k=3, metric=lambda t, p: sizes.append(len(t)) or 0.0)
    eq(sizes, [4, 3, 3])


def test_p1_returns_floats(sol):
    eq(all(type(s) is float for s in sol.cross_val_score(Majority, X, Y, k=5)), True)


def test_p2_stratified_basic(sol):
    eq(sol.stratified_folds(Y, 5), [[0, 5], [1, 6], [2, 7], [3, 8], [4, 9]])


def test_p2_stratified_continues_deal(sol):
    eq(sol.stratified_folds([1, 0, 1, 0, 0], 2), [[1, 2, 4], [0, 3]])


def test_p2_stratified_cover(sol):
    y = np.random.default_rng(0).integers(0, 3, 50)
    eq(sorted(i for f in sol.stratified_folds(y, 4) for i in f), list(range(50)))


def test_p2_stratified_balance(sol):
    y = np.array([0] * 30 + [1] * 10)
    eq([int((y[f] == 1).sum()) for f in sol.stratified_folds(y, 5)], [2, 2, 2, 2, 2])


def test_p2_grid_best(sol):
    p, s = sol.grid_search(Threshold, {"t": [0.5, 4.5, 8.5], "flip": [True, False]}, X, Y, k=5)
    eq((p, s), ({"flip": False, "t": 4.5}, 1.0))


def test_p2_grid_tie_first(sol):
    p, _ = sol.grid_search(Threshold, {"t": [100.0, 200.0]}, X, Y, k=2)
    eq(p, {"t": 100.0})


def test_p2_grid_score_is_mean(sol):
    _, s = sol.grid_search(Threshold, {"t": [2.5]}, X, Y, k=2)
    close(s, 0.8)


def test_p2_grid_sorted_keys_order(sol):
    seen = []

    def make(**kw):
        seen.append(tuple(kw.items()))
        return Threshold(**kw)

    sol.grid_search(make, {"t": [1.0, 2.0], "flip": [False]}, X, Y, k=2)
    eq(seen[0], (("flip", False), ("t", 1.0)))
