import numpy as np

from check import close, eq

XOR = np.array([[0.0, 0], [0, 1], [1, 0], [1, 1]] * 3)
YX = np.array([0, 1, 1, 0] * 3)
rng = np.random.default_rng(1)
XR = rng.random((300, 4))
YR = ((XR[:, 0] > 0.5) & (XR[:, 2] < 0.3)).astype(int)


def test_p1_xor_has_no_greedy_split(sol):
    # every first split of xor has zero gain, so the spec says: leaf
    eq(sol.DecisionTree().fit(XOR, YX).predict(XOR[:4]).tolist(), [0, 0, 0, 0])


def test_p1_memorizes(sol):
    eq((sol.DecisionTree().fit(XR, YR).predict(XR) == YR).mean(), 1.0)


def test_p1_generalizes(sol):
    t = sol.DecisionTree(max_depth=3).fit(XR[:200], YR[:200])
    eq((t.predict(XR[200:]) == YR[200:]).mean() > 0.9, True)


def test_p1_max_depth_zero(sol):
    eq(sol.DecisionTree(max_depth=0).fit(XR, YR).predict(XR[:3]).tolist(), [0, 0, 0])


def test_p1_single_class(sol):
    eq(sol.DecisionTree().fit(XR, np.ones(300)).predict(XR[:2]).tolist(), [1.0, 1.0])


def test_p1_min_samples_split(sol):
    t = sol.DecisionTree(min_samples_split=1000).fit(XR, YR)
    eq(len(set(t.predict(XR).tolist())), 1)


def test_p1_string_labels(sol):
    y = np.where(YR == 1, "surge", "calm")
    eq(sol.DecisionTree(max_depth=2).fit(XR, y).predict(np.array([[0.9, 0, 0.1, 0]])).tolist(), ["surge"])


def test_p1_threshold_midpoint(sol):
    t = sol.DecisionTree().fit(np.array([[1.0], [3.0]]), np.array([0, 1]))
    eq(t.predict(np.array([[1.99], [2.0], [2.01]])).tolist(), [0, 0, 1])


def test_p1_majority_tie(sol):
    t = sol.DecisionTree().fit(np.ones((4, 1)), np.array([2, 1, 2, 1]))
    eq(t.predict(np.ones((1, 1))).tolist(), [1])


def test_p2_depth_and_leaves(sol):
    t = sol.DecisionTree().fit(np.arange(1.0, 7.0).reshape(6, 1), np.array([0, 0, 1, 1, 2, 2]))
    eq((t.depth(), t.n_leaves(), t.predict(np.array([[1.0], [3.5], [6.0]])).tolist()), (2, 3, [0, 1, 2]))


def test_p2_depth_capped(sol):
    eq(sol.DecisionTree(max_depth=2).fit(XR, YR).depth() <= 2, True)


def test_p2_lone_leaf(sol):
    t = sol.DecisionTree(max_depth=0).fit(XR, YR)
    eq((t.depth(), t.n_leaves()), (0, 1))


def test_p2_proba(sol):
    t = sol.DecisionTree(max_depth=0).fit(XOR, YX)
    close(t.predict_proba(XOR[:2]), np.array([[0.5, 0.5], [0.5, 0.5]]))


def test_p2_proba_rows_sum(sol):
    close(sol.DecisionTree(max_depth=2).fit(XR, YR).predict_proba(XR).sum(1), np.ones(300))


def test_p2_importances(sol):
    imp = sol.DecisionTree().fit(XR, YR).feature_importances_
    close(imp.sum(), 1.0)
    eq(set(np.argsort(imp)[-2:].tolist()), {0, 2})


def test_p2_importances_single_leaf(sol):
    close(sol.DecisionTree(max_depth=0).fit(XR, YR).feature_importances_, np.zeros(4))


def test_p2_importances_one_split(sol):
    X = np.array([[0.0, 5], [1, 5], [0, 6], [1, 6]])
    close(sol.DecisionTree().fit(X, np.array([0, 1, 0, 1])).feature_importances_, np.array([1.0, 0.0]))
