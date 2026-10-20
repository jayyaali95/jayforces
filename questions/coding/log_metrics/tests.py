from check import table

GOOD = "2024-05-01T10:00:00Z GET /rides 200 123ms"
LOG = [GOOD, "2024-05-01T10:00:01Z GET /rides 500 300ms", "garbage",
       "2024-05-01T10:00:02Z POST /rides 201 80ms", "", "2024-05-01T10:00:03Z GET /rides?id=3 200 30ms",
       "2024-05-01T10:00:04Z GET /drivers 404 15ms", "2024-05-01T10:00:05Z GET /rides 2OO 10ms"]

table(globals(), 1, lambda s, l: s.parse_line(l), [
    ("valid", GOOD, {"ts": "2024-05-01T10:00:00Z", "method": "GET", "path": "/rides", "status": 200, "ms": 123}),
    ("extra spaces ok", "t   GET  /a  200   5ms", {"ts": "t", "method": "GET", "path": "/a", "status": 200, "ms": 5}),
    ("missing field", "t GET /a 200", None),
    ("extra field", "t GET /a 200 5ms x", None),
    ("bad method", "t FETCH /a 200 5ms", None),
    ("bad path", "t GET a 200 5ms", None),
    ("status letters", "t GET /a 2OO 5ms", None),
    ("status range", "t GET /a 700 5ms", None),
    ("latency unit", "t GET /a 200 5s", None),
    ("negative latency", "t GET /a 200 -5ms", None),
    ("blank", "", None),
])
table(globals(), 1, lambda s, l: s.status_counts(l), [
    ("counts", LOG, {200: 2, 500: 1, 201: 1, 404: 1}),
    ("no valid lines", ["x", ""], {}),
])
STATS = {("GET", "/rides"): {"count": 3, "avg_ms": 151.0, "p50_ms": 123, "error_rate": 0.3333},
         ("POST", "/rides"): {"count": 1, "avg_ms": 80.0, "p50_ms": 80, "error_rate": 0.0},
         ("GET", "/drivers"): {"count": 1, "avg_ms": 15.0, "p50_ms": 15, "error_rate": 0.0}}
table(globals(), 2, lambda s, l: s.endpoint_stats(l), [
    ("full log", LOG, STATS),
    ("lower median even count", ["t GET /a 200 10ms", "t GET /a 200 20ms"],
     {("GET", "/a"): {"count": 2, "avg_ms": 15.0, "p50_ms": 10, "error_rate": 0.0}}),
    ("all errors", ["t GET /a 503 1ms", "t GET /a 500 2ms"],
     {("GET", "/a"): {"count": 2, "avg_ms": 1.5, "p50_ms": 1, "error_rate": 1.0}}),
    ("avg rounding", ["t GET /a 200 1ms", "t GET /a 200 1ms", "t GET /a 200 2ms"],
     {("GET", "/a"): {"count": 3, "avg_ms": 1.33, "p50_ms": 1, "error_rate": 0.0}}),
    ("empty", [], {}),
])
