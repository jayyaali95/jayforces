import numpy as np

from check import close, eq

R = np.random.default_rng(0)
X = R.normal(3, 2, size=(8, 4))


def test_p1_init(sol):
    b = sol.BatchNorm1d(4)
    close((b.gamma, b.beta, b.running_mean, b.running_var), (np.ones(4), np.zeros(4), np.zeros(4), np.ones(4)))


def test_p1_normalized(sol):
    y = sol.BatchNorm1d(4).forward(X)
    close((y.mean(0), y.std(0)), (np.zeros(4), np.ones(4)), tol=1e-3)


def test_p1_exact(sol):
    close(sol.BatchNorm1d(4).forward(X), (X - X.mean(0)) / np.sqrt(X.var(0) + 1e-5))


def test_p1_gamma_beta(sol):
    b = sol.BatchNorm1d(4)
    b.gamma, b.beta = np.full(4, 2.0), np.full(4, -1.0)
    close(b.forward(X), 2 * (X - X.mean(0)) / np.sqrt(X.var(0) + 1e-5) - 1)


def test_p1_running_mean(sol):
    b = sol.BatchNorm1d(4)
    b.forward(X)
    close(b.running_mean, 0.1 * X.mean(0))


def test_p1_running_var_unbiased(sol):
    b = sol.BatchNorm1d(4)
    b.forward(X)
    close(b.running_var, 0.9 + 0.1 * X.var(0, ddof=1))


def test_p1_eval_uses_running(sol):
    b = sol.BatchNorm1d(4)
    b.running_mean, b.running_var = np.full(4, 3.0), np.full(4, 4.0)
    close(b.forward(X, training=False), (X - 3) / np.sqrt(4 + 1e-5))


def test_p1_eval_no_update(sol):
    b = sol.BatchNorm1d(4)
    b.forward(X, training=False)
    close((b.running_mean, b.running_var), (np.zeros(4), np.ones(4)))


def test_p1_momentum(sol):
    b = sol.BatchNorm1d(4, momentum=0.5)
    b.forward(X)
    b.forward(X)
    close(b.running_mean, 0.75 * X.mean(0))


def loss_and_grads(sol, x, gamma, beta, dout):
    b = sol.BatchNorm1d(x.shape[1])
    b.gamma, b.beta = gamma.copy(), beta.copy()
    y = b.forward(x)
    return (y * dout).sum(), b.backward(dout)


def numeric(f, a, eps=1e-6):
    g = np.zeros_like(a)
    for i in np.ndindex(a.shape):
        a[i] += eps
        hi = f()
        a[i] -= 2 * eps
        lo = f()
        a[i] += eps
        g[i] = (hi - lo) / (2 * eps)
    return g


G, BETA, DOUT = R.normal(size=4), R.normal(size=4), R.normal(size=(8, 4))


def test_p2_dx(sol):
    x = X.copy()
    _, (dx, _, _) = loss_and_grads(sol, x, G, BETA, DOUT)
    close(dx, numeric(lambda: loss_and_grads(sol, x, G, BETA, DOUT)[0], x), tol=1e-4)


def test_p2_dgamma(sol):
    g = G.copy()
    _, (_, dg, _) = loss_and_grads(sol, X, g, BETA, DOUT)
    close(dg, numeric(lambda: loss_and_grads(sol, X, g, BETA, DOUT)[0], g), tol=1e-4)


def test_p2_dbeta(sol):
    _, (_, _, db) = loss_and_grads(sol, X, G, BETA, DOUT)
    close(db, DOUT.sum(0))


def test_p2_dx_sums_to_zero(sol):
    _, (dx, _, _) = loss_and_grads(sol, X, G, BETA, DOUT)
    close(dx.sum(0), np.zeros(4), tol=1e-8)


def test_p2_shapes(sol):
    _, (dx, dg, db) = loss_and_grads(sol, X, G, BETA, DOUT)
    eq((dx.shape, dg.shape, db.shape), ((8, 4), (4,), (4,)))


def test_p2_large_batch(sol):
    x = R.normal(size=(64, 3))
    d = R.normal(size=(64, 3))
    _, (dx, _, _) = loss_and_grads(sol, x, np.ones(3), np.zeros(3), d)
    close(dx, numeric(lambda: loss_and_grads(sol, x, np.ones(3), np.zeros(3), d)[0], x), tol=1e-4)
