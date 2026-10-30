METHODS = {"GET", "POST", "PUT", "DELETE"}


def parse_line(line):
    """Return a dict for a valid line, else None."""
    parts = line.split()
    if len(parts) != 5:
        return None
    ts, method, path, status, ms = parts
    if method not in METHODS or not path.startswith("/"):
        return None
    if not (len(status) == 3 and status.isdigit() and 100 <= int(status) <= 599):
        return None
    if not (ms.endswith("ms") and ms[:-2].isdigit()):
        return None
    return {"ts": ts, "method": method, "path": path, "status": int(status), "ms": int(ms[:-2])}


def status_counts(lines):
    """Return {status: count} over valid lines."""
    out = {}
    for rec in filter(None, map(parse_line, lines)):
        out[rec["status"]] = out.get(rec["status"], 0) + 1
    return out


def endpoint_stats(lines):
    """Return per (method, path) count, avg, p50 and error rate."""
    groups = {}
    for rec in filter(None, map(parse_line, lines)):
        groups.setdefault((rec["method"], rec["path"].split("?")[0]), []).append(rec)
    out = {}
    for key, recs in groups.items():
        ms = sorted(r["ms"] for r in recs)
        n = len(ms)
        out[key] = {"count": n, "avg_ms": round(sum(ms) / n, 2), "p50_ms": ms[(n - 1) // 2],
                    "error_rate": round(sum(r["status"] >= 500 for r in recs) / n, 4)}
    return out
