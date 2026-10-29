#!/usr/bin/env python3
"""Search DuckDuckGo HTML for secondary sources on a given query."""
import urllib.request, urllib.parse, re, sys

queries = sys.argv[1:]
for q in queries:
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        text = resp.read().decode("utf-8", errors="replace")
        print(f"\n=== Query: {q} ===")
        print(f"Page length: {len(text)} chars")
        # Debug: look for all result links
        links = re.findall(r'href="([^"]+)"', text)
        result_links = [l for l in links if "duckduckgo.com" not in l and "uddg=" in l]
        print(f"Found {len(result_links)} result links")
        for l in result_links[:8]:
            actual = urllib.parse.parse_qs(urllib.parse.urlparse(l).query).get("uddg", ["unknown"])[0]
            print(f"  URL: {actual[:200]}")
    except Exception as e:
        print(f"Error for {q}: {e}")
