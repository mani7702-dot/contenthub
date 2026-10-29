#!/usr/bin/env python3
"""Fetch full Listverse feed to see all items."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
url = "https://listverse.com/feed/"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, "-L", url], capture_output=True, text=True)

import xml.etree.ElementTree as ET
try:
    root = ET.fromstring(r.stdout)
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        print(t)
except Exception as e:
    print("ERR", e)
