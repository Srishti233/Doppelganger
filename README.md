# Doppelganger

![Tests](https://github.com/Srishti233/Doppelganger/actions/workflows/tests.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Status](https://img.shields.io/badge/status-early%20preview-orange.svg)

A faceless AI twin that **thinks, sounds, looks and acts** like you.

It runs entirely on your own machine. There are no accounts, no cloud services, and none of your personal data in this repo.

> **Early preview (v0.1).** The core experience works today. Voice cloning is experimental, and more features are on the way. Feedback and ideas are welcome.

## What it does

| | Out of the box | After you add your own data |
|---|---|---|
| **Think** | Persona from `profile.md` | Also learns your writing style from your chats |
| **Sound** | Your browser's default voice | Your cloned voice (local, experimental) |
| **Look** | Plain faceless silhouette | Hair, head and clothing colors taken from your photo |
| **Act** | Sways while thinking, glows green while listening, nods while speaking | Head motion follows your cloned voice |

The avatar never has a face: no eyes, nose, lips or eyebrows.

## How it works

```
you speak -> browser speech-to-text -> /chat -> persona + your style + local LLM (Ollama) -> reply
          -> /tts (your voice) or browser voice -> avatar animates
```

## Quick start

1. Install [Ollama](https://ollama.com) and pull a model:
   ```bash
   ollama pull llama3.2
   ```
2. Set up the project (Python 3.9+ is required, nothing else):
   ```bash
   pip install -r requirements.txt     # only Pillow, optional
   cp .env.example .env
   cp profile.example.md profile.md    # describe yourself in this file
   python run.py
   ```
3. Open http://localhost:5000 and talk with the mic (Chrome or Edge) or type.

Run `python run.py --check` at any time to see what the app found: whether Ollama is running, how many of your messages it learned, and whether voice cloning is active.

## Make it you

Everything personal stays on your machine and is git-ignored. See [`data/README.md`](data/README.md) for details.

| Folder | Put here | Effect |
|---|---|---|
| `data/chats/` | WhatsApp "Export chat" `.txt` files, plain `.txt` (one message per line), or `.json` (a list of strings) | Learns how you write. Only **your** messages are kept. |
| `data/voice/` | 1 to 5 clean recordings of you speaking (`.wav`, `.mp3`, `.flac`), 10 to 30 seconds each | Cloned voice (also run `pip install -r requirements-voice.txt`) |
| `data/images/` | One clear, centered portrait photo (`.jpg` or `.png`) | Sets the avatar's colors. No face is ever drawn. |

If a folder is missing, just create it. Then set `MY_NAME` in `.env` to your name as it appears in your WhatsApp export, so it knows which messages are yours.

## Project layout

```
run.py            start the app (or --check)
dg/               brain, chat reader, voice, avatar, server
web/index.html    the faceless avatar and chat page
tests/            automated tests
data/             your private files (git-ignored)
```

## Privacy and safety

- Everything runs locally, including the language model. Nothing is sent to any cloud service.
- Only your own messages are read from chat exports, and links, emails and phone numbers are redacted.
- Never commit `.env`, `profile.md`, or anything inside `data/`. They are git-ignored by default.
- A voice clone can be abused for scams. Don't publish voice models, and don't use your cloned voice with anything that relies on voice verification.
- Only clone yourself, or someone who has clearly consented.

## Known limitations

- Voice cloning uses Coqui XTTS. It is a large download, works best with a GPU, uses a non-commercial model license, and is not yet well tested.
- Turning a photo into colors is a simple heuristic. It works best with a centered, well-lit portrait.
- There is no memory between sessions yet.

## Tests

```bash
python -m unittest discover -s tests
```

The tests also run automatically on every push through GitHub Actions.

## License

MIT. See [`LICENSE`](LICENSE).
