#!/usr/bin/env python3
"""Count words in main body only (excluding for-grown-ups and Sources)."""
import sys, re

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    content = f.read()

parts = content.split("---", 2)
body = parts[2] if len(parts) >= 3 else content

# Cut off at ## Sources or ## for-grown-ups
cut_markers = ["## Sources", "## for-grown-ups", "## Sources\n"]
main_body = body
for marker in ["## for-grown-ups", "## Sources"]:
    idx = main_body.find(marker)
    if idx > 0:
        main_body = main_body[:idx]

main_body = re.sub(r'!\[.*?\]\(.*?\)', '', main_body)
main_body = re.sub(r'#.*', '', main_body, flags=re.MULTILINE)
main_body = re.sub(r'<.*?>', '', main_body)

words = main_body.split()
print(f"Main body word count: {len(words)}")
print(f"Target range: 300-500 words")
if 300 <= len(words) <= 500:
    print("✓ WITHIN target range")
else:
    print("✗ OUTSIDE target range")
