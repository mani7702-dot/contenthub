#!/usr/bin/env python3
"""Cross-check Lismore discovery via Bing search."""
import subprocess, re, html
from urllib.parse import quote

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

queries = [
    "Lismore Clare Ellis Antiquity monastery archaeology excavation",
    "Lismore Historical Society archaeology monastery Scotland Antiquity",
    'site:archaeology.co.uk OR site:thecourier.co.uk "Lismore" "monastery"',
    "University of Aberdeen Gordon Noble Lismore Antiquity",
]

for q in queries:
    print(f"\n=== Bing: {q} ===")
    search_url = f"https://www.bing.com/search?q={quote(q)}"
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, "-L", search_url], capture_output=True, text=True)
    print(f"Page length: {len(r.stdout)}")
    text = re.sub(r'<script[^>]*>.*?</script>', '', r.stdout, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', text)
    text = html.unescape(text)
    lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 50]
    for line in lines[:20]:
        print(line[:300])
