#!/usr/bin/env python3
"""Extract abstract and authors from cached Nature HTML."""
import subprocess
from bs4 import BeautifulSoup
import re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
URL = "https://www.nature.com/articles/s41467-026-77572-3"

p = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, URL], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Save for inspection
with open("/tmp/nature_page.html", "w") as f:
    f.write(html)

soup = BeautifulSoup(html, "html.parser")

# Title
title_tag = soup.find("title")
print(f"PAGE TITLE: {title_tag.get_text() if title_tag else 'NOT FOUND'}")

# Meta tags
for meta in soup.find_all("meta"):
    name = meta.get("name", "")
    content = meta.get("content", "")
    if "citation" in name and "author" in name:
        print(f"  Author: {content}")
    if "citation_title" in name:
        print(f"  Article Title: {content}")
    if "citation_doi" in name:
        print(f"  DOI: {content}")

# Find abstract in the page
abstract_divs = soup.find_all(attrs={"data-test": "abstract-body"})
if abstract_divs:
    for d in abstract_divs:
        text = d.get_text(" ", strip=True)
        print(f"ABSTRACT: {text[:800]}")
else:
    # Try to find abstract by text content
    for p_tag in soup.find_all("p"):
        text = p_tag.get_text(" ", strip=True)
        if "abstract" in text.lower()[:50] or "using light" in text.lower()[:50] or "optical switching" in text.lower()[:50]:
            print(f"TEXT: {text[:400]}")

# Search for abstract text in the full HTML
abstract_match = re.search(r'"description"\s*:\s*"([^"]{100,})"', html)
if abstract_match:
    print(f"\nMETA DESC: {abstract_match.group(1)[:500]}")

# Look for abstract in JSON-LD
ld_scripts = soup.find_all("script", type="application/ld+json")
for script in ld_scripts:
    text = script.get_text()
    if "abstract" in text.lower():
        print(f"\nLD JSON abstract found: {text[:600]}")
        break
