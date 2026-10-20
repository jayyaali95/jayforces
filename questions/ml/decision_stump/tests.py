import numpy as np

from check import close, eq, table

table(globals(), 1, lambda s, y: s.gini(y), [
    ("pure", [1, 1, 1], 0.0), ("even", [0, 1], 0.5), ("three classes", ["a", "b", "c"], 2 / 3),
    ("skewed", [0, 0, 0, 1], 0.375), ("empty gini", [], 0.0),
])
table(globals(), 1, lambda s, y: s.entropy(y), [
    ("pure entropy", [2, 2], 0.0), ("one bit", [0, 1], 1.0), ("two bits", [0, 1, 2, 3], 2.0),
    ("skewed entropy", [0, 0, 0, 1], -(0.75 * np.log2(0.75) + 0.25 * np.log2(0.25))), ("empty entropy", [], 0.0),
])

X = np.array([[1.0, 10], [2, 30], [3, 20], [4, 40]])
Y = np.array([0, 0, 1, 1])


def test_p2_best_split(sol):
    close(sol.best_split(X, Y), (0, 2.5, 0.5))


def test_p2_tie_smallest_feature(sol):
    close(sol.best_split(np.array([[1.0, 1], [2, 2]]), np.array([0, 1])), (0, 1.5, 0.5))


def test_p2_entropy_criterion(sol):
    close(sol.best_split(X, Y, "entropy"), (0, 2.5, 1.0))


def test_p2_second_feature(sol):
    close(sol.best_split(X, np.array([0, 1, 0, 1])), (1, 25.0, 0.5))


def test_p2_no_gain(sol):
    eq(sol.best_split(X, np.array([1, 1, 1, 1])), None)


def test_p2_constant_feature(sol):
    eq(sol.best_split(np.ones((4, 1)), Y), None)


def test_p2_stump_predict(sol):
    m = sol.Stump().fit(X, Y)
    eq((m.feature_, m.threshold_, m.predict(np.array([[0, 0], [9, 0]])).tolist()), (0, 2.5, [0, 1]))


def test_p2_stump_no_split(sol):
    m = sol.Stump().fit(np.ones((3, 1)), np.array(["b", "a", "b"]))
    eq((m.feature_, m.predict(np.zeros((2, 1))).tolist()), (None, ["b", "b"]))


def test_p2_stump_majority_tie(sol):
    m = sol.Stump().fit(np.array([[0.0], [1.0], [1.0], [1.0]]), np.array([0, 2, 1, 0]))
    eq((m.left_, m.right_), (0, 0))


def test_p2_noisy_data(sol):
    rng = np.random.default_rng(0)
    Xr = rng.random((200, 3))
    yr = (Xr[:, 2] > 0.6).astype(int)
    m = sol.Stump().fit(Xr, yr)
    eq((m.feature_, (m.predict(Xr) == yr).mean()), (2, 1.0))
