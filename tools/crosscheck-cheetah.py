#!/usr/bin/env python3
"""Cross-check cheetah cubs story with Smithsonian/National Zoo source."""
import subprocess, re
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
# Try Smithsonian National Zoo cheetah page
urls = [
    "https://nationalzoo.si.edu/animals/cheetah",
    "https://www.smithsonian.org/press/",
    "https://nationalzoo.si.edu/cam/cheetah-cub-cam",
]
for url in urls:
    print(f"=== Trying: {url} ===")
    p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, url], capture_output=True)
    html = p.stdout.decode("utf-8", errors="ignore")
    if len(html) < 1000:
        print("  (page too small or redirect)")
        continue
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    # Look for cheetah-related content
    idx = text.lower().find("cheetah")
    if idx > 0:
        print(text[idx:idx+2000])
    else:
        print(text[:500])
    print()
