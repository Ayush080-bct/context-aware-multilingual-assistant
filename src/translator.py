"""
translator.py

Translates text between Nepali and English using deep-translator, which
wraps Google Translate's free web endpoint (no API key required for
light/moderate usage). Chosen for the MVP because it has solid Nepali
support and zero setup cost; can be swapped later for NLLB or a paid
API if quality/rate-limits become an issue.
"""

from deep_translator import GoogleTranslator

# Language codes used throughout the project.
NEPALI = "ne"
ENGLISH = "en"


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translates text from source_lang to target_lang.

    Args:
        text: the text to translate.
        source_lang: "ne" or "en" (or "auto" to auto-detect).
        target_lang: "ne" or "en".

    Returns:
        The translated text as a string.
    """
    if not text.strip():
        return ""

    translator = GoogleTranslator(source=source_lang, target=target_lang)
    return translator.translate(text)


def translate_ne_to_en(text: str) -> str:
    return translate_text(text, source_lang=NEPALI, target_lang=ENGLISH)


def translate_en_to_ne(text: str) -> str:
    return translate_text(text, source_lang=ENGLISH, target_lang=NEPALI)


if __name__ == "__main__":
    # Quick manual test
    sample_ne = "मलाई पोखरा जानको लागि बस टिकट चाहिन्छ।"
    print("NE -> EN:", translate_ne_to_en(sample_ne))

    sample_en = "I need a bus ticket to go to Pokhara."
    print("EN -> NE:", translate_en_to_ne(sample_en))