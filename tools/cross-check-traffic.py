#!/usr/bin/env python3
"""Cross-check the knitted traffic cops story with secondary sources."""
import subprocess, re, urllib.parse

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try searching for the story
searches = [
    "Fillongley knitted traffic cops slowing speeding drivers",
    "Fillongley Knit and Natter traffic cops speeding",
    "Nuneaton Road Fillongley accidents knitted traffic",
]

for q in searches:
    # Try Bing search
    url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}"
    r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
    
    # Extract visible links
    links = re.findall(r'href="(https?://[^"]+)"', r.stdout)
    # Filter out bing/microsoft links
    relevant = [l for l in links if "bing" not in l.lower() and "microsoft" not in l.lower() and "msn" not in l.lower()]
    print(f"Search: {q}")
    print(f"  Found {len(relevant)} non-bing links")
    for l in relevant[:5]:
        print(f"  -> {l[:150]}")
    print()

# Also try BBC directly
print("=== BBC local news search ===")
url = "https://www.bbc.co.uk/search?q=Fillongley+knitted+traffic+cops"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
links = re.findall(r'href="(/news/[^"]+)"', r.stdout)
print(f"BBC news links: {len(links)}")
for l in links[:5]:
    print(f"  -> https://www.bbc.co.uk{l}")

# Try ITV/Birmingham live
print("\n=== ITV News search ===")
url = "https://www.itv.com/news/search?q=Fillongley+knitted+traffic"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
print(f"ITV length: {len(r.stdout)}")
if "knitted" in r.stdout.lower() or "Fillongley" in r.stdout:
    print("  Found relevant content!")
    # Extract text
    text = re.sub(r"<[^>]+>", " ", r.stdout)
    idx = text.lower().find("fillongley")
    if idx >= 0:
        print(f"  Context: ...{text[max(0,idx-50):idx+200]}...")
