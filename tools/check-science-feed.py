#!/usr/bin/env python3
"""Check ScienceDaily top RSS for fresh science stories."""
import subprocess, xml.etree.ElementTree as ET, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.sciencedaily.com/rss/top.xml"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
try:
    root = ET.fromstring(data)
except ET.ParseError:
    print("PARSE ERROR")
    exit(1)
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    desc = (it.findtext("description") or "").strip()[:300]
    print(f"TITLE: {t}")
    print(f"URL: {link}")
    print(f"DESC: {desc}")
    print()
