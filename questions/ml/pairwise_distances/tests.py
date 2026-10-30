import time

import numpy as np

from check import close, eq

A = np.array([[0.0, 0.0], [3.0, 4.0], [1.0, 1.0]])
B = np.array([[0.0, 0.0], [6.0, 8.0]])
rng = np.random.default_rng(1)
RA, RB = rng.normal(size=(30, 5)), rng.normal(size=(20, 5))


def loop(f, a, b):
    return np.array([[f(x, y) for y in b] for x in a])


def test_p1_small(sol):
    close(sol.euclidean(A, B), np.array([[0.0, 10.0], [5.0, 5.0], [np.sqrt(2), np.sqrt(74)]]))


def test_p1_random(sol):
    close(sol.euclidean(RA, RB), loop(lambda x, y: np.linalg.norm(x - y), RA, RB))


def test_p1_self_zero_diag(sol):
    d = sol.euclidean(RA, RA)
    eq(np.isnan(d).any(), False)
    close(np.diag(d), np.zeros(30), tol=1e-5)


def test_p1_shape(sol):
    eq(sol.euclidean(RA, RB).shape, (30, 20))


def test_p1_fast(sol):
    X = np.random.default_rng(0).normal(size=(2000, 32))
    t0 = time.perf_counter()
    sol.euclidean(X, X)
    eq(time.perf_counter() - t0 < 2, True, msg="2000x2000 should be well under 2s with vectorized code")


def test_p1_lists(sol):
    close(sol.euclidean([[0, 0]], [[3, 4]]), np.array([[5.0]]))


def test_p2_manhattan(sol):
    close(sol.manhattan(RA, RB), loop(lambda x, y: np.abs(x - y).sum(), RA, RB))


def test_p2_manhattan_small(sol):
    close(sol.manhattan(A, B), np.array([[0.0, 14.0], [7.0, 7.0], [2.0, 12.0]]))


def test_p2_cosine(sol):
    close(sol.cosine_similarity(RA, RB), loop(lambda x, y: x @ y / np.linalg.norm(x) / np.linalg.norm(y), RA, RB))


def test_p2_cosine_parallel(sol):
    close(sol.cosine_similarity([[1.0, 2.0]], [[2.0, 4.0], [-1.0, -2.0]]), np.array([[1.0, -1.0]]))


def test_p2_cosine_zero_row(sol):
    out = sol.cosine_similarity(A, B)
    eq(np.isnan(out).any(), False)
    close(out[0], np.zeros(2))


def test_p2_top_k(sol):
    q = np.array([[1.0, 0.0]])
    b = np.array([[0.0, 1.0], [1.0, 0.1], [1.0, 0.0], [-1.0, 0.0]])
    eq(sol.top_k_similar(q, b, 2), np.array([[2, 1]]))


def test_p2_top_k_ties(sol):
    b = np.array([[2.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    eq(sol.top_k_similar(np.array([[1.0, 0.0]]), b, 3), np.array([[0, 1, 2]]))


def test_p2_top_k_shape(sol):
    eq(sol.top_k_similar(RA, RB, 4).shape, (30, 4))


def test_p2_top_k_matches_brute(sol):
    s = loop(lambda x, y: x @ y / np.linalg.norm(x) / np.linalg.norm(y), RA, RB)
    eq(sol.top_k_similar(RA, RB, 1)[:, 0], s.argmax(1))
