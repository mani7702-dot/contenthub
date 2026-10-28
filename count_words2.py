#!/usr/bin/env python3
import re
path = "/home/ubuntu/contenthub/content/blog/2026-10-28-how-did-a-teacher-daily-positivity-practice-spread-through-an-elementary-school.md"
with open(path, "r") as f:
    text = f.read()
m = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', text, re.S)
body = m.group(2) if m else text
words = body.split()
print(f"Body word count: {len(words)}")
