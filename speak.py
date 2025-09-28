# speak.py
import pyttsx3
from typing import Optional

_engine = pyttsx3.init()  # SAPI5 on Windows, NSSpeechSynthesizer on macOS
_engine.setProperty("rate", 170)   # 150–190 is comfortable
_engine.setProperty("volume", 0.9) # 0.0–1.0

def list_voices() -> None:
    """Print available voice ids (run once to pick your favorite)."""
    for v in _engine.getProperty("voices"):
        print(f"- id: {v.id} | name: {getattr(v, 'name', '')}")

def set_voice(prefer: Optional[str] = None) -> None:
    """
    Set a voice by substring match (e.g., 'female', 'zira', 'male', 'david').
    Falls back to default if not found.
    """
    voices = _engine.getProperty("voices")
    if not prefer:
        return
    prefer_l = prefer.lower()
    for v in voices:
        name = f"{v.id} {getattr(v, 'name', '')}".lower()
        if prefer_l in name:
            _engine.setProperty("voice", v.id)
            break

def speak(text: str, voice_hint: Optional[str] = None, rate: Optional[int] = None) -> None:
    """
    Speak text synchronously.
    - voice_hint: pick voice by substring (e.g., 'female', 'zira', 'david')
    - rate: override words-per-minute
    """
    if voice_hint:
        set_voice(voice_hint)
    if rate:
        _engine.setProperty("rate", rate)
    _engine.say(text)
    _engine.runAndWait()
