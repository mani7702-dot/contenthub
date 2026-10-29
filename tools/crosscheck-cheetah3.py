#!/usr/bin/env python3
"""Fetch Smithsonian cheetah page for more content."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try multiple URL patterns for the cheetah cam
urls = [
    "https://nationalzoo.si.edu/webcams/cheetahs-5-cubs",
    "https://nationalzoo.si.edu/webcams",
    "https://nationalzoo.si.edu/animals/cheetah",
]

for url in urls:
    print(f"\n=== {url} ===\n")
    p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, url], capture_output=True)
    html = p.stdout.decode("utf-8", errors="ignore")
    
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Find cheetah-specific content - skip past the nav/header
    keywords = ["7,000", "cub", "conservation", "endangered", "habitat", "wild"]
    for kw in keywords:
        positions = [m.start() for m in re.finditer(kw, text, re.IGNORECASE)]
        for pos in positions:
            start = max(0, pos - 300)
            end = min(len(text), pos + 800)
            snippet = text[start:end]
            if len(snippet) > 200:
                print(f"--- Context around '{kw}' ---")
                print(snippet)
                print()
                break
        break  # Only show first match per keyword
