from check import eq


def setup(sol, *patterns):
    bus, seen = sol.EventBus(), []
    tokens = [bus.subscribe(p, lambda t, x, p=p: seen.append((p, t, x))) for p in patterns]
    return bus, seen, tokens


def test_p1_exact(sol):
    bus, seen, _ = setup(sol, "rides.created")
    eq((bus.publish("rides.created", 1), seen), (1, [("rides.created", "rides.created", 1)]))


def test_p1_no_match(sol):
    bus, seen, _ = setup(sol, "rides.created")
    eq((bus.publish("rides.cancelled", 1), seen), (0, []))


def test_p1_star(sol):
    bus, seen, _ = setup(sol, "rides.*")
    eq([bus.publish(t, 0) for t in ("rides.created", "rides", "rides.a.b", "drivers.created")], [1, 0, 0, 0])


def test_p1_star_middle(sol):
    bus, _, _ = setup(sol, "*.created")
    eq([bus.publish(t, 0) for t in ("rides.created", "drivers.created", "rides.done")], [1, 1, 0])


def test_p1_order(sol):
    bus, seen, _ = setup(sol, "a.*", "a.b", "*.b")
    bus.publish("a.b", 0)
    eq([p for p, _, _ in seen], ["a.*", "a.b", "*.b"])


def test_p1_tokens_unique(sol):
    _, _, tokens = setup(sol, "a", "a", "b")
    eq(len(set(tokens)), 3)


def test_p1_same_handler_twice(sol):
    bus, calls = sol.EventBus(), []
    h = lambda t, x: calls.append(x)
    bus.subscribe("a", h); bus.subscribe("a", h)
    eq((bus.publish("a", 7), calls), (2, [7, 7]))


def test_p2_unsubscribe(sol):
    bus, seen, (t1, t2) = setup(sol, "a", "a")
    eq((bus.unsubscribe(t1), bus.publish("a", 0)), (True, 1))


def test_p2_unsubscribe_unknown(sol):
    bus, _, (t1,) = setup(sol, "a")
    bus.unsubscribe(t1)
    eq(bus.unsubscribe(t1), False)


def test_p2_hash(sol):
    bus, _, _ = setup(sol, "rides.#")
    eq([bus.publish(t, 0) for t in ("rides.a", "rides.a.b.c", "rides", "x.a")], [1, 1, 0, 0])


def test_p2_hash_after_star(sol):
    bus, _, _ = setup(sol, "*.x.#")
    eq([bus.publish(t, 0) for t in ("a.x.y", "a.x", "a.y.z")], [1, 0, 0])


def test_p2_error_isolated(sol):
    bus, seen = sol.EventBus(), []
    bus.subscribe("a", lambda t, x: 1 / 0)
    bus.subscribe("a", lambda t, x: seen.append(x))
    eq((bus.publish("a", 5), seen), (2, [5]))


def test_p2_errors_collected(sol):
    bus = sol.EventBus()
    bus.subscribe("a.*", lambda t, x: (_ for _ in ()).throw(KeyError(x)))
    bus.publish("a.b", "k1"); bus.publish("a.c", "k2")
    eq([(t, type(e).__name__) for t, e in bus.errors()], [("a.b", "KeyError"), ("a.c", "KeyError")])


def test_p2_subscribe_during_publish(sol):
    bus, seen = sol.EventBus(), []
    bus.subscribe("a", lambda t, x: bus.subscribe("a", lambda t2, y: seen.append("late")))
    eq((bus.publish("a", 0), seen), (1, []))


def test_p2_unsubscribe_during_publish(sol):
    bus, seen = sol.EventBus(), []
    tok = {}
    bus.subscribe("a", lambda t, x: bus.unsubscribe(tok["b"]))
    tok["b"] = bus.subscribe("a", lambda t, x: seen.append("b"))
    bus.publish("a", 0)
    eq((seen, bus.publish("a", 0)), (["b"], 1))
