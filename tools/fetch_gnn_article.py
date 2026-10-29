#!/usr/bin/env python3
"""Fetch a GNN article and extract content."""
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

# Extract meta description if present
desc_match = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html, re.IGNORECASE)
if desc_match:
    print("META DESC:", desc_match.group(1)[:500])

# Strip tags
text = re.sub(r'<[^>]+>', '\n', html)
text = re.sub(r'&[a-z]+;', ' ', text)
text = re.sub(r'&amp;', '&', text)
text = re.sub(r'&#039;', "'", text)
text = re.sub(r'\n\s*\n+', '\n', text)

lines = text.split('\n')
for i, line in enumerate(lines):
    line = line.strip()
    if len(line) > 60:
        print(f"[{i}] {line[:500]}")
