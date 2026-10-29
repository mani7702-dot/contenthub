#!/usr/bin/env python3
"""Fetch secondary sources for cross-checking - try different URLs."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Try the actual Google News decoded URLs for Sci.News and Earth.com
urls = [
    ("Sci.News", "https://scinews.com/"),
    ("ScienceDaily search", "https://www.sciencedaily.com/search/term/?query=dark+energy+einstein+temple"),
    ("Universe Today", "https://www.universetoday.com/"),
]

for name, url in urls:
    print(f"=== {name}: {url} ===")
    p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, url],
                       capture_output=True)
    html = p.stdout.decode("utf-8", errors="replace")
    print(f"Length: {len(html)} bytes")
    print()

# Now try fetching the ScienceDaily search for the paper
print("=== Searching ScienceDaily ===")
search_url = "https://www.sciencedaily.com/search/term/?query=einstein+dark+energy+unstable"
p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, search_url],
                   capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
# Find article links
links = re.findall(r'href="(/releases/[^"]+)"', html)
titles = re.findall(r'<h\d[^>]*>(.*?)</h\d>', html, re.DOTALL)
for i, link in enumerate(links[:10]):
    print(f"LINK: {link}")
if titles:
    for t in titles[:10]:
        text = re.sub(r"<[^>]+>", "", t).strip()
        if text:
            print(f"TITLE: {text[:100]}")
