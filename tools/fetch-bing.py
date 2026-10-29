#!/usr/bin/env python3
import urllib.request, re, html, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Bing News search for "cheetah cubs Zura Smithsonian"
url = 'https://www.bing.com/news/search?q=cheetah+cubs+Zura+Smithsonian+Front+Royal+October+2026'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
try:
    raw = urllib.request.urlopen(req, timeout=20, context=ctx).read().decode('utf-8', errors='replace')
    text = re.sub(r'<[^>]+>', ' ', raw)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    # Look for article snippets
    for kw in ['cheetah', 'Zura', 'cub', 'Smithsonian']:
        idx = text.lower().find(kw.lower())
        if idx >= 0:
            print(f"[{kw}] ..." + text[max(0,idx-100):idx+300] + "...")
            print()
except Exception as e:
    print(f"ERROR: {e}")
