import numpy as np

from check import close, eq

rng = np.random.default_rng(0)
P0 = {"w": rng.normal(size=(3, 2)), "b": rng.normal(size=2)}
GRADS = [{"w": rng.normal(size=(3, 2)), "b": rng.normal(size=2)} for _ in range(5)]


def run(opt, n=5):
    p = {k: v.copy() for k, v in P0.items()}
    for g in GRADS[:n]:
        opt.step(p, g)
    return p


def ref_sgd(lr, mom, wd, n=5):
    p = {k: v.copy() for k, v in P0.items()}
    buf = {}
    for g in GRADS[:n]:
        for k in p:
            d = g[k] + wd * p[k]
            if mom:
                buf[k] = d if k not in buf else mom * buf[k] + d
                d = buf[k]
            p[k] = p[k] - lr * d
    return p


def ref_adam(lr, b1, b2, eps, wd, n=5):
    p = {k: v.copy() for k, v in P0.items()}
    m = {k: np.zeros_like(v) for k, v in p.items()}
    v_ = {k: np.zeros_like(v) for k, v in p.items()}
    for t, g in enumerate(GRADS[:n], 1):
        for k in p:
            d = g[k] + wd * p[k]
            m[k] = b1 * m[k] + (1 - b1) * d
            v_[k] = b2 * v_[k] + (1 - b2) * d * d
            p[k] = p[k] - lr * (m[k] / (1 - b1 ** t)) / (np.sqrt(v_[k] / (1 - b2 ** t)) + eps)
    return p


def test_p1_plain_sgd(sol):
    close(run(sol.SGD(0.1)), ref_sgd(0.1, 0, 0))


def test_p1_one_step(sol):
    close(run(sol.SGD(0.5), 1), {k: P0[k] - 0.5 * GRADS[0][k] for k in P0})


def test_p1_momentum(sol):
    close(run(sol.SGD(0.1, momentum=0.9)), ref_sgd(0.1, 0.9, 0))


def test_p1_momentum_first_step_is_plain(sol):
    close(run(sol.SGD(0.1, momentum=0.9), 1), ref_sgd(0.1, 0, 0, 1))


def test_p1_weight_decay(sol):
    close(run(sol.SGD(0.1, momentum=0.5, weight_decay=0.01)), ref_sgd(0.1, 0.5, 0.01))


def test_p1_in_place(sol):
    p = {k: v.copy() for k, v in P0.items()}
    w = p["w"]
    sol.SGD(0.1).step(p, GRADS[0])
    eq(p["w"] is w, True)


def test_p1_grads_untouched(sol):
    g = {k: v.copy() for k, v in GRADS[0].items()}
    sol.SGD(0.1, momentum=0.9).step({k: v.copy() for k, v in P0.items()}, g)
    close(g, GRADS[0])


def test_p2_adam_one_step(sol):
    close(run(sol.Adam(0.01), 1), ref_adam(0.01, 0.9, 0.999, 1e-8, 0, 1))


def test_p2_adam_first_step_size(sol):
    p = run(sol.Adam(0.01), 1)
    close(np.abs(p["w"] - P0["w"]), np.full((3, 2), 0.01), tol=1e-6)


def test_p2_adam_five_steps(sol):
    close(run(sol.Adam(0.01)), ref_adam(0.01, 0.9, 0.999, 1e-8, 0))


def test_p2_adam_betas(sol):
    close(run(sol.Adam(0.05, betas=(0.5, 0.9))), ref_adam(0.05, 0.5, 0.9, 1e-8, 0))


def test_p2_adam_weight_decay(sol):
    close(run(sol.Adam(0.01, weight_decay=0.1)), ref_adam(0.01, 0.9, 0.999, 1e-8, 0.1))


def test_p2_adam_in_place(sol):
    p = {k: v.copy() for k, v in P0.items()}
    b = p["b"]
    sol.Adam().step(p, GRADS[0])
    eq(p["b"] is b, True)


def test_p2_minimize_quadratic(sol):
    target = np.array([3.0, -2.0])
    x = sol.minimize(lambda x: 2 * (x - target), np.zeros(2), sol.Adam(0.1), 500)
    close(x, target, tol=1e-3)


def test_p2_minimize_sgd(sol):
    x = sol.minimize(lambda x: 2 * x, np.array([5.0]), sol.SGD(0.1), 100)
    close(x, np.array([5.0 * 0.8 ** 100]))


def test_p2_minimize_copies(sol):
    x0 = np.array([1.0])
    sol.minimize(lambda x: x, x0, sol.SGD(0.1), 3)
    eq(x0.tolist(), [1.0])


def test_p2_minimize_rosenbrock(sol):
    def g(p):
        x, y = p
        return np.array([-2 * (1 - x) - 400 * x * (y - x * x), 200 * (y - x * x)])
    close(sol.minimize(g, np.array([-1.0, 1.0]), sol.Adam(0.02), 5000), np.array([1.0, 1.0]), tol=0.05)
