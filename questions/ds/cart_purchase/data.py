import numpy as np
import pandas as pd

from dsgen import bernoulli, cat, eff, flag, sigmoid

TARGET, TASK, METRIC, SCORES = "purchased", "binary", "auc", (0.7, 0.74, 0.76)
KINDS = {
    "traffic_source": "cat", "device": "cat", "country": "cat", "browser": "cat", "landing_category": "cat",
    "customer_segment": "cat", "pages_viewed": "num", "session_minutes": "unit:min", "cart_value": "money",
    "items_in_cart": "num", "prior_orders": "numtxt", "is_logged_in": "bool", "has_coupon": "bool", "is_weekend": "bool",
}
SENTINEL = {"prior_orders": -1}
MISSING = {"cart_value": 0.1, "session_minutes": 0.07, "browser": 0.12}


def make(rng, n):
    d = pd.DataFrame({
        "traffic_source": cat(rng, n, dict(organic=5, paid_search=4, social=3, email=2, direct=3, affiliate=1)),
        "device": cat(rng, n, dict(mobile=6, desktop=4, tablet=1)),
        "country": cat(rng, n, dict(us=6, uk=2, de=2, fr=1.5, india=3, brazil=1.5, canada=1.5)),
        "browser": cat(rng, n, dict(chrome=6, safari=3, firefox=1, edge=1, other_browser=.5)),
        "landing_category": cat(rng, n, dict(electronics=3, fashion=4, home=2, beauty=2, sports=1.5)),
        "customer_segment": cat(rng, n, dict(new=5, returning=3, loyal=1)),
    })
    d["pages_viewed"] = (rng.poisson(5, n) + 1).astype(float)
    d["session_minutes"] = np.round(d.pages_viewed * rng.gamma(2, .9, n) + rng.gamma(1.5, 1, n))
    d["items_in_cart"] = np.where(flag(rng, n, .45), rng.integers(1, 6, n), 0).astype(float)
    d["cart_value"] = np.round(d.items_in_cart * rng.gamma(3, 22, n), 2)
    d["prior_orders"] = np.where(d.customer_segment == "new", 0, rng.poisson(np.where(d.customer_segment == "loyal", 9, 3))).astype(float)
    d["is_logged_in"] = flag(rng, n, .4) | (d.customer_segment == "loyal")
    d["has_coupon"] = flag(rng, n, .15)
    d["is_weekend"] = flag(rng, n, .3)
    z = -3.4 + 1.1 * (d.items_in_cart > 0) + .12 * d.pages_viewed.clip(0, 14) + .6 * d.is_logged_in + .5 * d.has_coupon - .003 * d.cart_value.clip(0, 300)
    z += .12 * d.prior_orders.clip(0, 10) + .01 * d.session_minutes.clip(0, 40)
    z += eff(d.traffic_source, dict(organic=0, paid_search=-.1, social=-.5, email=.7, direct=.4, affiliate=-.2)) + eff(d.device, dict(mobile=-.3, desktop=.3, tablet=0))
    z += eff(d.customer_segment, dict(new=-.3, returning=.2, loyal=.4)) + eff(d.landing_category, dict(electronics=-.1, fashion=0, home=.1, beauty=.2, sports=0))
    d[TARGET] = bernoulli(rng, z, 0.15, 1.5)
    return d
