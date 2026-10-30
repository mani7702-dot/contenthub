import urllib.request, re, sys

url = "https://www.nature.com/articles/s41566-026-01976-2"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)',
    'Accept': 'text/html',
})
try:
    raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(0)

print(f"Page length: {len(raw)}")

# Abstract
abstract = re.findall(r'<div[^>]*class="[^"]*abstract[^"]*"[^>]*>(.*?)</div>', raw, re.DOTALL | re.IGNORECASE)
if abstract:
    txt = re.sub(r'<[^>]+>', ' ', abstract[0]).strip()
    print(f"ABSTRACT: {txt[:1200]}")

# Meta description
desc = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', raw, re.IGNORECASE)
if desc:
    print(f"\nMETA DESC: {desc.group(1)[:800]}")

# Authors
authors = re.findall(r'<meta[^>]+name="citation_author"[^>]+content="([^"]+)"', raw, re.IGNORECASE)
print(f"AUTHORS: {authors[:10]}")

# Title
title = re.search(r'<meta[^>]+name="citation_title"[^>]+content="([^"]+)"', raw, re.IGNORECASE)
if title:
    print(f"TITLE: {title.group(1)}")

# Published date
date = re.search(r'<meta[^>]+name="citation_date"[^>]+content="([^"]+)"', raw, re.IGNORECASE)
if date:
    print(f"DATE: {date.group(1)}")

# Also check for paywall / restricted content
if 'access' in raw.lower()[:5000] or len(raw) < 5000:
    print("NOTE: May be behind paywall or minimal JS page")
