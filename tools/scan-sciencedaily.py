#!/usr/bin/env python3
"""Fetch and parse the full ScienceDaily top RSS feed, bypassing the 6-item limit."""
import xml.etree.ElementTree as ET
import sys

feed_url = "https://www.sciencedaily.com/rss/top.xml"

# Use curl via subprocess to fetch
import subprocess
result = subprocess.run(
    ['curl', '-s', '--max-time', '15', feed_url],
    capture_output=True, text=True
)
content = result.stdout

# Strip everything after </rss>
idx = content.rfind('</rss>')
if idx != -1:
    content = content[:idx + len('</rss>')]

try:
    tree = ET.fromstring(content)
except ET.ParseError as e:
    print(f"Parse error: {e}", file=sys.stderr)
    # Try stripping the comment after </rss>
    sys.exit(1)

items = tree.findall('.//item')
print(f'Total ScienceDaily top items: {len(items)}')
for item in items:
    title_elem = item.find('title')
    link_elem = item.find('link')
    title = title_elem.text if title_elem is not None else 'N/A'
    link = link_elem.text if link_elem is not None else 'N/A'
    print(f'- {title}')
    print(f'  {link}')
