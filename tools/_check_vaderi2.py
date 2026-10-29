#!/usr/bin/env python3
"""Get full details from Wikipedia on Bathynomus vaderi."""
import urllib.request
import re

url = "https://en.wikipedia.org/wiki/Bathynomus_vaderi"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8', errors='replace')

html2 = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
html2 = re.sub(r'<style[^>]*>.*?</style>', '', html2, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', '\n', html2)
text = re.sub(r'\n+', '\n', text)
text = re.sub(r'[ \t]+', ' ', text)
lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 30]

# Print everything
for line in lines[10:50]:
    print(line[:300])
