#!/usr/bin/env python3
"""Try fetching the NYT article via Google News proxy."""
import urllib.request, re, html as htmlmod

# NYT is often the same URL via Google News proxy
urls_to_try = [
    ("NYT-proxy", "https://news.google.com/rss/articles/CBMiZ0FVX3lxTE5rYVc1a1lXd3VZbTUXQWdwaFlGdDBVMmxqYm05MFgyMXphVEJ3Q2hrekJVeGthek5yMVhZYVMyUnBka1Zua0FB?oc=5"),
    ("DW-proxy", "https://news.google.com/rss/articles/CBMidkFVX3lxTFB4Nm81a0RLRmItZFM4VVFtYXdKTVpweDJPY01GdWlyVXNkcUNwNndlSy00ZGhNVFJhNnlkem1ZNU83SF9fNkNSM29xREdHTENwelgxNEVEeFRNcjZDc1BxWFFyVGRBU0RCdHBuWFlOZ0hWcTRFNEhZ0gF8QVVfeXFMTEJ4b09RRzIySFBHQk9XNnRqdEItb09yS3V5enJxR3lUTkJvdmI3YUdadnMzMVdzUFR0WkZvbXBKcGtIWDB0ZGRyQTdncVllV29uaXJsMVVtdC12Q0pJa2oxRXVvNmtySFJFVnJkOFc5bmh5QUNuUUh3Q0JIcw?oc=5"),
]

for name, url in urls_to_try:
    print(f"\n=== {name} ===")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"})
    try:
        resp = urllib.request.urlopen(req, timeout=20)
        html = resp.read().decode("utf-8", errors="replace")
        print(f"Got response: {len(html)} chars")
        # Try finding content in JSON within the page
        # Google News proxy pages often contain the content in a specific format
        m = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
        if m:
            print(f"Title: {htmlmod.unescape(m.group(1).strip())[:300]}")
        # Look for the actual article text in the page
        # Sometimes it's in a specific div or in a data element
        texts = re.findall(r'"text":"([^"]{50,500})"', html)
        for t in texts[:10]:
            print(f"JSON text: {t[:300]}")
        # Also try finding text in the main content area
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        for p in paragraphs[:10]:
            clean = re.sub(r'<[^>]+>', '', p).strip()
            if len(clean) > 50:
                print(f"P: {clean[:400]}")
        # Try to find description meta
        desc = re.search(r'<meta[^>]*name="description"[^>]*content="(.*?)"', html, re.DOTALL | re.IGNORECASE)
        if desc:
            print(f"Desc: {htmlmod.unescape(desc.group(1).strip())[:500]}")
    except Exception as e:
        print(f"Error: {e}")