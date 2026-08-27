"""
text_to_speech.py

Converts translated text back into spoken audio using gTTS (Google
Text-to-Speech). Chosen for the MVP because it's free, requires no API
key, and supports Nepali ("ne") and English ("en") voices out of the box.
"""

import os
import tempfile
from gtts import gTTS


def synthesize_speech(text: str, lang: str, output_path: str | None = None) -> str:
    """
    Converts text into a spoken audio file.

    Args:
        text: the text to speak.
        lang: "ne" or "en".
        output_path: where to save the .mp3 file. If None, a temp file
            is created automatically.

    Returns:
        The path to the generated .mp3 audio file.
    """
    if not text.strip():
        raise ValueError("Cannot synthesize empty text.")

    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)

    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)

    return output_path


if __name__ == "__main__":
    # Quick manual test: generates test_en.mp3 and test_ne.mp3 in cwd
    path_en = synthesize_speech(
        "I need a bus ticket to go to Pokhara.", lang="en", output_path="test_en.mp3"
    )
    print(f"Saved: {path_en}")

    path_ne = synthesize_speech(
        "मलाई पोखरा जानको लागि बस टिकट चाहिन्छ।", lang="ne", output_path="test_ne.mp3"
    )
    print(f"Saved: {path_ne}")