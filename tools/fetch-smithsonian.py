#!/usr/bin/env python3
import urllib.request, re, html, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://nationalzoo.si.edu/news/litter-five-cheetah-cubs-are-born-smithsonian-conservation-campus-cheetah-cub-cam-returns'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
raw = resp.read().decode('utf-8', errors='replace')
print("STATUS:", resp.status, "len:", len(raw))

text = re.sub(r'<script.*?</script>', '', raw, flags=re.DOTALL)
text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = html.unescape(text)
text = re.sub(r'\s+', ' ', text).strip()
print(text[:6000])
