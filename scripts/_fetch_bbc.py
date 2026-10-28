#!/usr/bin/env python3
"""Fetch BBC article body text for cross-checking."""
import sys
import re
import html
import urllib.request

url = sys.argv[1] if len(sys.argv) > 1 else "https://www.bbc.co.uk/news/articles/c6gelgxjwzdzo"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
with urllib.request.urlopen(req, timeout=30) as resp:
    raw = resp.read().decode("utf-8", errors="replace")

# strip scripts/styles
raw = re.sub(r"<script[^>]*>.*?</script>", "", raw, flags=re.S | re.I)
raw = re.sub(r"<style[^>]*>.*?</style>", "", raw, flags=re.S | re.I)

paras = re.findall(r"<p[^>]*>(.*?)</p>", raw, flags=re.S | re.I)
out = []
for p in paras:
    txt = re.sub(r"<[^>]+>", "", p)
    txt = html.unescape(txt).strip()
    if len(txt) > 40:
        out.append(txt)
print("\n\n".join(out[:80]))
