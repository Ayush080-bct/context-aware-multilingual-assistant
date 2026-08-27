# Context-Aware Multilingual AI Assistant

An AI-powered voice assistant that helps people communicate across languages by converting speech to text, translating it, and speaking the translation back.

**MVP scope:** Nepali ↔ English voice translation.

## How it works

```
Speech → Speech-to-Text → Translation → Text-to-Speech → Speech
```

## Tech Stack

- Python
- Streamlit (web interface)
- Speech-to-Text, Machine Translation, and Text-to-Speech models (final choices TBD — evaluating free-tier options with good Nepali support)

## Project Structure

```
app.py
src/
  speech_to_text.py
  translator.py
  text_to_speech.py
  pipeline.py
tests/
  test_pipeline.py
assets/
  screenshots/
requirements.txt
```

## Status

🚧 In development — Day 1 (project setup)

## Long-Term Vision

Beyond the MVP, this project aims to explore **context-aware translation for low-resource languages**, using Nepali as a case study — investigating whether conversation history improves translation quality over sentence-by-sentence translation.

## License

TBD