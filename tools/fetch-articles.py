#!/usr/bin/env python3
"""Fetch Reuters and NPR articles about European youth protests."""
import urllib.request, re

articles = {
    "Reuters": "https://www.reuters.com/world/europe/nobody-heard-us-why-gen-z-are-leading-protests-across-europe-2026-10-29/",
    "NPR": "https://www.npr.org/2026/10/29/protests-europe-milan-marseille-madrid",
}

for name, url in articles.items():
    print(f"\n=== {name}: {url} ===")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode("utf-8", errors="replace")
        # Extract title
        title = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
        if title:
            print(f"Title: {title.group(1).strip()[:200]}")
        # Extract meta description
        desc = re.search(r'<meta[^>]*name="description"[^>]*content="(.*?)"', html, re.DOTALL | re.IGNORECASE)
        if desc:
            print(f"Desc: {desc.group(1).strip()[:300]}")
        # Extract body paragraphs
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        for p in paragraphs:
            clean = re.sub(r'<[^>]+>', '', p).strip()
            if len(clean) > 50:
                print(f"  P: {clean[:300]}")
                print("---")
        if not paragraphs:
            texts = re.findall(r'>([^<]{80,400})<', html)
            for t in texts[:15]:
                t = t.strip()
                if len(t) > 60 and not t.startswith(('var ', 'function', '{', 'window', 'http', 'if ')):
                    print(f"  T: {t[:300]}")
    except Exception as e:
        print(f"Error: {e}")