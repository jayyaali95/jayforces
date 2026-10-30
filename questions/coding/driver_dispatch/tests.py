import random
import time

from check import eq, table

D = {"d1": (0, 0), "d2": (5, 5), "d3": (10, 0)}

table(globals(), 1, lambda s, d, r: s.nearest(d, r), [
    ("closest", (D, (1, 1)), "d1"), ("other closest", (D, (9, 1)), "d3"),
    ("tie by id", ({"b": (1, 0), "a": (-1, 0)}, (0, 0)), "a"),
    ("no drivers", ({}, (0, 0)), None), ("on top", (D, (5, 5)), "d2"),
])

table(globals(), 2, lambda s, d, r: s.simulate(d, r), [
    ("one request", (D, [("r1", 0, (1, 0), (3, 0))]), {"r1": ("d1", 1)}),
    ("second goes elsewhere", (D, [("r1", 0, (0, 0), (0, 4)), ("r2", 1, (0, 0), (1, 0))]),
     {"r1": ("d1", 0), "r2": ("d2", 11)}),
    ("driver frees at dropoff", ({"d": (0, 0)}, [("r1", 0, (0, 0), (5, 0)), ("r2", 5, (6, 0), (6, 1))]),
     {"r1": ("d", 0), "r2": ("d", 6)}),
    ("busy until exactly t is free", ({"d": (0, 0)}, [("a", 0, (0, 0), (2, 0)), ("b", 2, (2, 0), (2, 0))]),
     {"a": ("d", 0), "b": ("d", 2)}),
    ("unmatched", ({"d": (0, 0)}, [("a", 0, (0, 0), (9, 0)), ("b", 3, (0, 0), (1, 0))]), {"a": ("d", 0), "b": None}),
    ("order by time not input", ({"d": (0, 0)}, [("late", 5, (0, 0), (0, 0)), ("early", 0, (0, 0), (0, 9))]),
     {"early": ("d", 0), "late": None}),
    ("ties by request id", ({"d": (0, 0)}, [("b", 0, (0, 0), (0, 1)), ("a", 0, (0, 0), (0, 1))]), {"a": ("d", 0), "b": None}),
    ("no drivers sim", ({}, [("a", 0, (0, 0), (1, 1))]), {"a": None}),
])


def test_p2_scale(sol):
    rnd = random.Random(7)
    drivers = {f"d{i:04d}": (rnd.randrange(100), rnd.randrange(100)) for i in range(1000)}
    reqs = [(f"r{i:05d}", rnd.randrange(5000), (rnd.randrange(100), rnd.randrange(100)), (rnd.randrange(100), rnd.randrange(100)))
            for i in range(10000)]
    t0 = time.perf_counter()
    out = sol.simulate(drivers, reqs)
    eq((len(out), time.perf_counter() - t0 < 8), (10000, True), msg="should finish within a few seconds")


table(globals(), 3, lambda s, d, r, h: s.utilization(d, r, h), [
    ("single trip", ({"d": (0, 0)}, [("a", 0, (2, 0), (4, 0))], 10), {"d": 0.4}),
    ("clipped at horizon", ({"d": (0, 0)}, [("a", 0, (0, 0), (20, 0))], 10), {"d": 1.0}),
    ("idle driver", ({"d": (0, 0), "e": (50, 50)}, [("a", 0, (0, 0), (1, 0))], 4), {"d": 0.25, "e": 0.0}),
    ("starts after horizon", ({"d": (0, 0)}, [("a", 20, (0, 0), (1, 0))], 10), {"d": 0.0}),
    ("two trips", ({"d": (0, 0)}, [("a", 0, (0, 0), (1, 0)), ("b", 5, (1, 0), (3, 0))], 10), {"d": 0.3}),
])
