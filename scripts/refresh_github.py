"""Fetch public GitHub data for the static build without committing snapshots."""
import calendar
import json
import os
import re
import time
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]


def fetch(url):
    headers = {"User-Agent": "devport-github-refresh"}
    if url.startswith("https://api.github.com/") and os.getenv("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=headers), timeout=30) as response:
                return response.read()
        except (URLError, TimeoutError) as error:
            if isinstance(error, HTTPError) and error.code not in (429, 500, 502, 503, 504):
                raise
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


class ContributionCalendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = {}
        self.counts = {}
        self.tooltip = None
        self.text = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "td" and "data-date" in attrs:
            self.days[attrs["id"]] = (attrs["data-date"], int(attrs["data-level"]))
        if tag == "tool-tip" and "for" in attrs:
            self.tooltip = attrs["for"]
            self.text = ""

    def handle_data(self, data):
        if self.tooltip:
            self.text += data

    def handle_endtag(self, tag):
        if tag == "tool-tip" and self.tooltip:
            match = re.match(r"\s*(No|[\d,]+) contributions?", self.text)
            if match:
                self.counts[self.tooltip] = 0 if match[1] == "No" else int(match[1].replace(",", ""))
            self.tooltip = None


def contributions(login, year):
    parser = ContributionCalendar()
    parser.feed(fetch(f"https://github.com/users/{login}/contributions?from={year}-01-01&to={year}-12-31").decode())
    days = [{"date": date, "count": parser.counts[key], "level": level}
            for key, (date, level) in parser.days.items()]
    days.sort(key=lambda day: day["date"])
    expected = 366 if calendar.isleap(year) else 365
    if (len(days) != expected or len({day['date'] for day in days}) != expected
            or days[0]['date'] != f'{year}-01-01' or days[-1]['date'] != f'{year}-12-31'
            or any(not 0 <= day['level'] <= 4 or day['count'] < 0 for day in days)):
        raise ValueError(f"Incomplete or invalid contribution calendar for {login}")
    return days


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def main():
    updates = {}
    year = datetime.now(timezone.utc).year
    for login, filename in (("omkarmohanta09", "contributions.json"),
                            ("omkarmohanta50", "personal-contributions.json")):
        profile = json.loads(fetch("https://api.github.com/users/" + login))
        if profile["login"].lower() != login:
            raise ValueError("Unexpected GitHub profile")
        metadata = {"login": profile["login"], "name": profile["name"], "bio": profile["bio"],
                    "repos": profile["public_repos"], "followers": profile["followers"]}
        updates[f"src/data/{login}.json"] = encode(metadata)
        image = fetch(profile["avatar_url"])
        if not image.startswith((b"\xff\xd8", b"\x89PNG")):
            raise ValueError("Unexpected avatar response")
        updates[f"public/images/{login}.jpg"] = image
        updates[f"src/data/{filename}"] = encode(contributions(login, year))

    result = json.loads(fetch("https://api.github.com/search/issues?q=author:omkarmohanta09+org:vegastack+is:pr+is:merged&sort=updated&per_page=100"))
    if result.get("incomplete_results"):
        raise ValueError("GitHub returned incomplete contribution results")
    counts = Counter(item["pull_request"]["merged_at"][:10] for item in result["items"])
    updates["src/data/activity.json"] = encode([
        {"day": day, "Count": count} for day, count in sorted(counts.items(), reverse=True)
    ])
    # All external reads and validation finish before any local snapshot changes.
    for relative, content in updates.items():
        (ROOT / relative).write_bytes(content)
    print(f"Refreshed both public GitHub profiles and {year} calendars.")


if __name__ == "__main__":
    main()
