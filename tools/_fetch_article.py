#!/usr/bin/env python3
"""Fetch and extract text from a single URL for cross-checking."""
import re
import sys
import urllib.request
import json

def fetch_text(url, timeout=20):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=timeout)
    html = resp.read().decode('utf-8', errors='replace')
    # Remove script/style
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

if __name__ == '__main__':
    url = sys.argv[1]
    try:
        text = fetch_text(url)
        # Print a relevant chunk - find the main article
        # Look for the article body
        snippets = []
        # Find key terms
        for term in ['magma', 'supervolcano', 'Kikai', 'caldera', 'Japan', 'eruption']:
            idx = text.lower().find(term.lower())
            if idx > 0:
                start = max(0, idx - 200)
                end = min(len(text), idx + 800)
                snippets.append(f"[{term}] ...{text[start:end]}...")
        print('\n'.join(snippets))
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
