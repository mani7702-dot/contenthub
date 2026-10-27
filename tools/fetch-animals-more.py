#!/usr/bin/env python3
"""Fetch more animal stories from all three animal feeds."""
import subprocess, xml.etree.ElementTree as ET, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

feeds = [
    ("Good News Network", "https://www.goodnewsnetwork.org/feed/"),
    ("BBC Earth", "https://www.bbc.co.uk/news/science_env/rss"),
    ("ScienceDaily animals", "https://www.sciencedaily.com/news/plants_animals/animals/"),
]

for label, url in feeds:
    try:
        p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
        data = p.stdout
        if data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)
        root = ET.fromstring(data)
        items = []
        for it in root.iter("item"):
            t = (it.findtext("title") or "").strip()
            if t and len(t) > 25:
                items.append(t)
        print(f"=== {label} ({len(items)} items) ===")
        for t in items[:15]:
            print(f"  {t}")
    except Exception as e:
        print(f"=== {label} === ERROR: {e}")
