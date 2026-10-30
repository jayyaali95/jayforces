from check import eq, raises, table

ROWS = [{"id": 1, "city": "sf", "fare": 20, "mins": 15}, {"id": 2, "city": "ny", "fare": 35},
        {"id": 3, "city": "sf", "fare": 10, "mins": 5}, {"id": 4, "city": "la", "fare": 35, "mins": 30},
        {"id": 5, "fare": 7, "mins": 2}]

Q = lambda s: s.Query(ROWS)
ids = lambda q: [r["id"] for r in q.all()]
table(globals(), 1, lambda s, f: f(Q(s)), [
    ("all rows", lambda q: ids(q), [1, 2, 3, 4, 5]),
    ("where eq", lambda q: ids(q.where("city", "==", "sf")), [1, 3]),
    ("where missing field", lambda q: ids(q.where("mins", "<", 100)), [1, 3, 4, 5]),
    ("where in", lambda q: ids(q.where("city", "in", {"ny", "la"})), [2, 4]),
    ("chained where", lambda q: ids(q.where("fare", ">=", 10).where("city", "!=", "ny")), [1, 3, 4]),
    ("order desc stable", lambda q: ids(q.order_by("fare", desc=True)), [2, 4, 1, 3, 5]),
    ("missing last", lambda q: ids(q.order_by("mins")), [5, 3, 1, 4, 2]),
    ("missing last desc", lambda q: ids(q.order_by("mins", desc=True)), [4, 1, 3, 5, 2]),
    ("select", lambda q: q.where("id", "==", 2).select("id", "mins").all(), [{"id": 2, "mins": None}]),
    ("limit after order", lambda q: ids(q.order_by("fare").limit(2)), [5, 3]),
    ("order after limit", lambda q: ids(q.limit(2).order_by("fare")), [1, 2]),
])


def test_p1_immutable(sol):
    q = Q(sol)
    q.where("city", "==", "sf")
    q.limit(1)
    eq(len(q.all()), 5)


def test_p1_results_are_copies(sol):
    q = Q(sol)
    q.all()[0]["fare"] = 999
    eq((q.all()[0]["fare"], ROWS[0]["fare"]), (20, 20))


def test_p1_unknown_op(sol):
    raises(ValueError, Q(sol).where, "fare", "~", 1)


table(globals(), 2, lambda s, f: f(Q(s)), [
    ("group count", lambda q: q.group_by("city").agg(n=(None, "count")).all(),
     [{"city": "sf", "n": 2}, {"city": "ny", "n": 1}, {"city": "la", "n": 1}]),
    ("group sum avg", lambda q: q.group_by("city").agg(total=("fare", "sum"), avg=("fare", "avg")).where("city", "==", "sf").all(),
     [{"city": "sf", "total": 30, "avg": 15.0}]),
    ("group after where", lambda q: q.where("fare", ">", 15).group_by("fare").agg(n=(None, "count")).all(),
     [{"fare": 20, "n": 1}, {"fare": 35, "n": 2}]),
    ("global agg", lambda q: q.agg(lo=("fare", "min"), hi=("fare", "max"), avg=("fare", "avg")).all(), [{"lo": 7, "hi": 35, "avg": 21.4}]),
    ("agg then order", lambda q: q.group_by("city").agg(t=("fare", "sum")).order_by("t", desc=True).select("city").all(),
     [{"city": "ny"}, {"city": "la"}, {"city": "sf"}]),
])
