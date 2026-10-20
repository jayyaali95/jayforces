from check import eq, table

table(globals(), 1, lambda s, r, d: s.multiplier(r, d), [
    ("calm", (10, 10), 1.0), ("just under first tier", (119, 100), 1.0), ("first tier edge", (12, 10), 1.25),
    ("second tier", (15, 10), 1.5), ("third tier", (20, 10), 2.0), ("just under top", (29, 10), 2.0),
    ("top tier", (30, 10), 2.5), ("way over", (100, 1), 2.5), ("no drivers no riders", (0, 0), 1.0),
    ("no drivers", (5, 0), 2.5), ("negative", (-1, 3), ValueError),
])
table(globals(), 2, lambda s, p, r: s.update_zones(p, r), [
    ("new zone limited jump", ({}, {"z": (30, 10)}), {"z": 1.5}),
    ("reaches target", ({"z": 2.25}, {"z": (30, 10)}), {"z": 2.5}),
    ("drops limited", ({"z": 2.5}, {"z": (1, 10)}), {"z": 2.0}),
    ("decay unreported", ({"z": 2.0}, {}), {"z": 1.75}),
    ("decay stops at one", ({"z": 1.1}, {}), {"z": 1.0}),
    ("mixed", ({"a": 2.0, "b": 1.0}, {"b": (20, 10), "c": (12, 10)}), {"a": 1.75, "b": 1.5, "c": 1.25}),
])


def test_p2_returns_new_dict(sol):
    prev = {"a": 2.0}
    sol.update_zones(prev, {})
    eq(prev, {"a": 2.0})
