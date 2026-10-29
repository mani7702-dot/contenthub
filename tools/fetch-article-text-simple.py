#!/usr/bin/env python3
"""Fetch the full text of a GNN article for cross-checking."""
import subprocess, sys, re

url = sys.argv[1]
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Extract paragraph text
paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL | re.IGNORECASE)
for para in paras:
    clean = re.sub(r'<[^>]+>', '', para).strip()
    clean = re.sub(r'&#8217;|&#8220;|&#8221;|&nbsp;', " ", clean)
    clean = re.sub(r'&#\d+;', '', clean)
    if len(clean) > 30:
        print(clean)
        print()
