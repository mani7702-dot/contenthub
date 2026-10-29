#!/usr/bin/env python3
"""Compute the slug for a given title, matching build.py/deploy.sh logic."""
import re
import sys
title = sys.argv[1]
slug = re.sub(r"[^a-z0-9]+", "-", "-".join(w for w in title.lower().split() if w)).strip("-")[:90]
print(slug)
