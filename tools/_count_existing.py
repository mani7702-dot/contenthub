#!/usr/bin/env python3
"""Count prose words in an existing article."""
import re

def count_article(path):
    with open(path) as f:
        content = f.read()
    body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    body = body.split('## Sources')[0] if '## Sources' in body else body
    body = re.sub(r'^#.*$', '', body, flags=re.MULTILINE)
    body = re.sub(r'https?://\S+', '', body)
    body = re.sub(r'\*\*|\*', '', body)
    words = body.split()
    return len(words)

articles = [
    'content/news/2026-10-26-flare-ribbons-solar-explosions.md',
    'content/news/2026-10-26-nasa-swift-mission-ends.md',
]
for a in articles:
    print(f"{a}: {count_article(a)} prose words")
