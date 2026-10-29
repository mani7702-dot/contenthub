#!/usr/bin/env python3
"""Fetch Listverse article and extract story items by finding h2/h3 headers."""
import sys
import re
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

def fetch(url):
    result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url],
                          capture_output=True)
    return result.stdout.decode('utf-8', errors='replace')

url = sys.argv[1]
html = fetch(url)

# Find all text between tags
text = re.sub(r'<[^>]+>', '\n', html)
text = re.sub(r'&[a-z]+;', ' ', text)
text = re.sub(r'&amp;', '&', text)
text = re.sub(r'&#039;', "'", text)
text = re.sub(r'\n\s*\n+', '\n', text)

lines = text.split('\n')
for i, line in enumerate(lines):
    line = line.strip()
    if len(line) > 40:
        print(f"[{i}] {line[:500]}")
