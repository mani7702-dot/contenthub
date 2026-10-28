#!/usr/bin/env python3
"""Compute slug from title using build.py's formula."""
import re

title = "How Did a Stranger Pay $420 for a Group's Lunch in South Korea?"
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(f"Title: {title}")
print(f"Slug: {slug}")
