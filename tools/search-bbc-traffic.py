#!/usr/bin/env python3
"""Search BBC and other UK news for knitted traffic cops in Fillongley."""
import subprocess, re, urllib.parse

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try BBC search
queries = [
    "Fillongley knitted traffic cops speeding",
    "Warwickshire knitted traffic cones speeding village",
]

for q in queries:
    url = f"https://www.bbc.co.uk/search?q={urllib.parse.quote(q)}"
    r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
    # Extract result links
    links = re.findall(r'href="(/news/[^"]+)"', r.stdout)
    print(f"Query: {q}")
    print(f"  Found {len(links)} BBC news links")
    for l in links[:5]:
        print(f"  -> https://www.bbc.co.uk{l}")
    print()
