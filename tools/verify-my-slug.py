#!/usr/bin/env python3
import re
title = "How Did a Tiny Scottish Island Become One Of Early Christianitys Greatest Centers?"
slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90]
print(f"Title: {title}")
print(f"Slug: {slug}")
print(f"Expected filename: 2026-10-28-{slug}.md")
print(f"Actual filename: 2026-10-28-how-did-a-tiny-scottish-island-become-one-of-early-christianitys-greatest-centers.md")
