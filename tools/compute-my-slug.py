#!/usr/bin/env python3
"""Compute slug from a title using the same formula as build.py and deploy.sh."""
import re, sys
title = sys.argv[1] if len(sys.argv) > 1 else input("Title: ")
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(slug)
