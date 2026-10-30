def _by_id(records):
    return {r["id"]: r for r in records}


def reconcile(internal, bank):
    """Compare two ledgers by id."""
    a, b = _by_id(internal), _by_id(bank)
    both = sorted(a.keys() & b.keys())
    same = lambda i: a[i]["amount"] == b[i]["amount"] and a[i]["driver"] == b[i]["driver"]
    return {"matched": [i for i in both if same(i)],
            "mismatched": [(i, a[i]["amount"], b[i]["amount"]) for i in both if not same(i)],
            "missing_in_bank": sorted(a.keys() - b.keys()),
            "missing_in_internal": sorted(b.keys() - a.keys())}


def fuzzy_match(internal, bank, window=60, tolerance=0):
    """Greedy pairing by driver, amount tolerance and time window."""
    unused = {r["id"]: r for r in bank}
    pairs, lonely = [], []
    for r in sorted(internal, key=lambda r: (r["ts"], r["id"])):
        cands = [c for c in unused.values() if c["driver"] == r["driver"]
                 and abs(c["amount"] - r["amount"]) <= tolerance and abs(c["ts"] - r["ts"]) <= window]
        if not cands:
            lonely.append(r["id"])
            continue
        best = min(cands, key=lambda c: (abs(c["ts"] - r["ts"]), abs(c["amount"] - r["amount"]), c["id"]))
        del unused[best["id"]]
        pairs.append((r["id"], best["id"]))
    return {"pairs": pairs, "unmatched_internal": sorted(lonely), "unmatched_bank": sorted(unused)}
