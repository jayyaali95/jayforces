from decimal import ROUND_HALF_UP, Decimal

RATES = {"standard": {"base": 250, "per_mile": 150, "per_min": 30, "minimum": 700},
         "xl": {"base": 400, "per_mile": 250, "per_min": 45, "minimum": 1100}}


def _round(x):
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def fare(miles, minutes, ride_type="standard", surge=1.0):
    """Return the fare in integer cents."""
    if miles < 0 or minutes < 0 or surge < 1 or ride_type not in RATES:
        raise ValueError("bad fare input")
    r = RATES[ride_type]
    raw = Decimal(r["base"]) + Decimal(r["per_mile"]) * Decimal(str(miles)) + Decimal(r["per_min"]) * Decimal(str(minutes))
    return max(_round(raw * Decimal(str(surge))), r["minimum"])


def apply_promo(cents, promo):
    """Return cents after the promo, never below zero."""
    if promo is None:
        return cents
    kind = promo.get("type") if isinstance(promo, dict) else None
    if kind == "percent":
        off = _round(Decimal(cents) * Decimal(str(promo["value"])) / 100)
        if promo.get("cap") is not None:
            off = min(off, promo["cap"])
    elif kind == "flat":
        off = promo["value"]
    else:
        raise ValueError("unknown promo")
    return max(cents - off, 0)
