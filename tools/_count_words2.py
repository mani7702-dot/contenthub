#!/usr/bin/env python3
"""Count prose words excluding frontmatter, headings, sources, and URLs."""
import re

with open('/home/ubuntu/contenthub/content/news/2026-10-27-kikai-supervolcano-refilling.md') as f:
    content = f.read()

# Strip frontmatter
body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

# Cut at Sources
body = body.split('## Sources')[0]

# Remove markdown headings
body = re.sub(r'^#.*$', '', body, flags=re.MULTILINE)

# Remove URLs
body = re.sub(r'https?://\S+', '', body)

# Remove markdown bold/italic
body = re.sub(r'\*\*', '', body)
body = re.sub(r'\*', '', body)

# Count words
words = body.split()
print(f"Article body words (prose only): {len(words)}")
