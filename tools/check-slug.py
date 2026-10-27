#!/usr/bin/env python3
import re
TITLE = "How Did 10 Million More Acres of Amazon Rainforest Get Saved in Just 7 Months?"
slug = re.sub(r"[^a-z0-9]+", "-", TITLE.lower()).strip("-")[:90]
print("Slug:", slug)
print("Length:", len(slug))
