#!/usr/bin/env python3
"""List GNN feed titles so we can spot fresh kid-safe candidates."""
import urllib.request, re, html, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://www.goodnewsnetwork.org/feed/',
    headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'}
)
raw = urllib.request.urlopen(req, timeout=20, context=ctx).read().decode('utf-8', errors='replace')
items = re.findall(r'<title>(.*?)</title>', raw, re.DOTALL)
for i in items[:40]:
    print(html.unescape(re.sub(r'\s+', ' ', i.strip())))
