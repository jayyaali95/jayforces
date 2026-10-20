from check import table

S = [(0, 60), (30, 90), (60, 120), (100, 200)]
table(globals(), 1, lambda s, x: s.max_online(x), [
    ("overlap", S, 2), ("empty", [], 0), ("single", [(5, 10)], 1),
    ("back to back", [(0, 10), (10, 20), (20, 30)], 1), ("nested", [(0, 100), (10, 90), (20, 80)], 3),
    ("identical", [(0, 10)] * 4, 4), ("invalid ignored", [(10, 5), (3, 3), (0, 1)], 1),
    ("unsorted", [(50, 70), (0, 100), (60, 65)], 3),
])
table(globals(), 2, lambda s, *a: s.gaps(*a), [
    ("one driver needed", (S, 1, 0, 240), [(200, 240)]),
    ("two needed", (S, 2, 0, 240), [(0, 30), (90, 100), (120, 240)]),
    ("no shifts", ([], 1, 0, 100), [(0, 100)]),
    ("fully covered", ([(0, 100)], 1, 0, 100), []),
    ("clip outside day", ([(-50, 20), (90, 500)], 1, 0, 100), [(20, 90)]),
    ("touching shifts no gap", ([(0, 50), (50, 100)], 1, 0, 100), []),
    ("k zero", (S, 0, 0, 240), []),
    ("gap at start", ([(10, 100)], 1, 0, 100), [(0, 10)]),
    ("merged gap", ([(0, 10), (5, 30)], 2, 0, 40), [(0, 5), (10, 40)]),
])
