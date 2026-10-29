#!/usr/bin/env python3
"""Search for secondary sources on Tanzania natural gas discovery."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Search via Bing News
url = "https://www.bing.com/news/search?q=Tanzania+natural+gas+discovery+Mnazi+Bay+2026"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, "-L", url], capture_output=True, text=True)
html = r.stdout

# Extract news article links and titles
links = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</a>', html, re.DOTALL)
print("=== Bing News Results (title links) ===")
seen = set()
for l, t in links[:15]:
    t = re.sub(r'<[^>]+>', '', t).strip()
    if l not in seen and ('tanzania' in l.lower() or 'gas' in l.lower() or 'bbc' in l.lower() or 'reuters' in l.lower() or 'energy' in l.lower()):
        seen.add(l)
        print(f"  {t}")
        print(f"  URL: {l}")
        print()

# Try extracting all article snippets
snippets = re.findall(r'<p[^>]*class="[^"]*snippet[^"]*"[^>]*>(.*?)</p>', html, re.DOTALL)
print("=== Snippets ===")
for s in snippets[:10]:
    text = re.sub(r'<[^>]+>', '', s).strip()
    text = re.sub(r'\s+', ' ', text)
    if len(text) > 20:
        print(f"  {text[:200]}")
