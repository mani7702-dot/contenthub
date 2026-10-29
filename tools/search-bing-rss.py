#!/usr/bin/env python3
"""Fetch the Bing News RSS and search for the actual article URLs."""
import subprocess, urllib.parse, xml.etree.ElementTree as ET

# Search Bing News via RSS for the study
queries = [
    "excess oxygen magma National Science Review",
    "oxygen reservoir deep inside Earth magma volcano",
]
for q in queries:
    url = f"https://www.bing.com/news/search?q={urllib.parse.quote(q)}&format=RSS"
    p = subprocess.run(["curl", "-s", "--max-time", "15", "-A",
        "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)", url], capture_output=True)
    data = p.stdout
    print(f"\n=== {q} ===")
    try:
        root = ET.fromstring(data)
        for item in root.iter("item"):
            t = (item.findtext("title") or "").strip()
            l = (item.findtext("link") or "").strip()
            d = (item.findtext("description") or "").strip()
            print(f"Title: {t}")
            print(f"URL: {l}")
            print(f"Desc: {d[:300]}")
            print()
    except Exception as e:
        print(f"Error: {e}")
