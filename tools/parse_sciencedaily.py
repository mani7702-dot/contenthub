#!/usr/bin/env python3
"""Parse ScienceDaily top RSS, stripping trailing junk after </rss>."""
import sys, xml.etree.ElementTree as ET, gzip, subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.sciencedaily.com/rss/top.xml"

p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)

text = data.decode("utf-8", "ignore")
idx = text.find("</rss>")
if idx > 0:
    text = text[:idx + 6]

root = ET.fromstring(text)
count = 0
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    d = (it.findtext("description") or "").strip()[:300]
    if len(t) < 20:
        continue
    print(f"TITLE: {t}")
    print(f"URL: {l}")
    print(f"DESC: {d}")
    print("---")
    count += 1
    if count >= 25:
        break
