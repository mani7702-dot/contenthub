#!/usr/bin/env python3
"""Fetch the full Listverse article text for the isopod story."""
import urllib.request
import re

url = "https://listverse.com/2026/10/28/10-animals-discovered-in-the-most-unexpected-places/"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8', errors='replace')

html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', '\n', html)
text = re.sub(r'\n+', '\n', text)
text = re.sub(r'[ \t]+', ' ', text)
lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 40]

# Find the article content - starts after the title appears in content
for i, line in enumerate(lines):
    if 'Scientists often discover' in line:
        # Print all content from here
        for line2 in lines[i:i+80]:
            print(line2[:300])
        break
