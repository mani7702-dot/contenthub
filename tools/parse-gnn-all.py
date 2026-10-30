#!/usr/bin/env python3
"""Parse full GNN feed - all 50 items."""
import xml.etree.ElementTree as ET
import subprocess

url = "https://www.goodnewsnetwork.org/feed/"
result = subprocess.run(
    ['curl', '-s', '--max-time', '15',
     '-A', 'Mozilla/5.0 (ContentHub; contact andugulamani722@gmail.com)',
     url],
    capture_output=True, text=True, timeout=20
)
html = result.stdout

idx = html.find('</rss>')
if idx > 0:
    html = html[:idx + len('</rss>')]

root = ET.fromstring(html)
for i, item in enumerate(root.iter('item'), 1):
    title = item.findtext('title', '').strip()
    link = item.findtext('link', '').strip()
    print(f"{i}. {title}")
    print(f"   URL: {link}")
    print()
