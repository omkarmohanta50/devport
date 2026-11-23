"""Keep pasted browser headers local and hidden during setup."""
from getpass import getpass
from pathlib import Path
from ytmusicapi import setup

path = Path(__file__).resolve().parents[1] / ".astro" / "ytmusic.json"
path.parent.mkdir(exist_ok=True)
print("Paste YouTube Music request headers one line at a time. Input is hidden.")
print("Finish with an empty line. JSON headers may be pasted as one line.")
lines = []
while True:
    line = getpass("")
    if not line:
        break
    lines.append(line)
if not lines:
    raise SystemExit("No headers entered.")
setup(filepath=str(path), headers_raw="\n".join(lines).replace("\\n", "\n"))
print("Local session saved. Restart the portfolio preview.")
