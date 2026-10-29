#!/usr/bin/env python3
"""Fetch article text from a URL and extract paragraph content."""
import subprocess, sys, re, html as html_module

url = sys.argv[1]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, "--compressed", url], capture_output=True)
raw = p.stdout.decode("utf-8", errors="replace")

# Check if we got real content
if len(raw) < 1000:
    print(f"WARNING: Only {len(raw)} bytes received")
    print(raw[:500])
    sys.exit(1)

# Remove scripts and styles
raw = re.sub(r'<script[^>]*>.*?</script>', '', raw, flags=re.DOTALL | re.IGNORECASE)
raw = re.sub(r'<style[^>]*>.*?</style>', '', raw, flags=re.DOTALL | re.IGNORECASE)

# Extract paragraphs
paras = re.findall(r'<p[^>]*>(.*?)</p>', raw, re.DOTALL | re.IGNORECASE)
for para in paras:
    clean = re.sub(r'<[^>]+>', '', para).strip()
    clean = html_module.unescape(clean)
    if len(clean) > 30:
        print(clean)
        print()
