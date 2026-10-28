#!/usr/bin/env python3
"""Fetch the Current Archaeology article about Lismore - find the actual URL."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://www.archaeology.co.uk/"
p = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url], capture_output=True, text=True)
content = p.stdout

# Find the article link
links = re.findall(r'href="([^"]*)"', content)
for link in links:
    if 'island' in link.lower() or 'scottish' in link.lower() or 'lismore' in link.lower():
        print(f"Link: {link}")
