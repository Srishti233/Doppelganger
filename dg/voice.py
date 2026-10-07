"""The 'sound' part. Clones your voice locally from data/voice/*.wav using Coqui XTTS v2.

If no samples (or no TTS library) are present, the UI falls back to the browser's default voice.
Voice samples never leave your machine.
"""
import importlib.util
import os
import tempfile
import threading

from . import config

_lock, _tts = threading.Lock(), None


def samples():
    return sorted(p for p in config.VOICE.glob("*") if p.suffix.lower() in (".wav", ".mp3", ".flac"))


def available():
    return bool(samples()) and importlib.util.find_spec("TTS") is not None


def synthesize(text):
    """Return WAV bytes of `text` spoken in your cloned voice."""
    global _tts
    with _lock:
        if _tts is None:
            import torch
            from TTS.api import TTS
            device = "cuda" if torch.cuda.is_available() else "cpu"
            _tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        fd, path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        try:
            _tts.tts_to_file(text=text, speaker_wav=[str(p) for p in samples()[:5]],
                             language=config.get("VOICE_LANG", "en"), file_path=path)
            with open(path, "rb") as f:
                return f.read()
        finally:
            os.remove(path)
