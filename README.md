# Inzobere NLP assistant

Inzobere answers NLP questions from the project's English and Kinyarwanda FAQ knowledge bases. The English chatbot now offers a live comparison between its TF-IDF baseline and a hybrid model that combines TF-IDF with GloVe word embeddings.

## Run the chatbot

```powershell
py -m pip install -r requirements.txt
py run.py
```

Open the local page at `http://127.0.0.1:8000`. Keep the terminal running while chatting; press `Ctrl+C` there to stop the app. Use the model selector to switch between **Hybrid: TF-IDF + GloVe** and **TF-IDF baseline**. Answer labels show the TF-IDF and GloVe similarity scores used for English matches; both modes show two alternative FAQ matches that users can select.

The first English hybrid question downloads the pretrained `glove-wiki-gigaword-100` vectors (about 130 MB) and needs an internet connection. Later runs use the downloaded model cache. If the backend is unavailable, the page displays a message and falls back to the browser's TF-IDF search.

GloVe is trained on English text, so Kinyarwanda questions continue to use the existing bilingual TF-IDF pipeline. The page indicates this fallback in its answer label.

## Show and evaluate the change

The live system searches the same English FAQs from `kb.txt` with both methods. Its embedding vectors are IDF-weighted averages of pretrained word vectors, centered over the FAQ collection and compared with cosine similarity. The hybrid equally combines normalized TF-IDF and embedding scores; adjust `HYBRID_ALPHA` in `semantic_search.py` to change the balance. The best answer plus two alternatives make the improved top-3 coverage useful in the chat.

Run the evaluation on reworded questions for the project's own knowledge base:

```powershell
py evaluate_inzobere.py
```

It reports top-1 accuracy, top-3 accuracy, and mean reciprocal rank for TF-IDF, GloVe alone, and several hybrid weights. Results are saved to `data/results/inzobere_comparison.csv`. The questions and expected answers are in `data/inzobere_test_questions.csv`.

For the embedding exploration and the separate coursework FAQ experiment, run:

```powershell
py explore_embeddings.py
py evaluate.py
py chatbot.py --test
```

The exploration plot is saved to `data/results/embedding_space_pca.png`. The coursework experiment in `data/faq.csv` is retained separately from Inzobere's bilingual knowledge bases.

## Main files

- `index.html`, `template.html`, `kb.txt`, `kb_rw.txt`: Inzobere browser app and its bilingual FAQ content.
- `build.py`: rebuilds `index.html` from the template and both knowledge bases.
- `run.py`: local web server and JSON search endpoint used by the live hybrid model.
- `semantic_search.py`: TF-IDF, GloVe, and hybrid retrieval over the English Inzobere FAQ.
- `evaluate_inzobere.py`, `data/inzobere_test_questions.csv`: evaluation for the actual Inzobere knowledge base.
- `chatbot.py`, `embed_chatbot.py`, `evaluate.py`: the separate coursework FAQ comparison.

## Limits

The manually reworded test set is small. Here is the measured comparison on its 21 questions:

| Model | Top-1 | Top-3 | MRR |
|---|---:|---:|---:|
| TF-IDF baseline | 61.9% | 81.0% | 0.728 |
| GloVe embeddings | 57.1% | 71.4% | 0.653 |
| Hybrid, alpha 0.50 | 52.4% | 85.7% | 0.703 |

The hybrid places the correct response in its top three more often, but the baseline still has better top-1 accuracy and MRR. The UI shows alternatives to make that top-3 improvement usable; these results do not show a universal accuracy improvement. GloVe uses static word vectors, which do not represent word meaning differently by sentence context. Kinyarwanda currently uses the original keyword and TF-IDF pipeline because the selected GloVe model is English-only.
