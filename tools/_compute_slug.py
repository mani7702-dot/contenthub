#!/usr/bin/env python3
"""Compute slug for article title."""
import re
import sys

title = sys.argv[1] if len(sys.argv) > 1 else "How Did a Simple Fiber Supplement Reduce Arthritis Pain and Boost Strength?"
slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:90]
print(slug)
