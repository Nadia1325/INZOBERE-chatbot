"""Compare TF-IDF, GloVe embeddings, and their hybrid on Inzobere's KB."""

import csv

from semantic_search import FAQ, FAQMatcher, HYBRID_ALPHA, ROOT


TEST_PATH = ROOT / "data" / "inzobere_test_questions.csv"
OUTPUT_PATH = ROOT / "data" / "results" / "inzobere_comparison.csv"


def load_tests():
    with TEST_PATH.open(encoding="utf-8", newline="") as source:
        tests = list(csv.DictReader(source))
    known_questions = {item["question"] for item in FAQ}
    missing = [row["expected_question"] for row in tests
               if row["expected_question"] not in known_questions]
    if missing:
        raise ValueError(f"Expected FAQ questions are missing from kb.txt: {missing}")
    return tests


def evaluate(matcher, tests, mode, alpha=HYBRID_ALPHA):
    top1 = top3 = reciprocal_rank = 0.0
    mistakes = []
    correct_examples = []
    for test in tests:
        ranked = matcher.search(test["test_question"], mode, top=len(FAQ), alpha=alpha)
        questions = [result["question"] for result in ranked]
        rank = questions.index(test["expected_question"]) + 1
        top1 += rank == 1
        top3 += rank <= 3
        reciprocal_rank += 1 / rank
        if rank != 1:
            mistakes.append((test["test_question"], test["expected_question"], questions[0]))
        elif not correct_examples:
            correct_examples.append((test["test_question"], test["expected_question"], questions[0]))
    count = len(tests)
    return {
        "top1": top1 / count,
        "top3": top3 / count,
        "mrr": reciprocal_rank / count,
        # Single-label FAQ classification predicts exactly one FAQ per query.
        # Therefore micro-averaged precision, recall, F1 and accuracy coincide.
        "accuracy": top1 / count,
        "precision_micro": top1 / count,
        "recall_micro": top1 / count,
        "f1_micro": top1 / count,
        "mistakes": mistakes,
        "correct_examples": correct_examples,
    }


def main():
    tests = load_tests()
    matcher = FAQMatcher()
    rows = []
    evaluations = [("tfidf", "TF-IDF baseline", 1.0),
                   ("embeddings", "GloVe embeddings", 1.0)]
    evaluations.extend(("hybrid", f"Hybrid alpha={alpha:.2f}", alpha)
                       for alpha in (0.5, 0.65, 0.85))
    for mode, label, alpha in evaluations:
        result = evaluate(matcher, tests, mode, alpha)
        rows.append({"model": label, "test_count": len(tests),
                     "top1": result["top1"], "top3": result["top3"],
                     "mrr": result["mrr"], "accuracy": result["accuracy"],
                     "precision_micro": result["precision_micro"],
                     "recall_micro": result["recall_micro"],
                     "f1_micro": result["f1_micro"]})
        print(f"{label:26} Top-1 {result['top1']:.1%}  "
              f"P/R/F1(micro) {result['precision_micro']:.1%}/"
              f"{result['recall_micro']:.1%}/{result['f1_micro']:.1%}  "
              f"Top-3 {result['top3']:.1%}  MRR {result['mrr']:.3f}")
        if mode != "hybrid" or alpha == HYBRID_ALPHA:
            if result["correct_examples"]:
                query, expected, predicted = result["correct_examples"][0]
                print(f"  Correct example: {query!r} | expected {expected!r} | got {predicted!r}")
            for query, expected, predicted in result["mistakes"]:
                print(f"  Miss: {query!r} | expected {expected!r} | got {predicted!r}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved comparison to {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
