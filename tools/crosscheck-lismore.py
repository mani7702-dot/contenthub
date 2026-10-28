#!/usr/bin/env python3
"""Search for corroborating sources for the Lismore monastery discovery."""
import subprocess, re, html
from urllib.parse import quote

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

queries = [
    "Lismore Scotland monastery excavation Cathedral Clare Ellis Antiquity",
    '"Lismore Historical Society" archaeology monastery',
    '"Lios Mòr" monastery excavation Scotland archaeology 2026',
    'Gordon Noble Lismore archaeology Scotland',
]

for q in queries:
    print(f"\n=== Bing: {q} ===")
    search_url = f"https://www.bing.com/search?q={quote(q)}"
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, "-L", search_url], capture_output=True, text=True)
    print(f"Page length: {len(r.stdout)}")
    # Extract result snippets
    text = re.sub(r'<script[^>]*>.*?</script>', '', r.stdout, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', text)
    text = html.unescape(text)
    lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 50]
    for line in lines[:20]:
        print(line[:300])
