from check import close, eq


def calls(sol, limit, window, seq):
    rl = sol.RateLimiter(limit, window)
    return [rl.allow(u, t) for u, t in seq]


def test_p1_under_limit(sol):
    eq(calls(sol, 3, 10, [("a", 0), ("a", 1), ("a", 2)]), [True] * 3)


def test_p1_over_limit(sol):
    eq(calls(sol, 2, 10, [("a", 0), ("a", 1), ("a", 2)]), [True, True, False])


def test_p1_window_slides(sol):
    eq(calls(sol, 2, 10, [("a", 0), ("a", 1), ("a", 10)]), [True, True, True])


def test_p1_boundary_is_exclusive(sol):
    eq(calls(sol, 1, 10, [("a", 0), ("a", 9.999), ("a", 10)]), [True, False, True])


def test_p1_users_independent(sol):
    eq(calls(sol, 1, 10, [("a", 0), ("b", 0), ("a", 1)]), [True, True, False])


def test_p1_rejected_not_counted(sol):
    eq(calls(sol, 1, 10, [("a", 0), ("a", 5), ("a", 10)]), [True, False, True])


def test_p1_same_timestamp(sol):
    eq(calls(sol, 2, 1, [("a", 5), ("a", 5), ("a", 5)]), [True, True, False])


def test_p1_long_run(sol):
    out = calls(sol, 5, 60, [("a", t) for t in range(0, 600, 6)])
    eq(sum(out), 50)


def test_p1_burst_then_quiet(sol):
    eq(calls(sol, 3, 10, [("a", 0)] * 5 + [("a", 100)] * 3), [True] * 3 + [False] * 2 + [True] * 3)


RULES = {"/rides": (2, 10), "*": (1, 5)}


def test_p2_allowed(sol):
    eq(sol.MultiLimiter(RULES).check("a", "/rides", 0), (True, 0.0))


def test_p2_retry_after(sol):
    m = sol.MultiLimiter(RULES)
    m.check("a", "/rides", 0)
    m.check("a", "/rides", 3)
    ok, wait = m.check("a", "/rides", 4)
    eq(ok, False)
    close(wait, 6.0)


def test_p2_retry_works(sol):
    m = sol.MultiLimiter(RULES)
    m.check("a", "/rides", 0)
    m.check("a", "/rides", 3)
    _, wait = m.check("a", "/rides", 4)
    eq(m.check("a", "/rides", 4 + wait)[0], True)


def test_p2_default_rule(sol):
    m = sol.MultiLimiter(RULES)
    m.check("a", "/profile", 0)
    eq(m.check("a", "/profile", 1), (False, 4.0))


def test_p2_default_per_endpoint(sol):
    m = sol.MultiLimiter(RULES)
    m.check("a", "/profile", 0)
    eq(m.check("a", "/history", 1), (True, 0.0))


def test_p2_no_default_allows(sol):
    m = sol.MultiLimiter({"/rides": (1, 10)})
    eq([m.check("a", "/x", t)[0] for t in range(5)], [True] * 5)


def test_p2_users_separate(sol):
    m = sol.MultiLimiter(RULES)
    m.check("a", "/rides", 0)
    m.check("a", "/rides", 0)
    eq(m.check("b", "/rides", 0), (True, 0.0))


def test_p2_rejection_not_counted(sol):
    m = sol.MultiLimiter({"*": (1, 10)})
    m.check("a", "/x", 0)
    m.check("a", "/x", 5)
    eq(m.check("a", "/x", 10), (True, 0.0))
