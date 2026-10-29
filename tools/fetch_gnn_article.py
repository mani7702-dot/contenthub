#!/usr/bin/env python3
"""Fetch and parse a GNN article URL to extract readable text."""
import subprocess, re, sys

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = sys.argv[1] if len(sys.argv) > 1 else (
    "https://www.goodnewsnetwork.org/coconut-oil-could-make-great-sustainable-jet-fuel-pioneering-experiments-demonstrate/"
)

p = subprocess.run(
    ["curl", "-s", "--max-time", "25", "-A", UA, url],
    capture_output=True
)
html = p.stdout.decode("utf-8", errors="replace")

# Try to find article content
m = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
if m:
    text = m.group(1)
else:
    # Fallback: look for common content divs
    m = re.search(r'class="[^"]*content[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
    text = m.group(1) if m else html

# Strip HTML tags
text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'&#8217;', "'", text)
text = re.sub(r'&#8220;|&#8221;', '"', text)
text = re.sub(r'&amp;', '&', text)
text = re.sub(r'&nbsp;', ' ', text)
text = re.sub(r'\s+', ' ', text)
print(text[:5000])
