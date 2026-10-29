#!/usr/bin/env python3
"""Cross-check the laser memory story against UC San Diego press release and Nature Communications."""
import subprocess, re
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Fetch ScienceDaily article
p = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA,
                    "https://www.sciencedaily.com/releases/2026/10/261025073046.htm"],
                   capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
soup = BeautifulSoup(html, "html.parser")

# Extract title and meta
title_tag = soup.find("title")
print(f"Title: {title_tag.get_text() if title_tag else 'N/A'}")

meta_desc = soup.find("meta", attrs={"name": "description"})
if meta_desc:
    print(f"Meta desc: {meta_desc.get('content', '')[:300]}")

# Extract all links
print("\n=== All external links ===")
for a in soup.find_all("a"):
    href = a.get("href")
    if href and href.startswith("http"):
        text = a.get_text(strip=True)
        if text:
            print(f"  {text[:50]}: {href[:100]}")

# Extract DOI
dois = re.findall(r'(10\.\d+/[^\s<>"\']+)', html)
print(f"\nDOIs found: {dois}")

# Extract all paragraph text for facts
print("\n=== Key facts from article ===")
paragraphs = []
for p_tag in soup.find_all("p"):
    text = p_tag.get_text(" ", strip=True)
    if len(text) > 80:
        paragraphs.append(text)

for p_text in paragraphs:
    print(f"  - {p_text[:250]}")

# Try Nature Communications
print("\n=== Nature Communications (journal search) ===")
nc_url = "https://www.nature.com/articles/s41467-026-XXXXX"  # placeholder
# Try searching for the paper
search_url = "https://www.nature.com/search?q=optical+switching+laser+magnetic+memory+ndao+uc+san+diego"
p2 = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, search_url], capture_output=True)
news_html = p2.stdout.decode("utf-8", errors="replace")
news_soup = BeautifulSoup(news_html, "html.parser")
results = news_soup.find_all("a", href=re.compile(r"/articles/"))
count = 0
for r in results:
    title = r.get_text(strip=True)
    href = r.get("href", "")
    if "optical" in title.lower() or "laser" in title.lower() or "magnetic" in title.lower():
        print(f"  {title[:100]}: https://www.nature.com{href}")
        count += 1
        if count >= 5:
            break

if count == 0:
    print("  No matching articles found in Nature search")
