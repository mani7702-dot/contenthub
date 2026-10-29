#!/usr/bin/env python3
"""Fetch a Listverse article and extract the actual article content."""
import sys
import re
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

def fetch(url):
    result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url],
                          capture_output=True)
    return result.stdout.decode('utf-8', errors='replace')

url = sys.argv[1] if len(sys.argv) > 1 else "https://listverse.com/2026/10/29/10-true-tales-from-the-tower-of-londons-1000-year-history/"
html = fetch(url)

# Find the article body
# Listverse uses <article> with inside it
# Let's just strip all tags and look for the intro text
# Find the section starting with "William intended" or similar
text = re.sub(r'<[^>]+>', '\n', html)
text = re.sub(r'&[a-z]+;', ' ', text)
text = re.sub(r'\n\s*\n', '\n', text)
# Remove CSS/JS
text = re.sub(r'(function\s*\([^)]*\)[^{]*\{[^}]*\})', '', text)
text = re.sub(r'\{[^}]*\}', '', text)

# Find relevant content
lines = text.split('\n')
for i, line in enumerate(lines):
    line = line.strip()
    if len(line) > 80 and not line.startswith('function') and not line.startswith('get') and not line.startswith('{') and not line.startswith('window') and not line.startswith('var'):
        if any(w in line.lower() for w in ['tower', 'london', 'execution', 'prison', 'jailed', 'crown', 'queen', 'king', 'anne', 'elizabeth', 'princess', '1000']):
            print(f"Line {i}: {line[:500]}\n")
