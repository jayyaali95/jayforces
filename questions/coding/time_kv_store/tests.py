import time

from check import eq


def store(sol, ops):
    s = sol.TimeStore()
    for op in ops:
        getattr(s, op[0])(*op[1:])
    return s


BASE = [("set", "car", "prius", 10), ("set", "car", "camry", 20), ("set", "zone", "sf", 5)]


def test_p1_exact(sol):
    eq(store(sol, BASE).get("car", 10), "prius")


def test_p1_between(sol):
    eq(store(sol, BASE).get("car", 15), "prius")


def test_p1_after(sol):
    eq(store(sol, BASE).get("car", 99), "camry")


def test_p1_before_first(sol):
    eq(store(sol, BASE).get("car", 9), None)


def test_p1_missing_key(sol):
    eq(store(sol, BASE).get("nope", 9), None)


def test_p1_out_of_order(sol):
    s = store(sol, [("set", "k", "late", 30), ("set", "k", "early", 10)])
    eq((s.get("k", 15), s.get("k", 30)), ("early", "late"))


def test_p1_overwrite(sol):
    eq(store(sol, [("set", "k", 1, 5), ("set", "k", 2, 5)]).get("k", 5), 2)


def test_p1_falsy_values(sol):
    eq(store(sol, [("set", "k", 0, 5)]).get("k", 6), 0)


def test_p1_fast_enough(sol):
    s = sol.TimeStore()
    for t in range(20000):
        s.set("k", t, t)
    t0 = time.perf_counter()
    for t in range(0, 20000, 2):
        s.get("k", t + 0.5)
    eq(time.perf_counter() - t0 < 0.5, True, msg="10k gets should be well under 0.5s")


DEL = BASE + [("delete", "car", 25), ("set", "car", "tesla", 40)]


def test_p2_deleted(sol):
    eq(store(sol, DEL).get("car", 30), None)


def test_p2_set_after_delete(sol):
    eq(store(sol, DEL).get("car", 40), "tesla")


def test_p2_before_delete(sol):
    eq(store(sol, DEL).get("car", 24), "camry")


def test_p2_history(sol):
    eq(store(sol, DEL).history("car", 0, 100), [(10, "prius"), (20, "camry"), (40, "tesla")])


def test_p2_history_bounds(sol):
    eq(store(sol, DEL).history("car", 10, 20), [(10, "prius"), (20, "camry")])


def test_p2_history_missing(sol):
    eq(store(sol, DEL).history("x", 0, 9), [])


def test_p2_keys_at(sol):
    eq(store(sol, DEL).keys_at(30), ["zone"])


def test_p2_keys_at_both(sol):
    eq(store(sol, DEL).keys_at(41), ["car", "zone"])
