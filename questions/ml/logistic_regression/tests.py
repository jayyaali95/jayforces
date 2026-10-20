import warnings

import numpy as np

from check import close, eq

rng = np.random.default_rng(3)
X = rng.normal(size=(200, 2))
Y = (X[:, 0] + 2 * X[:, 1] > 0.3).astype(int)


def test_p1_sigmoid_values(sol):
    close(sol.sigmoid(np.array([0.0, 2.0, -2.0])), 1 / (1 + np.exp(-np.array([0.0, 2.0, -2.0]))))


def test_p1_sigmoid_extremes_no_warning(sol):
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        out = sol.sigmoid(np.array([-1000.0, 1000.0]))
    close(out, np.array([0.0, 1.0]))


def test_p1_sigmoid_shape(sol):
    eq(sol.sigmoid(np.zeros((3, 4))).shape, (3, 4))


def test_p1_log_loss(sol):
    close(sol.log_loss([1, 0], [0.8, 0.1]), -(np.log(0.8) + np.log(0.9)) / 2)


def test_p1_log_loss_clipped(sol):
    eq(np.isfinite(sol.log_loss([1, 0], [0.0, 1.0])), True)


def test_p1_log_loss_perfect(sol):
    close(sol.log_loss([1, 0], [1.0, 0.0]), 0.0, tol=1e-9)


def test_p2_accuracy(sol):
    m = sol.LogisticRegression(lr=0.5, epochs=500).fit(X, Y)
    eq((m.predict(X) == Y).mean() > 0.95, True)


def test_p2_exact_first_steps(sol):
    w, b = np.zeros(2), 0.0
    for _ in range(2):
        p = 1 / (1 + np.exp(-(X @ w + b)))
        w, b = w - 0.3 * (X.T @ (p - Y) / 200), b - 0.3 * np.mean(p - Y)
    m = sol.LogisticRegression(lr=0.3, epochs=2).fit(X, Y)
    close((m.coef_, m.intercept_), (w, b))


def test_p2_losses_recorded(sol):
    m = sol.LogisticRegression(epochs=50).fit(X, Y)
    eq(len(m.losses_), 50)
    close(m.losses_[0], float(np.log(2)))


def test_p2_losses_decrease(sol):
    l = sol.LogisticRegression(lr=0.5, epochs=100).fit(X, Y).losses_
    eq(all(a >= b - 1e-12 for a, b in zip(l, l[1:])), True)


def test_p2_proba_range(sol):
    p = sol.LogisticRegression(epochs=100).fit(X, Y).predict_proba(X)
    eq((p.shape, bool(((p > 0) & (p < 1)).all())), ((200,), True))


def test_p2_predict_ints(sol):
    eq(set(sol.LogisticRegression(epochs=10).fit(X, Y).predict(X).tolist()) <= {0, 1}, True)


def test_p2_threshold(sol):
    m = sol.LogisticRegression(epochs=100).fit(X, Y)
    eq(m.predict(X, threshold=0.0).sum(), 200)


def test_p2_l2_shrinks(sol):
    a = sol.LogisticRegression(lr=0.5, epochs=300).fit(X, Y).coef_
    b = sol.LogisticRegression(lr=0.5, epochs=300, l2=0.5).fit(X, Y).coef_
    eq(np.linalg.norm(b) < np.linalg.norm(a), True)


def test_p2_l2_exact_step(sol):
    p = np.full(200, 0.5)
    w = -0.1 * (X.T @ (p - Y) / 200)
    p2 = 1 / (1 + np.exp(-(X @ w - 0.1 * np.mean(p - Y))))
    w2 = w - 0.1 * (X.T @ (p2 - Y) / 200 + 1.0 * w)
    close(sol.LogisticRegression(lr=0.1, epochs=2, l2=1.0).fit(X, Y).coef_, w2)
