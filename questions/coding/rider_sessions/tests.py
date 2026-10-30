from check import table

EV = [("u1", 0, "home"), ("u1", 100, "set_destination"), ("u1", 160, "request_ride"),
      ("u1", 5000, "home"), ("u2", 50, "home"), ("u2", 1850, "request_ride"), ("u2", 1900, "set_destination")]

table(globals(), 1, lambda s, e, *g: s.sessionize(e, *g), [
    ("example", EV, {"u1": [[(0, "home"), (100, "set_destination"), (160, "request_ride")], [(5000, "home")]],
                     "u2": [[(50, "home"), (1850, "request_ride"), (1900, "set_destination")]]}),
    ("gap exactly allowed", [("a", 0, "x"), ("a", 1800, "y")], {"a": [[(0, "x"), (1800, "y")]]}),
    ("gap one over splits", [("a", 0, "x"), ("a", 1801, "y")], {"a": [[(0, "x")], [(1801, "y")]]}),
    ("unsorted input", [("a", 30, "y"), ("a", 10, "x")], {"a": [[(10, "x"), (30, "y")]]}),
    ("stable ties", [("a", 5, "first"), ("a", 5, "second")], {"a": [[(5, "first"), (5, "second")]]}),
    ("custom gap", ([("a", 0, "x"), ("a", 11, "y"), ("a", 20, "z")], 10), {"a": [[(0, "x")], [(11, "y"), (20, "z")]]}),
    ("empty", [], {}),
    ("users dont mix", [("a", 0, "x"), ("b", 10, "y"), ("a", 20, "z")], {"a": [[(0, "x"), (20, "z")]], "b": [[(10, "y")]]}),
])
table(globals(), 2, lambda s, e, *g: s.session_stats(e, *g), [
    ("example stats", EV, {"sessions": 3, "avg_length": 670.0, "conversion": 0.333}),
    ("empty stats", [], {"sessions": 0, "avg_length": 0.0, "conversion": 0.0}),
    ("request before destination does not count", [("a", 0, "request_ride"), ("a", 1, "set_destination")],
     {"sessions": 1, "avg_length": 1.0, "conversion": 0.0}),
    ("conversion must be same session", [("a", 0, "set_destination"), ("a", 9999, "request_ride")],
     {"sessions": 2, "avg_length": 0.0, "conversion": 0.0}),
    ("all convert", [("a", 0, "set_destination"), ("a", 5, "request_ride"), ("b", 0, "set_destination"), ("b", 9, "request_ride")],
     {"sessions": 2, "avg_length": 7.0, "conversion": 1.0}),
    ("rounding", [("a", 0, "x"), ("a", 1, "y"), ("b", 0, "x"), ("c", 0, "x")], {"sessions": 3, "avg_length": 0.3, "conversion": 0.0}),
    ("gap param", ([("a", 0, "set_destination"), ("a", 50, "request_ride")], 10), {"sessions": 2, "avg_length": 0.0, "conversion": 0.0}),
])
