#!/usr/bin/env python3
"""Cross-check: Fetch the Nature/Scientific Reports journal article for cranberry tooth decay study."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "http://dx.doi.org/10.1038/s41598-026-56025-3"

result = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url], capture_output=True, text=True)
final_url = result.url if hasattr(result, 'url') else url
html = result.stdout

print(f"DOI redirect - Final URL: {final_url}")
print(f"Response length: {len(html)}")

# Extract title
title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
if title_match:
    print(f"\nTitle: {title_match.group(1).strip()}")

# Extract description/meta
meta = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE | re.DOTALL)
if meta:
    print(f"\nMeta description: {meta.group(1).strip()[:600]}")

# Extract authors
authors = re.findall(r'<meta[^>]*name=["\']citation_author["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE)
print(f"\nAuthors: {authors[:10]}")

# Extract journal
journal = re.search(r'<meta[^>]*name=["\']citation_journal_title["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE)
if journal:
    print(f"Journal: {journal.group(1)}")

pub_date = re.search(r'<meta[^>]*name=["\']citation_date["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE)
if pub_date:
    print(f"Date: {pub_date.group(1)}")

# Extract paragraph text
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
paras = re.findall(r'<p[^>]*>(.*?)</p>', text, re.DOTALL)
for i, p in enumerate(paras[:25]):
    clean = re.sub(r'<[^>]+>', '', p).strip()
    if len(clean) > 30:
        print(f"\n--- Para {i+1} ---")
        print(clean[:600])

# Also try fetching via the Scientific Reports direct URL
print("\n\n=== Also checking alternate URL ===")
url2 = "https://www.nature.com/articles/s41598-026-56025-3"
result2 = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url2], capture_output=True, text=True)
html2 = result2.stdout
print(f"Nature.com response length: {len(html2)}")
title2 = re.search(r'<title[^>]*>(.*?)</title>', html2, re.DOTALL | re.IGNORECASE)
if title2:
    print(f"Title: {title2.group(1).strip()}")
meta2 = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html2, re.IGNORECASE | re.DOTALL)
if meta2:
    print(f"Meta: {meta2.group(1).strip()[:600]}")
