#!/usr/bin/env python3
"""Search Nature via their API and try to find the article."""
import subprocess, re, json

ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try Nature's search API (returns JSON)
print("=== Nature search API ===")
api_url = "https://www.nature.com/nature/articlesapi/search?query=gut+microbiome+biological+aging&order=relevance&per_page=5"
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, api_url], capture_output=True)
response = p.stdout.decode("utf-8", errors="replace")
print(f"API response ({len(response)} chars): {response[:500]}")

# Try to find via Nature's search results page - look for ALL article links
print("\n=== Nature search page - all /articles/ links ===")
search_url = "https://www.nature.com/search?query=gut+microbiome+DNA+methylation+aging+Maunakea"
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, search_url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
# Find ALL links to /articles/
all_art_links = re.findall(r'href="([^"]*/articles/[^"]*)"', html)
print(f"All /articles/ links found: {len(all_art_links)}")
for link in all_art_links[:10]:
    print(f"  {link[:200]}")

# Also try a simpler Nature search
print("\n=== Simple Nature search ===")
search_url2 = "https://www.nature.com/search?query=gut+microbiome+aging+Maunakea"
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, search_url2], capture_output=True)
html2 = p.stdout.decode("utf-8", errors="replace")
all_art_links2 = re.findall(r'href="([^"]*/articles/[^"]*)"', html2)
print(f"All /articles/ links found: {len(all_art_links2)}")
for link in all_art_links2[:10]:
    print(f"  {link[:200]}")

# Try Nature's Scientific Reports journal page
print("\n=== Sci Rep journal page ===")
sr_url = "https://www.nature.com/srep/"
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, sr_url], capture_output=True)
html3 = p.stdout.decode("utf-8", errors="replace")
# Look for the most recent articles
titles = re.findall(r'<a[^>]*href="([^"]*/srep/articles/[^"]*)"[^>]*>(.*?)</a>', html3, re.DOTALL)
print(f"Recent Sci Rep articles: {len(titles)}")
for link, title_text in titles[:5]:
    clean = re.sub(r"<[^>]+>", "", title_text).strip()
    print(f"  {clean[:100]} -> {link[:100]}")
