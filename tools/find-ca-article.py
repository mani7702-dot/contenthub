#!/usr/bin/env python3
"""Fetch the Current Archaeology article about Lismore."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Find the article URL
url = "https://www.archaeology.co.uk/"
p = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url], capture_output=True, text=True)
content = p.stdout

# Find links related to Scottish island
links = re.findall(r'href="(https?://[^"]*scottish[^"]*|https?://[^"]*island[^"]*|https?://[^"]*lismore[^"]*)"[^>]*>([^<]+)', content, re.IGNORECASE)
for href, title in links[:10]:
    print(f"  {title[:100]} -> {href[:200]}")

# Also search for the article text
text = re.sub(r'<[^>]+>', ' ', content)
text = html.unescape(text)
idx = text.lower().find("scottish island")
if idx >= 0:
    print(f"\nContext around 'Scottish island':")
    print(text[max(0,idx-200):idx+500])
