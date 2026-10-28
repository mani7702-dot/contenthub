#!/usr/bin/env python3
"""Check Wikipedia for AlphaFold Nobel / phantom citations facts."""
import re, html, urllib.request

urls = {
    "AlphaFold": "https://en.wikipedia.org/wiki/AlphaFold",
    "AI-generated_text": "https://en.wikipedia.org/wiki/AI-generated_text",
}
for name, url in urls.items():
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        paras = re.findall(r"<p[^>]*>(.*?)</p>", raw, flags=re.S | re.I)
        print(f"=== {name} ===")
        count = 0
        for p in paras:
            txt = re.sub(r"<[^>]+>", "", p)
            txt = html.unescape(txt).strip()
            if len(txt) > 50 and ("nobel" in txt.lower() or "fake" in txt.lower() or "hallucinat" in txt.lower() or "citation" in txt.lower() or "slop" in txt.lower() or "phantom" in txt.lower()):
                print(txt[:400])
                print("---")
                count += 1
            if count >= 8:
                break
    except Exception as e:
        print(f"Error fetching {name}: {e}")
    print()
