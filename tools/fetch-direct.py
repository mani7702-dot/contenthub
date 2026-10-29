#!/usr/bin/env python3
"""Try to fetch Reuters and NPR articles directly."""
import urllib.request, re

sources = {
    "Reuters-direct": "https://www.reuters.com/world/europe/nobody-heard-us-why-gen-z-are-leading-protests-across-europe-2026-10-29/",
    "NPR-direct": "https://www.npr.org/2026/10/29/npr-protests-europe-gen-z",
}

for name, url in sources.items():
    print(f"\n=== {name}: {url} ===")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"})
    try:
        resp = urllib.request.urlopen(req, timeout=20)
        html = resp.read().decode("utf-8", errors="replace")
        print(f"Got response: {len(html)} chars")
        title = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
        if title:
            print(f"Title: {title.group(1).strip()[:300]}")
        desc = re.search(r'<meta[^>]*name="description"[^>]*content="(.*?)"', html, re.DOTALL | re.IGNORECASE)
        if desc:
            print(f"Desc: {desc.group(1).strip()[:500]}")
        kw = re.search(r'<meta[^>]*name="keywords"[^>]*content="(.*?)"', html, re.DOTALL | re.IGNORECASE)
        if kw:
            print(f"Keywords: {kw.group(1).strip()[:300]}")
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        for p in paragraphs[:20]:
            clean = re.sub(r'<[^>]+>', '', p).strip()
            if len(clean) > 50:
                print(f"  P: {clean[:400]}")
                print("---")
        if not paragraphs:
            texts = re.findall(r'>([^<]{80,400})<', html)
            count = 0
            for t in texts:
                t = t.strip()
                if len(t) > 60 and not t.startswith(('var ', 'function', '{', 'window', 'http', 'if ', 'goog', 'cookie', 'Sign', 'Subscribe', 'Privacy', 'Terms')):
                    print(f"  T: {t[:300]}")
                    count += 1
                    if count > 10:
                        break
    except Exception as e:
        print(f"Error: {e}")