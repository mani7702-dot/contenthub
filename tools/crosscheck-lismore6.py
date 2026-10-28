#!/usr/bin/env python3
"""Cross-check: Try Bing search for Lismore archaeology."""
import subprocess, re, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://www.bing.com/search?q=Lismore+archaeology+monastery+Saint+Moluag+precious+metal+crucible"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url], capture_output=True)
text = r.stdout.decode("utf-8", errors="replace")

# Find result snippets
results = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)
for p in results[:15]:
    clean = re.sub(r'<[^>]+>', '', p).strip()
    if len(clean) > 60 and ("lismore" in clean.lower() or "moluag" in clean.lower() or "archaeolog" in clean.lower() or "monastery" in clean.lower()):
        print(f"  {clean[:300]}")
        print("---")
