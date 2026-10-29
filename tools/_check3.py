#!/usr/bin/env python3
"""Try to find the species name of the Vietnamese giant isopod."""
import urllib.request
import re

# The Listverse article says the species name was inspired by Darth Vader's helmet
# Let's search Wikipedia for isopod species and also try to search for the specific discovery

urls = [
    "https://en.wikipedia.org/wiki/Bathynomus",
]

for url in urls:
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode('utf-8', errors='replace')
        # Look for the species list
        # Find the species list section
        match = re.search(r'species of.*?</ul>', html, re.DOTALL)
        if not match:
            match = re.search(r'<ul>(.*?)</ul>.*?species', html, re.DOTALL | re.IGNORECASE)
        
        # Just extract all text from li elements
        items = re.findall(r'<li>(.*?)</li>', html, re.DOTALL)
        for item in items:
            clean = re.sub(r'<[^>]+>', ' ', item).strip()
            clean = re.sub(r'\s+', ' ', clean)
            if 'bathynomus' in clean.lower() or 'viet' in clean.lower() or 'species' in clean.lower() or 'darth' in clean.lower() or 'vader' in clean.lower():
                print(f"  {clean[:300]}")
    except Exception as e:
        print(f"Error: {e}")
