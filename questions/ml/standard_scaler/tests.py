import numpy as np

from check import close, eq, raises

X = np.array([[1.0, 10.0, 5.0], [3.0, 20.0, 5.0], [5.0, 60.0, 5.0]])


def test_p1_mean(sol):
    close(sol.StandardScaler().fit(X).mean_, np.array([3.0, 30.0, 5.0]))


def test_p1_std_population(sol):
    close(sol.StandardScaler().fit(X).std_, np.array([np.std([1, 3, 5]), np.std([10, 20, 60]), 1.0]))


def test_p1_fit_returns_self(sol):
    s = sol.StandardScaler()
    eq(s.fit(X) is s, True)


def test_p1_transform_zero_mean(sol):
    close(sol.StandardScaler().fit_transform(X).mean(axis=0), np.zeros(3))


def test_p1_transform_unit_std(sol):
    close(sol.StandardScaler().fit_transform(X)[:, :2].std(axis=0), np.ones(2))


def test_p1_constant_column(sol):
    close(sol.StandardScaler().fit_transform(X)[:, 2], np.zeros(3))


def test_p1_transform_new_data(sol):
    s = sol.StandardScaler().fit(X)
    close(s.transform(np.array([[3.0, 30.0, 6.0]])), np.array([[0.0, 0.0, 1.0]]))


def test_p1_not_fitted(sol):
    raises(RuntimeError, sol.StandardScaler().transform, X)


def test_p1_input_untouched(sol):
    x = X.copy()
    sol.StandardScaler().fit_transform(x)
    eq(x, X)


def test_p1_vectorized_big(sol):
    big = np.random.default_rng(0).normal(5, 3, size=(200000, 5))
    close(sol.StandardScaler().fit_transform(big).std(axis=0), np.ones(5))


def test_p2_inverse(sol):
    s = sol.StandardScaler()
    close(s.inverse_transform(s.fit_transform(X)), X)


def test_p2_nan_ignored_in_fit(sol):
    s = sol.StandardScaler().fit(np.array([[1.0], [np.nan], [3.0]]))
    close((s.mean_, s.std_), (np.array([2.0]), np.array([1.0])))


def test_p2_nan_kept(sol):
    z = sol.StandardScaler().fit_transform(np.array([[1.0], [np.nan], [3.0]]))
    eq(np.isnan(z[:, 0]).tolist(), [False, True, False])


def test_p2_all_nan_column(sol):
    s = sol.StandardScaler().fit(np.array([[np.nan, 1.0], [np.nan, 3.0]]))
    close((s.mean_, s.std_), (np.array([0.0, 2.0]), np.array([1.0, 1.0])))


def test_p2_inverse_before_fit(sol):
    raises(RuntimeError, sol.StandardScaler().inverse_transform, X)
