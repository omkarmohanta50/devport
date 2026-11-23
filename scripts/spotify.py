import base64
import json
import os
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from threading import Lock

_cache = {}
_valid_until = 0
_lock = Lock()

def last_track():
    global _cache, _valid_until
    with _lock:
        if time.monotonic() < _valid_until:
            return _cache
        client, secret, refresh = (os.getenv(k) for k in (
            "SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET", "SPOTIFY_REFRESH_TOKEN"))
        if not all((client, secret, refresh)):
            path = Path(__file__).resolve().parents[1] / '.astro' / 'spotify.json'
            if not path.exists():
                return {}
            credentials = json.loads(path.read_text())
            client, secret, refresh = (credentials[k] for k in ('client', 'secret', 'refresh'))
        auth = base64.b64encode(f"{client}:{secret}".encode()).decode()
        request = Request("https://accounts.spotify.com/api/token",
                          data=urlencode({"grant_type":"refresh_token", "refresh_token":refresh}).encode(),
                          headers={"Authorization":"Basic "+auth})
        with urlopen(request, timeout=5) as response:
            token = json.load(response)["access_token"]
        request = Request("https://api.spotify.com/v1/me/player/recently-played?limit=1",
                          headers={"Authorization":"Bearer "+token})
        with urlopen(request, timeout=5) as response:
            items = json.load(response)["items"]
        if items:
            track = items[0]["track"]
            images = track["album"]["images"]
            _cache = {"name":track["name"], "url":track["external_urls"]["spotify"],
                      "artist":", ".join(a["name"] for a in track["artists"]),
                      "image":images[-1]["url"] if images else ""}
        else:
            _cache = {}
        _valid_until = time.monotonic() + 120
        return _cache

