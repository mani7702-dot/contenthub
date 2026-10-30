#!/usr/bin/env python3
"""Extract the Nature.com article URL from Google News redirect page."""
import subprocess, re

ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# The Google News RSS link - try fetching with different params
url = "https://news.google.com/rss/articles/CBMieEFVX3lxTFB1Q0NPVGdLa1hLR3FTUk9kVmY0WWNtMEcyYVVrRFpvU3Z2bGtEMzhuZVdtNTZ5VkhGLXVoQ3Z0c1NBZDdnbm9ONTBRNk5JMzNHcERLck9lU1ZENUFtLVoyOVg4UHVEejFhZDZtQ0pTQy1rVVllcGhLYw?oc=5"
p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", ua, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Look for nature.com links in the HTML
nature_links = re.findall(r'https?://[^\s"\'<>]+nature\.com[^\s"\'<>]*s41598[^\s"\'<>]*', html)
print(f"Nature links found: {len(nature_links)}")
for link in nature_links[:5]:
    print(f"  {link}")

# Also look for the original article URL in any form
all_urls = re.findall(r'https?://[^\s"\'<>]+', html)
for u in all_urls:
    if 'nature' in u.lower() or 'sciencedaily' in u.lower() or 'hawaii' in u.lower() or 'scientific-reports' in u.lower():
        print(f"  Relevant: {u[:150]}")

# Try to find the article via Nature search
print("\n--- Trying Nature search ---")
search_url = "https://www.nature.com/search?query=gut+microbiome+biological+aging+Hawaii+Maunakea"
p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", ua, search_url], capture_output=True)
html2 = p.stdout.decode("utf-8", errors="replace")
print(f"Nature search chars: {len(html2)}")
# Look for article titles and links
titles = re.findall(r'<a[^>]*href="(.*?)s41598[^"<>]*"[^>]*>(.*?)</a>', html2, re.DOTALL | re.IGNORECASE)
print(f"Article links found: {len(titles)}")
for href, title in titles[:5]:
    print(f"  Title: {title.strip()[:100]}")
    print(f"  Href: {href[:100]}")

# Also look for the article via Google cache or other approach
print("\n--- Trying Semantic Scholar ---")
ss_url = "https://api.semanticscholar.org/graph/v1/paper/search?query=gut+microbiome+biological+aging+hawaii&limit=5"
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, "-H", "Accept: application/json", ss_url], capture_output=True)
print(f"Semantic Scholar response: {p.stdout[:500]}")
