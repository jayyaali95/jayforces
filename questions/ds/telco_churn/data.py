import numpy as np
import pandas as pd

from dsgen import bernoulli, cat, eff, flag, sigmoid

TARGET, TASK, METRIC, SCORES = "churned", "binary", "auc", (0.78, 0.82, 0.845)
KINDS = {
    "contract": "cat", "internet_service": "cat", "payment_method": "cat", "plan": "cat", "region": "cat",
    "acquisition_channel": "cat", "tenure_months": "num", "monthly_charges": "money", "total_charges": "money",
    "support_calls_90d": "numtxt", "data_gb": "unit:GB", "paperless_billing": "bool", "has_tech_support": "bool",
    "has_multiple_lines": "bool", "is_senior": "bool",
}
SENTINEL = {"support_calls_90d": -1}
MISSING = {"total_charges": 0.08, "data_gb": 0.1, "payment_method": 0.07}


def make(rng, n):
    d = pd.DataFrame({
        "contract": cat(rng, n, dict(month_to_month=5, one_year=2.5, two_year=2.5)),
        "internet_service": cat(rng, n, dict(fiber=4, dsl=3, no_internet=1.5)),
        "payment_method": cat(rng, n, dict(credit_card=3, bank_transfer=3, electronic_check=3, mailed_check=1.5)),
        "plan": cat(rng, n, dict(basic=4, standard=4, premium=2)),
        "region": cat(rng, n, dict(north=2, south=3, east=2.5, west=2.5, central=1.5)),
        "acquisition_channel": cat(rng, n, dict(store=3, online=4, referral=1.5, telemarketing=1.5)),
    })
    d["tenure_months"] = np.where(d.contract == "month_to_month", rng.gamma(1.6, 12, n), rng.gamma(3.5, 14, n)).clip(1, 72).round()
    d["monthly_charges"] = np.round(20 + eff(d.plan, dict(basic=0, standard=20, premium=45)) + eff(d.internet_service, dict(fiber=25, dsl=8, no_internet=-12)) + rng.normal(0, 6, n), 2).clip(15)
    d["total_charges"] = np.round(d.tenure_months * d.monthly_charges * rng.uniform(.9, 1.05, n), 2)
    d["support_calls_90d"] = rng.poisson(1.2, n).astype(float)
    d["data_gb"] = np.round(np.where(d.internet_service == "no_internet", 0, rng.gamma(2.5, 40, n)))
    d["paperless_billing"] = flag(rng, n, .6)
    d["has_tech_support"] = flag(rng, n, .3)
    d["has_multiple_lines"] = flag(rng, n, .4)
    d["is_senior"] = flag(rng, n, .16)
    z = -.4 - .045 * d.tenure_months + .012 * (d.monthly_charges - 60) + .22 * d.support_calls_90d.clip(0, 6) - .8 * d.has_tech_support + .35 * d.paperless_billing + .3 * d.is_senior
    z += eff(d.contract, dict(month_to_month=.9, one_year=-.2, two_year=-1.0)) + eff(d.payment_method, dict(credit_card=-.2, bank_transfer=-.15, electronic_check=.6, mailed_check=0))
    z += eff(d.internet_service, dict(fiber=.4, dsl=-.1, no_internet=-.6)) + eff(d.acquisition_channel, dict(store=-.1, online=.1, referral=-.4, telemarketing=.3))
    d[TARGET] = bernoulli(rng, z, 0.27, 1.3)
    return d
