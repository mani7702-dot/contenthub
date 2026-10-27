#!/usr/bin/env python3
"""Count body words of the article (between frontmatter and Sources)."""
import re

with open('/home/ubuntu/contenthub/content/news/2026-10-27-kikai-supervolcano-refilling.md') as f:
    content = f.read()

# Strip frontmatter
body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

# Remove source URLs line
body = re.sub(r'https?://\S+', '', body)

# Count words
words = body.split()
print(f"Body words (excluding frontmatter and URLs): {len(words)}")
