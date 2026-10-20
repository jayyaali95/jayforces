import time

import numpy as np

from check import close, eq, raises

X = np.array([1.0, 2.0, 3.0, 4.0, 10.0])


def test_p1_basic(sol):
    close(sol.sma(X, 2), np.array([1.5, 2.5, 3.5, 7.0]))


def test_p1_window_one(sol):
    close(sol.sma(X, 1), X)


def test_p1_full_window(sol):
    close(sol.sma(X, 5), np.array([4.0]))


def test_p1_list_input(sol):
    close(sol.sma([2, 4, 6], 3), np.array([4.0]))


def test_p1_bad_window(sol):
    raises(ValueError, sol.sma, X, 0)


def test_p1_window_too_big(sol):
    raises(ValueError, sol.sma, X, 6)


def test_p1_fast(sol):
    x = np.random.default_rng(0).random(2_000_000)
    t0 = time.perf_counter()
    out = sol.sma(x, 500)
    eq((len(out), time.perf_counter() - t0 < 1.5), (len(x) - 499, True))


def test_p1_random_matches(sol):
    x = np.random.default_rng(2).random(50)
    close(sol.sma(x, 7), np.array([x[i:i + 7].mean() for i in range(44)]))


def test_p2_ema(sol):
    close(sol.ema([10, 20, 30], 0.5), np.array([10.0, 15.0, 22.5]))


def test_p2_ema_alpha_one(sol):
    close(sol.ema(X, 1.0), X)


def test_p2_ema_bad_alpha(sol):
    raises(ValueError, sol.ema, X, 0)


def test_p2_ema_alpha_over_one(sol):
    raises(ValueError, sol.ema, X, 1.5)


def test_p2_zscore(sol):
    z = sol.rolling_zscore(X, 3)
    eq(np.isnan(z[:2]).all(), True)
    w = X[2:5]
    close(z[4], (10 - w.mean()) / w.std())


def test_p2_zscore_flat(sol):
    close(sol.rolling_zscore([5, 5, 5, 5], 2)[1:], np.zeros(3))


def test_p2_zscore_length(sol):
    eq(len(sol.rolling_zscore(np.arange(10), 4)), 10)


def test_p2_zscore_random(sol):
    x = np.random.default_rng(5).random(30)
    z = sol.rolling_zscore(x, 5)
    close(z[10], (x[10] - x[6:11].mean()) / x[6:11].std())
