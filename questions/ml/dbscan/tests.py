import numpy as np

from check import eq

LINE = np.array([[0.0], [1.0], [2.0], [10.0], [11.0], [12.0], [50.0]])



def test_p1_neighbors(sol):
    eq(sol.neighbors(LINE, 1.0), [[0, 1], [0, 1, 2], [1, 2], [3, 4], [3, 4, 5], [4, 5], [6]])


def test_p1_neighbors_inclusive(sol):
    eq(sol.neighbors(np.array([[0.0, 0.0], [3.0, 4.0]]), 5.0), [[0, 1], [0, 1]])


def test_p1_neighbors_self_only(sol):
    eq(sol.neighbors(LINE, 0.5), [[i] for i in range(7)])


def test_p1_core_mask(sol):
    eq(sol.core_mask(LINE, 1.0, 3).tolist(), [False, True, False, False, True, False, False])


def test_p1_core_counts_self(sol):
    eq(sol.core_mask(LINE, 1.0, 1).tolist(), [True] * 7)


def test_p1_core_dtype(sol):
    eq(sol.core_mask(LINE, 1.0, 2).dtype, np.dtype(bool))


def test_p2_two_clusters_and_noise(sol):
    eq(sol.dbscan(LINE, 1.0, 3).tolist(), [0, 0, 0, 1, 1, 1, -1])


def test_p2_all_noise(sol):
    eq(sol.dbscan(LINE, 0.5, 2).tolist(), [-1] * 7)


def test_p2_one_cluster(sol):
    eq(sol.dbscan(LINE, 100.0, 2).tolist(), [0] * 7)


def test_p2_chain(sol):
    X = np.arange(10, dtype=float).reshape(-1, 1)
    eq(sol.dbscan(X, 1.0, 3).tolist(), [0] * 10)


def test_p2_border_first_come(sol):
    # 1.5 is a border point of both clusters; the first cluster found claims it
    X = np.array([[0.0], [0.2], [0.4], [0.6], [1.5], [2.4], [2.6], [2.8], [3.0]])
    eq(sol.dbscan(X, 1.0, 4).tolist(), [0, 0, 0, 0, 0, 1, 1, 1, 1])


def test_p2_border_not_expanded(sol):
    # 1.5 joins as a border point but must not pull in 2.4
    X = np.array([[0.0], [0.2], [0.4], [0.6], [1.5], [2.4]])
    eq(sol.dbscan(X, 1.0, 4).tolist(), [0, 0, 0, 0, 0, -1])


def test_p2_ids_by_scan_order(sol):
    X = np.array([[100.0], [100.5], [101.0], [0.0], [0.5], [1.0]])
    eq(sol.dbscan(X, 1.0, 3).tolist(), [0, 0, 0, 1, 1, 1])


def test_p2_blobs(sol):
    rng = np.random.default_rng(0)
    X = np.vstack([rng.normal(0, 0.3, (40, 2)), rng.normal(5, 0.3, (40, 2)), [[20.0, 20.0]]])
    lab = sol.dbscan(X, 0.8, 4)
    eq((len(set(lab[:40].tolist())), len(set(lab[40:80].tolist())), lab[80], lab[0] != lab[40]), (1, 1, -1, True))


def test_p2_core_points_share_with_core_neighbors(sol):
    rng = np.random.default_rng(1)
    X = rng.random((60, 2))
    lab, core, nb = sol.dbscan(X, 0.15, 4), sol.core_mask(X, 0.15, 4), sol.neighbors(X, 0.15)
    eq(all(lab[i] == lab[j] for i in range(60) if core[i] for j in nb[i] if core[j]), True)


def test_p2_int_labels(sol):
    eq(np.issubdtype(np.asarray(sol.dbscan(LINE, 1.0, 3)).dtype, np.integer), True)
