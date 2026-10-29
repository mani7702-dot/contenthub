#!/usr/bin/env python3
"""Search for a second source on the giant isopod new species discovery."""
import urllib.request
import re
import sys

# Try to find Wikipedia info on giant isopods
# Also try to find the original research
queries = [
    "https://en.wikipedia.org/wiki/Giant_isopod",
    "https://en.wikipedia.org/wiki/Bathynomus",
]

for url in queries:
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
        print(f"=== {url} ===")
        for line in lines[:20]:
            print(line[:200])
        print("\n")
    except Exception as e:
        print(f"Error fetching {url}: {e}\n")
