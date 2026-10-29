#!/usr/bin/env python3
"""Fetch specific Listverse stories and check details."""
import subprocess, xml.etree.ElementTree as ET, gzip
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Get Listverse feed
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, "https://listverse.com/feed/"], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
root = ET.fromstring(data)
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    link = (it.findtext("link") or "").strip()
    desc = (it.findtext("description") or "").strip()[:500]
    print(f"TITLE: {t}")
    print(f"URL: {link}")
    print(f"DESC: {desc}")
    print()
