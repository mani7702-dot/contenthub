#!/usr/bin/env python3
"""Compute the title-derived slug for the article."""
import re
title = "How Did Three Italian Hobbits Find an Irishman's Lost Wedding Ring and Fly to Ireland?"
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(f"Title: {title}")
print(f"Slug: {slug}")
print(f"Slug length: {len(slug)}")
