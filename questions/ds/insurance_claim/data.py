import numpy as np
import pandas as pd

from dsgen import cat, eff, flag, sigmoid

TARGET, TASK, METRIC, SCORES = "claim_cost", "regression", "r2", (0.45, 0.6, 0.68)
KINDS = {
    "vehicle_class": "cat", "usage": "cat", "region": "cat", "coverage": "cat", "payment_plan": "cat", "occupation": "cat",
    "driver_age": "numtxt", "vehicle_age_years": "num", "annual_mileage": "unit:mi", "prior_claims_3y": "num",
    "premium_annual": "money", "credit_score": "numtxt", "has_telematics": "bool", "multi_policy": "bool", "garage_parked": "bool",
}
SENTINEL = {"driver_age": -1, "credit_score": 0}
MISSING = {"credit_score": 0.12, "annual_mileage": 0.1, "occupation": 0.1, "premium_annual": 0.03}


def make(rng, n):
    d = pd.DataFrame({
        "vehicle_class": cat(rng, n, dict(economy=3, sedan=4, suv=4, sports=1, luxury=1, truck=2)),
        "usage": cat(rng, n, dict(commute=6, pleasure=3, business=1.5)),
        "region": cat(rng, n, dict(urban=4, suburban=4, rural=2)),
        "coverage": cat(rng, n, dict(basic=3, standard=5, premium=2)),
        "payment_plan": cat(rng, n, dict(monthly=6, quarterly=1, annual=3)),
        "occupation": cat(rng, n, dict(professional=4, trades=2, student=1.5, retired=2, service_work=2.5)),
    })
    d["driver_age"] = np.clip(rng.normal(42, 14, n), 18, 85).round()
    d["vehicle_age_years"] = np.clip(rng.gamma(2.5, 2.5, n), 0, 25).round()
    d["annual_mileage"] = np.clip(rng.normal(11000, 4500, n) * eff(d.usage, dict(commute=1.1, pleasure=.7, business=1.5)), 1000, 40000).round()
    d["prior_claims_3y"] = rng.poisson(.35, n).clip(0, 5).astype(float)
    d["credit_score"] = np.clip(rng.normal(680, 70, n), 400, 850).round()
    d["has_telematics"] = flag(rng, n, .25)
    d["multi_policy"] = flag(rng, n, .35)
    d["garage_parked"] = flag(rng, n, .5)
    base = 2500 * eff(d.vehicle_class, dict(economy=.8, sedan=1, suv=1.15, sports=1.6, luxury=1.8, truck=1.2)) * eff(d.region, dict(urban=1.25, suburban=1, rural=.85))
    base *= eff(d.coverage, dict(basic=.7, standard=1, premium=1.4)) * (1 + .12 * d.prior_claims_3y) * (1 + .00002 * (d.annual_mileage - 11000))
    base *= np.where(d.driver_age < 25, 1.4, np.where(d.driver_age > 70, 1.15, 1)) * np.where(d.has_telematics, .9, 1) * np.where(d.garage_parked, .93, 1) * (1 - .0006 * (d.credit_score - 680))
    d["premium_annual"] = np.round(base * .45 * rng.lognormal(0, .08, n), 2)
    d[TARGET] = np.round(base * rng.lognormal(0, .2, n), -1)
    return d
