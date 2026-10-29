#!/usr/bin/env python3
"""Fetch the Smithsonian cheetah cub cam page and cheetah page."""
import subprocess, re
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# The cheetah page from Smithsonian National Zoo
url = "https://nationalzoo.si.edu/animals/cheetah"
p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="ignore")

text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text)

# Find cheetah-specific content
keywords = ["cheetah", "cubs", "Zura", "Smithsonian Conservation", "endangered", "7,000"]
for kw in keywords:
    idx = text.lower().find(kw.lower())
    if idx > 0:
        print(f"[Found '{kw}' at pos {idx}]")
        # Get surrounding context
        start = max(0, idx - 200)
        end = min(len(text), idx + 500)
        print(text[start:end])
        print("---")
        break

# Also look for the cheetah cam page
print("\n=== Searching for cheetah cam ===\n")
cam_url = "https://nationalzoo.si.edu/webcams/cheetahs"
p2 = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, cam_url], capture_output=True)
html2 = p2.stdout.decode("utf-8", errors="ignore")
if len(html2) > 1000:
    text2 = re.sub(r'<script[^>]*>.*?</script>', '', html2, flags=re.DOTALL)
    text2 = re.sub(r'<style[^>]*>.*?</style>', '', text2, flags=re.DOTALL)
    text2 = re.sub(r'<[^>]+>', ' ', text2)
    text2 = re.sub(r'\s+', ' ', text2)
    print(text2[:2000])
else:
    print(f"Page too small ({len(html2)} bytes)")
