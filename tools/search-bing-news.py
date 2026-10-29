#!/usr/bin/env python3
"""Search Bing News for a story and extract news outlet links."""
import subprocess, sys, re, urllib.parse

query = sys.argv[1]
encoded = urllib.parse.quote(query)
url = f"https://www.bing.com/news/search?q={encoded}"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, "--compressed", url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Find all article links
links = re.findall(r'href="(https?://[^"]+)"', html)
outlets = ["cbs", "nbc", "abc", "fox", "usatoday", "dallasnews", "star-telegram", "dallasobserver", "wfaa", "kdfw", "kxas", "click2houston", "khou"]
for l in links:
    if any(d in l.lower() for d in outlets):
        print(l)
