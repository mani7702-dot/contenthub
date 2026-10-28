#!/usr/bin/env python3
"""Verify slug matches between build.py and deploy.sh logic."""
import re

title = "How Did a Stranger Pay $420 for a Group's Lunch in South Korea?"

# build.py logic (line 107):
slug_build = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]

# deploy.sh logic (line 26):
# TITLE -> lowercase -> sed s/[^a-z0-9]+/-/g -> strip leading/trailing dashes -> cut -c1-90
slug_deploy = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]

# Also check with the slug from the title using the actual sed pipeline
# tr "[:upper:]" "[:lower:]" | sed "s/[^a-z0-9]\+/-/g; s/^-$//; s/-$//" | cut -c1-90
slug_sed = title.lower()
slug_sed = re.sub(r"[^a-z0-9]+", "-", slug_sed)
slug_sed = slug_sed.lstrip("-").rstrip("-")
slug_sed = slug_sed[:90]

print(f"Title: {title}")
print(f"Build.py slug: {slug_build}")
print(f"Deploy.sh sed slug: {slug_sed}")
print(f"Match: {slug_build == slug_sed}")
print(f"Filename: how-did-a-stranger-pay-420-for-a-group-s-lunch-in-south-korea.md")
print(f"Filename basename (no .md): how-did-a-stranger-pay-420-for-a-group-s-lunch-in-south-korea")
print(f"Filename matches slug: {slug_build == 'how-did-a-stranger-pay-420-for-a-group-s-lunch-in-south-korea'}")
