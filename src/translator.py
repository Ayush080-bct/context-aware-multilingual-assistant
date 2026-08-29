"""
translator.py

Translates text between Nepali and English using Meta's NLLB-200 model
(via Hugging Face transformers), run locally.

Switched from deep-translator (Google Translate scraping) because that
backend was unreliable in testing — intermittent TranslationNotFound /
RequestError failures even on simple input. NLLB runs offline once
downloaded, so there's no dependency on a flaky third-party endpoint.
"""

import re

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Language codes used throughout the rest of the project (app.py, pipeline.py).
NEPALI = "ne"
ENGLISH = "en"

# NLLB's own language codes (FLORES-200 codes), mapped from the simple ones above.
_NLLB_LANG_CODES = {
    "ne": "npi_Deva",
    "en": "eng_Latn",
}

_MODEL_NAME = "facebook/nllb-200-distilled-600M"

_tokenizer = None
_model = None


def _load_model():
    global _tokenizer, _model
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME)
        _model = AutoModelForSeq2SeqLM.from_pretrained(_MODEL_NAME)
    return _tokenizer, _model


def _split_sentences(text: str) -> list[str]:
    cleaned = text.strip()
    if not cleaned:
        return []

    parts = re.split(r"(?<=[.!?])\s+|\n+", cleaned)
    return [p.strip() for p in parts if p and p.strip()][:2]


def _translate_single(sentence: str, source_lang: str, target_lang: str) -> str:
    tokenizer, model = _load_model()

    src_code = _NLLB_LANG_CODES[source_lang]
    tgt_code = _NLLB_LANG_CODES[target_lang]

    tokenizer.src_lang = src_code
    inputs = tokenizer(sentence, return_tensors="pt")

    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_code),
            max_length=256,
        )

    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0].strip()


def translate_text(
    text: str,
    source_lang: str,
    target_lang: str,
    max_sentences: int = 2,
) -> str:
    """Translates text from source_lang to target_lang using NLLB-200."""
    if not text or not text.strip():
        return ""

    sentences = _split_sentences(text)
    if not sentences:
        return ""

    if max_sentences is not None:
        sentences = sentences[:max_sentences]

    translated = [
        _translate_single(sentence, source_lang, target_lang) for sentence in sentences
    ]
    return " ".join(part for part in translated if part)


def translate_ne_to_en(text: str, max_sentences: int = 2) -> str:
    return translate_text(
        text,
        source_lang=NEPALI,
        target_lang=ENGLISH,
        max_sentences=max_sentences,
    )


def translate_en_to_ne(text: str, max_sentences: int = 2) -> str:
    return translate_text(
        text,
        source_lang=ENGLISH,
        target_lang=NEPALI,
        max_sentences=max_sentences,
    )


if __name__ == "__main__":
    # Quick manual test
    sample_ne = "मलाई पोखरा जानको लागि बस टिकट चाहिन्छ।"
    print("NE -> EN:", translate_ne_to_en(sample_ne))

    sample_en = "I need a bus ticket to go to Pokhara."
    print("EN -> NE:", translate_en_to_ne(sample_en))