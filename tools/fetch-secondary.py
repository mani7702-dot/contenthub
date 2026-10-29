#!/usr/bin/env python3
"""Fetch the Reuters article via Google News proxy to verify facts."""
import urllib.request, re

url = "https://news.google.com/rss/articles/CBMirgFBVV95cUxPYjU3YkZqYTlQelp5OVJKRi1EN2pYVThKWGZRUDZQNlozeFk5OXBzbGo2THREaDdxZ05EOE9OYnViV2ZEYWJwRUNZb09LQk40NzhWMjc1c2pjeElGTUE0eFIzRnhrTmhGS0gzeTJPTldrUWlJN252THlTRkpHQ1JrOHlGeFpxS3VWUmoyaDVGOGpONXIwYVhzVUtMaVRrWDQ5eTNnbjhLMEt3WFZNUVE?oc=5"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"})
try:
    resp = urllib.request.urlopen(req, timeout=20)
    html = resp.read().decode("utf-8", errors="replace")
    print(f"Got response: {len(html)} chars")
    # Extract title
    title = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
    if title:
        print(f"Title: {title.group(1).strip()[:300]}")
    # Extract meta description
    desc = re.search(r'<meta[^>]*name="description"[^>]*content="(.*?)"', html, re.DOTALL | re.IGNORECASE)
    if desc:
        print(f"Desc: {desc.group(1).strip()[:500]}")
    # Extract meta keywords
    kw = re.search(r'<meta[^>]*name="keywords"[^>]*content="(.*?)"', html, re.DOTALL | re.IGNORECASE)
    if kw:
        print(f"Keywords: {kw.group(1).strip()[:300]}")
    # Extract body paragraphs
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
    for p in paragraphs[:15]:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if len(clean) > 50:
            print(f"  P: {clean[:400]}")
            print("---")
    if not paragraphs:
        # Try finding text content differently
        texts = re.findall(r'>([^<]{80,500})<', html)
        count = 0
        for t in texts:
            t = t.strip()
            if len(t) > 60 and not t.startswith(('var ', 'function', '{', 'window', 'http', 'if (', 'News', 'Sign', 'Subscribe')):
                print(f"  T: {t[:400]}")
                count += 1
                if count > 10: break
except Exception as e:
    print(f"Error: {e}")

# Also try the NPR article
print("\n\n=== NPR ===")
npr_items = [
    "https://news.google.com/rss/articles/CBMiiwFBVV95cUxPSGVwMkZTMENfY1g0LXdCc0xhVi0zemlCTThseW1vRGJ2Q29jSnZ4NlctQUd3R19jWjl5ZVF6RWtPcG8taV9zdS1oNktORlZlMXY4WFBRNllkSXFVb2t2T2ktcnVQeWpnRUpPajRnMXhCaWFGcVVmN1h4M1ZPbFJtWjd5WHc0LVZ3?oc=5",
    "https://news.google.com/rss/articles/CBMiywFBVV95cUxQTjYyR0V6aTZReS02bFlQWDUzUzlCWi13V0RKQkRFRHZreVhJTEtnMnR3emN0UUs5OFRnOWU2dUFaTG1RRktnbEZrUm9nVzhocGtReS1MMXZ6bEw1TFZ6a0F0a1ZVbEtNM1JvLXk?",
]
for url in npr_items:
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
    except Exception as e:
        print(f"Error: {e}")