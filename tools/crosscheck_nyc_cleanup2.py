#!/usr/bin/env python3
"""Cross-check NYC cleanup story via Bing News search."""
import subprocess, re, html

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

url = "https://www.bing.com/news/search?q=NYC+dumping+site+cleanup+Joshua+Service+Crown+Heights"
r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url],
                   capture_output=True, text=True)
text = r.stdout
links = re.findall(r'href="(https?://[^"]+)"', text)
news = [l for l in links if not any(b in l for b in ['bing.com', 'microsoft', 'go.microsoft', 'msn.com'])]

print("=== Bing News Results ===")
for l in news[:20]:
    print(l)

# Also search for the CBS article specifically
print("\n=== Searching for CBS News article ===")
search2 = "https://www.bing.com/search?q=site:cbsnews.com+service+cleanup+nyc+dumping"
r2 = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, search2],
                     capture_output=True, text=True)
text2 = r2.stdout
links2 = re.findall(r'href="(https?://[^"]+)"', text2)
cbs = [l for l in links2 if 'cbsnews.com' in l and 'bing.com' not in l]
for l in cbs[:10]:
    print(l)
