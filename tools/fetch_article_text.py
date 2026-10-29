#!/usr/bin/env python3
"""Fetch BBC article and extract text content."""
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

# Strip tags
text = re.sub(r'<[^>]+>', '\n', html)
text = re.sub(r'&[a-z]+;', ' ', text)
text = re.sub(r'\n\s*\n+', '\n', text)

lines = text.split('\n')
for i, line in enumerate(lines):
    line = line.strip()
    if len(line) > 80 and not line.startswith('function') and not line.startswith('{') and not line.startswith('window') and not line.startswith('var') and not line.startswith('get') and not line.startswith('cookie') and not line.startswith('\\'):
        if not re.search(r'(cookie|privacy|terms|subscribe|newsletter|bbc|copyright|follow|@|\.css|\.js|script)', line, re.IGNORECASE):
            print(f"[{i}] {line[:600]}\n")
