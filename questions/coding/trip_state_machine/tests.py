from check import eq, raises, table


def walk(sol, steps):
    t = sol.Trip()
    for s in steps:
        t.apply(s)
    return t.state


table(globals(), 1, walk, [
    ("starts requested", [], "REQUESTED"),
    ("happy path", ["ACCEPTED", "ARRIVED", "STARTED", "COMPLETED"], "COMPLETED"),
    ("cancel early", ["CANCELLED"], "CANCELLED"),
    ("cancel after arrive", ["ACCEPTED", "ARRIVED", "CANCELLED"], "CANCELLED"),
    ("skip step", ["ARRIVED"], ValueError),
    ("cancel after start", ["ACCEPTED", "ARRIVED", "STARTED", "CANCELLED"], ValueError),
    ("nothing after complete", ["ACCEPTED", "ARRIVED", "STARTED", "COMPLETED", "STARTED"], ValueError),
    ("unknown state", ["TELEPORTED"], ValueError),
])


def test_p1_can(sol):
    t = sol.Trip()
    eq((t.can("ACCEPTED"), t.can("STARTED")), (True, False))


def test_p1_failed_apply_keeps_state(sol):
    t = sol.Trip()
    raises(ValueError, t.apply, "COMPLETED")
    eq(t.state, "REQUESTED")


def ev(i, trip, state, ts):
    return {"id": i, "trip": trip, "state": state, "ts": ts}


STREAM = [ev(3, "t1", "ARRIVED", 30), ev(1, "t1", "REQUESTED", 10), ev(2, "t1", "ACCEPTED", 20),
          ev(4, "t2", "ACCEPTED", 5), ev(5, "t2", "COMPLETED", 6), ev(2, "t1", "ACCEPTED", 21), ev(6, "t2", "CANCELLED", 7)]

table(globals(), 2, lambda s, e: s.replay(e), [
    ("stream", STREAM, {"states": {"t1": "ARRIVED", "t2": "CANCELLED"}, "rejected": [5]}),
    ("empty", [], {"states": {}, "rejected": []}),
    ("implicit create", [ev(1, "t", "ACCEPTED", 1)], {"states": {"t": "ACCEPTED"}, "rejected": []}),
    ("explicit request ok", [ev(1, "t", "REQUESTED", 1)], {"states": {"t": "REQUESTED"}, "rejected": []}),
    ("second request rejected", [ev(1, "t", "REQUESTED", 1), ev(2, "t", "REQUESTED", 2)], {"states": {"t": "REQUESTED"}, "rejected": [2]}),
    ("duplicate skipped not rejected", [ev(1, "t", "ACCEPTED", 1), ev(1, "t", "ACCEPTED", 2)], {"states": {"t": "ACCEPTED"}, "rejected": []}),
    ("illegal first event", [ev(1, "t", "STARTED", 1)], {"states": {"t": "REQUESTED"}, "rejected": [1]}),
    ("stable ties", [ev(1, "t", "ACCEPTED", 5), ev(2, "t", "CANCELLED", 5)], {"states": {"t": "CANCELLED"}, "rejected": []}),
])
