#!/usr/bin/env python3
"""Get Wikipedia page on Silver diamine fluoride."""
import urllib.request
import re

url = "https://en.wikipedia.org/wiki/Silver_diamine_fluoride"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8', errors='replace')

with open('/tmp/sdf_page.html', 'w') as f:
    f.write(html)

# Look for the content div
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)

# Find mw-parser-output content
parser_match = re.search(r'<div class="mw-parser-output">(.*?)</div>\s*<!-- NewPP', text, re.DOTALL)
if parser_match:
    body = parser_match.group(1)
else:
    body = text

# Get text content
body_text = re.sub(r'<[^>]+>', '\n', body)
body_text = re.sub(r'\n+', '\n', body_text)
body_text = re.sub(r'[ \t]+', ' ', body_text)
lines = [l.strip() for l in body_text.split('\n') if len(l.strip()) > 30]

for line in lines[:40]:
    print(line[:300])
