# 🌐 Context-Aware Multilingual AI Assistant

An AI-powered voice assistant that helps people communicate across languages by converting speech to text, translating it, and speaking the translation back — no manual typing into a translator required.

**MVP scope:** Nepali ↔ English voice translation.

> This is the 7-day MVP version. It is a stepping stone toward a longer-term research direction: **context-aware speech translation for low-resource languages** (see below).

---


## 📖 Table of Contents

- [Overview](#-overview)
- [System Design](#-system-design)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Testing](#-testing)
- [Git Workflow](#-git-workflow)
- [Roadmap](#-roadmap)
- [Limitations](#-limitations)
- [Long-Term Research Direction](#-long-term-research-direction)
- [Status](#-status)
- [License](#-license)

---

## 🎯 Overview

Language barriers make communication difficult when two people don't share a language. This project lets someone speak in Nepali or English and have their words automatically transcribed, translated, and spoken back in the other language.

**Example:**

Person A speaks Nepali:
> "मलाई पोखरा जानको लागि बस टिकट चाहिन्छ।"

The system produces, as speech:
> "I need a bus ticket to go to Pokhara."

The reverse direction (English → Nepali) works the same way.

---

## 🧩 System Design

### High-level pipeline

```
                 ┌────────────────────┐
   🎤 Speech ──▶ │   Speech-to-Text   │──▶  Recognized Text
                 │   (faster-whisper) │
                 └────────────────────┘
                            │
                            ▼
                 ┌────────────────────┐
                 │   Translation      │──▶  Translated Text
                 │   (deep-translator)│
                 └────────────────────┘
                            │
                            ▼
                 ┌────────────────────┐
                 │   Text-to-Speech   │──▶  🔊 Translated Speech
                 │   (gTTS)           │
                 └────────────────────┘
```

### Component responsibilities

| Component | File | Responsibility |
|---|---|---|
| Speech-to-Text | `src/speech_to_text.py` | Converts recorded/uploaded audio into text, with language hinting (`ne`/`en`) |
| Translator | `src/translator.py` | Translates recognized text between Nepali and English |
| Text-to-Speech | `src/text_to_speech.py` | Converts translated text into an audio file |
| Pipeline | `src/pipeline.py` | Orchestrates the three stages above into one call: `run_pipeline()` |
| App | `app.py` | Streamlit UI: record/upload audio, choose direction, display results, play audio |

### Data flow (request lifecycle)

1. User selects a direction (Nepali → English or English → Nepali) in the UI.
2. User records or uploads an audio clip.
3. `app.py` saves the audio to a temp file and calls `pipeline.run_pipeline(audio_path, source_lang, target_lang)`.
4. `run_pipeline`:
   - calls `speech_to_text.transcribe_audio()` → recognized text
   - calls `translator.translate_text()` → translated text
   - calls `text_to_speech.synthesize_speech()` → output audio file path
5. `app.py` displays the recognized text, translated text, and an audio player for the result.

### Future system design (post-MVP)

Once conversation context is introduced, the pipeline gains two new stages:

```
Speech → ASR → Language Detection → Conversation History → Context Analysis
       → Context-Aware Translation → TTS
```

`Conversation History` will need lightweight state (e.g. a rolling buffer of prior sentence pairs) that `Context Analysis` uses to disambiguate the current sentence before translation — this is the core research question of the project (see [Long-Term Research Direction](#-long-term-research-direction)).

---

## ✨ Features

- 🎤 Record or upload speech in Nepali or English
- 📝 Automatic speech recognition (ASR)
- 🌍 Machine translation between Nepali and English (both directions)
- 🔊 Natural-sounding translated speech output
- 🖥️ Simple Streamlit web interface
- 🧪 Notebooks for model comparison and interactive pipeline testing

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Interface:** [Streamlit](https://streamlit.io/)
- **Speech-to-Text:** [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — open-source, runs locally, no API key, good Nepali support
- **Translation:** [deep-translator](https://github.com/nidhaloff/deep-translator) — free Google Translate endpoint, supports Nepali
- **Text-to-Speech:** [gTTS](https://github.com/pndurang/gTTS) — free, supports Nepali and English voices

> These were chosen for the MVP based on free-tier availability and Nepali language support. They can be swapped out later (e.g. for NLLB, Coqui/Piper, or a paid API) if quality or rate limits become a problem — see [Roadmap](#-roadmap).

---

## 📁 Project Structure

```
context-aware-multilingual-assistant/
│
├── app.py                      # Streamlit UI
│
├── src/
│   ├── __init__.py
│   ├── speech_to_text.py        # ASR (faster-whisper)
│   ├── translator.py            # Translation (deep-translator)
│   ├── text_to_speech.py        # TTS (gTTS)
│   └── pipeline.py              # Connects the three stages
│
├── notebooks/
│   ├── 01_model_comparison.ipynb   # Compare STT/MT/TTS options
│   └── 02_pipeline_testing.ipynb   # Interactive end-to-end testing
│
├── tests/
│   └── test_pipeline.py         # Automated tests (pytest)
│
├── assets/
│   └── screenshots/
│
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or later
- Git
- An internet connection (translation and TTS call external services at runtime; the Whisper model downloads on first use)

### Installation

```bash
git clone https://github.com/<your-username>/context-aware-multilingual-assistant.git
cd context-aware-multilingual-assistant

python3 -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`).

---

## 🖥️ Usage

1. Choose a translation direction: 🇳🇵 Nepali → English or 🇬🇧 English → Nepali.
2. Record your voice or upload an audio file (`.wav`, `.mp3`, `.m4a`).
3. Wait for processing — the app transcribes, translates, and generates speech.
4. Read the recognized text and translation, and play back the translated audio.

---

## 🧪 Testing

Automated tests:

```bash
pytest tests/
```

Interactive/manual testing (model comparison, listening to output, trying edge cases):

```bash
jupyter notebook notebooks/01_model_comparison.ipynb
jupyter notebook notebooks/02_pipeline_testing.ipynb
```

---

## 🔀 Git Workflow

This project follows a simplified Git Flow:

- `main` — always stable, working code
- `develop` — integration branch where finished features land first
- `feature/*` — one branch per feature, branched off `develop`

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# ...make changes, commit...

git push -u origin feature/your-feature-name
# open a PR: feature/your-feature-name → develop
```

Once `develop` is stable, it's merged into `main` via PR.

---

## 🗺️ Roadmap

**Phase 1 — 7-Day MVP** (current)
- [x] Project setup
- [x] Speech-to-Text
- [x] Translation
- [x] Text-to-Speech
- [x] Full pipeline + Streamlit UI
- [ ] Testing across accents/speeds/sentence lengths
- [ ] Documentation & demo

**Phase 2 — Beyond MVP**
- More languages
- Automatic language detection
- Conversation memory
- Context-aware translation
- Improved Nepali language support
- Multimodal input (image/text understanding)
- Mobile / offline / edge deployment
- Low-resource language optimization
- Research dataset creation and quantitative evaluation

---

## ⚠️ Limitations

The current MVP does **not** guarantee:

- Perfect translation accuracy
- Perfect Nepali speech recognition
- Real-time simultaneous interpretation
- Full conversational context understanding
- Support for languages beyond Nepali/English
- Professional-grade translation
- Offline operation

It is intended to demonstrate a **working end-to-end AI pipeline**, not a production-grade translator.

---

## 🔬 Long-Term Research Direction

> **Context-aware multilingual AI for low-resource languages**, with Nepali as the initial case study.

**Research question:** does using conversation history improve translation quality compared to translating each sentence in isolation?

```
Baseline:              Current Sentence → Translation

Proposed approach:     Conversation History + Current Sentence
                                    → Context Analysis
                                    → Translation
```

Potential evaluation metrics: BLEU, chrF, Word Error Rate (WER), semantic similarity, human evaluation, contextual error analysis, and translation latency. Methodology will be finalized after the MVP is working and a small evaluation dataset exists.

Other potential applications down the line: tourism, education, healthcare communication, agriculture, cross-border communication, and local-language digital services.

---

## 📌 Status

🚧 **In development.**

Current stage: MVP pipeline implemented (STT → Translation → TTS via Streamlit); testing and documentation in progress.

---

## 📄 License

TBD