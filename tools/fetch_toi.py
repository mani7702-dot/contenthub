#!/usr/bin/env python3
"""Fetch Times of India article for cross-check details."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://timesofindia.indiatimes.com/world/uk/an-irish-fathers-18-carat-wedding-ring-slipped-off-in-an-italian-stream-three-strangers-searched-for-three-days-found-it-in-the-riverbed-and-flew-to-ireland-to-return-it-to-its-owner/articleshow/135209930.cms"
r = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url], capture_output=True, text=True)
html = r.stdout
print(f"Fetched {len(html)} bytes")

title_match = re.search(r'<title>(.*?)</title>', html)
if title_match:
    print(f"Title: {title_match.group(1).strip()}")

meta = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
if meta:
    print(f"Description: {meta.group(1).strip()}")

# Search for key facts in text
text = re.sub(r"<[^>]+>", " ", html)
text = re.sub(r"\s+", " ", text)
for keyword in ["Mohr", "Malloggi", "Poggi", "Palagi", "Lucca", "hobbit", "days", "Glendalough", "Ryanair"]:
    idx = text.lower().find(keyword.lower())
    if idx > 0:
        print(f"\n[{keyword}]: {text[max(0,idx-60):idx+200]}")
