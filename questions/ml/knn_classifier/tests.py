import time

import numpy as np

from check import close, eq, raises

X = np.array([[0.0, 0], [1, 0], [0, 1], [5, 5], [6, 5], [5, 6]])
Y = np.array([0, 0, 0, 1, 1, 1])


def fit(sol, k=3, **kw):
    return sol.KNNClassifier(k, **kw).fit(X, Y)


def test_p1_obvious(sol):
    eq(fit(sol).predict([[0.2, 0.2], [5.5, 5.5]]), np.array([0, 1]))


def test_p1_fit_returns_self(sol):
    m = sol.KNNClassifier()
    eq(m.fit(X, Y) is m, True)


def test_p1_k1_exact_point(sol):
    eq(fit(sol, 1).predict([[6, 5]]), np.array([1]))


def test_p1_tie_smallest_label(sol):
    m = sol.KNNClassifier(2).fit([[0.0], [2.0]], [1, 0])
    eq(m.predict([[1.0]]), np.array([0]))


def test_p1_distance_ties_by_index(sol):
    m = sol.KNNClassifier(1).fit([[-1.0], [1.0]], ["b", "a"])
    eq(m.predict([[0.0]]), np.array(["b"]))


def test_p1_string_labels(sol):
    m = sol.KNNClassifier(3).fit(X, np.where(Y == 1, "far", "near"))
    eq(m.predict([[0, 0]]), np.array(["near"]))


def test_p1_k_all(sol):
    eq(fit(sol, 6).predict([[100, 100]]), np.array([0]))


def test_p1_bad_k(sol):
    raises(ValueError, fit(sol, 7).predict, [[0, 0]])


def test_p1_k_zero(sol):
    raises(ValueError, fit(sol, 0).predict, [[0, 0]])


def test_p1_vectorized(sol):
    rng = np.random.default_rng(0)
    Xb, yb = rng.normal(size=(3000, 8)), rng.integers(0, 3, 3000)
    t0 = time.perf_counter()
    out = sol.KNNClassifier(5).fit(Xb, yb).predict(rng.normal(size=(500, 8)))
    eq((out.shape, time.perf_counter() - t0 < 5), ((500,), True))


def test_p2_distance_weights_flip(sol):
    Xt, yt = [[0.0], [3.0], [3.2]], [0, 1, 1]
    q = [[0.5]]
    eq((sol.KNNClassifier(3).fit(Xt, yt).predict(q), sol.KNNClassifier(3, weights="distance").fit(Xt, yt).predict(q)),
       (np.array([1]), np.array([0])))


def test_p2_zero_distance_only(sol):
    m = sol.KNNClassifier(3, weights="distance").fit([[0.0], [0.0], [0.1]], [1, 1, 0])
    eq(m.predict([[0.0]]), np.array([1]))


def test_p2_regressor_uniform(sol):
    close(sol.KNNRegressor(2).fit([[0.0], [1], [10]], [1.0, 3, 100]).predict([[0.4]]), np.array([2.0]))


def test_p2_regressor_distance(sol):
    m = sol.KNNRegressor(2, weights="distance").fit([[0.0], [3.0]], [0.0, 30.0])
    close(m.predict([[1.0]]), np.array([(0 / 1 + 30 / 2) / (1 / 1 + 1 / 2)]))


def test_p2_regressor_exact_hit(sol):
    m = sol.KNNRegressor(3, weights="distance").fit([[0.0], [1.0], [2.0]], [5.0, 7.0, 9.0])
    close(m.predict([[1.0]]), np.array([7.0]))


def test_p2_regressor_bad_k(sol):
    raises(ValueError, sol.KNNRegressor(9).fit([[0.0]], [1.0]).predict, [[0.0]])
