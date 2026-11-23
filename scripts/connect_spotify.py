"""Authorize the portfolio's Spotify card using a loopback OAuth callback."""
import base64
import getpass
import json
import secrets
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import Request, urlopen

redirect = "http://127.0.0.1:8765/callback"
client = input("Spotify app client ID: ").strip()
secret = getpass.getpass("Spotify app client secret (hidden): ").strip()
state = secrets.token_urlsafe(32)
result = {}

class Callback(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        params = parse_qs(urlsplit(self.path).query)
        valid = urlsplit(self.path).path == "/callback" and secrets.compare_digest(params.get("state", [""])[0], state)
        if not valid:
            self.send_error(400)
            return
        result.update(params)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Authorization received. Return to the terminal.")

server = HTTPServer(("127.0.0.1", 8765), Callback)
server.timeout = 300
url = "https://accounts.spotify.com/authorize?" + urlencode({
    "client_id": client, "response_type": "code", "redirect_uri": redirect,
    "scope": "user-read-recently-played", "state": state})
print("Open this authorization link in your browser:")
print(url)
try:
    server.handle_request()
finally:
    server.server_close()
if "code" not in result:
    raise SystemExit("Authorization was declined or timed out.")
authorization = base64.b64encode(f"{client}:{secret}".encode()).decode()
request = Request("https://accounts.spotify.com/api/token",
    data=urlencode({"grant_type":"authorization_code", "code":result["code"][0], "redirect_uri":redirect}).encode(),
    headers={"Authorization":"Basic "+authorization})
with urlopen(request, timeout=15) as response:
    token = json.load(response)
credentials = Path(__file__).resolve().parents[1] / ".astro" / "spotify.json"
credentials.parent.mkdir(exist_ok=True)
credentials.write_text(json.dumps({"client":client, "secret":secret, "refresh":token["refresh_token"]}))
print("Spotify connected locally. Restart the portfolio preview server.")
