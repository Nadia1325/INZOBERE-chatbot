"""FAQ Chatbot v2 - word embeddings (GloVe) instead of only TF-IDF.

Idea in simple words:
  v1 (TF-IDF)  : matches the SAME words.   "correctness" != "accuracy"
  v2 (GloVe)   : matches similar MEANING.  "correctness" ~ "accuracy"
Each text becomes ONE vector = the average of its word vectors (rare words count more).
"""
import math, re
import numpy as np
import gensim.downloader as api
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from chatbot import DATA_DIR, FAQ, matrix, vectorizer, clean as tfidf_clean

MODEL_NAME = "glove-wiki-gigaword-100"   # 100-number vectors trained on Wikipedia + news (downloads once, ~130 MB)
_glove = None

def glove():
    global _glove
    if _glove is None:
        _glove = api.load(MODEL_NAME)
    return _glove

def tokens(text):
    words = re.sub(r"[^a-z0-9 ]", " ", text.lower()).split()
    return [w for w in words if w not in ENGLISH_STOP_WORDS and len(w) > 1]

# How rare is each word in our FAQ? Rare words get a bigger weight (same idea as IDF)
DOCS = [tokens(f"{r['question']} {r['question']} {r['answer']}") for r in FAQ]
_df = {}
for d in DOCS:
    for w in set(d):
        _df[w] = _df.get(w, 0) + 1
IDF = {w: math.log((1 + len(DOCS)) / (1 + n)) + 1 for w, n in _df.items()}
IDF_MAX = max(IDF.values())

def raw_vector(text):
    g, vecs, weights = glove(), [], []
    for w in tokens(text):
        if w in g.key_to_index:
            vecs.append(g[w]); weights.append(IDF.get(w, IDF_MAX))
    if not vecs:
        return np.zeros(g.vector_size)
    return np.average(vecs, axis=0, weights=weights)

_raw = np.array([raw_vector(" ".join(d)) for d in DOCS])
_mean = _raw.mean(axis=0)          # centering: remove what ALL texts share, so real differences stand out

def vector(text):
    v = raw_vector(text) - _mean
    n = np.linalg.norm(v)
    return v / n if n else v

E = np.array([v / (np.linalg.norm(v) or 1) for v in (_raw - _mean)])

def scores(text, method="hybrid", alpha=0.5):
    """Score of the question against all 100 stored questions (higher = better)."""
    tf = (vectorizer.transform([tfidf_clean(text)]) @ matrix.T).toarray()[0]
    em = E @ vector(text)
    if method == "tfidf": return tf
    if method == "embed": return em
    norm = lambda s: (s - s.min()) / ((s.max() - s.min()) or 1)   # put both on a 0..1 scale
    return alpha * norm(tf) + (1 - alpha) * norm(em)

def ask(text, method="hybrid", top=3, alpha=0.5):
    s = scores(text, method, alpha)
    best = s.argsort()[::-1][:top]
    return [(FAQ[i], float(s[i])) for i in best]

def reply(text):
    """Answer, or say 'not sure' when neither the words nor the meaning match well."""
    tf = (vectorizer.transform([tfidf_clean(text)]) @ matrix.T).toarray()[0].max()
    em = float((E @ vector(text)).max())
    (row, _), *others = ask(text)
    if tf < 0.10 and em < 0.30:   # only rejects nonsense; off-topic detection is still weak (see README)
        tips = "; ".join(r["question"] for r, _ in ask(text)[:3])
        return f"I am not sure. Try: {tips}", 0.0
    return row["answer"], em

if __name__ == "__main__":
    print("FAQ Chatbot v2 (word embeddings). Type a question (or 'quit').")
    while (q := input("You: ").strip()).lower() not in ("quit", "exit"):
        a, s = reply(q)
        print(f"Bot: {a}  [meaning score {s:.2f}]")
