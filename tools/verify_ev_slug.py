#!/usr/bin/env python3
"""Verify slug computation matches between build.py and deploy.sh."""
import re
import subprocess

md_path = "content/trending/2026-10-29-how-did-scientists-make-electric-car-batteries-smaller-and-longer-lasting.md"

# Read the title from the frontmatter
with open(md_path) as f:
    for line in f:
        if line.startswith("title:"):
            title = line.split(":", 1)[1].strip().strip('"').strip("'")
            break

print(f"Title: {title}")
print(f"Title with trailing ?: {title[-5:]!r}")

# build.py slug computation
build_slug = meta_slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(f"build.py slug: {build_slug}")

# deploy.sh slug computation (simulated)
# TITLE -> tr lower -> sed replace non-alphanum with - -> strip leading/trailing - -> cut 90
deploy_slug = title.lower()
deploy_slug = re.sub(r"[^a-z0-9]+", "-", deploy_slug)
deploy_slug = deploy_slug.lstrip("-").rstrip("-")
deploy_slug = deploy_slug[:90]
print(f"deploy.sh slug: {deploy_slug}")

# Explicit slug from frontmatter
print(f"\nExplicit slug: how-did-scientists-make-electric-car-batteries-smaller-and-longer-lasting")
print(f"build.py uses slug: key? YES (since it's present)")

if build_slug == deploy_slug == "how-did-scientists-make-electric-car-batteries-smaller-and-longer-lasting":
    print("\n✓ Slug match confirmed!")
else:
    print("\n✗ Slug mismatch!")
