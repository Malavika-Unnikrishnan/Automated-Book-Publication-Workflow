# audio_utils.py
from gtts import gTTS
import os
from pathlib import Path
import uuid

AUDIO_DIR = Path("data/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def text_to_mp3(text: str) -> str:
    """
    Generate an MP3 file from text and return its file path.
    Uses a hash/uuid so repeated calls don’t overwrite.
    """
    if not text.strip():
        raise ValueError("Empty text cannot be narrated.")

    file_path = AUDIO_DIR / f"{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang="en")
    tts.save(str(file_path))
    return str(file_path)
