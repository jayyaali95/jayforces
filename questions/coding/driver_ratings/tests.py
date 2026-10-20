from check import eq, raises, table


def run(sol, window, adds, query):
    r = sol.Ratings(window)
    for d, s in adds:
        r.add(d, s)
    return query(r)


avg = lambda d: (lambda r: r.average(d))
table(globals(), 1, lambda s, w, adds, q: run(s, w, adds, q), [
    ("single", (10, [("a", 5)], avg("a")), 5.0),
    ("mean rounded", (10, [("a", 5), ("a", 4), ("a", 4)], avg("a")), 4.33),
    ("unknown driver", (10, [("a", 5)], avg("b")), None),
    ("window drops old", (2, [("a", 1), ("a", 5), ("a", 5)], avg("a")), 5.0),
    ("window one", (1, [("a", 1), ("a", 3)], avg("a")), 3.0),
    ("window of 100", (100, [("a", 2)] * 150 + [("a", 4)] * 50, avg("a")), 3.0),
    ("drivers independent", (2, [("a", 1), ("b", 5), ("a", 1)], avg("b")), 5.0),
])


def test_p1_rejects_zero(sol):
    raises(ValueError, sol.Ratings().add, "a", 0)


def test_p1_rejects_six(sol):
    raises(ValueError, sol.Ratings().add, "a", 6)


def test_p1_rejects_float(sol):
    raises(ValueError, sol.Ratings().add, "a", 4.0)


def test_p1_rejects_bool(sol):
    raises(ValueError, sol.Ratings().add, "a", True)


def test_p1_bad_rating_not_recorded(sol):
    r = sol.Ratings()
    try:
        r.add("a", 9)
    except ValueError:
        pass
    eq(r.average("a"), None)


ADDS = [("a", 5), ("a", 4), ("b", 5), ("c", 4), ("c", 5), ("d", 3), ("e", 5), ("e", 5)]
table(globals(), 2, lambda s, w, adds, q: run(s, w, adds, q), [
    ("top all", (10, ADDS, lambda r: r.top(10)), ["e", "b", "a", "c", "d"]),
    ("top k", (10, ADDS, lambda r: r.top(2)), ["e", "b"]),
    ("min ratings", (10, ADDS, lambda r: r.top(10, 2)), ["e", "a", "c"]),
    ("nobody qualifies", (10, ADDS, lambda r: r.top(3, 5)), []),
    ("uses window", (1, [("a", 1), ("a", 5), ("b", 4)], lambda r: r.top(2)), ["a", "b"]),
    ("empty", (10, [], lambda r: r.top(3)), []),
])
