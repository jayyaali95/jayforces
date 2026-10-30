import csv
import io
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

REQUIRED = ("trip_id", "city", "fare", "currency")


def _check(row, cols, seen):
    if len(row) != len(cols):
        return "columns", None
    r = dict(zip(cols, row))
    city = r["city"].strip()
    if not city:
        return "city", None
    try:
        fare = Decimal(r["fare"].strip())
        if not fare.is_finite() or fare < 0:
            raise InvalidOperation
    except InvalidOperation:
        return "fare", None
    if r["currency"].strip() != "USD":
        return "currency", None
    if r["trip_id"] in seen:
        return "duplicate", None
    return None, (r["trip_id"], city, int((fare * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)))


def report(csv_text):
    """Return totals, per-line errors and the top city."""
    rows = list(csv.reader(io.StringIO(csv_text)))
    if not rows:
        raise ValueError("empty csv")
    cols = [c.strip() for c in rows[0]]
    if any(c not in cols for c in REQUIRED):
        raise ValueError("missing required columns")
    totals, errors, seen = {}, [], set()
    for line, row in enumerate(rows[1:], start=2):
        if not row:
            continue
        err, ok = _check(row, cols, seen)
        if err:
            errors.append((line, err))
            continue
        trip, city, cents = ok
        seen.add(trip)
        totals[city] = totals.get(city, 0) + cents
    top = min(totals, key=lambda c: (-totals[c], c)) if totals else None
    return {"totals": totals, "errors": errors, "top_city": top}


def revenue_by_city(csv_text):
    """Return {city: total cents} over valid rows."""
    return report(csv_text)["totals"]
