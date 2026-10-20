import numpy as np

from check import close, eq

Z = np.array([[1.0, 2.0, 3.0], [0.0, 0.0, 0.0], [-1.0, 5.0, 2.0]])
T = np.array([2, 0, 1])


def naive(z):
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def test_p1_matches_naive(sol):
    close(sol.softmax(Z), naive(Z))


def test_p1_rows_sum_to_one(sol):
    close(sol.softmax(Z).sum(axis=1), np.ones(3))


def test_p1_uniform(sol):
    close(sol.softmax(np.zeros((1, 4))), np.full((1, 4), 0.25))


def test_p1_large_logits(sol):
    out = sol.softmax(np.array([[1000.0, 1000.0], [1000.0, 0.0]]))
    eq(np.isfinite(out).all(), True)
    close(out, np.array([[0.5, 0.5], [1.0, 0.0]]))


def test_p1_shift_invariant(sol):
    close(sol.softmax(Z + 50), sol.softmax(Z))


def test_p1_log_softmax(sol):
    close(sol.log_softmax(Z), np.log(naive(Z)))


def test_p1_log_softmax_no_neg_inf(sol):
    out = sol.log_softmax(np.array([[0.0, 2000.0]]))
    close(out, np.array([[-2000.0, 0.0]]))


def test_p1_shape_kept(sol):
    eq(sol.softmax(np.zeros((5, 7))).shape, (5, 7))


def test_p2_ce_value(sol):
    close(sol.cross_entropy(Z, T), float(-np.log(naive(Z))[np.arange(3), T].mean()))


def test_p2_ce_perfect(sol):
    close(sol.cross_entropy(np.array([[100.0, 0.0]]), np.array([0])), 0.0)


def test_p2_ce_uniform(sol):
    close(sol.cross_entropy(np.zeros((4, 10)), np.array([1, 2, 3, 4])), float(np.log(10)))


def test_p2_ce_huge_wrong(sol):
    close(sol.cross_entropy(np.array([[0.0, 1000.0]]), np.array([0])), 1000.0)


def test_p2_ce_float(sol):
    eq(isinstance(sol.cross_entropy(Z, T), float), True)


def test_p2_grad_numeric(sol):
    g, eps = sol.cross_entropy_grad(Z, T), 1e-5
    num = np.zeros_like(Z)
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            zp, zm = Z.copy(), Z.copy()
            zp[i, j] += eps
            zm[i, j] -= eps
            num[i, j] = (sol.cross_entropy(zp, T) - sol.cross_entropy(zm, T)) / (2 * eps)
    close(g, num)


def test_p2_grad_rows_sum_zero(sol):
    close(sol.cross_entropy_grad(Z, T).sum(axis=1), np.zeros(3))


def test_p2_grad_does_not_mutate(sol):
    z = Z.copy()
    sol.cross_entropy_grad(z, T)
    eq(z, Z)
