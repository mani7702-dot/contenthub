#!/usr/bin/env python3
"""Scan GNN feed for candidate stories."""
import xml.etree.ElementTree as ET
import sys

data = open('/home/ubuntu/gnn_feed.xml', 'rb').read()
root = ET.fromstring(data)
items = list(root.iter('item'))
print(f'TOTAL ITEMS: {len(items)}')
print()
for i, it in enumerate(items[:50]):
    t = (it.findtext('title') or '').strip()
    link = (it.findtext('link') or '').strip()
    desc = (it.findtext('description') or '').strip()[:200]
    print(f'[{i+1}] {t}')
    print(f'    URL: {link}')
    print(f'    DESC: {desc[:160]}')
    print()
