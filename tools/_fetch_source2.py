#!/usr/bin/env python3
"""Search for a second source on Kikai supervolcano magma replenishment."""
import re
import urllib.request
import json

def fetch_text(url, timeout=20):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=timeout)
    html = resp.read().decode('utf-8', errors='replace')
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

# Try NASA Earth Observatory / Google News / Wikipedia on Kikai caldera
urls = [
    'https://en.wikipedia.org/wiki/Kikai',
    'https://www.sciencedirect.com/science/article/pii/S2613579X2400001X',
]

for url in urls:
    try:
        text = fetch_text(url)
        print(f"=== {url} ===")
        print(text[:3000])
        print()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
