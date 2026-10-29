#!/usr/bin/env python3
import urllib.request, re, html, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Fetch the cheetah article page from Smithsonian and extract body text
url = 'https://nationalzoo.si.edu/animals/news/smithsonian-national-zoos-cheetah-cub-cam-returns-five-adorable-reasons-tune'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
try:
    resp = urllib.request.urlopen(req, timeout=15, context=ctx)
    raw = resp.read().decode('utf-8', errors='replace')
    print("STATUS:", resp.status, "len:", len(raw))
    text = re.sub(r'<script.*?</script>', '', raw, flags=re.DOTALL)
    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    # Find cheetah content
    idx = text.lower().find('cheetah cub')
    if idx >= 0:
        print(text[max(0,idx-200):idx+5000])
    else:
        idx2 = text.lower().find('zura')
        if idx2 >= 0:
            print(text[max(0,idx2-200):idx2+5000])
        else:
            print(text[:3000])
except Exception as e:
    print(f"ERROR: {e}")
