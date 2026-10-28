#!/usr/bin/env python3
"""Search via Bing since DuckDuckGo blocked us."""
import re, html, urllib.request, urllib.parse

query = urllib.parse.quote("Kobak 147000 phantom citations AI-generated papers biomedical")
url = f"https://www.bing.com/search?q={query}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"})
try:
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    # extract result snippets
    snippets = re.findall(r'<p[^>]*class="b_lineclamp[^"]*"[^>]*>(.*?)</p>', raw, flags=re.S | re.I)
    if not snippets:
        snippets = re.findall(r'<p[^>]*>(.*?)</p>', raw, flags=re.S | re.I)
    for s in snippets[:12]:
        txt = re.sub(r"<[^>]+>", "", s)
        txt = html.unescape(txt).strip()
        if len(txt) > 30:
            print(txt[:350])
            print("---")
except Exception as e:
    print(f"Error: {e}")
