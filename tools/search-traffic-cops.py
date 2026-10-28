#!/usr/bin/env python3
"""Search for knitted traffic cops story on multiple sources."""
import subprocess, urllib.parse, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

searches = [
    "Fillongley knitted traffic cops slowing drivers",
    "knitted traffic cops village slowing speeding drivers UK",
    "knitted speed camera mannequins Fillongley",
]

for q in searches:
    url = f"https://www.google.com/search?q={urllib.parse.quote(q)}"
    r = subprocess.run(["curl", "-s", "--max-time", "15", "-A", UA, url], capture_output=True, text=True)
    links = re.findall(r'href="(https?://[^"]+)"', r.stdout)
    relevant = [l for l in links if "goodnewsnetwork" in l or "bbc" in l or "knitted" in l.lower() or "fillongley" in l.lower()]
    print(f"Search: {q}")
    print(f"  Total links: {len(links)}, relevant: {len(relevant)}")
    for l in relevant[:5]:
        print(f"  -> {l[:120]}")
    print()
