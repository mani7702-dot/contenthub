#!/usr/bin/env python3
"""Parse full ScienceDaily top XML with trailing-comment fix. Writes titles to stdout."""
import xml.etree.ElementTree as ET, sys

path = sys.argv[1]
data = open(path, 'rb').read()
idx = data.find(b'</rss>')
if idx != -1:
    data = data[:idx + 6]
root = ET.fromstring(data)
count = 0
for it in root.iter('item'):
    title = (it.findtext('title') or '').strip()
    link = (it.findtext('link') or '').strip()
    desc = (it.findtext('description') or '').strip()[:200]
    if len(title) < 25:
        continue
    count += 1
    print(f'[{count}] {title}')
    print(f'  url: {link}')
    print(f'  desc: {desc}')
print(f'TOTAL: {count}')
