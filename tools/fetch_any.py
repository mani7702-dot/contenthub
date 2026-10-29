#!/usr/bin/env python3
"""Fetch and parse a URL to extract readable text."""
import subprocess, re, sys

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = sys.argv[1]
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Strip HTML
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'&#8217;', "'", text)
text = re.sub(r'&#8220;|&#8221;', '"', text)
text = re.sub(r'&amp;', '&', text)
text = re.sub(r'&nbsp;', ' ', text)
text = re.sub(r'\s+', ' ', text)
print(text[:6000])
