#!/usr/bin/env python3
"""Fetch all ScienceDaily top RSS items for manual grep-dedup."""
import subprocess, xml.etree.ElementTree as ET, gzip

url = "https://www.sciencedaily.com/rss/top.xml"
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
idx = data.rfind(b"</rss>")
if idx != -1:
    data = data[:idx+6]
try:
    root = ET.fromstring(data)
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        if t and len(t) >= 25:
            print(t)
except Exception as e:
    print(f"Error: {e}")
