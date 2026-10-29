#!/usr/bin/env python3
"""Verify slug computation for the article title."""
import re
title = "Can You Watch Rare Cheetah Cubs Live From Birth at the Smithsonian?"
slug = re.sub(r'[^a-z0-9]+', '-', '-'.join([w for w in title.lower().split() if w])).strip('-')[:90]
print(f"Slug: {slug}")
print(f"Filename: 2026-10-29-{slug}.md")
