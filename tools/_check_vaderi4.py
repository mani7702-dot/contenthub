#!/usr/bin/env python3
"""Get full body text from Bathynomus vaderi Wikipedia page."""
import urllib.request
import re

url = "https://en.wikipedia.org/wiki/Bathynomus_vaderi"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
resp = urllib.request.urlopen(req, timeout=15)
raw = resp.read().decode('utf-8', errors='replace')

# Save to file for inspection
with open('/tmp/vaderi_page.html', 'w') as f:
    f.write(raw)

# Extract text from paragraphs in the body content
# Wikipedia uses <div id="mw-content-text"> 
match = re.search(r'<div id="mw-content-text".*?>(.*?)</div>\s*<!--', raw, re.DOTALL)
if not match:
    match = re.search(r'<div class="mw-parser-output".*?>(.*?)</div>\s*<!--', raw, re.DOTALL)

body = match.group(1) if match else raw

# Get paragraphs
paragraphs = re.findall(r'<p>(.*?)</p>', body, re.DOTALL)
for p in paragraphs:
    clean = re.sub(r'<[^>]+>', ' ', p).strip()
    clean = re.sub(r'\s+', ' ', clean)
    if len(clean) > 30:
        print(clean[:500])
        print()

if not paragraphs:
    print("No paragraphs found, trying broader extraction...")
    # Remove everything except body text
    body_clean = re.sub(r'<script[^>]*>.*?</script>', '', raw, flags=re.DOTALL)
    body_clean = re.sub(r'<style[^>]*>.*?</style>', '', body_clean, flags=re.DOTALL)
    body_clean = re.sub(r'<[^>]+>', '\n', body_clean)
    body_clean = re.sub(r'\n+', '\n', body_clean)
    body_clean = re.sub(r'[ \t]+', ' ', body_clean)
    lines = [l.strip() for l in body_clean.split('\n') if len(l.strip()) > 30]
    # Skip navigation and header stuff
    content_start = False
    for line in lines:
        if 'Bathynomus vaderi' in line and not content_start:
            content_start = True
        if content_start:
            print(line[:300])
