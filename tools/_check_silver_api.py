#!/usr/bin/env python3
"""Get full Wikipedia text on silver diamine fluoride - simplified."""
import urllib.request
import re

# Wikipedia has an API - let's use it
url = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext&titles=Silver%20diamine%20fluoride&format=json&formatversion=2"

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
resp = urllib.request.urlopen(req, timeout=15)
data = resp.read().decode('utf-8', errors='replace')

import json
parsed = json.loads(data)
pages = parsed.get('query', {}).get('pages', [])
if pages:
    text = pages[0].get('extract', 'No extract available')
    print(text[:3000])
