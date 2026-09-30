# Word embeddings in Inzobere

The hybrid retrieval model is connected to the live English FAQ chatbot. The browser sends an English question to the local Python service, which searches the same `kb.txt` data used by the original TF-IDF chatbot.

## Run and compare

```powershell
py -m pip install -r requirements.txt
py run.py
```

In the browser, choose **TF-IDF baseline** or **Hybrid: TF-IDF + GloVe**, then ask the same question in each mode. The answer metadata reports component similarity scores in hybrid mode. Both modes show two alternative FAQ matches. The first hybrid request downloads GloVe vectors.

Kinyarwanda continues through the existing browser-side keyword and TF-IDF pipeline because the selected pretrained GloVe model contains English word vectors. The interface labels this fallback.

## Evaluate the knowledge base

```powershell
py evaluate_inzobere.py
```

This compares TF-IDF, embeddings alone, and the hybrid on the reworded examples in `data/inzobere_test_questions.csv`. It prints top-1 accuracy, top-3 accuracy, and mean reciprocal rank, then saves the table to `data/results/inzobere_comparison.csv`.

## How the representation works

Each English FAQ entry combines its question (weighted twice) and answer. GloVe supplies a dense vector for each known word. The system averages those vectors with IDF weights, centers the FAQ vectors, and uses cosine similarity to rank answers. The hybrid combines normalized TF-IDF and embedding scores; `HYBRID_ALPHA` in `semantic_search.py` controls their balance. In this 21-question evaluation, the 50/50 hybrid improved top-3 accuracy by 4.7 percentage points but had lower top-1 accuracy than TF-IDF. TF-IDF remains available in the live app as the baseline.
