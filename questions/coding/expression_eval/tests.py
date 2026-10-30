from check import table

table(globals(), 1, lambda s, e: s.evaluate(e), [
    ("number", "42", 42.0), ("decimal", "2.5", 2.5), ("leading dot", ".5 + .5", 1.0),
    ("precedence", "2 + 3 * 4", 14.0), ("parens", "(2 + 3) * 4", 20.0),
    ("left assoc minus", "8 - 3 - 2", 3.0), ("left assoc div", "8 / 4 / 2", 1.0),
    ("unary", "-3 + 5", 2.0), ("unary parens", "-(2 + 1)", -3.0), ("unary after op", "2 * -3", -6.0),
    ("double unary", "--4", 4.0), ("whitespace", "  1+  2 *3 ", 7.0), ("nested", "((1 + 2) * (3 + 4)) / 7", 3.0),
    ("unbalanced", "(1 + 2", ValueError), ("extra close", "1 + 2)", ValueError), ("dangling", "1 +", ValueError),
    ("empty", "   ", ValueError), ("bad char", "2 ^ 3", ValueError), ("two numbers", "1 2", ValueError),
    ("div zero", "1 / (2 - 2)", ZeroDivisionError),
])
V = {"base": 3, "miles": 4, "surge": 1.5}
table(globals(), 2, lambda s, e, v: s.evaluate(e, v), [
    ("variables", ("base + 1.5 * (miles - 2)", V), 6.0),
    ("unknown var", ("tip * 2", V), NameError),
    ("min", ("min(miles, 2, 9)", V), 2.0),
    ("max nested", ("max(base, min(10, miles * surge))", V), 6.0),
    ("call in expression", ("2 * max(1, 3) + 1", V), 7.0),
    ("unknown function", ("abs(1)", V), NameError),
    ("no args", ("min()", V), ValueError),
    ("unary call", ("-max(1, 2)", V), -2.0),
    ("underscore names", ("min_fare * 2", {"min_fare": 3.5}), 7.0),
])
