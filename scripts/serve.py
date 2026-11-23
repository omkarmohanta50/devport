"""Serve the static production preview on loopback."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

root = Path(__file__).resolve().parents[1]
ThreadingHTTPServer(("127.0.0.1", 4323),
                    partial(SimpleHTTPRequestHandler, directory=str(root / "dist"))).serve_forever()
