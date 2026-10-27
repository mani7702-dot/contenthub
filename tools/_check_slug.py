#!/usr/bin/env python3
"""Compute the article slug from the title, matching build.py logic."""
import re

with open('/home/ubuntu/contenthub/content/news/2026-10-27-kikai-supervolcano-refilling.md') as f:
    txt = f.read()

m = re.match(r'^---\s*\n(.*?)\n---\s*\n', txt, re.S)
meta = {}
if m:
    for line in m.group(1).split('\n'):
        if ':' in line and not line.startswith((' ', '-')):
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip().strip('"\'')

title = meta.get('title', '')
# build.py: slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
slug_build = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]

# deploy.sh: tr lower, sed s/[^a-z0-9]+/-/g, strip leading/trailing dash, cut -c1-90
slug_deploy = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]

print(f"Title: {title}")
print(f"Slug (build.py): {slug_build}")
print(f"Slug (deploy.sh): {slug_deploy}")
print(f"Match: {slug_build == slug_deploy}")
print(f"URL: https://mani7702-dot.github.io/contenthub/articles/{slug_build}.html")

# Also verify article_id = slug in build.py
# a["id"] = slug, article file = a["id"] + ".html"
print(f"Article file: articles/{slug_build}.html")
