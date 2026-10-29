#!/usr/bin/env python3
"""Search BBC for Tanzania natural gas article - extract all links."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

url = "https://www.bing.com/news/search?q=Tanzania+natural+gas+discovery+Mnazi+Bay+2026"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, "-L", url], capture_output=True, text=True)
html = r.stdout

# Find all URLs that look like news articles
all_links = re.findall(r'href="(https?://[^"]+)"', html)
seen = set()
for l in all_links:
    if l not in seen and len(l) < 300:
        seen.add(l)
        if any(k in l.lower() for k in ['tanzania', 'gas', 'bbc', 'reuters', 'energy', 'news']):
            print(l)
