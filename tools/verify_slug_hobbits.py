#!/usr/bin/env python3
"""Verify the slug for the Italian hobbits article."""
import re
title = "How Did Three Italian Hobbits Find an Irishman's Lost Wedding Ring and Fly to Ireland?"
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(f"Title: {title}")
print(f"Slug:  {slug}")
print(f"Length: {len(slug)}")
print(f"Expected: how-did-three-italian-hobbits-find-an-irishman-s-lost-wedding-ring-and-fly-to-ireland")
print(f"Match: {slug == 'how-did-three-italian-hobbits-find-an-irishman-s-lost-wedding-ring-and-fly-to-ireland'}")
