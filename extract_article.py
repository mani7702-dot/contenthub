#!/usr/bin/env python3
import re, sys

with open('/home/ubuntu/contenthub/gnn_positivity.html', 'r', errors='replace') as f:
    html = f.read()

# Try to find the article body
match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
if not match:
    match = re.search(r'class="entry-content[^>]*>(.*?)</div>', html, re.DOTALL)
if match:
    content = match.group(1)
else:
    # Try to find the main body text after the title
    match = re.search(r'One Teacher.*?Practice.*?</h1>(.*?)(?:<aside|class="shared|class="comment|<footer)', html, re.DOTALL)
    if match:
        content = match.group(1)
    else:
        # Find the body content div
        match = re.search(r'<body[^>]*>(.*?)<footer', html, re.DOTALL)
        if match:
            content = match.group(1)
        else:
            content = html

text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()
print(text[:3000])
