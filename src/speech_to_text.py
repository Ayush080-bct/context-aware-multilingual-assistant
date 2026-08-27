"""
Speech_to_text.py 

converts spoken audio into text using faster-whisper.
Whisper supports multilingual transcription out of the box(it means that the system is already trained, 
fully equipped, and ready to understand multiple languages immediately
 without you needing to do any extra setup, coding, or separate downloads.), including
Nepali ("ne") and English ("en"), which is why it was chosen for the MVP
instead of a paid cloud STT API.
"""
from faster_whisper import WhisperModel
_MODEL_SIZE = 'small'
_model = None

def _get_model():
    global _model
    if _model is None:
        _model = WhisperModel(_MODEL_SIZE,device="cpu",compute_type="int8")
    return _model

def transcribe_audio(audio_path:str, language_hint: str | None=None)->dict:
    """
    Transcribe an audio file to text.
    Args:
        audio_path: path to a .wav/.mp3/.m4a audio file.
        lanuage hint:ISO
        return:dict "text","languaage"
    """
    model = _get_model()
    segments,info = model.transcribe(
        audio_path,
        language=language_hint,
        beam_size=5
    )
    full_text = " ".join(segment.text.strip() for segment in segments)

    return {
        "text": full_text.strip(),
        "language": info.language,
    }
 
if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print("Usage : python speech_to_text.py <audio_file>")
        sys.exit(1)
    result = transcribe_audio(sys.argv[1])
    print(f"Detected language: {result['language']}")
    print(f"Transcript: {result['text']}")