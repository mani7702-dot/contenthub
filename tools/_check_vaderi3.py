#!/usr/bin/env python3
"""Get the main text content from Bathynomus vaderi Wikipedia page."""
import urllib.request
import re

url = "https://en.wikipedia.org/wiki/Bathynomus_vaderi"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8', errors='replace')

# Extract the main content div
# Look for the intro paragraph
paragraphs = re.findall(r'<p>(.*?)</p>', html, re.DOTALL)
print("=== Main paragraphs ===")
for p in paragraphs:
    clean = re.sub(r'<[^>]+>', ' ', p).strip()
    clean = re.sub(r'\s+', ' ', clean)
    if len(clean) > 50 and not clean.startswith('This page'):
        print(clean[:400])
        print()
