"""Simple FAQ Chatbot - TF-IDF + cosine similarity (scikit-learn).
Run:  python chatbot.py          (chat in the terminal)
      python chatbot.py --test   (check how smart the bot is)
"""
import csv, re, sys
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity

THRESHOLD = 0.20  # below this score the bot says "I am not sure"

# 1) Load the 100 questions and answers
DATA_DIR = Path(__file__).resolve().parent / "data"

with (DATA_DIR / "faq.csv").open(encoding="utf-8", newline="") as f:
    FAQ = list(csv.DictReader(f))

# 2) Clean the text: lowercase -> remove symbols -> remove stopwords -> simple stemming
def stem(w):
    for end in ("ing", "ed", "es", "s"):
        if len(w) > 4 and w.endswith(end) and not w.endswith("ss"):
            return w[: -len(end)]
    return w

# Synonyms make the bot smarter: different words with the same meaning
SYN = {"bot": "chatbot", "correctness": "accuracy", "common": "stopwords", "computer": "machine",
       "translate": "translation", "review": "review sentiment", "reviews": "review sentiment"}

def clean(text):
    words = " ".join(SYN.get(w, w) for w in re.sub(r"[^a-z0-9 ]", " ", text.lower()).split()).split()
    return " ".join(stem(w) for w in words if w not in ENGLISH_STOP_WORDS and len(w) > 1)

# 3) Turn every stored question into TF-IDF numbers (single words + word pairs)
docs = [clean(f"{r['question']} {r['question']} {r['answer']}") for r in FAQ]
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
matrix = vectorizer.fit_transform(docs)

# 4) Compare the user question with every stored question (cosine similarity)
def ask(text, top=3):
    scores = cosine_similarity(vectorizer.transform([clean(text)]), matrix)[0]
    best = scores.argsort()[::-1][:top]
    return [(FAQ[i], float(scores[i])) for i in best]

def reply(text):
    (row, score), *others = ask(text)
    if score < THRESHOLD:
        tips = "; ".join(r["question"] for r, _ in others[:2] + [(row, 0)])
        return f"I am not sure. Try: {tips}", score
    return row["answer"], score

# 5) Small test: reworded questions -> expected stored question
TESTS = {
    "explain tf idf": "What is TF-IDF?", "explain how the bot works": "How does this chatbot work?",
    "what does stemming do": "What is stemming?", "find names of people in text": "What is Named Entity Recognition?",
    "which library gives ready models": "What is Hugging Face?", "why do we remove common words": "Why remove stopwords?",
    "how to measure similarity": "What is cosine similarity?", "how to check model correctness": "What is accuracy?",
    "detect positive or negative reviews": "What is sentiment analysis?", "translate text with computer": "What is machine translation?",
}

def run_tests():
    ok = sum(ask(q)[0][0]["question"] == a for q, a in TESTS.items())
    print(f"Top-1 accuracy on {len(TESTS)} reworded questions: {ok}/{len(TESTS)}")

if __name__ == "__main__":
    if "--test" in sys.argv:
        run_tests()
    else:
        print("FAQ Chatbot ready. Type a question (or 'quit').")
        while (q := input("You: ").strip().lower()) not in ("quit", "exit"):
            answer, score = reply(q)
            print(f"Bot: {answer}  [score {score:.2f}]")
