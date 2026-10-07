"""Load YOUR messages from data/chats (WhatsApp .txt exports, plain .txt, or .json list of strings).

Only the messages written by you are kept. Links, emails and phone numbers are redacted.
Other people's messages are never stored or sent anywhere.
"""
import json
import re
from collections import Counter
from pathlib import Path

from . import config

WA = re.compile(
    r"^\[?(\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4}),?\s+\d{1,2}[:.]\d{2}(?:[:.]\d{2})?"
    r"\s?(?:[APap]\.?[Mm]\.?)?\]?\s*(?:[-\u2013]\s*)?([^:]{1,40}?):\s(.*)$"
)
SKIP = ("<media omitted>", "this message was deleted", "you deleted this message",
        "image omitted", "(file attached)", "missed voice call", "missed video call")
URL = re.compile(r"https?://\S+")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"\+?\d[\d\s().-]{7,}\d")


def redact(text):
    text = URL.sub("[link]", text)
    text = EMAIL.sub("[email]", text)
    return PHONE.sub("[number]", text).strip()


def parse_whatsapp(text):
    """Return [(sender, message)], joining multi-line messages."""
    out = []
    for raw in text.splitlines():
        line = raw.replace("\u200e", "").replace("\u202f", " ").strip()
        m = WA.match(line)
        if m:
            out.append([m.group(2).strip(), m.group(3)])
        elif out and line:
            out[-1][1] += " " + line
    return [(s, m) for s, m in out]


def load_my_messages(folder=None, my_name=""):
    """Return (messages, notes)."""
    folder, msgs, notes = Path(folder or config.CHATS), [], []
    for f in sorted(folder.glob("*")):
        ext = f.suffix.lower()
        if ext == ".json":
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                msgs += [x for x in data if isinstance(x, str)]
            except (ValueError, OSError):
                notes.append(f"Could not read {f.name}")
        elif ext == ".txt":
            text = f.read_text(encoding="utf-8", errors="ignore")
            parsed = parse_whatsapp(text)
            if len(parsed) >= 3:
                names = Counter(s for s, _ in parsed)
                lower = {n.lower(): n for n in names}
                me = lower.get(my_name.lower()) if my_name else None
                if not me:
                    me = names.most_common(1)[0][0]
                    notes.append(f"{f.name}: MY_NAME not matched, assuming you are '{me}'")
                msgs += [m for s, m in parsed if s == me]
            else:
                msgs += [ln for ln in text.splitlines() if ln.strip()]
    clean = []
    for m in msgs:
        m = redact(m)
        if len(m) >= 2 and not any(s in m.lower() for s in SKIP):
            clean.append(m)
    return clean, notes
