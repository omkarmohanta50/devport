# Connect the Spotify card

1. Open https://developer.spotify.com/dashboard and create or select your app.
2. In its settings register this exact redirect URI, http://127.0.0.1:8765/callback.
3. Run python scripts/connect_spotify.py from the portfolio folder. Enter the app client ID and the client secret when prompted. The secret input is hidden.
4. Open the printed Spotify authorization URL in your browser and approve read access to recently played tracks.
5. The helper validates the callback state and exchanges the code. It saves local credentials in ignored .astro/spotify.json. Keep this file private.
6. Restart python scripts/serve.py. The card at http://127.0.0.1:4323/ reads the latest played track through /api/spotify. It caches the response for two minutes.

For public hosting, use server-side secret storage for SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, and SPOTIFY_REFRESH_TOKEN, and deploy an equivalent /api/spotify server endpoint. The static dist folder alone cannot run that endpoint.

The callback flow needs a free local port 8765 and network access. Account and app eligibility are governed by Spotify's current developer-mode restrictions.

Official guidance
https://developer.spotify.com/documentation/web-api/tutorials/code-flow
https://developer.spotify.com/documentation/web-api/concepts/redirect_uri
