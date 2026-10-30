import numpy as np

from check import close, eq, raises

rng = np.random.default_rng(4)
Z = rng.normal(size=(300, 2)) * np.array([5.0, 1.0])
R = np.array([[0.6, 0.8, 0.0], [-0.8, 0.6, 0.0], [0.0, 0.0, 1.0]])
X = np.hstack([Z, rng.normal(scale=0.1, size=(300, 1))]) @ R + np.array([10.0, -3.0, 2.0])


def ref(X, k):
    Xc = X - X.mean(0)
    vals, vecs = np.linalg.eigh(np.cov(Xc, rowvar=False))
    o = np.argsort(vals)[::-1]
    v = vecs[:, o].T[:k]
    v = v * np.sign(v[np.arange(k), np.abs(v).argmax(1)])[:, None]
    return v, vals[o], Xc @ v.T


def test_p1_mean(sol):
    close(sol.PCA(2).fit(X).mean_, X.mean(0))


def test_p1_components(sol):
    close(sol.PCA(2).fit(X).components_, ref(X, 2)[0])


def test_p1_first_component_direction(sol):
    close(sol.PCA(1).fit(X).components_[0], np.array([0.6, 0.8, 0.0]), tol=0.02)


def test_p1_unit_rows(sol):
    close(np.linalg.norm(sol.PCA(3).fit(X).components_, axis=1), np.ones(3))


def test_p1_sign_convention(sol):
    c = sol.PCA(3).fit(X).components_
    eq(bool((c[np.arange(3), np.abs(c).argmax(1)] > 0).all()), True)


def test_p1_variance(sol):
    close(sol.PCA(2).fit(X).explained_variance_, ref(X, 2)[1][:2])


def test_p1_ratio(sol):
    vals = ref(X, 2)[1]
    close(sol.PCA(2).fit(X).explained_variance_ratio_, vals[:2] / vals.sum())


def test_p1_transform(sol):
    close(sol.PCA(2).fit(X).transform(X), ref(X, 2)[2])


def test_p1_projected_uncorrelated(sol):
    T = sol.PCA(2).fit(X).transform(X)
    close(np.cov(T, rowvar=False)[0, 1], 0.0, tol=1e-6)


def test_p1_bad_k(sol):
    raises(ValueError, sol.PCA(4).fit, X)


def test_p1_bad_k_zero(sol):
    raises(ValueError, sol.PCA(0).fit, X)


def test_p2_full_reconstruction(sol):
    p = sol.PCA(3).fit(X)
    close(p.inverse_transform(p.transform(X)), X)


def test_p2_partial_reconstruction_error_small(sol):
    p = sol.PCA(2).fit(X)
    err = np.abs(p.inverse_transform(p.transform(X)) - X).max()
    eq(err < 0.5, True)


def test_p2_choose_k(sol):
    eq((sol.choose_k(X, 0.9), sol.choose_k(X, 0.99), sol.choose_k(X, 1.0)), (1, 2, 3))


def test_p2_choose_k_identity(sol):
    I = np.random.default_rng(0).normal(size=(5000, 4))
    eq(sol.choose_k(I, 0.5), 2)
