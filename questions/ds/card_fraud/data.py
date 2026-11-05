import numpy as np
import pandas as pd

from dsgen import bernoulli, cat, eff, flag, sigmoid

TARGET, TASK, METRIC, SCORES = "is_fraud", "binary", "ap", (0.2, 0.27, 0.3)
N_TRAIN, N_TEST = 4000, 3000
KINDS = {
    "merchant_category": "cat", "card_type": "cat", "channel": "cat", "merchant_country": "cat", "device_os": "cat",
    "card_network": "cat", "issuer_tier": "cat", "amount": "money", "acct_age_days": "numtxt", "txn_count_24h": "num",
    "avg_amount_30d": "money", "dist_from_home_km": "unit:km", "is_card_present": "bool", "is_new_merchant": "bool",
    "billing_zip_match": "bool",
}
SENTINEL = {"acct_age_days": -1}
MISSING = {"amount": 0.02, "is_card_present": 0.1, "dist_from_home_km": 0.12, "device_os": 0.15}


def make(rng, n):
    d = pd.DataFrame({
        "merchant_category": cat(rng, n, dict(grocery=6, fuel=4, restaurant=5, electronics=2, travel=2, online_services=3, jewelry=.5, pharmacy=2, entertainment=2, crypto_exchange=.4)),
        "card_type": cat(rng, n, dict(debit=6, credit=5, prepaid=1, virtual=1)),
        "channel": cat(rng, n, dict(pos=5, ecommerce=5, atm=1, mobile_wallet=2, contactless=3)),
        "merchant_country": cat(rng, n, dict(home=20, neighbor=2, foreign_low=1.5, foreign_high=.6)),
        "device_os": cat(rng, n, dict(ios=4, android=5, windows=2, macos=1, linux=.3, other_os=.3)),
        "card_network": cat(rng, n, dict(visa=6, mastercard=4, amex=1, discover=1)),
        "issuer_tier": cat(rng, n, dict(standard=6, gold=3, platinum=1)),
    })
    d["avg_amount_30d"] = np.round(rng.gamma(3, 25, n) + 5, 2)
    d["amount"] = np.round(d.avg_amount_30d * rng.lognormal(0, .7, n) * np.where(d.merchant_category.isin(["electronics", "jewelry", "travel"]), 3, 1), 2)
    d["acct_age_days"] = rng.integers(2, 3000, n).astype(float)
    d["txn_count_24h"] = rng.poisson(1.5, n).astype(float)
    d["dist_from_home_km"] = np.round(np.where(d.merchant_country == "home", rng.gamma(1.5, 12, n), rng.gamma(4, 400, n)))
    d["is_card_present"] = d.channel.isin(["pos", "atm", "contactless"]) & flag(rng, n, .97)
    d["is_new_merchant"] = flag(rng, n, .3)
    d["billing_zip_match"] = flag(rng, n, .9)
    z = -5.2 + 1.2 * np.log1p(d.amount / d.avg_amount_30d).clip(0, 4) + .45 * (d.txn_count_24h >= 5) + .9 * d.is_new_merchant
    z += eff(d.merchant_category, dict(grocery=-.5, fuel=-.2, restaurant=-.4, electronics=.8, travel=.5, online_services=.6, jewelry=1.1, pharmacy=-.4, entertainment=.1, crypto_exchange=1.8))
    z += eff(d.channel, dict(pos=-.3, ecommerce=.8, atm=.4, mobile_wallet=0, contactless=-.4)) + eff(d.merchant_country, dict(home=0, neighbor=.5, foreign_low=.9, foreign_high=1.8))
    z += eff(d.card_type, dict(debit=0, credit=-.1, prepaid=.9, virtual=.7)) - 1.0 * d.is_card_present - .8 * d.billing_zip_match + 1.0 * (d.acct_age_days < 30)
    d[TARGET] = bernoulli(rng, z, 0.05, 1.5)
    return d
