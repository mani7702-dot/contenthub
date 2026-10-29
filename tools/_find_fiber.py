#!/usr/bin/env python3
"""Fetch the fiber supplement article from ScienceDaily scan-all-lanes."""
import urllib.request
import re

# This should be in the ScienceDaily top feed - let's find it
url = "https://www.sciencedaily.com/rss/top.xml"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'
})
resp = urllib.request.urlopen(req, timeout=15)
xml = resp.read().decode('utf-8', errors='replace')

# Strip trailing comment if present
xml = xml.split('</rss>')[0] + '</rss>'

items = re.findall(r'<item>(.*?)</item>', xml, re.DOTALL)
print(f"Total items: {len(items)}")
for item in items:
    title_match = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
    link_match = re.search(r'<link>(.*?)</link>', item, re.DOTALL)
    if title_match and link_match:
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        link = link_match.group(1).strip()
        if 'fiber' in title.lower() or 'arthritis' in title.lower():
            print(f"  Title: {title}")
            print(f"  Link: {link}")
