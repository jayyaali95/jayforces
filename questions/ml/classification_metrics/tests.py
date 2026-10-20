import numpy as np

from check import close, eq, table

T = [1, 0, 1, 1, 0, 0, 1, 0]
P = [1, 0, 0, 1, 1, 0, 1, 0]
table(globals(), 1, lambda s, t, p: s.binary_metrics(t, p), [
    ("mixed", (T, P), {"accuracy": 0.75, "precision": 0.75, "recall": 0.75, "f1": 0.75}),
    ("perfect", ([1, 0], [1, 0]), {"accuracy": 1.0, "precision": 1.0, "recall": 1.0, "f1": 1.0}),
    ("never predicts positive", ([1, 0, 1], [0, 0, 0]), {"accuracy": 1 / 3, "precision": 0.0, "recall": 0.0, "f1": 0.0}),
    ("no positives at all", ([0, 0], [0, 0]), {"accuracy": 1.0, "precision": 0.0, "recall": 0.0, "f1": 0.0}),
    ("high recall low precision", ([1, 0, 0, 0], [1, 1, 1, 1]), {"accuracy": 0.25, "precision": 0.25, "recall": 1.0, "f1": 0.4}),
    ("numpy input", (np.array(T), np.array(P)), {"accuracy": 0.75, "precision": 0.75, "recall": 0.75, "f1": 0.75}),
    ("length mismatch", ([1, 0], [1]), ValueError),
    ("empty", ([], []), ValueError),
])


def test_p1_returns_floats(sol):
    eq(all(type(v) is float for v in sol.binary_metrics(T, P).values()), True)


YT = ["cat", "dog", "cat", "bird", "dog", "cat"]
YP = ["cat", "cat", "cat", "bird", "dog", "dog"]
table(globals(), 2, lambda s, *a: s.confusion_matrix(*a), [
    ("multiclass", (YT, YP), np.array([[1, 0, 0], [0, 2, 1], [0, 1, 1]])),
    ("given labels", (YT, YP, ["dog", "cat"]), np.array([[1, 1], [1, 2]])),
    ("binary matrix", (T, P), np.array([[3, 1], [1, 3]])),
    ("label only predicted", ([0, 0], [0, 2]), np.array([[1, 1], [0, 0]])),
])


def test_p2_matrix_is_int(sol):
    eq(np.issubdtype(np.asarray(sol.confusion_matrix(T, P)).dtype, np.integer), True)


def test_p2_macro_f1(sol):
    close(sol.macro_f1(YT, YP), (1.0 + 2 / 3 + 0.5) / 3)


def test_p2_macro_f1_missing_class(sol):
    close(sol.macro_f1([0, 0, 1], [0, 0, 0]), (0.8 + 0.0) / 2)
