#!/usr/bin/env python3
"""Extract the main article body from a Good News Network HTML page."""
import sys, re

filepath = sys.argv[1] if len(sys.argv) > 1 else '/tmp/kangaroo.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Look for the article body div
patterns = [
    r'<div[^>]*class="[^"]*entry-content[^"]*"[^>]*>(.*?)</div>\s*</div>',
    r'<div[^>]*class="[^"]*story-body[^"]*"[^>]*>(.*?)</div>\s*</div>',
    r'<article[^>]*>(.*?)</article>',
]

content = None
for pat in patterns:
    m = re.search(pat, html, re.DOTALL | re.IGNORECASE)
    if m:
        content = m.group(1)
        break

if not content:
    # Try finding all <p> tags that look like article body
    paragraphs = re.findall(r'<p>(.*?)</p>', html, re.DOTALL)
    body_paras = []
    for p in paragraphs:
        text = re.sub(r'<[^>]+>', '', p)
        text = text.strip()
        # Skip navigation/short text
        if len(text) > 40:
            body_paras.append(text)
    if body_paras:
        content = '\n'.join(body_paras[:15])

if content:
    text = re.sub(r'<[^>]+>', ' ', content)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&#8217;', "'", text)
    text = re.sub(r'&#8220;|&#8221;', '"', text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'\s+', ' ', text)
    print(text[:6000])
else:
    print("No content found")
