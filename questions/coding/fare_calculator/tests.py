from check import table

table(globals(), 1, lambda s, *a: s.fare(*a), [
    ("short ride hits minimum", (1, 2), 700),
    ("normal ride", (5, 15), 250 + 750 + 450),
    ("fractional miles", (2.5, 10), 250 + 375 + 300),
    ("surge", (5, 15, "standard", 1.5), 2175),
    ("round half up", (0.01, 100, "xl", 1.0), 400 + 3 + 4500),
    ("half cent rounds up", (3.3, 0, "standard", 1.5), 1118),
    ("xl minimum", (0, 0, "xl"), 1100),
    ("xl normal", (10, 20, "xl"), 400 + 2500 + 900),
    ("zero ride", (0, 0), 700),
    ("negative miles", (-1, 3), ValueError),
    ("negative minutes", (1, -3), ValueError),
    ("unknown type", (1, 1, "limo"), ValueError),
    ("surge below one", (1, 1, "standard", 0.9), ValueError),
])
table(globals(), 2, lambda s, c, p: s.apply_promo(c, p), [
    ("no promo", (1500, None), 1500),
    ("percent", (1500, {"type": "percent", "value": 20}), 1200),
    ("percent capped", (5000, {"type": "percent", "value": 20, "cap": 500}), 4500),
    ("percent rounds half up", (1005, {"type": "percent", "value": 10}), 904),
    ("flat", (1500, {"type": "flat", "value": 300}), 1200),
    ("flat floors at zero", (200, {"type": "flat", "value": 300}), 0),
    ("hundred percent", (999, {"type": "percent", "value": 100}), 0),
    ("unknown promo", (999, {"type": "bogo", "value": 1}), ValueError),
])
