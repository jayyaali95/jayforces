from check import table

E = [("c1", "OPEN", 0), ("c1", "REPAIR_START", 4), ("c1", "REPAIR_END", 6),
     ("c2", "OPEN", 1), ("c2", "CLOSE", 3), ("c3", "REPAIR_START", 2), ("c3", "OPEN", 5)]

table(globals(), 1, lambda s, ev: s.final_status(ev), [
    ("single open", [("a", "OPEN", 1)], {"a": "OPEN"}),
    ("open then close", [("a", "OPEN", 1), ("a", "CLOSE", 2)], {"a": "CLOSED"}),
    ("out of order input", [("a", "CLOSE", 2), ("a", "OPEN", 1)], {"a": "CLOSED"}),
    ("repair wins over open", [("a", "OPEN", 1), ("a", "REPAIR_START", 2)], {"a": "IN_REPAIR"}),
    ("repair finished", [("a", "OPEN", 1), ("a", "REPAIR_START", 2), ("a", "REPAIR_END", 3)], {"a": "OPEN"}),
    ("repair on closed car", [("a", "REPAIR_START", 2)], {"a": "IN_REPAIR"}),
    ("noise ignored", [("a", "OPEN", 1), ("a", "HONK", 2), ("b", "HONK", 3)], {"a": "OPEN"}),
    ("same ts keeps input order", [("a", "CLOSE", 5), ("a", "OPEN", 5)], {"a": "OPEN"}),
    ("empty", [], {}),
    ("fleet", E, {"c1": "OPEN", "c2": "CLOSED", "c3": "IN_REPAIR"}),
])

table(globals(), 2, lambda s, ev, car, until: s.drivable_windows(ev, car, until), [
    ("example", (E, "c1", 10), [(0, 4), (6, 10)]),
    ("closed shift", (E, "c2", 10), [(1, 3)]),
    ("never drivable", (E, "c3", 10), []),
    ("unknown car", (E, "zz", 10), []),
    ("until cuts window", (E, "c1", 5), [(0, 4)]),
    ("events at until ignored", ([("a", "OPEN", 0), ("a", "CLOSE", 5)], "a", 5), [(0, 5)]),
    ("touching windows merge", ([("a", "OPEN", 0), ("a", "REPAIR_START", 5), ("a", "REPAIR_END", 5)], "a", 9), [(0, 9)]),
    ("zero length dropped", ([("a", "OPEN", 3), ("a", "CLOSE", 3)], "a", 9), []),
    ("double open", ([("a", "OPEN", 0), ("a", "OPEN", 2), ("a", "CLOSE", 4)], "a", 9), [(0, 4)]),
    ("repair before shift", ([("a", "REPAIR_START", 0), ("a", "OPEN", 1), ("a", "REPAIR_END", 3)], "a", 6), [(3, 6)]),
])

table(globals(), 3, lambda s, ev, t: s.available_at(ev, t), [
    ("start of day", (E, 0), ["c1"]),
    ("both open", (E, 2), ["c1", "c2"]),
    ("inclusive t", (E, 3), ["c1"]),
    ("everyone in repair or closed", (E, 4), []),
    ("late", (E, 100), ["c1"]),
])
