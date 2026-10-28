#!/usr/bin/env python3
"""Try to find secondary sources for the Fillongley knitted traffic cops story."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Try Google News search
url = "https://news.google.com/search?q=Fillongley%20knitted%20traffic%20cops"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
stdout = r.stdout
print(f"Google News length: {len(stdout)}")

# Extract links
links = re.findall(r'href="(https?://[^"]+)"', stdout)
relevant = [l for l in links if "google" not in l.lower() and "w3.org" not in l.lower()]
print(f"Relevant links: {len(relevant)}")
for l in relevant[:10]:
    print(f"  -> {l[:200]}")

# Extract readable text snippets
text = re.sub(r"<[^>]+>", " ", stdout)
text = re.sub(r"\s+", " ", text).strip()
idx = text.lower().find("fillongley")
if idx >= 0:
    print(f"\nContext: ...{text[max(0,idx-50):idx+300]}...")
else:
    print("Fillongley not found in Google News text")

# Also try the Coventry Telegraph / Birmingham Live (local Warwickshire news)
print("\n=== Birmingham Live ===")
url = "https://www.birminghammail.co.uk/all-news"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
print(f"Birmingham Mail length: {len(r.stdout)}")
if "fillongley" in r.stdout.lower():
    print("Found Fillongley mention!")

# Try search on Birmingham Live
print("\n=== Birmingham Live search ===")
url = "https://www.birminghammail.co.uk/search/?q=fillongley+knitted+traffic"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
print(f"Search length: {len(r.stdout)}")
text = re.sub(r"<[^>]+>", " ", r.stdout)
text = re.sub(r"\s+", " ", text).strip()
idx = text.lower().find("fillongley")
if idx >= 0:
    print(f"Context: ...{text[max(0,idx-50):idx+300]}...")
else:
    print("Fillongley not found in search results")
