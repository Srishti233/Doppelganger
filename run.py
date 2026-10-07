#!/usr/bin/env python3
"""Start the doppelganger:  python run.py   |   python run.py --check"""
import sys
import urllib.request

from dg import avatar, config, voice
from dg.brain import Brain


def check():
    b = Brain()
    url = config.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")
    try:
        urllib.request.urlopen(url + "/api/tags", timeout=2)
        up = "running"
    except Exception:
        up = "NOT running (install from ollama.com)"
    print(f"Brain   : Ollama {up}, model={config.get('OLLAMA_MODEL', 'llama3.2')}")
    print(f"Chats   : {len(b.msgs)} of your messages learned" + ("" if b.msgs else " (add files to data/chats/)"))
    for n in b.notes:
        print("          note:", n)
    print(f"Voice   : {len(voice.samples())} sample(s); cloning {'ACTIVE' if voice.available() else 'off (default voice)'}")
    print(f"Avatar  : {'colors from your photo' if avatar.palette() else 'plain faceless default'}")


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    else:
        from dg.server import serve
        serve()
