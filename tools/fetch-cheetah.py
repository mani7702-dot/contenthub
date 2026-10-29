#!/usr/bin/env python3
import urllib.request, re, html, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
  'https://www.goodnewsnetwork.org/live-smithsonian-webcam-for-cheetah-den-and-5-cubs/',
  'https://www.goodnewsnetwork.org/man-named-service-cleans-up-nyc-dumping-site-on-his-own-initiative/'
]
for url in urls:
    print(f"\n{'='*60}")
    print(f"URL: {url}")
    print('='*60)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'})
    try:
        raw = urllib.request.urlopen(req, timeout=20, context=ctx).read().decode('utf-8', errors='replace')
        text = re.sub(r'<script.*?</script>', '', raw, flags=re.DOTALL)
        text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = html.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()
        # Print the latter half (article body)
        print(text[3000:7000])
    except Exception as e:
        print(f"ERROR: {e}")
