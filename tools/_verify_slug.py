#!/usr/bin/env python3
"""Verify ContentHub slug from a title (mirrors build.py / deploy.sh formula)."""
import re, sys
title = sys.argv[1] if len(sys.argv) > 1 else sys.exit("usage: _verify_slug.py \"<title>\"")
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(slug)
