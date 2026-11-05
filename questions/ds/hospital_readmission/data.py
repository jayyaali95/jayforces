import numpy as np
import pandas as pd

from dsgen import bernoulli, cat, eff, flag, sigmoid

TARGET, TASK, METRIC, SCORES = "readmitted_30d", "binary", "auc", (0.62, 0.68, 0.72)
N_TRAIN, N_TEST = 3500, 2500
KINDS = {
    "admission_type": "cat", "diagnosis_group": "cat", "discharge_to": "cat", "insurance": "cat", "age_band": "cat",
    "a1c_result": "cat", "specialty": "cat", "days_in_hospital": "unit:days", "num_lab_procedures": "num",
    "num_medications": "numtxt", "prior_inpatient_12m": "numtxt", "creatinine": "numtxt", "followup_scheduled": "bool",
    "on_insulin": "bool", "is_icu_stay": "bool",
}
SENTINEL = {"creatinine": -1, "prior_inpatient_12m": 99}
MISSING = {"a1c_result": 0.15, "creatinine": 0.12, "specialty": 0.1, "days_in_hospital": 0.02}


def make(rng, n):
    d = pd.DataFrame({
        "admission_type": cat(rng, n, dict(emergency=5, urgent=2, elective=3)),
        "diagnosis_group": cat(rng, n, dict(circulatory=3, respiratory=2, diabetes=2, injury=1.5, digestive=1.5, neoplasm=1, other_dx=2)),
        "discharge_to": cat(rng, n, dict(home=6, home_health=1.5, skilled_nursing=2, rehab=1, left_against_advice=.3)),
        "insurance": cat(rng, n, dict(medicare=4, medicaid=2, private=3.5, self_pay=.8)),
        "age_band": cat(rng, n, dict(a18_39=1.5, a40_59=3, a60_74=3.5, a75_plus=2.5)),
        "a1c_result": cat(rng, n, dict(not_tested=6, normal=1.5, high=1.5, very_high=1)),
        "specialty": cat(rng, n, dict(cardiology=2, internal_medicine=4, surgery=2, emergency_med=2, orthopedics=1, family_practice=2)),
    })
    d["days_in_hospital"] = np.clip(rng.gamma(2, 2, n) + 1, 1, 14).round()
    d["num_lab_procedures"] = np.clip(rng.normal(42, 16, n), 1, 120).round()
    d["num_medications"] = np.clip(rng.normal(15, 7, n), 1, 60).round()
    d["prior_inpatient_12m"] = rng.poisson(.6, n).clip(0, 8).astype(float)
    d["creatinine"] = np.round(np.clip(rng.lognormal(0, .35, n), .4, 6), 2)
    d["followup_scheduled"] = flag(rng, n, .55)
    d["on_insulin"] = flag(rng, n, .25) | (d.diagnosis_group == "diabetes") & flag(rng, n, .5)
    d["is_icu_stay"] = flag(rng, n, .1)
    z = -2.6 + .32 * d.prior_inpatient_12m + .06 * d.days_in_hospital + .012 * d.num_medications + .5 * (d.creatinine > 1.5) - .5 * d.followup_scheduled + .3 * d.on_insulin + .25 * d.is_icu_stay
    z += eff(d.discharge_to, dict(home=0, home_health=.3, skilled_nursing=.5, rehab=.2, left_against_advice=1.1)) + eff(d.admission_type, dict(emergency=.3, urgent=.1, elective=-.4))
    z += eff(d.diagnosis_group, dict(circulatory=.3, respiratory=.25, diabetes=.35, injury=-.2, digestive=0, neoplasm=.2, other_dx=-.1)) + eff(d.age_band, dict(a18_39=-.4, a40_59=-.1, a60_74=.1, a75_plus=.35))
    z += eff(d.a1c_result, dict(not_tested=0, normal=-.1, high=.2, very_high=.45)) + eff(d.insurance, dict(medicare=.15, medicaid=.2, private=-.15, self_pay=.1))
    d[TARGET] = bernoulli(rng, z, 0.15, 1.9)
    return d
