#!/usr/bin/env python3
"""Verify slug computation from title."""
import re, sys
title = sys.argv[1] if len(sys.argv) > 1 else "How Do T Cells Feel Their Surroundings to Help Us Stay Healthy?"
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(f"Title: {title}")
print(f"Slug:  {slug}")
