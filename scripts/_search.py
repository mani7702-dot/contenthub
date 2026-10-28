#!/usr/bin/env python3
"""Quick web search via DuckDuckGo to cross-check facts from the BBC article."""
import sys
import json
import urllib.request
import urllib.parse

query = sys.argv[1] if len(sys.argv) > 1 else "OpenAI Navier-Stokes AI proof September 2026"
url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
with urllib.request.urlopen(req, timeout=20) as resp:
    raw = resp.read().decode("utf-8", errors="replace")

import re, html
# extract result snippets
snippets = re.findall(r'result__snippet[^>]*>(.*?)</a>', raw, flags=re.S | re.I)
links = re.findall(r'result__a[^>]*href="([^"]+)"', raw)
for i, s in enumerate(snippets[:8]):
    txt = re.sub(r"<[^>]+>", "", s)
    txt = html.unescape(txt).strip()
    print(f"[{i+1}] {txt[:300]}")
    print()
if not snippets:
    # fallback: just dump text
    txt = re.sub(r"<[^>]+>", " ", raw)
    txt = html.unescape(txt)
    print(txt[:1500])
