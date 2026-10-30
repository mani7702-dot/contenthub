#!/usr/bin/env python3
"""Try multiple approaches to find secondary sources for the gut bacteria aging study."""
import subprocess, re

ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# 1. Check University of Hawaii at Manoa press release
urls = [
    "https://www.hawaii.edu/news/2026/10/gut-microbiome-aging/",
    "https://manoa.hawaii.edu/news/2026/gut-microbiome-aging/",
]
for url in urls:
    p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", ua, url], capture_output=True)
    html = p.stdout.decode("utf-8", errors="replace")
    if len(html) > 500:
        title = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
        t = title.group(1).strip() if title else "NO TITLE"
        print(f"FOUND: {url}")
        print(f"Title: {t}")
        # Extract paragraphs
        paras = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL | re.IGNORECASE)
        for para in paras[:10]:
            clean = re.sub(r"<[^>]+>", "", para).strip()
            if len(clean) > 50:
                print(f"  PARA: {clean[:200]}")
        print()
    else:
        print(f"NOT FOUND or empty: {url} (chars: {len(html)})")

# 2. Try Google News RSS for "gut microbiome aging"
rss_url = "https://news.google.com/rss/search?q=gut+microbiome+aging+hawaii"
p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", ua, rss_url], capture_output=True)
rss_html = p.stdout.decode("utf-8", errors="replace")
print(f"\nGoogle News RSS chars: {len(rss_html)}")
if len(rss_html) > 100:
    titles = re.findall(r"<title[^>]*>(.*?)</title>", rss_html, re.DOTALL | re.IGNORECASE)
    links = re.findall(r"<link[^>]*>(.*?)</link>", rss_html, re.DOTALL | re.IGNORECASE)
    for i, t in enumerate(titles[:8]):
        clean_t = re.sub(r"<!\[CDATA\[|\]\]>", "", t).strip()
        print(f"  RSS Title {i+1}: {clean_t}")
        if i < len(links)-1:
            clean_l = re.sub(r"<!\[CDATA\[|\]\]>", "", links[i+1]).strip()
            print(f"  RSS Link {i+1}: {clean_l}")

# 3. Try Nature.com / Springer Nature for the study
for url3 in [
    "https://www.nature.com/articles/s41598-026-00000-0",
    "https://www.scientificreports.com/",
]:
    p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, url3], capture_output=True)
    html3 = p.stdout.decode("utf-8", errors="replace")
    print(f"\n{url3}: chars={len(html3)}")
