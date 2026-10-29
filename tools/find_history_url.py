#!/usr/bin/env python3
"""Find the correct GNN article URL for 'Good News in History, October 28'."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
url = "https://www.goodnewsnetwork.org/?s=good+news+in+history+october+28"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, "-L", url], capture_output=True, text=True)

links = re.findall(r'href="(https://www\.goodnewsnetwork\.org/[^"]+)"', r.stdout)
seen = set()
for l in links:
    if l not in seen and "s=" not in l and "feed" not in l and "category" not in l:
        seen.add(l)
        print(l)
