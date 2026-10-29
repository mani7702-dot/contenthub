#!/usr/bin/env python3
"""Fetch Wikipedia Exomoon article for cross-checking (Tirith-safe)."""
import subprocess, re

url = "https://en.wikipedia.org/wiki/Lumina_(cosmological_simulation)"
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL | re.IGNORECASE)
for para in paras:
    clean = re.sub(r'<[^>]+>', '', para).strip()
    clean = clean.replace('&#8217;', "'").replace('&#8220;', '"').replace('&#8221;', '"')
    clean = re.sub(r'&#\d+;', '', clean)
    clean = re.sub(r'\s+', ' ', clean)
    if len(clean) > 40:
        print(clean)
        print()
