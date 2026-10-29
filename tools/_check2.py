#!/usr/bin/env python3
"""Search for second source on Vietnamese giant isopod new species."""
import urllib.request
import re

# Try to find the species name - might be Bathynomus vkll? or something similar
# Let's search for it
search_urls = [
    "https://en.wikipedia.org/wiki/Bathynomus",
]

for url in search_urls:
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode('utf-8', errors='replace')
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', '\n', html)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 40]
        
        # Look for species info
        print(f"=== {url} (showing lines about Vietnam/species/name) ===")
        for line in lines:
            if 'viet' in line.lower() or 'species' in line.lower() or 'isopod' in line.lower() or 'bathynomus' in line.lower():
                print(line[:300])
        print()
    except Exception as e:
        print(f"Error: {e}\n")

# Also try to get the actual Listverse article description which mentioned the species name
# Let's also try Wikipedia for "Giant isopod" which had truncated content
