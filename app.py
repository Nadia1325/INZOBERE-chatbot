"""Streamlit entry point for the Inzobere FAQ assistant."""

import json
import sys
from functools import lru_cache
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Inzobere | NLP Assistant", page_icon="🤖", layout="centered")
st.markdown(
    """
    <style>
    .stApp { background: var(--background-color); color: var(--text-color); }
    [data-testid="stHeader"] { background: var(--background-color); }
    [data-testid="stSidebar"] { background: var(--secondary-background-color); }
    [data-testid="stChatMessage"] {
        background: var(--secondary-background-color);
        color: var(--text-color);
        border: 1px solid color-mix(in srgb, var(--text-color) 18%, transparent);
        border-radius: 16px;
    }
    [data-testid="stChatInput"] textarea {
        background: var(--secondary-background-color);
        color: var(--text-color);
        border-color: color-mix(in srgb, var(--text-color) 28%, transparent);
    }
    h1, h2, h3 { color: var(--primary-color); }
    div.stButton > button {
        color: var(--primary-color);
        background: var(--secondary-background-color);
        border-color: var(--primary-color);
    }
    div.stButton > button:hover {
        color: var(--background-color);
        background: var(--primary-color);
        border-color: var(--primary-color);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@lru_cache(maxsize=1)
def get_english_matcher():
    from semantic_search import FAQMatcher

    return FAQMatcher()


@lru_cache(maxsize=1)
def get_rw_matcher():
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    rows = []
    for line in (ROOT / "kb_rw.txt").read_text(encoding="utf-8").splitlines():
        question, separator, answer = line.partition("|")
        if separator:
            rows.append({"question": question.strip(), "answer": answer.strip()})
    documents = [f"{row['question']} {row['question']} {row['answer']}" for row in rows]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(documents)

    def search(question, top=3):
        scores = cosine_similarity(vectorizer.transform([question]), matrix)[0]
        indices = np.argsort(scores)[::-1][:top]
        return [
            {"question": rows[i]["question"], "answer": rows[i]["answer"],
             "tfidf": float(scores[i]), "embedding": None}
            for i in indices
        ]

    return search


def transcribe(audio_file, language):
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    locale = "rw-RW" if language == "Kinyarwanda" else "en-US"
    return recognizer.recognize_google(audio, language=locale)


def speak(text, language):
    safe_text = json.dumps(text, ensure_ascii=False)
    locale = "rw-RW" if language == "Kinyarwanda" else "en-US"
    components.html(
        f"""<script>
        const utterance = new SpeechSynthesisUtterance({safe_text});
        utterance.lang = {json.dumps(locale)};
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
        </script>""",
        height=0,
    )


with st.sidebar:
    st.header("How it works")
    st.markdown(
        "1. Ask by typing or using the microphone.\n"
        "2. Inzobere compares your question with its FAQ.\n"
        "3. It shows the closest answer and other matches.\n"
        "4. Press **Read answer aloud** to hear the response."
    )
    st.divider()
    st.caption("English supports TF-IDF and the optional GloVe hybrid. Kinyarwanda uses TF-IDF.")

st.title("🤖 Inzobere")
st.caption("Your bilingual NLP question and answer assistant")
language = st.radio("Language / Ururimi", ("English", "Kinyarwanda"), horizontal=True)
if language == "English":
    hybrid_available = sys.version_info < (3, 14)
    modes = ("tfidf", "hybrid") if hybrid_available else ("tfidf",)
    mode = st.selectbox(
        "Search model", modes,
        format_func=lambda value: "TF-IDF baseline" if value == "tfidf" else "Hybrid: TF-IDF + GloVe",
    )
    if not hybrid_available:
        st.caption("Hybrid search requires GloVe, which is not supported by this Python version. TF-IDF is available.")
else:
    mode = "tfidf"

if "messages" not in st.session_state:
    st.session_state.messages = []

for index, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            with st.expander("Other possible answers"):
                for alternative in message.get("alternatives", []):
                    st.markdown(f"**{alternative['question']}**")
                    st.write(alternative["answer"])
            if st.button("🔊 Read answer aloud", key=f"speak-{index}"):
                speak(message["content"], language)

with st.expander("🎙️ Ask with your microphone"):
    audio = st.audio_input("Record your question", sample_rate=16000)
    if audio and st.button("Transcribe recording", key="transcribe"):
        try:
            recognized = transcribe(audio, language)
            st.session_state.voice_question = recognized
            st.success(f"Recognized: {recognized}")
        except Exception as error:
            st.error(f"Could not transcribe audio: {type(error).__name__}: {error}")

prefilled = st.session_state.pop("voice_question", "")
question = st.chat_input("Ask an NLP question… / Baza ikibazo kuri NLP…")
if question or prefilled:
    question = question or prefilled
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Finding an answer…"):
                if language == "Kinyarwanda":
                    results = get_rw_matcher()(question)
                else:
                    results = get_english_matcher().search(question, mode=mode, top=3)
            best, *alternatives = results
            st.markdown(best["answer"])
            st.caption(f"Matched: {best['question']} · TF-IDF {best['tfidf']:.3f}")
            st.session_state.messages.append(
                {"role": "assistant", "content": best["answer"], "alternatives": alternatives}
            )
        except Exception as error:
            st.error(f"Search failed: {type(error).__name__}: {error}")

if st.session_state.messages and st.button("Clear conversation"):
    st.session_state.messages = []
    st.rerun()
