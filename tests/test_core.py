import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dg.brain import Brain  # noqa: E402
from dg.chats import load_my_messages, parse_whatsapp, redact  # noqa: E402

WA = """12/03/24, 10:15 - Sam: hey are you free tonight
12/03/24, 10:16 - Alex: yeah bro what's the plan
and maybe food too
12/03/24, 10:17 - Sam: <Media omitted>
12/03/24, 10:18 - Alex: call me on +91 98765 43210 or mail a@b.com
12/03/24, 10:19 - Sam: ok see https://x.com/y
[13/03/2024, 09:00:01] Alex: ngl i'm tired lol
"""


class Core(unittest.TestCase):
    def test_parse_multiline_and_formats(self):
        p = parse_whatsapp(WA)
        self.assertEqual(p[1][1], "yeah bro what's the plan and maybe food too")
        self.assertEqual(p[-1], ("Alex", "ngl i'm tired lol"))

    def test_only_my_messages_and_redaction(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "chat.txt").write_text(WA)
            msgs, notes = load_my_messages(d, "alex")
        self.assertEqual(len(msgs), 3)
        self.assertFalse(any("free tonight" in m for m in msgs))
        self.assertIn("call me on [number] or mail [email]", msgs)
        self.assertEqual(notes, [])

    def test_redact(self):
        self.assertEqual(redact("see https://a.com now"), "see [link] now")

    def test_empty_data_still_works(self):
        with tempfile.TemporaryDirectory() as d:
            b = Brain(d)
        self.assertEqual(b.msgs, [])
        self.assertIn("PROFILE", b.system("hi"))

    def test_retrieval_and_style(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "m.json").write_text('["i love spicy noodles","gym at six tomorrow","spicy ramen again lol"]')
            b = Brain(d)
        self.assertTrue(all("spicy" in m for m in b.retrieve("any spicy food?")))
        self.assertIn("Average message length", b.style())
        self.assertIn("REAL PAST MESSAGES", b.system("spicy"))

    def test_friendly_error_when_ollama_down(self):
        import os
        os.environ["OLLAMA_URL"] = "http://127.0.0.1:9"
        with tempfile.TemporaryDirectory() as d:
            b = Brain(d)
        with self.assertRaises(RuntimeError) as ctx:
            b.reply([{"role": "user", "content": "hi"}])
        self.assertIn("ollama.com", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
