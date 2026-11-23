"""Serve the built portfolio and its first-party view counter on loopback."""
import json
import sqlite3
import hashlib
import uuid
from http.cookies import SimpleCookie
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

root = Path(__file__).resolve().parents[1]
database = root / ".astro" / "views.sqlite"
database.parent.mkdir(exist_ok=True)
with sqlite3.connect(database) as connection:
    connection.execute("CREATE TABLE IF NOT EXISTS views (id INTEGER PRIMARY KEY, count INTEGER NOT NULL)")
    connection.execute("INSERT OR IGNORE INTO views VALUES (1, 0)")
    connection.execute("CREATE TABLE IF NOT EXISTS visitors (browser TEXT PRIMARY KEY)")

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/api/views":
            return super().do_GET()
        with sqlite3.connect(database) as conn:
            count = conn.execute("SELECT COUNT(*) FROM visitors").fetchone()[0]
        body = json.dumps({"views": count}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/api/views" or urlsplit(self.headers.get("Origin", "")).netloc != self.headers.get("Host"):
            self.send_error(403)
            return
        cookies = SimpleCookie()
        cookies.load(self.headers.get("Cookie", ""))
        try:
            browser = str(uuid.UUID(cookies["portfolio_browser"].value))
        except (KeyError, ValueError):
            browser = str(uuid.uuid4())
        fingerprint = hashlib.sha256(browser.encode()).hexdigest()
        with sqlite3.connect(database) as conn:
            conn.execute("INSERT OR IGNORE INTO visitors VALUES (?)", (fingerprint,))
            count = conn.execute("SELECT COUNT(*) FROM visitors").fetchone()[0]
        body = json.dumps({"views": count}).encode()
        self.send_response(200)
        self.send_header("Set-Cookie", f"portfolio_browser={browser}; Max-Age=31536000; Path=/; HttpOnly; SameSite=Lax")
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

ThreadingHTTPServer(("127.0.0.1", 4323), partial(Handler, directory=str(root / "dist"))).serve_forever()




