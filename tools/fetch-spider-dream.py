#!/usr/bin/env python3
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Find the ScienceDaily URL for the spiders dream story
# Let's fetch the full RSS feed and extract the item
import xml.etree.ElementTree as ET, gzip

url = "https://www.sciencedaily.com/rss/top.xml"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
idx = data.rfind(b"</rss>")
if idx >= 0:
    data = data[:idx+6]
root = ET.fromstring(data)
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    if "spiders dream" in t.lower() or "spiders" in t.lower():
        link = (it.findtext("link") or "").strip()
        desc = (it.findtext("description") or "").strip()
        print(f"Title: {t}")
        print(f"URL: {link}")
        print(f"Desc: {desc}")