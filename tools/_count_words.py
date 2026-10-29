#!/usr/bin/env python3
"""Count words in the article body (excluding frontmatter)."""
import sys, re

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    content = f.read()

# Split frontmatter
parts = content.split("---", 2)
body = parts[2] if len(parts) >= 3 else content

# Remove markdown
body = re.sub(r'!\[.*?\]\(.*?\)', '', body)
body = re.sub(r'\*.*?\*', '', body)
body = re.sub(r'#.*', '', body, flags=re.MULTILINE)
body = re.sub(r'<.*?>', '', body)

words = body.split()
print(f"Article body word count: {len(words)}")
print(f"Target range: 300-500 words")
if 300 <= len(words) <= 500:
    print("✓ WITHIN target range")
else:
    print("✗ OUTSIDE target range")
