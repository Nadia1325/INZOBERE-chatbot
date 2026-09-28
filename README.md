# Inzobere - NLP FAQ Assistant
TF-IDF + cosine similarity retrieval chatbot with voice input, Kinyarwanda questions and a hidden 100-answer knowledge base.

## Run (2 options)
1. Easiest: double-click `index.html` (open with Google Chrome).
2. With Python: `python run.py` -> opens http://localhost:8000 (needed if voice is blocked on file://).

## Files
- index.html  the app (all code + hidden knowledge base inside)
- kb.txt      the 100 Questions|Answers (edit, then run `python build.py`)
- template.html / build.py  rebuild tools
- Inzobere_Presentation.pptx  slides (includes all 100 Q&A in appendix)

## Use
Type or press the microphone. Choose Kinyarwanda in the top-right to ask in Kinyarwanda (voice uses rw-RW). Press "Translate" under an answer to open it in Kinyarwanda.

## v2: ChatGPT-style chat
Free-typing chat (typing dots + streaming answers). 100 Q&A in English (kb.txt) and Kinyarwanda (kb_rw.txt, same order). The bot replies in the language of the matched question; the 🌍 button switches an answer between English and Kinyarwanda. Off-topic questions get a caring "outside my knowledge" reply.
