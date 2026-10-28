#!/usr/bin/env python3
"""Quick body word count for the article."""
import re, sys
path = sys.argv[1]
t = open(path).read()
parts = t.split('---', 2)
if len(parts) >= 3:
    body = parts[2]
else:
    body = t
words = len(re.findall(r'\S+', body))
print(f"Body word count ~{words}")
