from check import eq, table

DEPS = {"report": ["clean", "join"], "join": ["load_a", "load_b"], "clean": ["load_a"]}

table(globals(), 1, lambda s, d: s.run_order(d), [
    ("pipeline", DEPS, ["load_a", "clean", "load_b", "join", "report"]),
    ("implicit jobs", {"b": ["a"]}, ["a", "b"]),
    ("independent alphabetical", {"c": [], "a": [], "b": []}, ["a", "b", "c"]),
    ("empty", {}, []),
    ("diamond", {"d": ["b", "c"], "b": ["a"], "c": ["a"]}, ["a", "b", "c", "d"]),
    ("self cycle", {"a": ["a"]}, ValueError),
    ("two cycle", {"a": ["b"], "b": ["a"]}, ValueError),
])


def test_p1_cycle_message(sol):
    try:
        sol.run_order({"x": ["a"], "a": ["b"], "b": ["c"], "c": ["a"]})
    except ValueError as e:
        msg = str(e)
        eq(all(j in msg for j in ("a", "b", "c")) and "cycle" in msg, True, msg=f"message was {msg!r}")
    else:
        raise AssertionError("expected ValueError")


table(globals(), 2, lambda s, d: s.stages(d), [
    ("pipeline stages", DEPS, [["load_a", "load_b"], ["clean", "join"], ["report"]]),
    ("chain", {"c": ["b"], "b": ["a"]}, [["a"], ["b"], ["c"]]),
    ("flat", {"b": [], "a": []}, [["a", "b"]]),
    ("empty stages", {}, []),
    ("uneven", {"z": ["a", "y"], "y": ["x"], "x": ["a"]}, [["a"], ["x"], ["y"], ["z"]]),
])
DUR = {"load_a": 5, "load_b": 2, "clean": 1, "join": 3, "report": 1}
table(globals(), 3, lambda s, d, du: s.finish_time(d, du), [
    ("pipeline time", (DEPS, DUR), 9), ("default durations", (DEPS, {}), 3), ("empty time", ({}, {}), 0),
])
table(globals(), 3, lambda s, d, du: s.critical_path(d, du), [
    ("pipeline path", (DEPS, DUR), ["load_a", "join", "report"]),
    ("tie alphabetical", ({"c": ["a", "b"]}, {}), ["a", "c"]),
    ("single job", ({"a": []}, {"a": 4}), ["a"]),
])
