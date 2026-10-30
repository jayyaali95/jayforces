import numpy as np

from check import eq

X = np.array([10.0, 12, 11, 13, 12, 11, 10, 12, 95])
NORMAL = np.random.default_rng(0).normal(0, 1, 1000)


def test_p1_zscore_finds_glitch(sol):
    eq(sol.zscore_mask(X, 2.5).tolist(), [False] * 8 + [True])


def test_p1_zscore_default_threshold(sol):
    eq(int(sol.zscore_mask(NORMAL).sum()) <= 5, True)


def test_p1_zscore_constant(sol):
    eq(sol.zscore_mask([3, 3, 3]).tolist(), [False] * 3)


def test_p1_zscore_dtype(sol):
    eq(sol.zscore_mask(X).dtype, np.dtype(bool))


def test_p1_zscore_strict(sol):
    x = np.array([-1.0, 1.0])
    eq(sol.zscore_mask(x, 1.0).tolist(), [False, False])


def test_p1_iqr(sol):
    eq(sol.iqr_mask(X).tolist(), [False] * 8 + [True])


def test_p1_iqr_low_outlier(sol):
    eq(sol.iqr_mask([-50, 10, 11, 12, 13, 14]).tolist(), [True] + [False] * 5)


def test_p1_iqr_k(sol):
    x = np.array([1.0, 2, 3, 4, 5, 9])
    q1, q3 = np.percentile(x, [25, 75])
    eq(sol.iqr_mask(x, 0.5).tolist(), ((x < q1 - 0.5 * (q3 - q1)) | (x > q3 + 0.5 * (q3 - q1))).tolist())


def test_p1_iqr_normal(sol):
    m = sol.iqr_mask(NORMAL)
    eq(0 < m.sum() < 30, True)


def test_p2_mad(sol):
    eq(sol.mad_mask(X).tolist(), [False] * 8 + [True])


def test_p2_mad_robust_to_many_outliers(sol):
    x = np.array([10.0] * 6 + [11.0] * 4 + [500, 600, 700])
    eq(sol.mad_mask(x).tolist()[-3:], [True, True, True])


def test_p2_mad_zero(sol):
    eq(sol.mad_mask([5, 5, 5, 5, 6]).tolist(), [False] * 4 + [True])


def test_p2_mad_threshold(sol):
    x = np.array([1.0, 2, 3, 4, 8])
    med, mad = 3.0, 1.0
    eq(sol.mad_mask(x, 2.0).tolist(), (np.abs(0.6745 * (x - med) / mad) > 2.0).tolist())


def test_p2_group(sol):
    v = np.array([10, 11, 12, 11, 60, 100, 101, 99, 102, 100, 60])
    g = np.array(["a"] * 5 + ["b"] * 6)
    eq(sol.group_iqr_mask(v, g).tolist(), [False] * 4 + [True] + [False] * 5 + [True])


def test_p2_group_order_kept(sol):
    v = np.array([100, 10, 101, 11, 99, 12, 500, 13])
    g = np.array(["b", "a"] * 4)
    eq(sol.group_iqr_mask(v, g).tolist(), [False] * 6 + [True, False])
