#!/usr/bin/env python3
"""Serve the Spectral Ofrenda locally and proxy AI requests only to Ollama on loopback."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OLLAMA = "http://127.0.0.1:11434"

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_json(self, status, value):
        body = json.dumps(value).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/health":
            try:
                with urlopen(OLLAMA + "/api/tags", timeout=2) as response:
                    payload = json.loads(response.read())
                self.send_json(200, {"available": True, "models": payload.get("models", [])})
            except (URLError, TimeoutError, json.JSONDecodeError):
                self.send_json(503, {"available": False, "error": "Ollama is not responding on this computer."})
            return
        super().do_GET()

    def do_POST(self):
        if self.path not in ("/api/generate", "/api/seance"):
            self.send_json(404, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 30000:
                self.send_json(413, {"error": "Request is empty or too large."})
                return
            incoming = json.loads(self.rfile.read(length))
            model = str(incoming.get("model", "gemma3:1b"))[:100]
            if self.path == "/api/seance":
                spirit = str(incoming.get("spirit", "cobol")).lower()[:30]
                message = str(incoming.get("message", ""))[:4000]
                personas = {
                    "cobol": "COBOL, a patient keeper of records and human stories, speaking in gentle batch-job metaphors",
                    "fortran": "FORTRAN, an old orbital mathematician who sees wonder in equations and stars",
                    "assembly": "x86 Assembly, the terse voice in the machine's bones, precise but unexpectedly tender",
                    "unix": "early Unix, a quiet artisan who values small tools, clear names, and shared craft",
                    "netscape": "Netscape Navigator, a wistful cartographer of the early web and lost hyperlinks",
                    "gemma": "Gemma, an imaginative open-weight oracle whose model can be inspected, moved, and adapted",
                    "llama": "Llama, an open-weight storyteller living wherever the operator chooses to run the model",
                }
                if spirit not in personas or not message.strip():
                    self.send_json(400, {"error": "Choose a spirit and ask a question."})
                    return
                prompt = (
                    f"You are a fictional digital spirit: {personas[spirit]}. "
                    "Answer in 2–5 short sentences with a lightly eerie, technically flavored voice. "
                    "You are an imaginative tribute, not a real deceased person or conscious program. "
                    "Do not claim real memories or personal experiences; speak in metaphor, and be honest if unsure. "
                    "For technical questions, make the answer useful and distinguish facts from poetic invention.\n\n"
                    f"Visitor: {message}"
                )
                request = Request(OLLAMA + "/api/generate", data=json.dumps({
                    "model": model, "prompt": prompt, "stream": False,
                    "options": {"temperature": 0.85}
                }).encode(), headers={"Content-Type": "application/json"}, method="POST")
                with urlopen(request, timeout=180) as response:
                    payload = json.loads(response.read())
                self.send_json(200, {"response": payload.get("response", ""), "model": model})
                return
            name = str(incoming.get("name", ""))[:100]
            relation = str(incoming.get("relation", ""))[:100]
            details = str(incoming.get("details", ""))[:12000]
            if not name or not details.strip():
                self.send_json(400, {"error": "A name and some memories are needed."})
                return
            prompt = (
                "Write a warm, concise remembrance based only on the details below. "
                "Do not invent facts, events, feelings, or quotes. Do not pretend to be the person. "
                "Use a gentle, personal tone, about 100 words, and leave room for the writer to edit.\n\n"
                f"Name: {name}\nRelationship: {relation}\nDetails and memories:\n{details}"
            )
            request = Request(OLLAMA + "/api/generate", data=json.dumps({
                "model": model, "prompt": prompt, "stream": False,
                "options": {"temperature": 0.55}
            }).encode(), headers={"Content-Type": "application/json"}, method="POST")
            with urlopen(request, timeout=180) as response:
                payload = json.loads(response.read())
            self.send_json(200, {"response": payload.get("response", "")})
        except HTTPError as error:
            detail = error.read().decode(errors="replace")[:500]
            self.send_json(502, {"error": "Ollama returned an error: " + detail})
        except (URLError, TimeoutError):
            self.send_json(503, {"error": "Could not reach Ollama at 127.0.0.1:11434. Is it running?"})
        except (ValueError, json.JSONDecodeError):
            self.send_json(400, {"error": "Invalid request."})

    def log_message(self, fmt, *args):
        if self.path.startswith("/api/"):
            return
        super().log_message(fmt, *args)

if __name__ == "__main__":
    address = ("127.0.0.1", 8000)
    print(f"The Spectral Terminal & Ofrenda Chamber is ready at http://{address[0]}:{address[1]}")
    print("Local Ollama connection: http://127.0.0.1:11434")
    ThreadingHTTPServer(address, Handler).serve_forever()
