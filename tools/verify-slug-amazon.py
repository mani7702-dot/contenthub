#!/usr/bin/env python3
"""Verify that build.py and deploy.sh produce the same slug."""
import re, subprocess

TITLE = "How Did 10 Million More Acres of Amazon Rainforest Get Saved in Just 7 Months?"

# build.py logic (line 101)
slug_build = re.sub(r"[^a-z0-9]+", "-", TITLE.lower()).strip("-")[:90]
print("build.py slug:", slug_build)

# deploy.sh logic (lines 25-26)
deploy_slug = subprocess.run(
    ["bash", "-c", f'echo "{TITLE}" | tr "[:upper:]" "[:lower:]" | sed "s/[^a-z0-9]\\+/-/g; s/^-//; s/-$//" | cut -c1-90'],
    capture_output=True, text=True
).stdout.strip()
print("deploy.sh slug:", deploy_slug)
print("MATCH:", slug_build == deploy_slug)
