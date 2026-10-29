#!/usr/bin/env python3
"""Search ScienceDaily top XML for SDF article."""
import urllib.request
import re

url = "https://www.sciencedaily.com/rss/top.xml"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
resp = urllib.request.urlopen(req, timeout=15)
xml = resp.read().decode('utf-8', errors='replace')

# Parse XML for items containing SDF/cavity/silver
items = re.findall(r'<item>(.*?)</item>', xml, re.DOTALL)
print(f"Total items: {len(items)}")
for item in items:
    title_match = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
    link_match = re.search(r'<link>(.*?)</link>', item, re.DOTALL)
    desc_match = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
    if title_match and link_match:
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        link = link_match.group(1).strip()
        desc = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip() if desc_match else ''
        if 'sdf' in title.lower() or 'silver' in title.lower() or 'diamine' in title.lower() or 'cavity' in title.lower() or 'fluoride' in title.lower():
            print(f"  Title: {title}")
            print(f"  Link: {link}")
            print(f"  Desc: {desc[:200]}")
            print()
