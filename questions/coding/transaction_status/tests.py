from check import table


def ev(txn, status, ts):
    return {"txn": txn, "status": status, "ts": ts}


FLOW = [ev("a", "CREATED", 1), ev("a", "AUTHORIZED", 2), ev("a", "SETTLED", 9),
        ev("b", "CREATED", 3), ev("b", "FAILED", 4), ev("c", "CREATED", 2), ev("c", "AUTHORIZED", 5)]

table(globals(), 1, lambda s, e: s.final_status(e), [
    ("single", [ev("a", "CREATED", 1)], {"a": "CREATED"}),
    ("latest wins", [ev("a", "CREATED", 1), ev("a", "CAPTURED", 4)], {"a": "CAPTURED"}),
    ("out of order", [ev("a", "SETTLED", 9), ev("a", "CREATED", 1)], {"a": "SETTLED"}),
    ("tie uses precedence", [ev("a", "CAPTURED", 5), ev("a", "AUTHORIZED", 5)], {"a": "CAPTURED"}),
    ("tie refund over settled", [ev("a", "REFUNDED", 5), ev("a", "SETTLED", 5)], {"a": "REFUNDED"}),
    ("later low beats earlier high", [ev("a", "REFUNDED", 1), ev("a", "CREATED", 2)], {"a": "CREATED"}),
    ("unknown status ignored", [ev("a", "CREATED", 1), ev("a", "WAT", 7)], {"a": "CREATED"}),
    ("only unknown", [ev("a", "WAT", 1)], {}),
    ("duplicates", [ev("a", "CREATED", 1), ev("a", "CREATED", 1)], {"a": "CREATED"}),
    ("many txns", FLOW, {"a": "SETTLED", "b": "FAILED", "c": "AUTHORIZED"}),
    ("empty", [], {}),
])
table(globals(), 2, lambda s, e: s.status_counts(e), [
    ("counts", FLOW, {"SETTLED": 1, "FAILED": 1, "AUTHORIZED": 1}),
    ("same status", [ev("a", "CREATED", 1), ev("b", "CREATED", 1)], {"CREATED": 2}),
    ("empty counts", [], {}),
])
table(globals(), 2, lambda s, e, now, age: s.stuck(e, now, age), [
    ("stuck one", (FLOW, 20, 10), ["c"]),
    ("terminal never stuck", (FLOW, 1000, 1), ["c"]),
    ("boundary not stuck", (FLOW, 15, 10), []),
    ("all young", (FLOW, 6, 10), []),
    ("sorted", ([ev("z", "CREATED", 0), ev("m", "CAPTURED", 0)], 50, 1), ["m", "z"]),
])
