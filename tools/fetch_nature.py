#!/usr/bin/env python3
"""Fetch Nature Communications page and extract abstract + authors."""
import subprocess
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
URL = "https://www.nature.com/articles/s41467-026-77572-3"

p = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, URL], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
soup = BeautifulSoup(html, "html.parser")

title_tag = soup.find("title")
print(f"TITLE: {title_tag.get_text() if title_tag else 'NOT FOUND'}")

# Abstract
for div in soup.find_all("div"):
    cls = div.get("class", "")
    if cls and "abstract" in str(cls).lower():
        text = div.get_text(" ", strip=True)
        if len(text) > 20:
            print(f"ABSTRACT: {text[:600]}")
            break

# Also try meta description
meta = soup.find("meta", attrs={"name": "citation_author"})
if meta:
    print(f"AUTHOR (citation): {meta.get('content', '')}")

# Find all citation_author metas
authors = soup.find_all("meta", attrs={"name": "citation_author"})
for a in authors:
    print(f"  Author: {a.get('content', '')}")

# Find DOI
doi_meta = soup.find("meta", attrs={"name": "citation_doi"})
if doi_meta:
    print(f"DOI: {doi_meta.get('content', '')}")

# Keywords
kw_meta = soup.find("meta", attrs={"name": "citation_keywords"})
if kw_meta:
    print(f"Keywords: {kw_meta.get('content', '')}")

# First paragraphs
printed = 0
for p_tag in soup.find_all("p"):
    text = p_tag.get_text(" ", strip=True)
    if len(text) > 80:
        print(f"PARA {printed}: {text[:300]}")
        printed += 1
        if printed >= 5:
            break
