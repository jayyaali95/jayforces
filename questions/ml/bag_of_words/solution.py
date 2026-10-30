import re

import numpy as np

_TOKEN = re.compile(r"[a-z0-9']+")


def tokenize(text):
    """Lowercase word tokens."""
    return _TOKEN.findall(text.lower())


class CountVectorizer:
    """Docs -> word count matrix."""

    def __init__(self):
        self.vocabulary_ = None

    def fit(self, docs):
        words = sorted({w for d in docs for w in tokenize(d)})
        self.vocabulary_ = {w: i for i, w in enumerate(words)}
        return self

    def transform(self, docs):
        m = np.zeros((len(docs), len(self.vocabulary_)), dtype=int)
        for r, d in enumerate(docs):
            for w in tokenize(d):
                if w in self.vocabulary_:
                    m[r, self.vocabulary_[w]] += 1
        return m

    def fit_transform(self, docs):
        return self.fit(docs).transform(docs)


def tfidf(docs):
    """Smoothed, L2 normalized TF-IDF."""
    cv = CountVectorizer().fit(docs)
    tf = cv.transform(docs).astype(float)
    df = (tf > 0).sum(axis=0)
    w = tf * (np.log((1 + len(docs)) / (1 + df)) + 1)
    norms = np.linalg.norm(w, axis=1, keepdims=True)
    return np.divide(w, norms, out=np.zeros_like(w), where=norms > 0), cv.vocabulary_
