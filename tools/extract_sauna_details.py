#!/usr/bin/env python3
"""Fetch the full HTML of the ScienceDaily article for details like duration, temp, journal."""
import urllib.request, re, html

url = 'https://www.sciencedaily.com/releases/2026/10/261027231021.htm'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'})
data = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')

# Extract meta description
m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', data, re.I)
if m:
    print(f"META DESC: {m.group(1)}")

# Extract the full body text
m = re.search(r'<div[^>]*id=["\']text["\'][^>]*>(.*?)</div>', data, re.S)
if m:
    txt = re.sub(r'<[^>]+>', ' ', m.group(1))
    txt = html.unescape(re.sub(r'\s+', ' ', txt)).strip()
    print(f"\n=== FULL TEXT ({len(txt)} chars) ===")
    print(txt)

# Also look for citation / journal info
for m in re.finditer(r'<div[^>]*class=["\'][^"\']*citation[^"\']*["\'][^>]*>(.*?)</div>', data, re.S | re.I):
    txt = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(1))).strip())
    if txt:
        print(f"\nCITATION: {txt}")

# Look for summary key points
for m in re.finditer(r'<p>(.*?)</p>', data, re.S):
    p = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(1))).strip())
    if any(kw in p.lower() for kw in ['minute', 'minute', 'celsius', 'fahrenheit', 'degree', '30 ', 'hour', 'blood pressure', 'heart rate', 'volunteer', 'participants']):
        print(f"\nDETAIL: {p}")
