from check import table


def r(i, d, amt, ts=0):
    return {"id": i, "driver": d, "amount": amt, "ts": ts}


A = [r("p1", "d1", 100), r("p2", "d1", 250), r("p3", "d2", 75), r("p4", "d3", 10)]
B = [r("p1", "d1", 100), r("p2", "d1", 200), r("p3", "d9", 75), r("p5", "d3", 10)]

table(globals(), 1, lambda s, a, b: s.reconcile(a, b), [
    ("mixed", (A, B), {"matched": ["p1"], "mismatched": [("p2", 250, 200), ("p3", 75, 75)],
                      "missing_in_bank": ["p4"], "missing_in_internal": ["p5"]}),
    ("identical", (A, A), {"matched": ["p1", "p2", "p3", "p4"], "mismatched": [], "missing_in_bank": [], "missing_in_internal": []}),
    ("empty bank", (A, []), {"matched": [], "mismatched": [], "missing_in_bank": ["p1", "p2", "p3", "p4"], "missing_in_internal": []}),
    ("both empty", ([], []), {"matched": [], "mismatched": [], "missing_in_bank": [], "missing_in_internal": []}),
    ("duplicate keeps last", ([r("x", "d", 1), r("x", "d", 2)], [r("x", "d", 2)]),
     {"matched": ["x"], "mismatched": [], "missing_in_bank": [], "missing_in_internal": []}),
    ("sorted ids", ([r("b", "d", 1), r("a", "d", 1)], []),
     {"matched": [], "mismatched": [], "missing_in_bank": ["a", "b"], "missing_in_internal": []}),
])
table(globals(), 2, lambda s, *a, **k: s.fuzzy_match(*a), [
    ("renamed ids", ([r("i1", "d1", 100, 0)], [r("BANK-9", "d1", 100, 30)]),
     {"pairs": [("i1", "BANK-9")], "unmatched_internal": [], "unmatched_bank": []}),
    ("outside window", ([r("i1", "d1", 100, 0)], [r("b1", "d1", 100, 61)]),
     {"pairs": [], "unmatched_internal": ["i1"], "unmatched_bank": ["b1"]}),
    ("window edge", ([r("i1", "d1", 100, 0)], [r("b1", "d1", 100, 60)]),
     {"pairs": [("i1", "b1")], "unmatched_internal": [], "unmatched_bank": []}),
    ("driver must match", ([r("i1", "d1", 100, 0)], [r("b1", "d2", 100, 0)]),
     {"pairs": [], "unmatched_internal": ["i1"], "unmatched_bank": ["b1"]}),
    ("closest time wins", ([r("i1", "d1", 5, 100)], [r("b1", "d1", 5, 50), r("b2", "d1", 5, 110)]),
     {"pairs": [("i1", "b2")], "unmatched_internal": [], "unmatched_bank": ["b1"]}),
    ("each used once", ([r("i1", "d1", 5, 0), r("i2", "d1", 5, 1)], [r("b1", "d1", 5, 0)]),
     {"pairs": [("i1", "b1")], "unmatched_internal": ["i2"], "unmatched_bank": []}),
    ("tolerance", ([r("i1", "d1", 100, 0)], [r("b1", "d1", 103, 0)], 60, 5),
     {"pairs": [("i1", "b1")], "unmatched_internal": [], "unmatched_bank": []}),
    ("tolerance tie break on amount", ([r("i1", "d1", 100, 0)], [r("b1", "d1", 104, 5), r("b2", "d1", 101, 5)], 60, 5),
     {"pairs": [("i1", "b2")], "unmatched_internal": [], "unmatched_bank": ["b1"]}),
    ("processing order", ([r("late", "d", 1, 10), r("early", "d", 1, 0)], [r("b", "d", 1, 9)]),
     {"pairs": [("early", "b")], "unmatched_internal": ["late"], "unmatched_bank": []}),
])
