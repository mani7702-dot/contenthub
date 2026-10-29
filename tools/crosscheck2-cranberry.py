#!/usr/bin/env python3
"""Cross-check cranberry juice tooth decay research via multiple approaches."""
import subprocess, re, json

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# 1. Try Google News RSS search for cranberry tooth decay
gn_url = "https://news.google.com/rss/search?q=cranberry+juice+tooth+decay+University+Illinois+Chicago"
result = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, gn_url], capture_output=True, text=True)
html = result.stdout
print(f"Google News RSS response length: {len(html)}")

# Parse RSS
items = re.findall(r'<item[^>]*>(.*?)</item>', html, re.DOTALL)
print(f"\nGoogle News RSS items found: {len(items)}")
for item in items[:10]:
    title = re.search(r'<title[^>]*>(.*?)</title>', item, re.DOTALL)
    link = re.search(r'<link[^>]*>(.*?)</link>', item, re.DOTALL)
    if title:
        t = re.sub(r'\s+', ' ', title.group(1).strip())
        l = link.group(1).strip() if link else ""
        print(f"  Title: {t}")
        print(f"  Link:  {l}")
        print()

# 2. Try Bing News search
bing_url = "https://www.bing.com/news/search?q=cranberry+juice+tooth+decay+University+of+Illinois+Chicago"
result2 = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, bing_url], capture_output=True, text=True)
html2 = result2.stdout
print(f"\nBing News response length: {len(html2)}")

# Extract article snippets from Bing
snippets = re.findall(r'<p[^>]*class="b_algoSlug[^"]*"[^>]*>(.*?)</p>', html2, re.DOTALL | re.IGNORECASE)
snippets2 = re.findall(r'<p[^>]*>(.*?)</p>', html2, re.DOTALL)
for s in snippets2[:20]:
    clean = re.sub(r'<[^>]+>', '', s).strip()
    if len(clean) > 40 and 'cranberry' in clean.lower():
        print(f"  Bing snippet: {clean[:300]}")

# 3. Try UIC website directly
uic_url = "https://uic.edu/edu-health-sciences/"
result3 = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, uic_url], capture_output=True, text=True)
html3 = result3.stdout
print(f"\nUIC response length: {len(html3)}")

# 4. Try the ScienceDaily article page for source/journal info
sd_url = "https://www.sciencedaily.com/releases/2026/10/261028232701.htm"
result4 = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, sd_url], capture_output=True, text=True)
html4 = result4.stdout

# Look for journal reference and citation
journal = re.findall(r'(?:Journal:[^<]*|published in[^<]*|Nature|Science|Journal of[^<]{0,100})', html4)
print(f"\nScienceDaily journal refs: {journal[:5]}")

# Look for the original research link
research_links = re.findall(r'href="(https?://[^"]*pubmed[^"]*)"', html4, re.IGNORECASE)
research_links2 = re.findall(r'href="(https?://[^"]*ncbi[^"]*)"', html4, re.IGNORECASE)
research_links3 = re.findall(r'href="(https?://[^"]*doi[^"]*)"', html4, re.IGNORECASE)
print(f"PubMed links: {research_links[:3]}")
print(f"NCBI links: {research_links2[:3]}")
print(f"DOI links: {research_links3[:3]}")

# Look for the institution name in the article
inst = re.findall(r'(University of Illinois[^<]{0,100})', html4)
print(f"\nInstitution mentions: {inst[:5]}")

# Look for author/credit block
credit = re.findall(r'(Christine Wu[^<]{0,100})', html4)
print(f"Author mentions: {credit[:5]}")

# Extract the full description meta
meta = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html4, re.IGNORECASE | re.DOTALL)
if meta:
    print(f"\nMeta description: {meta.group(1).strip()[:500]}")

# Look for journal name
journal_match = re.search(r'journal["\']?\s*content="([^"]+)"', html4, re.IGNORECASE)
if journal_match:
    print(f"Journal: {journal_match.group(1)}")

# Try to find the Nature/Science/Database link
links_all = re.findall(r'href="(https?://[^"]*sciencedaily[^"]*releases[^"]*)"', html4)
print(f"\nAll ScienceDaily release links: {links_all[:5]}")
