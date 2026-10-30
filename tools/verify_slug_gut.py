#!/usr/bin/env python3
"""Verify the slug for the article title."""
import re
t = "How Did the Bacteria in Your Gut Reveal How Fast You're Aging?"
slug = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:90]
print(f"Title: {t}")
print(f"Slug: {slug}")
