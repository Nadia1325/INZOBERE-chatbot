"""Compare v1 (TF-IDF) with v2 (embeddings) using the SAME metrics on the SAME test questions.
Run: python evaluate.py   -> prints a table and saves results/comparison.csv
"""
import csv
import embed_chatbot as eb
from chatbot import TESTS

def load_tests():
    with (eb.DATA_DIR / "test_questions.csv").open(encoding="utf-8", newline="") as f:
        return [(r["test_question"], r["expected_question"]) for r in csv.DictReader(f)]

def metrics(pairs, method, alpha=0.5):
    top1 = top3 = mrr = 0
    wrong = []
    for q, expected in pairs:
        s = eb.scores(q, method, alpha)
        order = [eb.FAQ[i]["question"] for i in s.argsort()[::-1]]
        rank = order.index(expected) + 1
        top1 += rank == 1; top3 += rank <= 3; mrr += 1 / rank
        if rank > 1: wrong.append((q, expected, order[0]))
    n = len(pairs)
    return top1 / n, top3 / n, mrr / n, wrong

if __name__ == "__main__":
    sets = {"New test set (40 reworded questions)": load_tests(),
            "Old test set (10 questions from v1)": list(TESTS.items())}
    rows = []
    for name, pairs in sets.items():
        for label, method in [("v1 TF-IDF", "tfidf"), ("v2 Embeddings only", "embed"), ("v2 Hybrid (TF-IDF + embeddings)", "hybrid")]:
            t1, t3, mrr, wrong = metrics(pairs, method)
            rows.append([name, label, f"{t1:.3f}", f"{t3:.3f}", f"{mrr:.3f}"])
            if name.startswith("New") and method != "embed":
                print(f"\n[{label}] wrong on:"); [print("  -", q, "->", got) for q, exp, got in wrong]
    print(); print(f"{'Test set':40} {'Model':34} Top-1  Top-3  MRR")
    for r in rows: print(f"{r[0]:40} {r[1]:34} {r[2]}  {r[3]}  {r[4]}")
    output_dir = eb.DATA_DIR / "results"
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "comparison.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["test_set", "model", "top1", "top3", "mrr"]); w.writerows(rows)
    print("\nAlpha check (share of TF-IDF in the hybrid), new test set:")
    for a in (0.0, 0.25, 0.5, 0.75, 1.0):
        t1, t3, mrr, _ = metrics(sets["New test set (40 reworded questions)"], "hybrid", a)
        print(f"  alpha={a:.2f}  top1={t1:.3f}  top3={t3:.3f}  mrr={mrr:.3f}")
