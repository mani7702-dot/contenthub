#!/usr/bin/env python3
"""Fetch a URL and dump raw HTML for inspection."""
import subprocess, sys

url = sys.argv[1]
p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "--compressed", url], capture_output=True)
raw = p.stdout.decode("utf-8", errors="replace")
print(f"Length: {len(raw)}")
print(raw[:3000])
