#!/usr/bin/env python3
import re
title = "How Did Scientists Simulate the Universe's First 2 Billion Years in One Giant Computer?"
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(f"Title: {title}")
print(f"Slug: {slug}")
print(f"Length: {len(slug)}")
fn = f"2026-10-29-{slug}.md"
print(f"Filename: content/news/{fn}")
