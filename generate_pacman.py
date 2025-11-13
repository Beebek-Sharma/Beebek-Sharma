#!/usr/bin/env python3
"""
generate_pacman.py
Fetches pacman-style GitHub contribution SVGs (light & dark) and writes them to files.
Designed to be run inside GitHub Actions.
"""

import os
import sys
import time
from typing import Tuple
import requests

# === CONFIG ===
USERNAME = "Beebek-Sharma"  # <- make sure this is your GitHub username
OUTPUT_LIGHT = "pacman-contribution-graph.svg"
OUTPUT_DARK = "pacman-contribution-graph-dark.svg"

# Public service endpoint that returns pacman-style SVGs.
# If you prefer a different provider, replace these URLs.
API_BASE = "https://github-contribution-stats.vercel.app/api/pacman"

# HTTP settings
TIMEOUT = 15
RETRY = 3
RETRY_DELAY = 2  # seconds

def fetch_svg(username: str, theme: str) -> str:
    """
    Fetch an SVG from the API. Retries on transient errors.
    """
    url = f"{API_BASE}?username={username}&theme={theme}"
    last_exc = None
    for attempt in range(1, RETRY + 1):
        try:
            resp = requests.get(url, timeout=TIMEOUT)
            resp.raise_for_status()
            text = resp.text
            if not text.strip():
                raise ValueError("Empty response from SVG API")
            return text
        except Exception as exc:
            last_exc = exc
            if attempt < RETRY:
                time.sleep(RETRY_DELAY)
            else:
                raise
    raise last_exc

def write_if_changed(path: str, content: str) -> bool:
    """
    Write `content` to `path` only if it differs. Returns True if written (changed).
    """
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                old = f.read()
            if old == content:
                print(f"No change for {path}")
                return False
        except Exception:
            # fallback to write
            pass
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {path}")
    return True

def main() -> int:
    try:
        svg_light = fetch_svg(USERNAME, "light")
        svg_dark = fetch_svg(USERNAME, "dark")
    except Exception as e:
        print("Error fetching SVGs:", str(e))
        return 2

    changed_light = write_if_changed(OUTPUT_LIGHT, svg_light)
    changed_dark = write_if_changed(OUTPUT_DARK, svg_dark)

    if changed_light or changed_dark:
        print("One or more SVGs changed.")
        # Exit 0 so workflow proceeds to commit step which will commit the files.
        return 0
    else:
        print("No changes to SVGs.")
        # Exit 0 as well (no changes) — commit step in workflow will handle gracefully.
        return 0

if __name__ == "__main__":
    sys.exit(main())
