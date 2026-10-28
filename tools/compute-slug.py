#!/usr/bin/env python3
"""Compute the slug from the article title."""
import re

title = "How Do Our Immune Cells 'Feel' the World Around Them With a Hidden Sense of Touch?"
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(f"Title: {title}")
print(f"Slug: {slug}")
