import numpy as np
import pandas as pd

from dsgen import bernoulli, cat, eff, flag, sigmoid

TARGET, TASK, METRIC, SCORES = "clicked", "binary", "auc", (0.65, 0.72, 0.75)
N_TRAIN, N_TEST = 4000, 3000
KINDS = {
    "publisher": "cat", "ad_format": "cat", "device_type": "cat", "os": "cat", "country": "cat", "vertical": "cat",
    "placement": "cat", "connection": "cat", "user_age": "numtxt", "bid_cpm": "money", "past_ctr": "pct",
    "impressions_7d": "num", "days_since_install": "numtxt", "is_returning_user": "bool", "is_logged_in": "bool",
}
SENTINEL = {"user_age": 0, "days_since_install": 9999}
MISSING = {"user_age": 0.15, "os": 0.08, "past_ctr": 0.12, "connection": 0.1}
_PUB = np.random.default_rng(11).normal(0, .55, 25)
_PUB_P = np.random.default_rng(12).dirichlet(np.ones(25) * .6)


def make(rng, n):
    pubs = [f"pub_{i:02d}" for i in range(25)]
    d = pd.DataFrame({
        "publisher": rng.choice(pubs, n, p=_PUB_P),
        "ad_format": cat(rng, n, dict(banner=5, native=3, video=2, interstitial=1)),
        "device_type": cat(rng, n, dict(phone=7, tablet=1, desktop=3, tv=.4)),
        "os": cat(rng, n, dict(ios=4, android=5, windows=2, macos=1, other_os=.5)),
        "country": cat(rng, n, dict(us=6, uk=2, de=1.5, fr=1.5, india=3, brazil=2, japan=1, canada=1, mexico=1, spain=1, italy=1, australia=1)),
        "vertical": cat(rng, n, dict(finance=2, gaming=3, travel=2, retail=4, auto=1.5, education=1, health=1.5)),
        "placement": cat(rng, n, dict(feed=4, sidebar=2, header=2, footer=1, in_article=2)),
        "connection": cat(rng, n, dict(wifi=5, lte=3, g5=2, g3=.4)),
    })
    d["user_age"] = np.clip(rng.normal(34, 11, n), 16, 80).round()
    d["bid_cpm"] = np.round(rng.gamma(3, 1.1, n) * eff(d.vertical, dict(finance=2, gaming=1, travel=1.3, retail=1, auto=1.5, education=.8, health=1.2)), 2)
    d["impressions_7d"] = rng.poisson(14, n).astype(float)
    d["is_returning_user"] = flag(rng, n, .5)
    d["is_logged_in"] = flag(rng, n, .35)
    d["days_since_install"] = np.where(d.is_returning_user, rng.integers(1, 700, n), rng.integers(0, 5, n)).astype(float)
    d["past_ctr"] = np.round(np.clip(rng.beta(1.2, 40, n) * 100 * (1 + .6 * d.is_returning_user), 0, 40), 1)
    z = -4.1 + .09 * d.past_ctr + .35 * d.is_returning_user + .25 * d.is_logged_in - .012 * (d.user_age - 34) - .02 * d.impressions_7d.clip(0, 40) + .1 * np.log1p(d.bid_cpm)
    z += eff(d.publisher, dict(zip(pubs, _PUB))) + eff(d.ad_format, dict(banner=-.3, native=.35, video=.2, interstitial=.5)) + eff(d.placement, dict(feed=.3, sidebar=-.3, header=0, footer=-.5, in_article=.2))
    z += eff(d.device_type, dict(phone=.1, tablet=0, desktop=-.2, tv=-.5)) + eff(d.vertical, dict(finance=-.2, gaming=.4, travel=0, retail=.1, auto=-.1, education=0, health=.05)) + eff(d.connection, dict(wifi=0, lte=.05, g5=.1, g3=-.4))
    z += .5 * ((d.vertical == "gaming") & (d.device_type == "phone")) + .4 * ((d.ad_format == "video") & (d.connection != "g3"))
    d[TARGET] = bernoulli(rng, z, 0.05, 1.8)
    return d
