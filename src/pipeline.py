"""
pipeline.py

Connects the three stages of the MVP into a single end-to-end function:

    Speech -> Speech-to-Text -> Translation -> Text-to-Speech -> Speech

This is the module app.py (the Streamlit UI) calls into.
"""

from speech_to_text import transcribe_audio
from translator import translate_text, NEPALI, ENGLISH
from text_to_speech import synthesize_speech


def run_pipeline(audio_path: str, source_lang: str, target_lang: str) -> dict:
    """
    Runs the full speech-to-speech translation pipeline.

    Args:
        audio_path: path to the input audio file (recorded speech).
        source_lang: "ne" or "en" — the language being spoken.
        target_lang: "ne" or "en" — the language to translate into.

    Returns:
        dict with keys:
            "recognized_text": transcript of the input audio
            "translated_text": translation of the transcript
            "output_audio_path": path to the synthesized speech file
    """
    # 1. Speech-to-Text
    stt_result = transcribe_audio(audio_path, language_hint=source_lang)
    recognized_text = stt_result["text"]

    # 2. Translation
    translated_text = translate_text(
        recognized_text, source_lang=source_lang, target_lang=target_lang
    )

    # 3. Text-to-Speech
    output_audio_path = synthesize_speech(translated_text, lang=target_lang)

    return {
        "recognized_text": recognized_text,
        "translated_text": translated_text,
        "output_audio_path": output_audio_path,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python -m src.pipeline <audio_file> <source_lang> <target_lang>")
        print("Example: python -m src.pipeline sample.wav ne en")
        sys.exit(1)

    audio_file, src, tgt = sys.argv[1], sys.argv[2], sys.argv[3]
    result = run_pipeline(audio_file, src, tgt)

    print(f"Recognized ({src}): {result['recognized_text']}")
    print(f"Translated ({tgt}): {result['translated_text']}")
    print(f"Output audio saved to: {result['output_audio_path']}")