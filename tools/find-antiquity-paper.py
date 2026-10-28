#!/usr/bin/env python3
"""Search for the Antiquity journal paper about Lismore monastery."""
import subprocess, re, html
from urllib.parse import quote

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try searching Cambridge Core (Antiquity journal publisher)
queries = [
    "site:cambridge.org Lismore monastery excavation",
    "site:cambridge.org Clare Ellis Lismore",
    "site:cambridge.org Gordon Noble Lismore",
    "site:cambridge.org Lismore Cathedral archaeology",
]

for q in queries:
    print(f"\n=== Bing: {q} ===")
    search_url = f"https://www.bing.com/search?q={quote(q)}"
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, "-L", search_url], capture_output=True, text=True)
    print(f"Page length: {len(r.stdout)}")
    text = re.sub(r'<script[^>]*>.*?</script>', '', r.stdout, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    # Extract result links and snippets
    results = re.findall(r'<li class="b_algo">(.*?)</li>', r.stdout, re.DOTALL)
    if results:
        for res in results[:5]:
            # Extract URL
            url_match = re.search(r'href="(https?://[^"]+)"', res)
            # Extract title
            title_match = re.search(r'<h2>(.*?)</h2>', res, re.DOTALL)
            # Extract snippet
            snippet_match = re.search(r'<p[^>]*>(.*?)</p>', res, re.DOTALL)
            if url_match and title_match:
                url = url_match.group(1)
                title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
                snippet = re.sub(r'<[^>]+>', '', snippet_match.group(1)).strip() if snippet_match else ""
                print(f"  Title: {title[:150]}")
                print(f"  URL: {url[:200]}")
                print(f"  Snippet: {snippet[:200]}")
                print()
    else:
        # Try generic extraction
        text2 = re.sub(r'<[^>]+>', '\n', r.stdout)
        text2 = html.unescape(text2)
        lines = [l.strip() for l in text2.split('\n') if l.strip() and len(l.strip()) > 50]
        for line in lines[:15]:
            print(line[:300])
