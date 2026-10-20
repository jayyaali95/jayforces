from check import eq, raises


def flaky(fail_times, exc=RuntimeError):
    state = {"n": 0}

    def f(x=1):
        """doc here"""
        state["n"] += 1
        if state["n"] <= fail_times:
            raise exc(f"boom {state['n']}")
        return x * 10

    return f, state


def make(sol, fail_times, exc=RuntimeError, **kw):
    sleeps = []
    f, state = flaky(fail_times, exc)
    return sol.retry(sleep=sleeps.append, **kw)(f), state, sleeps


def test_p1_success_first_try(sol):
    g, st, sl = make(sol, 0)
    eq((g(2), st["n"], sl), (20, 1, []))


def test_p1_success_after_failures(sol):
    g, st, _ = make(sol, 2, times=3)
    eq((g(), st["n"]), (10, 3))


def test_p1_raises_last_error(sol):
    g, st, _ = make(sol, 5, times=3)
    try:
        g()
    except RuntimeError as e:
        eq((str(e), st["n"]), ("boom 3", 3))
    else:
        raise AssertionError("expected RuntimeError")


def test_p1_backoff_delays(sol):
    g, _, sl = make(sol, 3, times=4, delay=1.0, backoff=3.0)
    g()
    eq(sl, [1.0, 3.0, 9.0])


def test_p1_no_sleep_after_last(sol):
    g, _, sl = make(sol, 9, times=2, delay=1.0)
    raises(RuntimeError, g)
    eq(sl, [1.0])


def test_p1_wraps(sol):
    g, _, _ = make(sol, 0)
    eq((g.__name__, g.__doc__), ("f", "doc here"))


def test_p1_bad_times(sol):
    raises(ValueError, sol.retry, times=0)


def test_p1_kwargs_passed(sol):
    g, _, _ = make(sol, 1)
    eq(g(x=4), 40)


def test_p1_times_one(sol):
    g, st, _ = make(sol, 1, times=1)
    raises(RuntimeError, g)
    eq(st["n"], 1)


def test_p2_only_listed(sol):
    g, st, _ = make(sol, 1, exc=KeyError, on=(ValueError,))
    raises(KeyError, g)
    eq(st["n"], 1)


def test_p2_listed_retried(sol):
    g, st, _ = make(sol, 2, exc=ValueError, on=(ValueError,))
    eq((g(), st["n"]), (10, 3))


def test_p2_subclass_retried(sol):
    g, st, _ = make(sol, 1, exc=FileNotFoundError, on=(OSError,))
    eq(g(), 10)


def test_p2_max_delay(sol):
    g, _, sl = make(sol, 4, times=5, delay=1.0, backoff=10.0, max_delay=5.0)
    g()
    eq(sl, [1.0, 5.0, 5.0, 5.0])


def test_p2_attempts(sol):
    g, _, _ = make(sol, 2, times=5)
    g()
    eq(g.attempts, 3)


def test_p2_attempts_per_call(sol):
    g, _, _ = make(sol, 2, times=5)
    g(); g()
    eq(g.attempts, 1)
