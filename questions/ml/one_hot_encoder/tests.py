import numpy as np

from check import eq, raises

V = ["xl", "standard", "lux", "standard"]


def test_p1_categories_sorted(sol):
    eq(sol.OneHotEncoder().fit(V).categories_, ["lux", "standard", "xl"])


def test_p1_fit_returns_self(sol):
    e = sol.OneHotEncoder()
    eq(e.fit(V) is e, True)


def test_p1_transform(sol):
    eq(sol.OneHotEncoder().fit(V).transform(["lux", "xl"]), np.array([[1.0, 0, 0], [0, 0, 1.0]]))


def test_p1_shape(sol):
    eq(sol.OneHotEncoder().fit(V).transform(V).shape, (4, 3))


def test_p1_rows_sum_to_one(sol):
    eq(sol.OneHotEncoder().fit(V).transform(V).sum(axis=1), np.ones(4))


def test_p1_float_dtype(sol):
    eq(sol.OneHotEncoder().fit(V).transform(V).dtype.kind, "f")


def test_p1_unknown_raises(sol):
    raises(ValueError, sol.OneHotEncoder().fit(V).transform, ["bike"])


def test_p1_numeric_categories(sol):
    eq(sol.OneHotEncoder().fit([3, 1, 2, 1]).transform([2]), np.array([[0.0, 1.0, 0.0]]))


def test_p1_empty_transform(sol):
    eq(sol.OneHotEncoder().fit(V).transform([]).shape, (0, 3))


def test_p2_ignore_unknown(sol):
    eq(sol.OneHotEncoder("ignore").fit(V).transform(["bike", "xl"]), np.array([[0.0, 0, 0], [0, 0, 1.0]]))


def test_p2_inverse(sol):
    e = sol.OneHotEncoder().fit(V)
    eq(e.inverse_transform(e.transform(V)), V)


def test_p2_inverse_zero_row(sol):
    eq(sol.OneHotEncoder().fit(V).inverse_transform(np.zeros((1, 3))), [None])


def test_p2_inverse_soft_scores(sol):
    eq(sol.OneHotEncoder().fit(V).inverse_transform(np.array([[0.2, 0.7, 0.1]])), ["standard"])


def test_p2_min_frequency(sol):
    eq(sol.OneHotEncoder(min_frequency=2).fit(V).categories_, ["standard"])


def test_p2_rare_is_unknown(sol):
    e = sol.OneHotEncoder("ignore", min_frequency=2).fit(V)
    eq(e.transform(["lux", "standard"]), np.array([[0.0], [1.0]]))
