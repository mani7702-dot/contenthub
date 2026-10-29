#!/usr/bin/env python3
"""Get Wikipedia info on inulin and gut microbiome."""
import urllib.request
import re
import json

urls = [
    "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext&titles=Inulin&format=json&formatversion=2",
    "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext&titles=Gut_microbiota&format=json&formatversion=2",
    "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext&titles=Short-chain_fatty_acid&format=json&formatversion=2",
    "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext&titles=Glucagon-like_peptide-1&format=json&formatversion=2",
]

for url in urls:
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read().decode('utf-8', errors='replace'))
        pages = data.get('query', {}).get('pages', [])
        if pages:
            title = pages[0].get('title', '')
            text = pages[0].get('extract', '')
            if text:
                print(f"=== {title} ===")
                print(text[:800])
                print()
            else:
                print(f"=== {title} === (no extract - stub article)")
                print()
    except Exception as e:
        print(f"Error: {e}\n")
