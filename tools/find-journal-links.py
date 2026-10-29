#!/usr/bin/env python3
"""Extract journal links and DOIs from a ScienceDaily article page."""
import subprocess, re, sys

url = sys.argv[1] if len(sys.argv) > 1 else "https://www.sciencedaily.com/releases/2026/10/261027063702.htm"
p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "--compressed", url], capture_output=True)
raw = p.stdout.decode("utf-8", errors="replace")

# Find links containing 'national' or 'doi' or journal
links = re.findall(r'href=["\']([^"\']*)', raw)
keywords = ["national", "doi", "nsr", "scichina", "journal", "oxford", "springer"]
for l in links:
    low = l.lower()
    if any(k in low for k in keywords):
        print("LINK:", l[:200])
