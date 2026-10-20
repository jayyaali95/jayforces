import numpy as np

from check import close, eq

rng = np.random.default_rng(0)
CENTERS = np.array([[0.0, 0.0], [10.0, 10.0], [0.0, 10.0]])
X = np.vstack([c + rng.normal(scale=0.5, size=(50, 2)) for c in CENTERS])


def ref(X, C, max_iter=100, tol=1e-6):
    C = C.astype(float).copy()
    it = 0
    for _ in range(max_iter):
        lab = np.array([np.argmin([np.sum((x - c) ** 2) for c in C]) for x in X])
        new = np.array([X[lab == j].mean(0) if (lab == j).any() else C[j] for j in range(len(C))])
        it += 1
        moved = np.linalg.norm(new - C, axis=1).max()
        C = new
        if moved <= tol:
            break
    return C, np.array([np.argmin([np.sum((x - c) ** 2) for c in C]) for x in X]), it


INIT = np.array([[1.0, 1.0], [9.0, 9.0], [1.0, 9.0]])


def test_p1_finds_blobs(sol):
    C, _, _ = sol.kmeans(X, INIT)
    close(C, np.array([X[:50].mean(0), X[50:100].mean(0), X[100:].mean(0)]))


def test_p1_labels(sol):
    _, lab, _ = sol.kmeans(X, INIT)
    eq(lab, np.repeat([0, 1, 2], 50))


def test_p1_matches_reference(sol):
    init = X[[0, 1, 2]]
    C, lab, it = sol.kmeans(X, init)
    rc, rl, ri = ref(X, init)
    close(C, rc)
    eq((lab, it), (rl, ri))


def test_p1_max_iter(sol):
    _, _, it = sol.kmeans(X, X[[0, 1, 2]], max_iter=1)
    eq(it, 1)


def test_p1_converged_iterations(sol):
    _, _, it = sol.kmeans(X, INIT)
    eq(it, ref(X, INIT)[2])


def test_p1_empty_cluster_stays(sol):
    C, lab, _ = sol.kmeans(X, np.array([[1.0, 1.0], [100.0, 100.0]]))
    close(C[1], np.array([100.0, 100.0]))
    eq(set(lab.tolist()), {0})


def test_p1_init_not_mutated(sol):
    init = INIT.copy()
    sol.kmeans(X, init)
    eq(init, INIT)


def test_p1_tie_lower_index(sol):
    _, lab, _ = sol.kmeans(np.array([[0.0, 0.0]]), np.array([[1.0, 0.0], [-1.0, 0.0]]), max_iter=1)
    eq(lab.tolist(), [0])


def test_p1_one_cluster(sol):
    C, _, _ = sol.kmeans(X, X[:1])
    close(C, X.mean(0, keepdims=True))


def test_p2_inertia(sol):
    C, lab, _ = sol.kmeans(X, INIT)
    close(sol.inertia(X, C, lab), float(sum(((X[lab == j] - C[j]) ** 2).sum() for j in range(3))))


def test_p2_inertia_zero(sol):
    close(sol.inertia(X[:3], X[:3], np.array([0, 1, 2])), 0.0)


def ref_pp(X, k, seed):
    r = np.random.default_rng(seed)
    C = [X[r.integers(len(X))]]
    for _ in range(1, k):
        D = np.array([min(np.sum((x - c) ** 2) for c in C) for x in X])
        C.append(X[r.choice(len(X), p=D / D.sum())])
    return np.array(C)


def test_p2_pp_exact(sol):
    close(sol.kmeans_pp_init(X, 3, seed=5), ref_pp(X, 3, 5))


def test_p2_pp_shape(sol):
    eq(sol.kmeans_pp_init(X, 4).shape, (4, 2))


def test_p2_pp_points_from_data(sol):
    C = sol.kmeans_pp_init(X, 3, seed=1)
    eq(all(any(np.allclose(c, x) for x in X) for c in C), True)


def test_p2_pp_spreads_out(sol):
    C = sol.kmeans_pp_init(X, 3, seed=2)
    eq(len({int(np.argmin(((CENTERS - c) ** 2).sum(1))) for c in C}), 3)


def test_p2_pp_then_kmeans(sol):
    C, lab, _ = sol.kmeans(X, sol.kmeans_pp_init(X, 3, seed=3))
    eq(sol.inertia(X, C, lab) < 200, True)
