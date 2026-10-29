#!/usr/bin/env python3
"""Get full Wikipedia text on silver diamine fluoride - API approach."""
import urllib.request
import json

url = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext&titles=Silver_diamine_fluoride&format=json&formatversion=2"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
resp = urllib.request.urlopen(req, timeout=15)
raw = resp.read().decode('utf-8', errors='replace')
print(f"Response length: {len(raw)}")
print(f"Response: {raw[:2000]}")
parsed = json.loads(raw)
pages = parsed.get('query', {}).get('pages', [])
if pages:
    text = pages[0].get('extract', 'No extract available')
    print(f"\n=== Article text ({len(text)} chars) ===")
    print(text[:3000])
else:
    print("No pages found")
    print(json.dumps(parsed, indent=2))
