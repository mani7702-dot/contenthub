#!/usr/bin/env python3
"""Extract key facts from ScienceDaily EV battery article."""
import re
import sys

html = open(sys.argv[1], encoding="utf-8", errors="replace").read()
# Remove scripts/styles
html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r"<[^>]+>", " ", html)
text = re.sub(r"&[a-z]+;", " ", text)
text = re.sub(r"\s+", " ", text)

# Find key facts
print("=== DOI mention ===")
for m in re.finditer(r"DOI[^\n]*", text):
    print(m.group()[:200])

print("\n=== Journal mention ===")
for m in re.finditer(r"Advanced Functional Materials[^\n]*", text):
    print(m.group()[:200])

print("\n=== Publication date ===")
for m in re.finditer(r"October[^\n]*2026", text):
    print(m.group()[:100])

print("\n=== Key numbers ===")
for m in re.finditer(r"\d+\.?\d*\s*(?:nanometer|nm|micrometer|micron|nm|times|lifespan|battery)", text, re.I):
    print(m.group()[:100])
