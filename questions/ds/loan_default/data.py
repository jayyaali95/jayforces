import numpy as np
import pandas as pd

from dsgen import bernoulli, cat, eff, flag, sigmoid

TARGET, TASK, METRIC, SCORES = "defaulted", "binary", "auc", (0.62, 0.67, 0.69)
KINDS = {
    "purpose": "cat", "home_ownership": "cat", "emp_length": "cat", "verification": "cat", "term": "cat", "region": "cat",
    "application_type": "cat", "loan_amount": "money", "annual_income": "money", "dti": "num", "interest_rate": "pct",
    "revolving_util": "pct", "open_accounts": "numtxt", "credit_history_years": "numtxt", "has_delinq_2y": "bool",
}
SENTINEL = {"credit_history_years": -1}
MISSING = {"annual_income": 0.08, "emp_length": 0.12, "revolving_util": 0.1, "dti": 0.06}


def make(rng, n):
    d = pd.DataFrame({
        "purpose": cat(rng, n, dict(debt_consolidation=8, credit_card=4, home_improvement=2, major_purchase=1, medical=1, small_business=1, car=1.5, vacation=.5)),
        "home_ownership": cat(rng, n, dict(rent=4, own=1, mortgage=5)),
        "emp_length": cat(rng, n, dict(lt_1y=1, y1_3=3, y4_6=2.5, y7_9=1.5, y10_plus=4)),
        "verification": cat(rng, n, dict(verified=3, source_verified=3, not_verified=3)),
        "term": cat(rng, n, dict(m36=7, m60=3)),
        "region": cat(rng, n, dict(northeast=2, south=4, midwest=2, west=3)),
        "application_type": cat(rng, n, dict(individual=9, joint=1)),
    })
    d["annual_income"] = np.round(rng.lognormal(11.0, .5, n), 2)
    d["loan_amount"] = np.round(np.clip(d.annual_income * rng.uniform(.08, .45, n), 1000, 40000), 2)
    d["dti"] = np.round(np.clip(rng.normal(18, 8, n), 0, 45), 1)
    d["revolving_util"] = np.round(np.clip(rng.normal(48, 24, n), 0, 100), 1)
    d["open_accounts"] = np.clip(rng.poisson(10, n), 1, 40).astype(float)
    d["credit_history_years"] = np.clip(rng.gamma(4, 4, n), 1, 45).round()
    d["has_delinq_2y"] = flag(rng, n, .18)
    risk = .035 * (d.dti - 18) + .012 * (d.revolving_util - 48) + .7 * d.has_delinq_2y - .03 * d.credit_history_years - .5 * np.log(d.annual_income / 60000) + .00002 * d.loan_amount
    risk += eff(d.term, dict(m36=0, m60=.5)) + eff(d.purpose, dict(debt_consolidation=0, credit_card=-.1, home_improvement=-.2, major_purchase=-.1, medical=.2, small_business=.6, car=-.2, vacation=.3))
    risk += eff(d.verification, dict(verified=.15, source_verified=.05, not_verified=-.1)) + eff(d.emp_length, dict(lt_1y=.3, y1_3=.15, y4_6=0, y7_9=-.1, y10_plus=-.25)) + eff(d.home_ownership, dict(rent=.2, own=0, mortgage=-.15))
    d["interest_rate"] = np.round(np.clip(11 + 3.2 * risk + rng.normal(0, 1.6, n), 5, 30), 1)
    d[TARGET] = bernoulli(rng, risk, 0.15, 2.0)
    return d
