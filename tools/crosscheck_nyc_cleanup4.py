#!/usr/bin/env python3
"""Search Bing News for NYC cleanup story and extract news outlet links."""
import subprocess, re, urllib.parse

query = "Joshua Service NYC dumping site cleanup Crown Heights CBS"
encoded = urllib.parse.quote(query)
url = f"https://www.bing.com/news/search?q={encoded}"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, "--compressed", url],
                   capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
print(f"Page size: {len(html)} bytes")

links = re.findall(r'href="(https?://[^"]+)"', html)
out = set()
for l in links:
    if any(d in l.lower() for d in ['cbs', 'nbc', 'abc', 'fox', 'usatoday', 'nydailynews',
                                     'nypost', 'njcom', 'amny', 'pix11', 'abc7', 'cbsnewyork']):
        out.add(l)

print("=== News outlet links ===")
for l in sorted(out):
    print(l)

if not out:
    print("No specific outlet links found. Full link list:")
    for l in links[:30]:
        if 'bing' not in l and 'microsoft' not in l:
            print(l)
