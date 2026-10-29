#!/usr/bin/env python3
"""Find secondary sources for the autism face processing study."""
import requests
import re

headers = {"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"}

# Search for the study on other news sites
search_queries = [
    "https://www.google.com/search?q=%22autistic+brain+processes+faces+differently%22+yale+nature+mental+health",
    "https://www.google.com/search?q=mcpartland+autism+face+processing+EEG+128+electrodes+nature+mental+health+2026",
]

for sq in search_queries:
    try:
        r = requests.get(sq, headers=headers, timeout=15)
        print(f"Google search Status: {r.status_code}")
        # Extract result URLs
        results = re.findall(r'href="https?://[^"]+"', r.text)
        sciencedaily_refs = [r for r in results if 'sciencedaily' in r]
        other_refs = [r for r in results if 'sciencedaily' not in r and 'google' not in r and 'youtube' not in r][:5]
        print(f"  ScienceDaily refs: {sciencedaily_refs[:3]}")
        print(f"  Other refs: {other_refs[:5]}")
    except Exception as e:
        print(f"Search error: {e}")

# Check Yahoo News / AP for the story
try:
    r = requests.get("https://news.google.com/rss/search?q=autism+face+processing+brain+yale", headers=headers, timeout=15)
    print(f"\nGoogle News RSS Status: {r.status_code}")
    titles = re.findall(r'<title>(.*?)</title>', r.text)
    for t in titles[:10]:
        text = re.sub(r'&[a-z]+;', '', t).strip()
        if 'autism' in text.lower() or 'face' in text.lower():
            print(f"  GN: {text[:200]}")
except Exception as e:
    print(f"Google News RSS error: {e}")
