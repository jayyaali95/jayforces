import numpy as np

from check import close, eq, table

DOCS = ["Driver was late", "driver was great, GREAT ride", "late late late"]

table(globals(), 1, lambda s, t: s.tokenize(t), [
    ("lowercase", "Driver WAS late", ["driver", "was", "late"]),
    ("punctuation", "great, ride!", ["great", "ride"]),
    ("apostrophe", "didn't show", ["didn't", "show"]),
    ("digits", "waited 20 min", ["waited", "20", "min"]),
    ("empty", "", []),
])


def test_p1_vocab_sorted(sol):
    eq(sol.CountVectorizer().fit(DOCS).vocabulary_, {"driver": 0, "great": 1, "late": 2, "ride": 3, "was": 4})


def test_p1_fit_returns_self(sol):
    v = sol.CountVectorizer()
    eq(v.fit(DOCS) is v, True)


def test_p1_counts(sol):
    eq(sol.CountVectorizer().fit(DOCS).transform(DOCS), np.array([[1, 0, 1, 0, 1], [1, 2, 0, 1, 1], [0, 0, 3, 0, 0]]))


def test_p1_unknown_words(sol):
    eq(sol.CountVectorizer().fit(DOCS).transform(["bad driver"]), np.array([[1, 0, 0, 0, 0]]))


def test_p1_int_dtype(sol):
    eq(np.issubdtype(sol.CountVectorizer().fit(DOCS).transform(DOCS).dtype, np.integer), True)


def test_p1_empty_doc(sol):
    eq(sol.CountVectorizer().fit(DOCS).transform([""]), np.zeros((1, 5), dtype=int))


def ref(docs):
    vocab = sorted({w for d in docs for w in d.lower().replace(",", " ").split()})
    tf = np.array([[d.lower().replace(",", " ").split().count(w) for w in vocab] for d in docs], dtype=float)
    idf = np.log((1 + len(docs)) / (1 + (tf > 0).sum(0))) + 1
    w = tf * idf
    return w / np.linalg.norm(w, axis=1, keepdims=True)


def test_p2_tfidf_values(sol):
    close(sol.tfidf(DOCS)[0], ref(DOCS))


def test_p2_tfidf_vocab(sol):
    eq(sol.tfidf(DOCS)[1], {"driver": 0, "great": 1, "late": 2, "ride": 3, "was": 4})


def test_p2_rows_unit_norm(sol):
    close(np.linalg.norm(sol.tfidf(DOCS)[0], axis=1), np.ones(3))


def test_p2_rare_word_weighs_more(sol):
    m, v = sol.tfidf(["a b", "a c", "a d"])
    eq(m[0, v["b"]] > m[0, v["a"]], True)


def test_p2_empty_row_stays_zero(sol):
    m, _ = sol.tfidf(["ride", "!!!"])
    eq((np.isnan(m).any(), m[1].tolist()), (False, [0.0]))


def test_p2_single_doc(sol):
    m, _ = sol.tfidf(["x x y"])
    close(m, np.array([[2, 1]]) / np.sqrt(5))
