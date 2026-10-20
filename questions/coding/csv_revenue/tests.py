from check import table

H = "trip_id,city,fare,currency,completed_at\n"
GOOD = H + 't1,"San Francisco, CA",12.50,USD,2024-05-01\nt2,Austin,10,USD,2024-05-01\nt3,Austin,0.005,USD,2024-05-02\n'
MESSY = H + ("t1,Austin,10.00,USD,d\n"
             "t2,Austin,5\n"
             "t3,,5,USD,d\n"
             "t4,Austin,abc,USD,d\n"
             "t5,Austin,-1,USD,d\n"
             "t6,Austin,5,EUR,d\n"
             "t1,Austin,10.00,USD,d\n"
             't7,  Denver ,2.345,USD,d\n')

table(globals(), 1, lambda s, t: s.revenue_by_city(t), [
    ("good rows", GOOD, {"San Francisco, CA": 1250, "Austin": 1001}),
    ("header only", H, {}),
    ("reordered columns", "fare,currency,city,trip_id\n3.10,USD,Reno,a\n", {"Reno": 310}),
    ("skip bad currency", H + "t1,Austin,5,CAD,d\n", {}),
    ("skip negative", H + "t1,Austin,-5,USD,d\n", {}),
    ("skip nan", H + "t1,Austin,nan,USD,d\n", {}),
    ("trim city", H + "t1,  Reno  ,1,USD,d\n", {"Reno": 100}),
    ("round half up", H + "t1,Reno,0.125,USD,d\n", {"Reno": 13}),
    ("quoted fare", H + 't1,Reno,"7.00",USD,d\n', {"Reno": 700}),
])
table(globals(), 2, lambda s, t: s.report(t), [
    ("messy", MESSY, {"totals": {"Austin": 1000, "Denver": 235}, "top_city": "Austin",
                      "errors": [(3, "columns"), (4, "city"), (5, "fare"), (6, "fare"), (7, "currency"), (8, "duplicate")]}),
    ("no rows", H, {"totals": {}, "errors": [], "top_city": None}),
    ("tie alphabetical", H + "a,Zed,1,USD,d\nb,Abe,1,USD,d\n", {"totals": {"Zed": 100, "Abe": 100}, "errors": [], "top_city": "Abe"}),
    ("invalid row does not reserve id", H + "a,Reno,x,USD,d\na,Reno,1,USD,d\n", {"totals": {"Reno": 100}, "errors": [(2, "fare")], "top_city": "Reno"}),
    ("missing column", "trip_id,city,fare\n", ValueError),
    ("check order city before fare", H + "a,,x,EUR,d\n", {"totals": {}, "errors": [(2, "city")], "top_city": None}),
])
