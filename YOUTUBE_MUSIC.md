# Connect YouTube Music

The card displays your last track after you connect a local session. The integration uses the unofficial ytmusicapi library. Authentication stays on the server.

1. Run python -m pip install -r scripts/requirements.txt in the Python environment used by the preview.
2. Open https://music.youtube.com in your browser and sign in.
3. Open Developer Tools, select Network, filter by /browse, then click Library.
4. Select a successful authenticated POST request. In its Request Headers section, copy the headers as documented at https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html.
5. Run python scripts/connect_youtube_music.py in a private local terminal. Paste the header lines into the hidden prompts and finish with an empty line. Do not paste them in chat. They contain Google session credentials.
6. Restart python scripts/serve.py and open http://127.0.0.1:4323/. The card requests /api/music and refreshes from history on page load, with a two-minute server cache.

The helper saves .astro/ytmusic.json, covered by .gitignore. This file must stay outside public assets, source control, and static deployment output. For hosting, set YTMUSIC_AUTH_FILE to a private server-side file and deploy the API handler alongside the site. A static dist deployment alone cannot read listening history.

The session can expire or become invalid. Reconnect if the card stays unavailable. The setup and card can be tested locally without publishing listening history. Public deployment will reveal the most recently played track.

The unofficial API can change when YouTube Music changes. Listening history describes the latest recorded track, rather than a real-time playback state.
