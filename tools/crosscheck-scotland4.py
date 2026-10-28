#!/usr/bin/env python3
"""Fetch Antiquity journal recent articles."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try the Project Gallery or recent articles
urls = [
    "https://www.antiquity.ac.uk/projectgallery/",
    "https://www.antiquity.ac.uk/past-issues/current/",
    "https://www.cambridge.org/core/journals/antiquity/recent",
]

for url in urls:
    print(f"\n=== {url} ===")
    p = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url], capture_output=True, text=True)
    content = p.stdout
    print(f"Page length: {len(content)}")
    text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', text)
    text = html.unescape(text)
    lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 40]
    for line in lines[:30]:
        if 'lismore' in line.lower() or 'scotland' in line.lower() or 'monastery' in line.lower() or 'elliss' in line.lower() or 'noble' in line.lower():
            print(f"*** MATCH: {line[:300]}")
        else:
            print(line[:200])