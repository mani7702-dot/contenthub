#!/usr/bin/env python3
"""Fetch Wikipedia article on Kikai caldera and search for additional sources."""
import re
import urllib.request

def fetch_text(url, timeout=20):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=timeout)
    html = resp.read().decode('utf-8', errors='replace')
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

# Wikipedia Kikai caldera page
urls = [
    'https://en.wikipedia.org/wiki/Kikai_Caldera',
]

for url in urls:
    try:
        text = fetch_text(url)
        print(f"=== {url} ===")
        # Find sections about eruption, magma, Yellowstone, Toba
        sections = []
        for term in ['7300', 'magma', 'supervolcano', 'caldera', 'Yellowstone', 'Toba', 'JAMSTEC', 'seismic', 'replenish', 'recharge', 'Kobe']:
            idx = text.lower().find(term.lower())
            if idx > 0:
                start = max(0, idx - 150)
                end = min(len(text), idx + 600)
                sections.append(f"[{term}] ...{text[start:end]}...")
        if sections:
            print('\n'.join(sections))
        else:
            print(text[:3000])
        print()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
