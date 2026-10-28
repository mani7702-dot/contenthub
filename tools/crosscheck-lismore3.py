#!/usr/bin/env python3
"""Cross-check: get Wikipedia content via REST API."""
import subprocess, json, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Use Wikipedia REST API for plain text summary
urls = [
    ("Lismore Scotland", "https://en.wikipedia.org/api/rest_v1/page/summary/Lismore,_Scotland"),
    ("Iona Scotland", "https://en.wikipedia.org/api/rest_v1/page/summary/Iona"),
]

for label, url in urls:
    print(f"\n=== {label} ===")
    r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-H", "Accept: application/json", url], capture_output=True)
    try:
        data = json.loads(r.stdout.decode("utf-8", errors="replace"))
        print(f"Title: {data.get('title', 'N/A')}")
        extract = data.get('extract', '')
        print(f"Summary: {extract[:500]}")
    except:
        print(f"Raw: {r.stdout[:200]}")
