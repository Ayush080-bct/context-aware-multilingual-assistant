"""
translator.py

Translates text between Nepali and English using deep-translator, which
wraps Google Translate's free web endpoint (no API key required for
light/moderate usage). Chosen for the MVP because it has solid Nepali
support and zero setup cost; can be swapped later for NLLB or a paid
API if quality/rate-limits become an issue.
"""

import time
from deep_translator import GoogleTranslator, MyMemoryTranslator
from deep_translator.exceptions import TranslationNotFound, RequestError

# Language codes used throughout the project.
NEPALI = "ne"
ENGLISH = "en"

# MyMemoryTranslator expects locale-style codes for some languages.
_MYMEMORY_LANG_MAP = {"ne": "ne-NP", "en": "en-GB"}


def _translate_with_google(text: str, source_lang: str, target_lang: str) -> str:
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    return translator.translate(text)


def _translate_with_mymemory(text: str, source_lang: str, target_lang: str) -> str:
    src = _MYMEMORY_LANG_MAP.get(source_lang, source_lang)
    tgt = _MYMEMORY_LANG_MAP.get(target_lang, target_lang)
    translator = MyMemoryTranslator(source=src, target=tgt)
    return translator.translate(text)


def translate_text(
    text: str, source_lang: str, target_lang: str, retries: int = 2
) -> str:
    """
    Translates text from source_lang to target_lang.

    Tries Google Translate first (usually best quality for Nepali), with a
    couple of retries since deep-translator's Google backend is a scraped
    endpoint and occasionally fails transiently. Falls back to MyMemory
    (a different free translation API) if Google keeps failing, so a single
    flaky request doesn't crash the whole pipeline.

    Args:
        text: the text to translate.
        source_lang: "ne" or "en".
        target_lang: "ne" or "en".
        retries: number of times to retry the primary (Google) backend
            before falling back.

    Returns:
        The translated text as a string, or an error placeholder if every
        backend fails.
    """
    if not text.strip():
        return ""

    last_error = None

    # Try Google first, with retries (handles transient scraping failures).
    for attempt in range(retries + 1):
        try:
            return _translate_with_google(text, source_lang, target_lang)
        except (TranslationNotFound, RequestError) as e:
            last_error = e
            if attempt < retries:
                time.sleep(0.5)

    # Google kept failing — fall back to MyMemory.
    try:
        return _translate_with_mymemory(text, source_lang, target_lang)
    except Exception as e:
        last_error = e

    # Both backends failed — don't crash the app, surface a clear message.
    return f"[Translation failed: {last_error}]"


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