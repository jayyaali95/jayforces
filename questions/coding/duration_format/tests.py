from check import table

table(globals(), 1, lambda s, x: s.format_duration(x), [
    ("zero", 0, "0s"), ("seconds", 45, "45s"), ("one minute", 60, "1m"),
    ("minutes and seconds", 187, "3m 07s"), ("just under an hour", 3599, "59m 59s"),
    ("one hour", 3600, "1h"), ("hour and minutes", 3900, "1h 05m"),
    ("seconds truncated", 3959, "1h 05m"), ("many hours", 36000 + 59, "10h"),
    ("negative", -1, ValueError),
])
table(globals(), 2, lambda s, x: s.parse_duration(x), [
    ("full", "1h 5m 3s", 3903), ("leading zero", "1h 05m", 3900), ("no spaces", "2h30m", 9000),
    ("only seconds", "45s", 45), ("upper case", "1H 2M", 3720), ("padding", "  7m  ", 420),
    ("roundtrip", "3m 07s", 187), ("empty", "", ValueError), ("wrong order", "5m 1h", ValueError),
    ("repeat", "1h 1h", ValueError), ("junk", "ten minutes", ValueError), ("bare number", "90", ValueError),
])
