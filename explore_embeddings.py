"""Explore the GloVe word space: neighbours, similarity, analogy, and a PCA picture.
Run: python explore_embeddings.py   -> saves results/embedding_space_pca.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from embed_chatbot import DATA_DIR, glove

g = glove()
print("== Nearest neighbours ==")
for w in ["chat", "sentiment", "translation", "accuracy", "kigali"]:
    print(w, "->", [(n, round(s, 2)) for n, s in g.most_similar(w, topn=5)])

print("\n== Similarity scores (0..1) ==")
for a, b in [("accuracy", "correctness"), ("good", "great"), ("good", "banana"), ("car", "automobile"), ("king", "queen")]:
    print(f"{a} vs {b}: {g.similarity(a, b):.2f}")

print("\n== Analogies (A - B + C) ==")
for pos, neg in [(["king", "woman"], ["man"]), (["paris", "rwanda"], ["france"]), (["walking", "swam"], ["swimming"])]:
    print(" + ".join(pos), "-", " - ".join(neg), "->", [(n, round(s, 2)) for n, s in g.most_similar(positive=pos, negative=neg, topn=3)])

groups = {"NLP": ["token", "corpus", "sentiment", "translation", "chat", "vocabulary", "grammar"],
          "Countries": ["rwanda", "france", "japan", "brazil", "kenya", "germany"],
          "Capitals": ["kigali", "paris", "tokyo", "brasilia", "nairobi", "berlin"],
          "Royalty": ["king", "queen", "prince", "princess", "man", "woman"]}
words = [w for ws in groups.values() for w in ws]
pts = PCA(n_components=2).fit_transform([g[w] for w in words])
plt.figure(figsize=(9, 6.5))
colors = dict(zip(groups, ["#1b4f9c", "#12857a", "#c0392b", "#8e44ad"]))
i = 0
for name, ws in groups.items():
    for w in ws:
        plt.scatter(*pts[i], color=colors[name], s=45); plt.annotate(w, pts[i], xytext=(4, 4), textcoords="offset points", fontsize=9); i += 1
    plt.scatter([], [], color=colors[name], label=name)
plt.legend(); plt.title("GloVe word vectors (100 dimensions) reduced to 2D with PCA")
plt.xlabel("PCA 1"); plt.ylabel("PCA 2"); plt.tight_layout()
output_dir = DATA_DIR / "results"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "embedding_space_pca.png"
plt.savefig(output_path, dpi=140)
print(f"\nSaved {output_path}")
