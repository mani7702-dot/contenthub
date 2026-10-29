#!/usr/bin/env python3
"""Try to find the University of Michigan press release on SDF."""
import urllib.request
import re

urls = [
    "https://en.wikipedia.org/wiki/Dental_caries",
    "https://en.wikipedia.org/wiki/Silver_diamine_fluoride",
]

for url in urls:
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode('utf-8', errors='replace')
        html2 = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        html2 = re.sub(r'<style[^>]*>.*?</style>', '', html2, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', '\n', html2)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 40]
        
        print(f"=== {url} ===")
        for line in lines[5:25]:
            if any(w in line.lower() for w in ['silver', 'diamine', 'fluoride', 'cavity', 'tooth', 'decay', 'children', 'sdf']):
                print(f"  {line[:300]}")
        print()
    except Exception as e:
        print(f"Error fetching {url}: {e}\n")
