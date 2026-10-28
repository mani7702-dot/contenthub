#!/usr/bin/env python3
"""Cross-check: try to get the raw HTML of the Antiquity page."""
import subprocess, re, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://www.antiquity.ac.uk/projgall/ellis2401/"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url], capture_output=True)
text = r.stdout
# Check if gzipped
if text[:2] == b'\x1f\x8b':
    text = gzip.decompress(text)
html = text.decode("utf-8", errors="replace")
# Just print the full text length and key sections
print(f"Total HTML length: {len(html)}")

# Extract just the body text
body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
if body_match:
    body = body_match.group(1)
else:
    body = html

# Remove scripts and styles
body = re.sub(r'<script[^>]*>.*?</script>', ' ', body, flags=re.DOTALL)
body = re.sub(r'<style[^>]*>.*?</style>', ' ', body, flags=re.DOTALL)
body = re.sub(r'<[^>]+>', ' ', body)
body = re.sub(r'\s+', ' ', body).strip()

# Print first 2000 chars of body
print(f"Body text (first 2000 chars):")
print(body[:2000])
