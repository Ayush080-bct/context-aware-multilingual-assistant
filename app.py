"""
app.py

Streamlit interface for the Context-Aware Multilingual AI Assistant.

Lets a user record/upload speech in Nepali or English, see the
recognized text and its translation, and play back the translated
speech.
"""

import streamlit as st
from src.pipeline import run_pipeline

st.set_page_config(page_title="Context-Aware Multilingual AI Assistant", layout="centered")

st.title("🌐 Context-Aware Multilingual AI Assistant")
st.caption("MVP: Nepali ↔ English speech translation")

st.divider()

direction = st.radio(
    "Choose translation direction:",
    options=["🇳🇵 Nepali → English", "🇬🇧 English → Nepali"],
    horizontal=True,
)

if direction.startswith("🇳🇵"):
    source_lang, target_lang = "ne", "en"
else:
    source_lang, target_lang = "en", "ne"

st.write("Upload or record a short audio clip:")

audio_file = st.audio_input("🎤 Record your voice")

if audio_file is None:
    audio_file = st.file_uploader("...or upload an audio file", type=["wav", "mp3", "m4a"])

if audio_file is not None:
    with st.spinner("Processing: transcribing → translating → generating speech..."):
        # Save uploaded/recorded audio to a temp file for the pipeline to read
        temp_input_path = "temp_input_audio.wav"
        with open(temp_input_path, "wb") as f:
            f.write(audio_file.getbuffer())

        try:
            result = run_pipeline(temp_input_path, source_lang, target_lang)

            st.subheader("Recognized Text")
            st.write(result["recognized_text"])

            st.subheader("Translated Text")
            st.write(result["translated_text"])

            st.subheader("🔊 Translated Speech")
            st.audio(result["output_audio_path"])

        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.divider()
st.caption(
    "Limitations: translation accuracy is not guaranteed, no conversation "
    "context yet, and this is not real-time simultaneous interpretation. "
    "See README for full roadmap."
)