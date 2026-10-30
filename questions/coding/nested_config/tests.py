import copy

from check import eq, raises, table

CFG = {"db": {"host": "x", "port": 5432, "pool": {"min": 1, "max": 9}}, "debug": False, "tags": ["a", "b"]}
FLAT = {"db.host": "x", "db.port": 5432, "db.pool.min": 1, "db.pool.max": 9, "debug": False, "tags": ["a", "b"]}

table(globals(), 1, lambda s, c, *a: s.flatten(c, *a), [
    ("nested", CFG, FLAT), ("already flat", {"a": 1}, {"a": 1}), ("empty", {}, {}),
    ("empty child kept", {"a": {}, "b": {"c": {}}}, {"a": {}, "b.c": {}}),
    ("custom sep", ({"a": {"b": 1}}, "/"), {"a/b": 1}),
    ("non string key", {"a": {1: 2}}, TypeError),
    ("key containing sep", {"a.b": 1}, ValueError),
    ("none leaf", {"a": {"b": None}}, {"a.b": None}),
])
table(globals(), 2, lambda s, f, *a: s.unflatten(f, *a), [
    ("roundtrip", FLAT, CFG), ("simple", {"a.b": 1, "a.c": 2}, {"a": {"b": 1, "c": 2}}),
    ("conflict", {"a": 1, "a.b": 2}, ValueError), ("conflict reversed", {"a.b": 2, "a": 1}, ValueError),
    ("custom sep unflatten", ({"a/b": 1}, "/"), {"a": {"b": 1}}),
    ("empty dict leaf", {"a": {}}, {"a": {}}),
])
table(globals(), 2, lambda s, b, o: s.deep_merge(b, o), [
    ("override leaf", ({"a": 1}, {"a": 2}), {"a": 2}),
    ("merge nested", ({"db": {"host": "x", "port": 1}}, {"db": {"port": 2}}), {"db": {"host": "x", "port": 2}}),
    ("dict replaces leaf", ({"a": 1}, {"a": {"b": 2}}), {"a": {"b": 2}}),
    ("leaf replaces dict", ({"a": {"b": 2}}, {"a": 3}), {"a": 3}),
    ("lists replaced", ({"a": [1, 2]}, {"a": [3]}), {"a": [3]}),
])


def test_p2_merge_no_mutation_or_sharing(sol):
    base, over = copy.deepcopy(CFG), {"db": {"pool": {"max": 20}}}
    out = sol.deep_merge(base, over)
    out["db"]["pool"]["min"] = 99
    out["tags"].append("z")
    eq((base, over), (CFG, {"db": {"pool": {"max": 20}}}))
