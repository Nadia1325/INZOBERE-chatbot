"""Retrieval over Inzobere's English knowledge base using TF-IDF and GloVe."""

from __future__ import annotations

import math
import re
import threading
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


ROOT = Path(__file__).resolve().parent
KB_PATH = ROOT / "kb.txt"
MODEL_NAME = "glove-wiki-gigaword-100"
MODEL_CACHE = ROOT / ".model_cache"
HYBRID_ALPHA = 0.5


def load_faq():
    rows = []
    with KB_PATH.open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            line = line.strip()
            if not line:
                continue
            question, separator, answer = line.partition("|")
            if not separator:
                raise ValueError(f"Expected question|answer at {KB_PATH.name}:{line_number}")
            rows.append({"question": question.strip(), "answer": answer.strip()})
    if not rows:
        raise ValueError(f"No FAQ entries found in {KB_PATH}")
    return rows


FAQ = load_faq()
DOCS = [f"{row['question']} {row['question']} {row['answer']}" for row in FAQ]
VECTORIZER = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
TFIDF_MATRIX = VECTORIZER.fit_transform(DOCS)


def _tokens(text):
    return [word for word in re.sub(r"[^a-z0-9 ]", " ", text.lower()).split()
            if word not in ENGLISH_STOP_WORDS and len(word) > 1]


class FAQMatcher:
    """Score the same Inzobere FAQ with TF-IDF or a TF-IDF/GloVe hybrid."""

    def __init__(self):
        self._glove = None
        self._vectors_ready = False
        self._faq_vectors = None
        self._center = None
        self._idf = self._make_idf()
        self._vector_lock = threading.Lock()

    @staticmethod
    def _make_idf():
        document_frequency = {}
        for doc in DOCS:
            for word in set(_tokens(doc)):
                document_frequency[word] = document_frequency.get(word, 0) + 1
        count = len(DOCS)
        return {word: math.log((1 + count) / (1 + frequency)) + 1
                for word, frequency in document_frequency.items()}

    def _load_vectors(self):
        if self._vectors_ready:
            return
        with self._vector_lock:
            if self._vectors_ready:
                return
            import gensim.downloader as gensim_api

            gensim_api.BASE_DIR = str(MODEL_CACHE)
            self._glove = gensim_api.load(MODEL_NAME)
            raw_vectors = np.vstack([self._raw_vector(doc) for doc in DOCS])
            self._center = raw_vectors.mean(axis=0)
            centered = raw_vectors - self._center
            norms = np.linalg.norm(centered, axis=1, keepdims=True)
            self._faq_vectors = centered / np.maximum(norms, 1e-12)
            self._vectors_ready = True

    def _raw_vector(self, text):
        words, vectors, weights = [], [], []
        for word in _tokens(text):
            if word in self._glove.key_to_index:
                words.append(word)
        if not words:
            return np.zeros(self._glove.vector_size, dtype=np.float32)
        for word in words:
            vectors.append(self._glove[word])
            weights.append(self._idf.get(word, 1.0))
        return np.average(vectors, axis=0, weights=weights)

    def scores(self, question, mode="hybrid", alpha=HYBRID_ALPHA):
        if mode not in {"tfidf", "hybrid", "embeddings"}:
            raise ValueError("mode must be tfidf, hybrid, or embeddings")
        tfidf = cosine_similarity(
            VECTORIZER.transform([question]), TFIDF_MATRIX
        )[0]
        if mode == "tfidf":
            return tfidf, None

        self._load_vectors()
        if not any(word in self._glove.key_to_index for word in _tokens(question)):
            return tfidf, np.zeros(len(FAQ), dtype=np.float32)
        query_vector = self._raw_vector(question) - self._center
        norm = np.linalg.norm(query_vector)
        if norm:
            query_vector /= norm
        embedded = self._faq_vectors @ query_vector
        if mode == "embeddings":
            return embedded, embedded

        scale = lambda values: (values - values.min()) / max(float(values.max() - values.min()), 1e-12)
        return alpha * scale(tfidf) + (1 - alpha) * scale(embedded), embedded

    def search(self, question, mode="hybrid", top=3, alpha=HYBRID_ALPHA):
        ranking, embedded = self.scores(question, mode, alpha)
        tfidf = cosine_similarity(
            VECTORIZER.transform([question]), TFIDF_MATRIX
        )[0]
        indices = np.argsort(ranking)[::-1][:max(1, min(int(top), len(FAQ)))]
        return [
            {
                "index": int(index),
                "question": FAQ[index]["question"],
                "answer": FAQ[index]["answer"],
                "score": float(ranking[index]),
                "tfidf": float(tfidf[index]),
                "embedding": float(embedded[index]) if embedded is not None else None,
            }
            for index in indices
        ]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Search Inzobere's English FAQ.")
    parser.add_argument("question", nargs="+", help="Question to search for")
    parser.add_argument("--mode", choices=("tfidf", "hybrid", "embeddings"), default="hybrid")
    args = parser.parse_args()
    matcher = FAQMatcher()
    for result in matcher.search(" ".join(args.question), args.mode):
        print(f"{result['score']:.3f}  {result['question']}\n  {result['answer']}")
