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
        links = re.findall(r'result__a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', text)
        snippets = re.findall(r'result__snippet[^>]*>(.*?)</a>', text, re.DOTALL)
        print(f"\n=== Query: {q} ===")
        count = 0
        for i, (link, title) in enumerate(links[:8]):
            clean_title = re.sub(r"<[^>]+>", "", title).strip()
            # DDG redirect links
            actual = link
            if "uddg=" in link:
                actual = urllib.parse.parse_qs(urllib.parse.urlparse(link).query).get("uddg", [link])[0]
            if not actual.startswith("http"):
                continue
            print(f"  [{count}] Title: {clean_title}")
            print(f"      URL: {actual[:200]}")
            if i < len(snippets):
                snip_text = re.sub(r"<[^>]+>", "", snippets[i]).strip()
                print(f"      Snippet: {snip_text[:300]}")
            count += 1
            if count >= 5:
                break
    except Exception as e:
        print(f"Error for {q}: {e}")
