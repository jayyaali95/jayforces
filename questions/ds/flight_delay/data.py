import numpy as np
import pandas as pd

from dsgen import bernoulli, cat, eff, flag, sigmoid

TARGET, TASK, METRIC, SCORES = "arr_delayed", "binary", "auc", (0.65, 0.71, 0.74)
KINDS = {
    "airline": "cat", "origin": "cat", "dest": "cat", "aircraft": "cat", "day_of_week": "cat", "dep_block": "cat",
    "season": "cat", "distance_miles": "unit:mi", "scheduled_minutes": "num", "wind_speed_kt": "num",
    "visibility_miles": "numtxt", "prior_leg_delay_min": "numtxt", "seats_sold_pct": "pct", "is_holiday_period": "bool",
    "is_codeshare": "bool",
}
SENTINEL = {"prior_leg_delay_min": -999}
MISSING = {"visibility_miles": 0.1, "prior_leg_delay_min": 0.1, "aircraft": 0.1, "seats_sold_pct": 0.08}
_HUBS = ["atl", "ord", "dfw", "den", "jfk", "sfo", "sea", "bos", "mia", "lax"]


def make(rng, n):
    o = rng.choice(_HUBS, n, p=np.array([3, 3, 2.5, 2, 2.5, 2, 1.2, 1.5, 1.5, 2.5]) / 21.7)
    dest = np.array([_HUBS[(_HUBS.index(h) + rng.integers(1, 10)) % 10] for h in o])
    d = pd.DataFrame({
        "airline": cat(rng, n, dict(skyline=4, bluejet=3, aerowest=2, nimbus=2, coastal=1, orion=1.5)),
        "origin": o, "dest": dest,
        "aircraft": cat(rng, n, dict(a320=4, b737=5, e175=2, a321=2, b787=1, crj900=1)),
        "day_of_week": cat(rng, n, dict(mon=1, tue=1, wed=1, thu=1, fri=1.2, sat=.8, sun=1)),
        "dep_block": cat(rng, n, dict(early_morning=2, morning=3.5, afternoon=3.5, evening=3, red_eye=.5)),
        "season": cat(rng, n, dict(winter=2, spring=2, summer=2.5, fall=2)),
    })
    d["distance_miles"] = np.clip(rng.gamma(3, 330, n), 120, 2700).round()
    d["scheduled_minutes"] = np.round(45 + d.distance_miles / 8 + rng.normal(0, 6, n))
    d["wind_speed_kt"] = np.round(np.clip(rng.gamma(3, 4, n), 0, 50), 1)
    d["visibility_miles"] = np.round(np.clip(rng.normal(8.5, 2.5, n), .25, 10), 1)
    d["seats_sold_pct"] = np.round(np.clip(rng.normal(82, 12, n), 30, 100), 1)
    d["is_holiday_period"] = flag(rng, n, .12)
    d["is_codeshare"] = flag(rng, n, .2)
    late = rng.random(n) < sigmoid(-1.3 + eff(d.dep_block, dict(early_morning=-.8, morning=-.3, afternoon=.3, evening=.7, red_eye=.1)))
    d["prior_leg_delay_min"] = np.where(late, rng.gamma(2, 14, n), np.maximum(rng.normal(-3, 4, n), -15)).round()
    z = -1.3 + .028 * d.prior_leg_delay_min.clip(-15, 120) + .035 * (d.wind_speed_kt - 12) - .25 * (d.visibility_miles - 8.5).clip(-9, 0) + .018 * (d.seats_sold_pct - 82) + .5 * d.is_holiday_period
    z += eff(d.airline, dict(skyline=0, bluejet=-.2, aerowest=.4, nimbus=.1, coastal=.5, orion=-.3)) + eff(d.origin, dict(atl=.1, ord=.4, dfw=.1, den=0, jfk=.5, sfo=.35, sea=-.1, bos=.3, mia=.2, lax=0))
    z += eff(d.season, dict(winter=.4, spring=0, summer=.25, fall=-.25)) + eff(d.day_of_week, dict(mon=0, tue=-.2, wed=-.2, thu=.1, fri=.3, sat=-.1, sun=.15)) + eff(d.aircraft, dict(a320=0, b737=0, e175=.15, a321=.1, b787=-.2, crj900=.3))
    d[TARGET] = bernoulli(rng, z, 0.28, 1.9)
    return d
