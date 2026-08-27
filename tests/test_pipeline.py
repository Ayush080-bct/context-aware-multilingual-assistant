"""
test_pipeline.py

Basic sanity tests. These test the translation and TTS stages directly
(no audio file needed), since STT requires a real audio sample.

Run with: pytest tests/test_pipeline.py
"""

import os
import sys

# Add project root to sys.path so "src" can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.translator import translate_ne_to_en, translate_en_to_ne
from src.text_to_speech import synthesize_speech


def test_translate_ne_to_en_not_empty():
    result = translate_ne_to_en("नमस्ते")
    assert isinstance(result, str)
    assert len(result) > 0


def test_translate_en_to_ne_not_empty():
    result = translate_en_to_ne("Hello")
    assert isinstance(result, str)
    assert len(result) > 0


def test_synthesize_speech_creates_file(tmp_path):
    output_path = str(tmp_path / "test_output.mp3")
    result_path = synthesize_speech("Hello world", lang="en", output_path=output_path)

    assert os.path.exists(result_path)
    assert os.path.getsize(result_path) > 0


def test_synthesize_speech_rejects_empty_text():
    try:
        synthesize_speech("", lang="en")
        assert False, "Expected ValueError for empty text"
    except ValueError:
        pass
