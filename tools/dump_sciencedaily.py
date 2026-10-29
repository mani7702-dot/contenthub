#!/usr/bin/env python3
"""Fetch ScienceDaily top RSS items, find one matching keyword, print details."""
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
root = ET.fromstring(data)
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    desc = (it.findtext("description") or "").strip()
    print(f"T: {t}")
    print(f"U: {link}")
    print(f"D: {desc[:300]}")
    print("---")
