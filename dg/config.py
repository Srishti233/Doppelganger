"""Paths and settings. Reads .env (if present) and environment variables."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CHATS, VOICE, IMAGES = DATA / "chats", DATA / "voice", DATA / "images"


def _load_env():
    p = ROOT / ".env"
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            v = v.split(" #")[0].strip().strip("\"'")
            os.environ.setdefault(k.strip(), v)


_load_env()


def get(key, default=""):
    return os.getenv(key) or default
