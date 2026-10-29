#!/usr/bin/env python3
"""Find the correct GNN article URL for the Van Gogh star clusters story."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# The feed title is: Star Clusters in Van Gogh's Starry Night Matches Taurus Sky From July 1889, Shows Study
# Let's try searching GNN directly
url = "https://www.goodnewsnetwork.org/?s=van+gogh+starry+night+taurus"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True, text=True)

# Find article links
links = re.findall(r'href="(https://www\.goodnewsnetwork\.org/[^"]+)"', r.stdout)
seen = set()
for l in links:
    if l not in seen and "s=" not in l:
        seen.add(l)
        print(l)
