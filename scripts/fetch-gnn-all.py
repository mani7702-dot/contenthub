#!/usr/bin/env python3
"""Fetch ALL headlines from the GNN RSS feed (no keyword filtering) with URLs."""
import subprocess, xml.etree.ElementTree as ET, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.goodnewsnetwork.org/feed/"

p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
root = ET.fromstring(data)

for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    desc = (it.findtext("description") or "").strip()
    if t and len(t) >= 25:
        print(f"TITLE: {t}")
        print(f"URL: {link}")
        print(f"DESC: {desc[:300]}")
        print("---")
