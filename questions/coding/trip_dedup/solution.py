def dedup(records):
    """Return the latest version of each trip, sorted by trip_id."""
    best = {}
    for r in records:
        cur = best.get(r["trip_id"])
        if cur is None or r["version"] >= cur["version"]:
            best[r["trip_id"]] = r
    return [dict(best[k]) for k in sorted(best)]


def rider_summary(records):
    """Return per rider trip count, completed spend and cancel rate."""
    out = {}
    for r in dedup(records):
        s = out.setdefault(r["rider"], {"trips": 0, "spend": 0, "cancelled": 0})
        s["trips"] += 1
        s["spend"] += r["fare"] if r["status"] == "COMPLETED" else 0
        s["cancelled"] += r["status"] == "CANCELLED"
    return {k: {"trips": v["trips"], "spend": v["spend"], "cancel_rate": round(v["cancelled"] / v["trips"], 3)}
            for k, v in out.items()}
