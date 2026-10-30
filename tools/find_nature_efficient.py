#!/usr/bin/env python3
"""Efficient search for the Nature Scientific Reports article and secondary verification."""
import subprocess, re

ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Approach 1: Try Nature's search page and extract article links
print("=== Nature.com search ===")
search_url = "https://www.nature.com/search?query=gut+microbiome+DNA+methylation+biological+aging+Maunakea&order=relevance"
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, "-H", "Accept: text/html", search_url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
print(f"Search page chars: {len(html)}")

# Extract article links (Nature article URLs contain /articles/)
article_links = re.findall(r'href="(https?://www\.nature\.com/articles/s41598[^\"]*)"', html)
print(f"Article links found: {len(article_links)}")
for link in article_links[:5]:
    print(f"  {link}")

# Also look for relative links
rel_links = re.findall(r'href="(/articles/s41598[^"]*)"', html)
print(f"Relative article links: {len(rel_links)}")
for link in rel_links[:5]:
    print(f"  https://www.nature.com{link}")

# If we found Nature article links, fetch the first one
all_links = article_links + [f"https://www.nature.com{l}" for l in rel_links]
if all_links:
    url = all_links[0]
    print(f"\n=== Fetching: {url} ===")
    p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, "-H", "Accept: text/html", url], capture_output=True)
    html = p.stdout.decode("utf-8", errors="replace")
    title = re.search(r'<meta name="dc.title" content="(.*?)"', html) or re.search(r'<h1[^>]*id="article-title"[^>]*>(.*?)</h1>', html, re.DOTALL) or re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
    if title:
        print(f"Title: {title.group(1).strip()[:200]}")
    description = re.search(r'<meta name="description" content="(.*?)"', html)
    if description:
        print(f"Description: {description.group(1)[:300]}")
    # Check for key terms
    for term in ["Bifidobacterium", "Succinivibrio", "DunedinPACE", "123 adults", "15%"]:
        if term.lower() in html.lower():
            print(f"  ✓ Found: {term}")
        else:
            print(f"  ✗ Missing: {term}")

# Approach 2: Try fetching the UH press release directly
print("\n=== UH Press Release ===")
# The Google News RSS said "Gut bacteria tied to biological aging, new UH study finds"
# Try various UH news URL patterns
uh_urls = [
    "https://www.hawaii.edu/news/2026/10/27/gut-bacteria-tied-to-biological-aging/",
    "https://www.hawaii.edu/news/2026/10/27/gut-bacteria-biological-aging/",
    "https://www.hawaii.edu/news/2026/10/27/gut-microbiome-aging-biological/",
]
for url in uh_urls:
    p = subprocess.run(["curl", "-sL", "--max-time", "10", "-A", ua, url], capture_output=True)
    html = p.stdout.decode("utf-8", errors="replace")
    title = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
    t = title.group(1).strip() if title else ""
    if len(html) > 10000 and "not found" not in t.lower() and "page not found" not in t.lower():
        print(f"  FOUND: {url}")
        print(f"  Title: {t[:150]}")
        # Extract paragraphs
        html_clean = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        html_clean = re.sub(r"<style[^>]*>.*?</style>", "", html_clean, flags=re.DOTALL | re.IGNORECASE)
        paras = re.findall(r"<p[^>]*>(.*?)</p>", html_clean, re.DOTALL | re.IGNORECASE)
        for para in paras[:15]:
            clean = re.sub(r"<[^>]+>", "", para).strip()
            if len(clean) > 50:
                print(f"  PARA: {clean[:250]}")
    else:
        print(f"  Not found: {url} (chars: {len(html)})")
