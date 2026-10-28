#!/usr/bin/env python3
"""Search for independent second source on the Italian hobbits wedding ring story."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try CBC As it Happened search
search_terms = [
    "https://www.google.com/search?q=patrick+mohr+italian+hobbits+wedding+ring+cbc",
    "https://www.google.com/search?q=3+italian+hobbits+wedding+ring+ireland+glendalough",
]

# Let's try fetching from a search engine results
for url in search_terms:
    print(f"=== Searching: {url[:80]} ===")
    r = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
    html = r.stdout
    # Extract visible text snippets
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    # Find relevant snippets
    for keyword in ["Mohr", "hobbit", "ring", "Poggi", "Malloggi", "Palagi", "Glendalough"]:
        idx = text.find(keyword)
        if idx > 0:
            print(f"  [{keyword}]: ...{text[max(0,idx-100):idx+200]}...")
            print()
    print()
