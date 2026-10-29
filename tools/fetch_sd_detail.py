#!/usr/bin/env python3
"""Fetch a full ScienceDaily article and extract key facts."""
import sys, subprocess
from bs4 import BeautifulSoup

URL = "https://www.sciencedaily.com/releases/2026/10/261025073046.htm"
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

p = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, URL], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
soup = BeautifulSoup(html, "html.parser")

print("=== PAGE TITLE ===")
title_tag = soup.find("title")
print(title_tag.get_text() if title_tag else "NOT FOUND")

print("\n=== META DESCRIPTION ===")
meta_desc = soup.find("meta", attrs={"name": "description"})
if meta_desc:
    print(meta_desc.get("content", "")[:500])
else:
    print("NOT FOUND")

print("\n=== ALL PARAGRAPHS (with substantial text) ===")
for p_tag in soup.find_all("p"):
    text = p_tag.get_text(" ", strip=True)
    if len(text) > 60:
        print(text[:400])
        print("---")
