#!/usr/bin/env python3
"""Fetch ScienceDaily top RSS and find the Einstein/dark-energy story."""
import subprocess, xml.etree.ElementTree as ET, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.sciencedaily.com/rss/top.xml"

p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url],
                   capture_output=True)
data = p.stdout
# Strip trailing comment after </rss>
idx = data.find(b"</rss>")
if idx != -1:
    data = data[:idx+6]

root = ET.fromstring(data)
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    if "einstein" in t.lower() or "dark energy" in t.lower():
        print(f"TITLE: {t}")
        print(f"LINK: {l}")
        d = (it.findtext("description") or "").strip()[:500]
        print(f"DESC: {d}")
        print("---")
