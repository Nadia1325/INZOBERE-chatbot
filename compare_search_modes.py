"""Compare the top FAQ match from GloVe embeddings and TF-IDF."""

from semantic_search import FAQMatcher


QUESTIONS = [
    "How can a computer make sense of human language?",
    "What lets a chatbot understand what I am saying?",
    "How do machines figure out the meaning of words?",
    "Can a computer understand spoken language?",
    "How can I teach a computer that happy and joyful are related?",
    "Why might bank mean different things in different sentences?",
    "How does a computer find words with similar meanings?",
]


def main():
    matcher = FAQMatcher()
    print("Question | GloVe top match | TF-IDF top match | Different?")
    print("-" * 110)
    for question in QUESTIONS:
        glove = matcher.search(question, mode="embeddings", top=1)[0]
        tfidf = matcher.search(question, mode="tfidf", top=1)[0]
        different = glove["index"] != tfidf["index"]
        print(f"\n{question}\n"
              f"  GloVe: {glove['question']} (score {glove['score']:.3f})\n"
              f"  TF-IDF: {tfidf['question']} (score {tfidf['score']:.3f})\n"
              f"  Top prediction differs: {'yes' if different else 'no'}")


if __name__ == "__main__":
    main()
