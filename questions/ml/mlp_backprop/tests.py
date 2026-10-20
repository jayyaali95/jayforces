import numpy as np

from check import close, eq

rng = np.random.default_rng(0)
X = rng.normal(size=(12, 3))
Y = rng.integers(0, 4, 12)


def test_p1_init_shapes(sol):
    p = sol.init_params(3, 5, 4)
    eq({k: v.shape for k, v in p.items()}, {"W1": (3, 5), "b1": (5,), "W2": (5, 4), "b2": (4,)})


def test_p1_init_values(sol):
    r = np.random.default_rng(7)
    W1 = r.normal(size=(3, 5)) * np.sqrt(2 / 3)
    W2 = r.normal(size=(5, 4)) * np.sqrt(2 / 5)
    p = sol.init_params(3, 5, 4, seed=7)
    close((p["W1"], p["W2"], p["b1"]), (W1, W2, np.zeros(5)))


def test_p1_forward_shape(sol):
    eq(sol.forward(sol.init_params(3, 5, 4), X)[0].shape, (12, 4))


def test_p1_forward_values(sol):
    p = sol.init_params(3, 5, 4, seed=1)
    close(sol.forward(p, X)[0], np.maximum(X @ p["W1"] + p["b1"], 0) @ p["W2"] + p["b2"])


def test_p1_loss_value(sol):
    p = sol.init_params(3, 5, 4, seed=1)
    z = np.maximum(X @ p["W1"], 0) @ p["W2"]
    e = np.exp(z)
    close(sol.loss(p, X, Y), float(-np.log((e / e.sum(1, keepdims=True))[np.arange(12), Y]).mean()))


def test_p1_loss_stable(sol):
    p = sol.init_params(3, 5, 4)
    p["b2"] = np.array([1000.0, 0, 0, 0])
    eq(np.isfinite(sol.loss(p, X, Y)), True)


def test_p1_loss_uniform(sol):
    p = sol.init_params(3, 5, 4)
    p["W2"][:] = 0
    close(sol.loss(p, X, Y), float(np.log(4)))


def numeric(sol, p, key, eps=1e-6):
    g = np.zeros_like(p[key])
    for i in np.ndindex(g.shape):
        p[key][i] += eps
        hi = sol.loss(p, X, Y)
        p[key][i] -= 2 * eps
        lo = sol.loss(p, X, Y)
        p[key][i] += eps
        g[i] = (hi - lo) / (2 * eps)
    return g


def test_p2_grad_W1(sol):
    p = sol.init_params(3, 5, 4, seed=2)
    close(sol.backward(p, X, Y)["W1"], numeric(sol, p, "W1"), tol=1e-5)


def test_p2_grad_b1(sol):
    p = sol.init_params(3, 5, 4, seed=2)
    p["b1"] = rng.normal(size=5) * 0.1
    close(sol.backward(p, X, Y)["b1"], numeric(sol, p, "b1"), tol=1e-5)


def test_p2_grad_W2(sol):
    p = sol.init_params(3, 5, 4, seed=2)
    close(sol.backward(p, X, Y)["W2"], numeric(sol, p, "W2"), tol=1e-5)


def test_p2_grad_b2(sol):
    p = sol.init_params(3, 5, 4, seed=2)
    close(sol.backward(p, X, Y)["b2"], numeric(sol, p, "b2"), tol=1e-5)


def test_p2_grad_shapes(sol):
    p = sol.init_params(3, 5, 4)
    eq({k: v.shape for k, v in sol.backward(p, X, Y).items()}, {k: v.shape for k, v in p.items()})


def test_p2_train_losses(sol):
    _, losses = sol.train(X, Y, epochs=10)
    eq(len(losses), 10)


def test_p2_train_fits(sol):
    r = np.random.default_rng(3)
    Xs = r.normal(size=(200, 2))
    ys = (Xs[:, 0] * Xs[:, 1] > 0).astype(int)
    params, losses = sol.train(Xs, ys, h=32, lr=0.5, epochs=500)
    acc = (sol.forward(params, Xs)[0].argmax(1) == ys).mean()
    eq((losses[-1] < losses[0], acc > 0.9), (True, True))


def test_p2_train_first_loss(sol):
    p = sol.init_params(3, 16, 4, seed=0)
    _, losses = sol.train(X, Y, epochs=1)
    close(losses[0], sol.loss(p, X, Y))
