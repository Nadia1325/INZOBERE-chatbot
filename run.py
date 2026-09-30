"""Serve the Inzobere website and its local TF-IDF/GloVe search endpoint."""

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import webbrowser


ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 8000
_matcher = None
_matcher_lock = threading.Lock()


def get_matcher():
    global _matcher
    if _matcher is None:
        with _matcher_lock:
            if _matcher is None:
                from semantic_search import FAQMatcher
                _matcher = FAQMatcher()
    return _matcher


class InzobereHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_POST(self):
        if self.path != "/api/search":
            self.send_error(404, "Not found")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 16_384:
                raise ValueError("Request body is empty or too large")
            payload = json.loads(self.rfile.read(length))
            question = str(payload.get("question", "")).strip()
            mode = str(payload.get("mode", "hybrid"))
            if not question:
                raise ValueError("Enter a question")
            results = get_matcher().search(question, mode)
            self._json(200, {"results": results, "mode": mode})
        except (ValueError, json.JSONDecodeError) as error:
            self._json(400, {"error": str(error)})
        except Exception as error:
            self.log_error("search failed: %s", error)
            self._json(503, {
                "error": "Search is unavailable.",
                "detail": f"{type(error).__name__}: {error}",
            })

    def _json(self, status, data):
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), InzobereHandler)
    url = f"http://{HOST}:{PORT}/index.html"
    print(f"Inzobere is running at {url} (Ctrl+C to stop).")
    print("English hybrid search downloads GloVe on its first use.")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Inzobere.")
    finally:
        server.server_close()
