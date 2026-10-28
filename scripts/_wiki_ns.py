#!/usr/bin/env python3
"""Fetch Wikipedia article for fact-checking the Navier-Stokes claim."""
import re, html, urllib.request

url = "https://en.wikipedia.org/wiki/Navier%E2%80%93Stokes_existence_and_smoothness"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
with urllib.request.urlopen(req, timeout=25) as resp:
    raw = resp.read().decode("utf-8", errors="replace")

# get first paragraph content
paras = re.findall(r"<p[^>]*>(.*?)</p>", raw, flags=re.S | re.I)
for p in paras[:15]:
    txt = re.sub(r"<[^>]+>", "", p)
    txt = html.unescape(txt).strip()
    if len(txt) > 40:
        print(txt)
        print("---")
