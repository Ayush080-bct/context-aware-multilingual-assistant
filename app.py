"""
app.py

Streamlit interface for the Context-Aware Multilingual AI Assistant.

Keeps a running conversation: every recording is appended to a session
history instead of replacing the previous result, so the user can go
back and forth (Nepali <-> English) in one continuous session until
they choose to clear/stop it.
"""

import streamlit as st
from src.pipeline import run_pipeline

st.set_page_config(page_title="Context-Aware Multilingual AI Assistant", layout="centered")

st.title("🌐 Context-Aware Multilingual AI Assistant")
st.caption("MVP: Nepali ↔ English speech translation — continuous conversation")

# ---------------------------------------------------------------------------
# Session state: holds the running conversation for this browser session.
# Each entry is a dict: {source_lang, target_lang, recognized_text,
# translated_text, output_audio_path}
# ---------------------------------------------------------------------------
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "turn_count" not in st.session_state:
    st.session_state.turn_count = 0

st.divider()

# ---------------------------------------------------------------------------
# Controls
# ---------------------------------------------------------------------------
col1, col2 = st.columns([3, 1])

with col1:
    direction = st.radio(
        "Speaking direction for this turn:",
        options=["🇳🇵 Nepali → English", "🇬🇧 English → Nepali"],
        horizontal=True,
    )

with col2:
    st.write("")  # spacing
    st.write("")
    if st.button("🗑️ Clear conversation"):
        st.session_state.conversation = []
        st.session_state.turn_count = 0
        st.rerun()

if direction.startswith("🇳🇵"):
    source_lang, target_lang = "ne", "en"
else:
    source_lang, target_lang = "en", "ne"

st.write("Record or upload the next turn:")

# The key changes every turn, which resets the widget so old audio doesn't
# get reprocessed after a rerun.
audio_key = f"audio_input_{st.session_state.turn_count}"
audio_file = st.audio_input("🎤 Record your voice", key=audio_key)

if audio_file is None:
    upload_key = f"file_uploader_{st.session_state.turn_count}"
    audio_file = st.file_uploader(
        "...or upload an audio file", type=["wav", "mp3", "m4a"], key=upload_key
    )

if audio_file is not None:
    with st.spinner("Processing: transcribing → translating → generating speech..."):
        temp_input_path = "temp_input_audio.wav"
        with open(temp_input_path, "wb") as f:
            f.write(audio_file.getbuffer())

        try:
            result = run_pipeline(temp_input_path, source_lang, target_lang)

            st.session_state.conversation.append(
                {
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "recognized_text": result["recognized_text"],
                    "translated_text": result["translated_text"],
                    "output_audio_path": result["output_audio_path"],
                }
            )
            st.session_state.turn_count += 1

            # Rerun so a fresh (empty) audio widget is shown for the next turn.
            st.rerun()

        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.divider()

# ---------------------------------------------------------------------------
# Conversation history
# ---------------------------------------------------------------------------
st.subheader("💬 Conversation")

if not st.session_state.conversation:
    st.info("No turns yet — record or upload audio above to start the conversation.")
else:
    lang_labels = {"ne": "🇳🇵 Nepali", "en": "🇬🇧 English"}

    total_turns = len(st.session_state.conversation)

    # Show newest turn first, without changing how turns are stored/numbered.
    for reverse_index, turn in enumerate(reversed(st.session_state.conversation)):
        i = total_turns - reverse_index
        src_label = lang_labels[turn["source_lang"]]
        tgt_label = lang_labels[turn["target_lang"]]

        with st.container(border=True):
            st.markdown(f"**Turn {i}: {src_label} → {tgt_label}**")

            st.markdown(f"🗣️ **Recognized ({src_label}):** {turn['recognized_text']}")
            st.markdown(f"🌍 **Translated ({tgt_label}):** {turn['translated_text']}")
            st.audio(turn["output_audio_path"])

st.divider()
st.caption(
    "Limitations: translation accuracy is not guaranteed, translation is currently "
    "sentence-level (each turn is translated independently, without using earlier "
    "turns as context yet), and this is not real-time simultaneous interpretation. "
    "See README for full roadmap."
)