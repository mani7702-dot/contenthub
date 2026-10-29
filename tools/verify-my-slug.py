#!/usr/bin/env python3
"""Simulate the deploy.sh slug computation and compare with frontmatter slug."""
import re

title = "How Did a Texas Barber Return $128,000 He Found at an ATM to Its Owner?"

# Simulate deploy.sh pipeline:
# tr "[:upper:]" "[:lower:]" -> .lower()
# sed "s/[^a-z0-9]\+/-/g; s/^-//; s/-\$//" -> replace non-alphanumeric runs with dashes, strip leading/trailing dashes
# cut -c1-90 -> first 90 chars
deploy_slug = title.lower()
deploy_slug = re.sub(r"[^a-z0-9]+", "-", deploy_slug).strip("-")[:90]

# build.py slug (from frontmatter)
frontmatter_slug = "how-did-a-texas-barber-return-128-000-he-found-at-an-atm-to-its-owner"

print(f"Title:          {title}")
print(f"deploy.sh slug: {deploy_slug}")
print(f"frontmatter:    {frontmatter_slug}")
print(f"Match: {deploy_slug == frontmatter_slug}")
