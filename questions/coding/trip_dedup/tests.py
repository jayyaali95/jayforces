import copy

from check import eq, table


def rec(t, v, rider="r1", fare=1000, status="COMPLETED"):
    return {"trip_id": t, "rider": rider, "version": v, "fare": fare, "status": status}


DATA = [rec("t2", 1, status="REQUESTED"), rec("t1", 1, fare=900), rec("t2", 3, fare=1500),
        rec("t1", 2, fare=950), rec("t3", 1, rider="r2", status="CANCELLED", fare=0), rec("t2", 2)]

table(globals(), 1, lambda s, r: s.dedup(r), [
    ("latest version", DATA, [rec("t1", 2, fare=950), rec("t2", 3, fare=1500), rec("t3", 1, rider="r2", status="CANCELLED", fare=0)]),
    ("tie keeps last seen", [rec("a", 1, fare=1), rec("a", 1, fare=2)], [rec("a", 1, fare=2)]),
    ("tie later wins even when earlier was higher first", [rec("a", 2, fare=1), rec("a", 1, fare=5), rec("a", 2, fare=3)], [rec("a", 2, fare=3)]),
    ("single", [rec("a", 7)], [rec("a", 7)]),
    ("empty", [], []),
    ("sorted output", [rec("b", 1), rec("a", 1), rec("c", 1)], [rec("a", 1), rec("b", 1), rec("c", 1)]),
])


def test_p1_does_not_mutate(sol):
    data = copy.deepcopy(DATA)
    out = sol.dedup(data)
    out[0]["fare"] = -1
    eq(data, DATA)


table(globals(), 2, lambda s, r: s.rider_summary(r), [
    ("summary", DATA, {"r1": {"trips": 2, "spend": 2450, "cancel_rate": 0.0}, "r2": {"trips": 1, "spend": 0, "cancel_rate": 1.0}}),
    ("only latest counted", [rec("a", 1, status="CANCELLED"), rec("a", 2)], {"r1": {"trips": 1, "spend": 1000, "cancel_rate": 0.0}}),
    ("non completed no spend", [rec("a", 1, status="IN_PROGRESS", fare=700)], {"r1": {"trips": 1, "spend": 0, "cancel_rate": 0.0}}),
    ("rate rounding", [rec("a", 1, status="CANCELLED"), rec("b", 1), rec("c", 1)], {"r1": {"trips": 3, "spend": 2000, "cancel_rate": 0.333}}),
    ("multi riders", [rec("a", 1, rider="x"), rec("b", 1, rider="y", fare=5)], {"x": {"trips": 1, "spend": 1000, "cancel_rate": 0.0}, "y": {"trips": 1, "spend": 5, "cancel_rate": 0.0}}),
    ("empty summary", [], {}),
    ("all cancelled", [rec("a", 1, status="CANCELLED"), rec("b", 1, status="CANCELLED")], {"r1": {"trips": 2, "spend": 0, "cancel_rate": 1.0}}),
    ("two thirds", [rec("a", 1, status="CANCELLED"), rec("b", 1, status="CANCELLED"), rec("c", 1)], {"r1": {"trips": 3, "spend": 1000, "cancel_rate": 0.667}}),
])
