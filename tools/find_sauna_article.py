#!/usr/bin/env python3
"""Fetch ScienceDaily top RSS and find sauna/immune article."""
import urllib.request, re, html

url = 'https://www.sciencedaily.com/rss/top.xml'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)'})
data = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')

# Strip trailing comment after </rss>
data = data.split('</rss>')[0] + '</rss>'

import xml.etree.ElementTree as ET
root = ET.fromstring(data)
for item in root.iter('item'):
    title = item.findtext('title', '')
    link = item.findtext('link', '')
    desc = item.findtext('description', '')
    if 'sauna' in title.lower() or 'immune' in title.lower() or 'lymphocyte' in title.lower() or 'T-cell' in title.lower() or 'T cell' in title.lower() or 'heat' in title.lower():
        print(f"TITLE: {title}")
        print(f"LINK: {link}")
        print(f"DESC: {re.sub(r'<[^>]+>','',desc)}")
        print()
