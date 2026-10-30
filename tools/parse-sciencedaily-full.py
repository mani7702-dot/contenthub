#!/usr/bin/env python3
"""Parse full ScienceDaily top RSS, strip trailing comment, print ALL items."""
import xml.etree.ElementTree as ET
import subprocess

url = "https://www.sciencedaily.com/rss/top.xml"
result = subprocess.run(
    ['curl', '-s', '--max-time', '15',
     '-A', 'Mozilla/5.0 (ContentHub; contact andugulamani722@gmail.com)',
     url],
    capture_output=True, text=True, timeout=20
)
html = result.stdout

# Strip everything after </rss>
idx = html.find('</rss>')
if idx > 0:
    html = html[:idx + len('</rss>')]

# Parse
root = ET.fromstring(html)
items = root.iter('item')
for i, item in enumerate(items, 1):
    title = item.findtext('title', '').strip()
    link = item.findtext('link', '').strip()
    print(f"{i}. {title}")
    print(f"   URL: {link}")
    print()
