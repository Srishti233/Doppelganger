"""HTTP server: the web UI plus /status, /chat and /tts."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import avatar, config, voice
from .brain import Brain

WEB = config.ROOT / "web" / "index.html"
brain = None


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, ctype, payload):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _json(self, code, obj):
        self._send(code, "application/json", json.dumps(obj).encode())

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, "text/html; charset=utf-8", WEB.read_bytes())
        elif self.path == "/status":
            self._json(200, {"name": config.get("DOPPELGANGER_NAME", "Me"),
                             "voice": voice.available(), "palette": avatar.palette(),
                             "messages": len(brain.msgs)})
        else:
            self._send(404, "text/plain", b"Not found")

    def do_POST(self):
        try:
            n = min(int(self.headers.get("Content-Length", 0)), 1_000_000)
            data = json.loads(self.rfile.read(n) or b"{}")
            if self.path == "/chat":
                self._json(200, {"reply": brain.reply(data.get("messages") or [])})
            elif self.path == "/tts":
                if not voice.available():
                    return self._json(501, {"error": "voice cloning not active"})
                self._send(200, "audio/wav", voice.synthesize(str(data.get("text", ""))[:1000]))
            else:
                self._send(404, "text/plain", b"Not found")
        except Exception as e:
            self._json(500, {"error": str(e)})

    def log_message(self, *args):
        pass


def serve():
    global brain
    brain = Brain()
    host, port = config.get("HOST", "127.0.0.1"), int(config.get("PORT", "5000"))
    print(f"Doppelganger running at http://localhost:{port}  (Ctrl+C to stop)")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
