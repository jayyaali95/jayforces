import numpy as np

from check import close, eq

rng = np.random.default_rng(0)
X = rng.normal(size=(100, 3))
TRUE_W = np.array([2.0, -1.0, 0.5])
Y = X @ TRUE_W + 4.0
YN = Y + rng.normal(scale=0.1, size=100)


def test_p1_recovers_exact(sol):
    m = sol.LinearRegression().fit(X, Y)
    close((m.coef_, m.intercept_), (TRUE_W, 4.0))


def test_p1_coef_shape(sol):
    eq(sol.LinearRegression().fit(X, Y).coef_.shape, (3,))


def test_p1_no_intercept(sol):
    m = sol.LinearRegression(fit_intercept=False).fit(X, X @ TRUE_W)
    close((m.coef_, m.intercept_), (TRUE_W, 0.0))


def test_p1_predict(sol):
    m = sol.LinearRegression().fit(X, Y)
    close(m.predict(np.array([[1.0, 1.0, 1.0]])), np.array([5.5]))


def test_p1_score_perfect(sol):
    close(sol.LinearRegression().fit(X, Y).score(X, Y), 1.0)


def test_p1_score_noisy(sol):
    s = sol.LinearRegression().fit(X, YN).score(X, YN)
    eq(0.99 < s < 1.0, True)


def test_p1_score_matches_formula(sol):
    m = sol.LinearRegression().fit(X[:50], YN[:50])
    p = m.predict(X[50:])
    close(m.score(X[50:], YN[50:]), 1 - ((YN[50:] - p) ** 2).sum() / ((YN[50:] - YN[50:].mean()) ** 2).sum())


def test_p1_rank_deficient(sol):
    Xd = np.hstack([X[:, :1], X[:, :1]])
    m = sol.LinearRegression().fit(Xd, 3 * X[:, 0])
    close(m.predict(Xd), 3 * X[:, 0])


def test_p1_constant_target(sol):
    close(sol.LinearRegression().fit(X, np.full(100, 7.0)).score(X, np.full(100, 7.0)), 1.0)


def test_p2_ridge_zero_alpha_is_ols(sol):
    w, b = sol.ridge_fit(X, YN, 0.0)
    m = sol.LinearRegression().fit(X, YN)
    close((w, b), (m.coef_, m.intercept_))


def test_p2_ridge_shrinks(sol):
    w0, _ = sol.ridge_fit(X, YN, 0.0)
    w1, _ = sol.ridge_fit(X, YN, 100.0)
    eq(np.linalg.norm(w1) < np.linalg.norm(w0), True)


def test_p2_ridge_values(sol):
    Xc, yc = X - X.mean(0), YN - YN.mean()
    w = np.linalg.solve(Xc.T @ Xc + 5 * np.eye(3), Xc.T @ yc)
    close(sol.ridge_fit(X, YN, 5.0), (w, float(YN.mean() - X.mean(0) @ w)))


def test_p2_ridge_intercept_not_penalized(sol):
    _, b = sol.ridge_fit(X, X @ np.zeros(3) + 50.0, 1e6)
    close(b, 50.0, tol=1e-3)


def test_p2_gd_converges(sol):
    w, b = sol.gd_fit(X, Y, lr=0.1, epochs=2000)
    close((w, b), (TRUE_W, 4.0), tol=1e-3)


def test_p2_gd_exact_steps(sol):
    w, b = np.zeros(3), 0.0
    for _ in range(3):
        err = X @ w + b - Y
        w = w - 0.05 * 2 * X.T @ err / 100
        b = b - 0.05 * 2 * err.mean()
    close(sol.gd_fit(X, Y, lr=0.05, epochs=3), (w, b))


def test_p2_gd_zero_epochs(sol):
    close(sol.gd_fit(X, Y, epochs=0), (np.zeros(3), 0.0))
