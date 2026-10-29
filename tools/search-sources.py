#!/usr/bin/env python3
"""Search for secondary sources on European youth protests October 2026."""
import urllib.request, re, json

# Search Euronews
urls = [
    "https://www.euronews.com/search?q=student+protest+france+october+2026",
    "https://www.euronews.com/search?q=youth+protest+europe+2026",
    "https://news.google.com/rss/search?q=student+protest+europe+2026&hl=en-US&gl=US&ceid=US:en",
]

for url in urls:
    print(f"\n=== {url} ===")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode("utf-8", errors="replace")
        # Find links
        links = re.findall(r'href="(https?://[^"]*euronews[^"]*)"', html)
        if links:
            print(f"Found {len(links)} euronews links")
            for l in links[:5]:
                print(f"  {l}")
        # Find article snippets
        texts = re.findall(r'>([^<]{60,300})<', html)
        for t in texts[:10]:
            t = t.strip()
            if len(t) > 50 and "protest" in t.lower():
                print(f"  SNIPPET: {t[:200]}")
    except Exception as e:
        print(f"Error: {e}")