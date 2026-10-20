---
title: Bag of words and TF-IDF
difficulty: easy
category: ml
tags: nlp, text, numpy
---
Turn support ticket text into features.

## Part 1: Count vectors

`tokenize(text)` lowercases and returns the list of tokens matching `[a-z0-9']+`.

Implement `CountVectorizer` with `fit(docs)` building `vocabulary_` as `{word: column}` with columns assigned in sorted
word order, returning `self`, and `transform(docs)` returning a numpy int array `(n_docs, n_words)` of counts. Unknown words are ignored.

## Part 2: TF-IDF

Implement `tfidf(docs)` returning `(matrix, vocab)` where vocab is the same sorted mapping, and

- `tf = count of word in doc` (raw counts)
- `idf = ln((1 + n_docs) / (1 + df)) + 1` (smoothed, like sklearn)
- each row of `tf * idf` is L2 normalized (rows of all zeros stay zero)
