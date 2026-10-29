#!/usr/bin/env python3
"""Fetch article snippets from Google News RSS."""
import urllib.request, re, html as htmlmod

# Get descriptions from Google News RSS
search_urls = [
    "https://news.google.com/rss/search?q=Gen+Z+protests+Europe+October+2026&hl=en-US&gl=US&ceid=US:en",
]

for url in search_urls:
    print(f"\n=== {url} ===")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        xml = resp.read().decode("utf-8", errors="replace")
        items = re.findall(r'<item>(.*?)</item>', xml, re.DOTALL)
        print(f"Found {len(items)} items")
        for item in items[:10]:
            title = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
            desc = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
            if title and desc:
                t = htmlmod.unescape(title.group(1).strip())
                d = htmlmod.unescape(desc.group(1).strip())
                d = re.sub(r'<[^>]+>', '', d).strip()
                print(f"\nTITLE: {t[:200]}")
                print(f"DESC: {d[:500]}")
    except Exception as e:
        print(f"Error: {e}")