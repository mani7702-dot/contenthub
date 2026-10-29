#!/usr/bin/env python3
"""Verify the slug computed from the article's title matches the expected slug."""
import re

# Read title from frontmatter
with open("content/news/2026-10-29-how-did-a-tiny-laser-beam-make-computer-memory-1000-times-faster.md", encoding="utf-8") as f:
    txt = f.read()

# Extract title
m = re.search(r'^title:\s*"(.*)"', txt, re.M)
title = m.group(1) if m else ""
# Extract slug
m2 = re.search(r'^slug:\s*(.*)', txt, re.M)
frontmatter_slug = m2.group(1).strip() if m2 else ""

# Compute slug (same as build.py and deploy.sh)
computed = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]

print(f"Title: {title}")
print(f"Frontmatter slug: {frontmatter_slug}")
print(f"Computed slug: {computed}")
print(f"Deploy.sh will use: {computed}")
print(f"Match: {computed == frontmatter_slug}")
