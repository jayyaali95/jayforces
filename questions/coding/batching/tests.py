import itertools
import types

from check import eq, raises, table

table(globals(), 1, lambda s, it, n: list(s.batched(it, n)), [
    ("even split", (range(6), 2), [[0, 1], [2, 3], [4, 5]]),
    ("short tail", (range(5), 2), [[0, 1], [2, 3], [4]]),
    ("size larger than input", ([1, 2], 10), [[1, 2]]),
    ("size one", ("ab", 1), [["a"], ["b"]]),
    ("empty", ([], 3), []),
    ("zero size", ([1], 0), ValueError),
])


def test_p1_is_generator(sol):
    eq(isinstance(sol.batched([1], 1), types.GeneratorType), True)


def test_p1_infinite_input(sol):
    eq(next(iter(sol.batched(itertools.count(), 3))), [0, 1, 2])


def test_p1_lazy_consumption(sol):
    it = iter(range(10))
    g = sol.batched(it, 3)
    next(g)
    eq(next(it), 3)


table(globals(), 2, lambda s, it, w, *f: list(s.batched_by_weight(it, w, *f)), [
    ("strings by length", (["ab", "cd", "efg", "h"], 4), [["ab", "cd"], ["efg", "h"]]),
    ("exact fit", (["aa", "bb"], 4), [["aa", "bb"]]),
    ("oversized alone", (["a", "toolong", "b"], 3), [["a"], ["toolong"], ["b"]]),
    ("oversized first", (["toolong", "a"], 3), [["toolong"], ["a"]]),
    ("custom weight", ([5, 1, 1, 3, 4], 5, lambda x: x), [[5], [1, 1, 3], [4]]),
    ("empty weighted", ([], 3), []),
    ("zero weights", (["", "", ""], 0), [["", "", ""]]),
])


def test_p2_infinite_weighted(sol):
    g = sol.batched_by_weight(itertools.repeat("ab"), 5)
    eq(next(g), ["ab", "ab"])
