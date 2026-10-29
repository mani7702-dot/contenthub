#!/usr/bin/env python3
"""Extract cheetah content from Smithsonian National Zoo page."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://nationalzoo.si.edu/animals/cheetah"

p = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="ignore")

# Look for content-rich sections
# Find paragraphs
paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
for para in paragraphs:
    clean = re.sub(r'<[^>]+>', '', para)
    clean = re.sub(r'&amp;', '&', clean)
    clean = re.sub(r'&lt;', '<', clean)
    clean = re.sub(r'&gt;', '>', clean)
    clean = re.sub(r'&quot;', '"', clean)
    clean = re.sub(r'&#039;', "'", clean)
    clean = re.sub(r'&nbsp;', ' ', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    if len(clean) > 50:
        print(f"PARA: {clean}")

# Also find content between article tags or main content
articles = re.findall(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
print(f"\n\n=== Found {len(articles)} articles ===")
for art in articles:
    clean = re.sub(r'<[^>]+>', ' ', art)
    clean = re.sub(r'\s+', ' ', clean).strip()
    if len(clean) > 100:
        print(f"ARTICLE: {clean[:2000]}")
