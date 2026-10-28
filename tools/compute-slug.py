#!/usr/bin/env python3
"""Compute ContentHub slug from a title (mirrors build.py line 107 / deploy.sh)."""
import re, sys
title = sys.argv[1] if len(sys.argv) > 1 else "How Did Scientists Make Electric Car Batteries Smaller and Longer-Lasting?"
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(slug)
