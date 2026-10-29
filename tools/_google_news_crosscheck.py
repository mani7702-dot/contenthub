#!/usr/bin/env python3
"""Cross-check using Google News RSS search."""
import subprocess, re, xml.etree.ElementTree as ET, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Google News RSS search for "Lumina universe simulation"
url = "https://news.google.com/rss/search?q=Lumina+universe+simulation+Smithsonian+Harvard"
p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)

try:
    root = ET.fromstring(data)
    items = list(root.iter("item"))
    print(f"Google News RSS: {len(items)} results")
    for it in items[:8]:
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        desc = (it.findtext("description") or "").strip()[:200]
        print(f"  - {title}")
        print(f"    {desc}")
        print()
except ET.ParseError as e:
    print(f"Parse error: {e}")
    print(f"Raw data start: {data[:200]}")
