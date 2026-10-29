#!/usr/bin/env python3
"""Get full Wikipedia text on silver diamine fluoride."""
import urllib.request
import re

url = "https://en.wikipedia.org/wiki/Silver_diamine_fluoride"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8', errors='replace')

html2 = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
html2 = re.sub(r'<style[^>]*>.*?</style>', '', html2, flags=re.DOTALL)

# Extract main content paragraphs
paragraphs = re.findall(r'<p>(.*?)</p>', html2, re.DOTALL)
for p in paragraphs:
    clean = re.sub(r'<[^>]+>', ' ', p).strip()
    clean = re.sub(r'\s+', ' ', clean)
    if len(clean) > 50:
        print(clean[:400])
        print()
