#!/usr/bin/env python3
"""Fetch the Current Archaeology article about Lismore - find the actual URL."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://www.archaeology.co.uk/"
p = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url], capture_output=True, text=True)
content = p.stdout

# Find ALL links containing 'island'
all_links = re.findall(r'href="([^"]*)"', content)
for link in all_links:
    lower = link.lower()
    if 'island' in lower or 'lismore' in lower or 'scottish' in lower:
        print(f"Link: {link}")

print("\n--- Also trying articles with 'scottish' in text ---")
# Search in full HTML for the article link
matches = re.findall(r'"([^"]*scottish[^"]*)"', content, re.IGNORECASE)
for m in matches[:10]:
    print(f"Match: {m}")

matches = re.findall(r'"([^"]*island[^"]*)"', content, re.IGNORECASE)
for m in matches[:10]:
    print(f"Match: {m}")
