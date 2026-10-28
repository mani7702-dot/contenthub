#!/usr/bin/env python3
"""Fetch the Current Archaeology article about Lismore - find the actual article URL."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://www.archaeology.co.uk/"
p = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url], capture_output=True, text=True)
content = p.stdout

# Find the article element and extract its link
# Look for article tags or post-item divs
articles = re.findall(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
print(f"Found {len(articles)} article elements")
for art in articles:
    # Find links in article
    links = re.findall(r'href="([^"]*)"', art)
    for link in links:
        if 'archaeology.co.uk' in link or '/articles/' in link:
            print(f"  Article link: {link}")
    # Also print the text
    text = re.sub(r'<[^>]+>', ' ', art)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    print(f"  Text: {text[:200]}")
    print()

# Also try finding post-item divs
post_items = re.findall(r'class="post-item[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', content, re.DOTALL)
for item in post_items:
    links = re.findall(r'href="([^"]*)"', item)
    text = re.sub(r'<[^>]+>', ' ', item)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    if 'scottish' in text.lower() or 'island' in text.lower():
        print(f"Post-item links: {links}")
        print(f"Post-item text: {text[:300]}")
