# Doppelganger

> ## ⚡ Early preview (v0.1)
> The core experience works today. Voice cloning is experimental, and more features are on the way.
> Feedback and ideas are welcome.

A faceless AI version of you that **thinks, sounds, looks and acts** like you.
**Local-first and private:** no accounts, no cloud services, and none of your personal data in this repo.

| | Out of the box | After you add your own data |
|---|---|---|
| **Think** | Persona from `profile.md` | + learns your writing style from your chats |
| **Sound** | Browser's default voice | Your cloned voice (local, experimental) |
| **Look** | Plain faceless silhouette | Hair / head / clothing colors from your photo |
| **Act** | Sways while thinking, glows green while listening, nods while speaking | Head motion follows your cloned voice |

```
you speak -> browser speech-to-text -> /chat -> persona + your style + local LLM (Ollama) -> reply
          -> /tts (your voice) or browser voice -> avatar animates
```

## Run it

1. Install [Ollama](https://ollama.com) and pull a model: `ollama pull llama3.2`
2. Python 3.9+ is required, nothing else:
   ```bash
   pip install -r requirements.txt     # only Pillow, optional
   cp .env.example .env
   cp profile.example.md profile.md    # describe yourself
   python run.py                       # open http://localhost:5000
   ```
3. Talk with the mic (Chrome/Edge) or type. `python run.py --check` shows what it found.

## Adding yourself later

See [`data/README.md`](data/README.md): chats in `data/chats/`, voice clips in `data/voice/`
(plus `pip install -r requirements-voice.txt`), a portrait in `data/images/`. All git-ignored.

## Privacy and safety

- Everything runs on your machine, including the language model. Nothing is sent to any cloud service.
- Only **your** messages are read from chat exports, with links, emails and phone numbers redacted.
- Never commit `.env`, `profile.md`, or anything in `data/` (git-ignored by default).
- A voice clone can be abused for scams. Don't publish voice models and don't use your cloned
  voice with anything that uses voice verification.
- Only clone yourself, or someone who has clearly consented.

## Known limitations

- Voice cloning uses Coqui XTTS (large download, GPU recommended, non-commercial model license) and is not yet well tested.
- Photo-to-colors is a simple heuristic that works best with a centered, well-lit portrait.
- No memory between sessions yet.

## Tests

`python -m unittest discover -s tests`

## License

MIT
