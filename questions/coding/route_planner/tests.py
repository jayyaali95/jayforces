import random

from check import eq, table

E = [("a", "b", 4), ("a", "c", 1), ("c", "b", 2), ("b", "d", 1), ("c", "d", 5), ("d", "e", 3), ("x", "y", 1)]

table(globals(), 1, lambda s, *a: s.fastest(*a), [
    ("indirect is faster", (E, "a", "b"), 3), ("to end", (E, "a", "e"), 7), ("same node", (E, "a", "a"), 0),
    ("unreachable", (E, "a", "x"), None), ("directed", (E, "b", "a"), None), ("unknown node", (E, "q", "a"), None),
    ("zero weights", ([("a", "b", 0), ("b", "c", 0)], "a", "c"), 0),
])


def test_p1_matches_bellman_ford(sol):
    rnd = random.Random(3)
    edges = [(rnd.randrange(40), rnd.randrange(40), rnd.randrange(1, 20)) for _ in range(300)]
    dist = {0: 0}
    for _ in range(40):
        for a, b, w in edges:
            if a in dist and dist[a] + w < dist.get(b, 10 ** 9):
                dist[b] = dist[a] + w
    eq([sol.fastest(edges, 0, n) for n in range(40)], [dist.get(n) for n in range(40)])


table(globals(), 2, lambda s, *a: s.route(*a), [
    ("route", (E, "a", "e"), (7, ["a", "c", "b", "d", "e"])),
    ("route same", (E, "a", "a"), (0, ["a"])),
    ("no route", (E, "e", "a"), None),
    ("lexicographic tie", ([("s", "b", 1), ("s", "a", 1), ("a", "t", 1), ("b", "t", 1)], "s", "t"), (2, ["s", "a", "t"])),
    ("parallel edges", ([("a", "b", 9), ("a", "b", 2)], "a", "b"), (2, ["a", "b"])),
])
table(globals(), 3, lambda s, *a: s.route_avoiding(*a), [
    ("avoid c", (E, "a", "e", {"c"}), (8, ["a", "b", "d", "e"])),
    ("avoid all paths", (E, "a", "e", {"d"}), None),
    ("closed destination", (E, "a", "e", {"e"}), None),
    ("nothing closed", (E, "a", "e", set()), (7, ["a", "c", "b", "d", "e"])),
])
table(globals(), 3, lambda s, *a: s.route_via(*a), [
    ("via d", (E, "a", ["d"], "e"), (7, ["a", "c", "b", "d", "e"])),
    ("via b then c", (E + [("b", "c", 1)], "a", ["b", "c"], "d"), (7, ["a", "c", "b", "c", "b", "d"])),
    ("via unreachable", (E, "a", ["x"], "e"), None),
    ("no stops", (E, "a", [], "b"), (3, ["a", "c", "b"])),
])
