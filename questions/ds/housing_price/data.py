import numpy as np
import pandas as pd

from dsgen import cat, eff, flag

TARGET, TASK, METRIC, SCORES = "sale_price", "regression", "r2", (0.7, 0.85, 0.89)
KINDS = {
    "neighborhood": "cat", "property_type": "cat", "heating": "cat", "condition": "cat", "parking": "cat",
    "listing_source": "cat", "sqft": "unit:sqft", "bedrooms": "num", "bathrooms": "num", "year_built": "numtxt",
    "hoa_fee": "money", "distance_to_center_km": "num", "has_pool": "bool", "renovated": "bool",
}
SENTINEL = {"year_built": 0}
MISSING = {"sqft": 0.03, "hoa_fee": 0.1, "year_built": 0.08}


def make(rng, n):
    d = pd.DataFrame({
        "neighborhood": cat(rng, n, dict(downtown=2, midtown=3, riverside=2, uptown=2, old_town=2, harbor=1, suburbs=4, hillside=1)),
        "property_type": cat(rng, n, dict(house=5, condo=4, townhouse=2, duplex=1)),
        "heating": cat(rng, n, dict(gas=5, electric=3, oil=1, heat_pump=2)),
        "condition": cat(rng, n, dict(poor=1, fair=3, good=5, excellent=2)),
        "parking": cat(rng, n, dict(garage=4, driveway=3, street=3, no_parking=1)),
        "listing_source": cat(rng, n, dict(agent=8, owner=2, bank=1, auction=1)),
    })
    d["sqft"] = np.clip(rng.normal(1700, 650, n), 450, 5000).round()
    d["bedrooms"] = np.clip(np.round(d.sqft / 600 + rng.normal(0, 0.7, n)), 1, 7)
    d["bathrooms"] = np.clip(np.round((d.bedrooms * 0.7 + rng.normal(0, 0.5, n)) * 2) / 2, 1, 5)
    d["year_built"] = rng.integers(1930, 2023, n).astype(float)
    d["hoa_fee"] = np.where(d.property_type.isin(["condo", "townhouse"]), rng.gamma(4, 90, n), 0.0)
    d["distance_to_center_km"] = np.round(rng.gamma(2.5, 4, n), 1)
    d["has_pool"] = flag(rng, n, 0.12)
    d["renovated"] = flag(rng, n, 0.25)
    per_sqft = 210 * np.exp(eff(d.neighborhood, dict(downtown=.45, midtown=.3, riverside=.35, uptown=.25, old_town=.1, harbor=.4, suburbs=-.1, hillside=.2)))
    per_sqft *= np.exp(eff(d.property_type, dict(house=.1, condo=0, townhouse=-.03, duplex=-.08)))
    per_sqft *= np.exp(eff(d.condition, dict(poor=-.3, fair=-.1, good=0, excellent=.15)))
    price = d.sqft * per_sqft * (1 + 0.06 * d.has_pool + 0.08 * d.renovated + 0.01 * d.bathrooms)
    price *= np.exp(-0.012 * d.distance_to_center_km + 0.0015 * (d.year_built - 1980))
    d[TARGET] = (price * np.exp(rng.normal(0, 0.07, n))).round(-2)
    return d
