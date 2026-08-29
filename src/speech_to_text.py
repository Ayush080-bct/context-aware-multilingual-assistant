"""
speech_to_text.py

Converts spoken audio into text using Meta's MMS (Massively Multilingual
Speech) ASR model via Hugging Face transformers.

Switched from faster-whisper to MMS because MMS was trained specifically
to cover 1000+ languages including Nepali, whereas Nepali is a smaller
part of Whisper's training data. Using transformers here also matches
the translator (NLLB), keeping the stack consistent.
"""

import torch
import librosa
from transformers import Wav2Vec2ForCTC, AutoProcessor

# Language codes used throughout the rest of the project (app.py, pipeline.py).
NEPALI = "ne"
ENGLISH = "en"

# MMS's own language codes, mapped from the simple ones above.
_MMS_LANG_CODES = {
    "ne": "npi",
    "en": "eng",
}

_MODEL_NAME = "facebook/mms-1b-all"
_TARGET_SAMPLE_RATE = 16000

_processor = None
_model = None
_current_adapter_lang = None


def _load_model():
    global _processor, _model
    if _model is None:
        _processor = AutoProcessor.from_pretrained(_MODEL_NAME)
        _model = Wav2Vec2ForCTC.from_pretrained(_MODEL_NAME)
    return _processor, _model


def _set_adapter_language(lang_code: str):
    """
    MMS uses per-language adapter weights loaded on top of a shared base
    model. Switching languages means loading a different adapter.
    """
    global _current_adapter_lang
    processor, model = _load_model()

    if _current_adapter_lang != lang_code:
        processor.tokenizer.set_target_lang(lang_code)
        model.load_adapter(lang_code)
        _current_adapter_lang = lang_code

    return processor, model


def transcribe_audio(audio_path: str, language_hint: str | None = None) -> dict:
    """
    Transcribes an audio file to text.

    Args:
        audio_path: path to a .wav/.mp3/.m4a audio file.
        language_hint: "ne" or "en". MMS requires an explicit language
            (unlike Whisper, it doesn't auto-detect), so this is required
            in practice — defaults to Nepali if not given.

    Returns:
        dict with keys: "text", "language" (the language code used)
    """
    lang = language_hint or NEPALI
    mms_lang = _MMS_LANG_CODES.get(lang, lang)

    processor, model = _set_adapter_language(mms_lang)

    # Load and resample audio to 16kHz mono, which MMS expects.
    audio, _ = librosa.load(audio_path, sr=_TARGET_SAMPLE_RATE, mono=True)

    inputs = processor(audio, sampling_rate=_TARGET_SAMPLE_RATE, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs).logits

    ids = torch.argmax(outputs, dim=-1)[0]
    text = processor.decode(ids)

    return {
        "text": text.strip(),
        "language": lang,
    }


if __name__ == "__main__":
    # Quick manual test: python speech_to_text.py path/to/audio.wav ne
    import sys

    if len(sys.argv) < 2:
        print("Usage: python speech_to_text.py <audio_file> [ne|en]")
        sys.exit(1)

    audio_file = sys.argv[1]
    lang_hint = sys.argv[2] if len(sys.argv) > 2 else "ne"

    result = transcribe_audio(audio_file, language_hint=lang_hint)
    print(f"Language: {result['language']}")
    print(f"Transcript: {result['text']}")