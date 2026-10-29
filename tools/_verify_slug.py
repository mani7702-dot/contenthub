#!/usr/bin/env python3
"""Compute the title-derived slug exactly like build.py line 107 / deploy.sh."""
import re, sys
title = sys.argv[1] if len(sys.argv) > 1 else sys.exit("usage: _verify_slug.py \"<title>\"")
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(slug)
