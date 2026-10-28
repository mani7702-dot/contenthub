#!/usr/bin/env python3
"""Fetch KSN-TV article for cross-checking."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www.ksn.com/community/positive-connections/positivity-tradition-spreads-through-haysville-school/"

p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, "-L", url], capture_output=True, text=True)
html_content = p.stdout
print(f"Page length: {len(html_content)}")

# Try to extract article content
for pattern in [r'<article[^>]*>(.*?)</article>', r'class="article-body"[^>]*>(.*?)</div>', r'class="entry-content"[^>]*>(.*?)</div>', r'class="post-content"[^>]*>(.*?)</div>']:
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        raw = match.group(1)
        text = re.sub(r'<[^>]+>', ' ', raw)
        text = html.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()
        print(f"Found with pattern: {pattern[:40]}")
        print(text[:5000])
        break
else:
    # Just print some text content
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', text)
    text = html.unescape(text)
    lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 40]
    for line in lines[:30]:
        print(line[:300])
