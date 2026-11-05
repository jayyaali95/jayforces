import numpy as np
import pandas as pd

from dsgen import cat, eff, flag, sigmoid

TARGET, TASK, METRIC, SCORES = "delivery_minutes", "regression", "r2", (0.6, 0.75, 0.8)
KINDS = {
    "cuisine": "cat", "vehicle": "cat", "weather": "cat", "traffic": "cat", "zone": "cat", "day_part": "cat",
    "distance_m": "unit:m", "n_items": "num", "order_value": "money", "courier_rating": "numtxt",
    "prep_time_min": "unit:min", "temp_c": "num", "is_weekend": "bool", "is_first_order": "bool", "is_scheduled": "bool",
}
SENTINEL = {"courier_rating": 0}
MISSING = {"distance_m": 0.04, "prep_time_min": 0.12, "weather": 0.08, "courier_rating": 0.1}


def make(rng, n):
    d = pd.DataFrame({
        "cuisine": cat(rng, n, dict(pizza=4, sushi=2, burgers=4, indian=2, thai=2, bakery=1, healthy=2)),
        "vehicle": cat(rng, n, dict(bike=3, scooter=5, car=2)),
        "weather": cat(rng, n, dict(clear=6, cloudy=3, rain=2, heavy_rain=.6, snow=.4)),
        "traffic": cat(rng, n, dict(low=3, medium=4, high=2, jam=.7)),
        "zone": cat(rng, n, dict(z_north=2, z_south=2, z_east=2, z_west=2, z_center=3, z_harbor=1, z_airport=.6, z_campus=1.4)),
        "day_part": cat(rng, n, dict(breakfast=1, lunch=4, dinner=5, late_night=1.2)),
    })
    d["distance_m"] = np.clip(rng.gamma(2.6, 1100, n), 200, 12000).round()
    d["n_items"] = (rng.poisson(2.2, n) + 1).astype(float)
    d["order_value"] = np.round(d["n_items"] * rng.gamma(4, 4.5, n), 2)
    d["courier_rating"] = np.round(np.clip(rng.normal(4.6, .35, n), 1, 5), 1)
    d["prep_time_min"] = np.round(np.clip(rng.gamma(4, 3.5, n) * eff(d.cuisine, dict(pizza=1.1, sushi=1.2, burgers=.8, indian=1.2, thai=1, bakery=.5, healthy=.7)), 2, 60))
    d["temp_c"] = np.round(rng.normal(14, 9, n), 1)
    d["is_weekend"] = flag(rng, n, .3)
    d["is_first_order"] = flag(rng, n, .1)
    d["is_scheduled"] = flag(rng, n, .08)
    speed = eff(d.vehicle, dict(bike=14, scooter=22, car=19)) * eff(d.traffic, dict(low=1.15, medium=1, high=.75, jam=.5)) * eff(d.weather, dict(clear=1, cloudy=1, rain=.85, heavy_rain=.65, snow=.55))
    t = 6 + d.prep_time_min * .9 + d.distance_m / 1000 / speed * 60 + 1.5 * d.n_items + 3 * d.is_weekend * (d.day_part == "dinner") + 2.5 * d.is_first_order
    t += eff(d.day_part, dict(breakfast=-2, lunch=2, dinner=4, late_night=-1)) + 1.5 * (d.zone == "z_airport") - 2 * (d.courier_rating - 4.6)
    d[TARGET] = np.round(t + rng.normal(0, 2.5, n), 1).clip(8)
    return d
