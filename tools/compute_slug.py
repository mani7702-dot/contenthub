#!/usr/bin/env python3
"""Compute the slug for the kangaroo rescue article."""
import re
title = "How Did a Kangaroo End Up 3 Kilometers Offshore — And How Did Divers Save It?"
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(f"Title: {title}")
print(f"Slug: {slug}")
