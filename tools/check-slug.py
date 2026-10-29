#!/usr/bin/env python3
import re
title = "Europe's youth take to the streets - they feel locked out of a promising future"
slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:90]
print(f"Title-derived slug: {slug}")
# Also check the frontmatter slug in the article
