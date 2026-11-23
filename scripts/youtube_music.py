"""Expose only the latest public track metadata from a private YT Music session."""
import os
import re
import time
from pathlib import Path
from threading import Lock

_cache = {}
_until = 0
_lock = Lock()

def last_track():
    global _cache, _until
    with _lock:
        if time.monotonic() < _until:
            return _cache
        auth = Path(os.getenv("YTMUSIC_AUTH_FILE", str(Path(__file__).resolve().parents[1] / ".astro" / "ytmusic.json")))
        if not auth.is_file():
            return {}
        from ytmusicapi import YTMusic
        history = YTMusic(str(auth), requests_timeout=10).get_history()
        track = next((row for row in history if re.fullmatch(r"[A-Za-z0-9_-]{11}", row.get("videoId", ""))), None)
        if track:
            thumbs = track.get("thumbnails", [])
            _cache = {
                "name": track.get("title", "Unknown track"),
                "artist": ", ".join(a["name"] for a in track.get("artists", []) if a.get("name")),
                "url": "https://music.youtube.com/watch?v=" + track["videoId"],
                "image": thumbs[-1]["url"] if thumbs else "",
            }
        else:
            _cache = {}
        _until = time.monotonic() + 120
        return _cache
