#!/usr/bin/env python3
"""Cross-check the Lismore archaeological discovery via the Antiquity journal / university."""
import subprocess, re, html
from urllib.parse import quote

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Search for the research paper
queries = [
    "Lismore Clare Ellis Antiquity archaeological excavation monastery",
    "Lismore Historical Society archaeology monastery Christian evangelism",
    '"Lismore" "Antiquity" "monastery" archaeology',
]

for q in queries:
    print(f"\n=== DuckDuckGo: {q} ===")
    search_url = f"https://html.duckduckgo.com/html/?q={quote(q)}"
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, "-L", search_url], capture_output=True, text=True)
    print(f"Page length: {len(r.stdout)}")
    text = re.sub(r'<script[^>]*>.*?</script>', '', r.stdout, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', text)
    text = html.unescape(text)
    lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 50]
    for line in lines[:20]:
        print(line[:300])
