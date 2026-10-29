#!/usr/bin/env python3
"""Fetch Reuters and NPR articles about European youth protests via Google News RSS."""
import urllib.request, re, json

# Try Google News RSS for secondary sources
urls = [
    "https://news.google.com/rss/search?q=Gen+Z+protests+Europe+October+2026&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=European+students+protest+future&hl=en-US&gl=US&ceid=US:en",
]

for url in urls:
    print(f"\n=== {url} ===")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        xml = resp.read().decode("utf-8", errors="replace")
        # Parse RSS items
        items = re.findall(r'<item>(.*?)</item>', xml, re.DOTALL)
        print(f"Found {len(items)} items")
        for item in items[:10]:
            title = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
            link = re.search(r'<link>(.*?)</link>', item, re.DOTALL)
            desc = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
            if title:
                print(f"  Title: {re.sub(r'&#39;|&amp;', '', title.group(1).strip())[:200]}")
            if link:
                print(f"  Link: {link.group(1).strip()}")
            if desc:
                d = re.sub(r'<[^>]+>', '', desc.group(1)).strip()
                print(f"  Desc: {d[:200]}")
                print("---")
    except Exception as e:
        print(f"Error: {e}")