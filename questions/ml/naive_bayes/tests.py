import numpy as np

from check import close, eq

X = np.array([[3, 0, 1], [2, 0, 0], [0, 4, 1], [0, 3, 2], [1, 1, 5]])
Y = np.array(["billing", "billing", "safety", "safety", "app"])


def test_p1_classes(sol):
    eq(sol.MultinomialNB().fit(X, Y).classes_, np.array(["app", "billing", "safety"]))


def test_p1_priors(sol):
    close(sol.MultinomialNB().fit(X, Y).class_log_prior_, np.log([0.2, 0.4, 0.4]))


def test_p1_feature_probs(sol):
    N = np.array([[1, 1, 5], [5, 0, 1], [0, 7, 3]], dtype=float)
    close(sol.MultinomialNB().fit(X, Y).feature_log_prob_, np.log((N + 1) / (N.sum(1, keepdims=True) + 3)))


def test_p1_alpha(sol):
    m = sol.MultinomialNB(alpha=0.5).fit(X, Y)
    close(m.feature_log_prob_[1], np.log((np.array([5, 0, 1]) + 0.5) / (6 + 1.5)))


def test_p1_rows_are_distributions(sol):
    close(np.exp(sol.MultinomialNB().fit(X, Y).feature_log_prob_).sum(1), np.ones(3))


def test_p1_predict(sol):
    eq(sol.MultinomialNB().fit(X, Y).predict(np.array([[5, 0, 0], [0, 5, 0], [0, 0, 9]])),
       np.array(["billing", "safety", "app"]))


def test_p1_log_joint(sol):
    m = sol.MultinomialNB().fit(X, Y)
    q = np.array([[1, 2, 3]])
    close(m.predict_log_joint(q), q @ m.feature_log_prob_.T + m.class_log_prior_)


def test_p1_unseen_word_no_inf(sol):
    eq(np.isfinite(sol.MultinomialNB().fit(X, Y).predict_log_joint(np.array([[0, 50, 0]]))).all(), True)


def test_p2_proba_sums(sol):
    close(sol.MultinomialNB().fit(X, Y).predict_proba(X).sum(1), np.ones(5))


def test_p2_proba_stable(sol):
    p = sol.MultinomialNB().fit(X, Y).predict_proba(np.array([[3000, 0, 0]]))
    eq((np.isfinite(p).all(), int(p.argmax())), (True, 1))


def test_p2_proba_matches_exp(sol):
    m = sol.MultinomialNB().fit(X, Y)
    j = np.exp(m.predict_log_joint(X[:1]))
    close(m.predict_proba(X[:1]), j / j.sum())


rng = np.random.default_rng(2)
GX = np.vstack([rng.normal([0, 0], 1, size=(50, 2)), rng.normal([4, 4], 0.5, size=(50, 2))])
GY = np.array([0] * 50 + [1] * 50)


def test_p2_gaussian_params(sol):
    m = sol.GaussianNB().fit(GX, GY)
    close((m.theta_, m.var_), (np.array([GX[:50].mean(0), GX[50:].mean(0)]),
                              np.array([GX[:50].var(0), GX[50:].var(0)]) + 1e-9 * GX.var(0).max()))


def test_p2_gaussian_predict(sol):
    eq((sol.GaussianNB().fit(GX, GY).predict(GX) == GY).mean() > 0.97, True)


def test_p2_gaussian_constant_feature(sol):
    Xc = np.column_stack([GX[:, 0], np.ones(100)])
    eq(np.isin(sol.GaussianNB().fit(Xc, GY).predict(Xc), [0, 1]).all(), True)


def test_p2_gaussian_variance_matters(sol):
    Xv = np.array([[0.0], [0.1], [-0.1], [-5.0], [5.0], [0.0]])
    yv = np.array(["tight", "tight", "tight", "wide", "wide", "wide"])
    eq(sol.GaussianNB().fit(Xv, yv).predict(np.array([[0.05], [3.0]])), np.array(["tight", "wide"]))
