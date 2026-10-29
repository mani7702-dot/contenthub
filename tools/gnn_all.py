#!/usr/bin/env python3
"""Fetch all GNN feed items (no keyword filter)."""
import subprocess, xml.etree.ElementTree as ET
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, "https://www.goodnewsnetwork.org/feed/"], capture_output=True)
try:
    root = ET.fromstring(p.stdout)
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        print(t)
except Exception as e:
    print("ERR", e)
