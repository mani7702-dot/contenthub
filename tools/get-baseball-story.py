#!/usr/bin/env python3
"""Fetch and display the baseball team GNN article."""
import subprocess, re, gzip, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Fetch RSS feed
url = "https://www.goodnewsnetwork.org/feed/"
r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = r.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
text = data.decode("utf-8", errors="replace")
items = re.findall(r"<item>(.*?)</item>", text, re.DOTALL)

for item in items:
    title_match = re.search(r"<title>(.*?)</title>", item, re.DOTALL)
    link_match = re.search(r"<link>(.*?)</link>", item, re.DOTALL)
    if title_match and "baseball" in title_match.group(1).lower():
        title = html.unescape(title_match.group(1).strip())
        link = link_match.group(1).strip() if link_match else "N/A"
        desc_match = re.search(r"<description>(.*?)</description>", item, re.DOTALL)
        desc = ""
        if desc_match:
            desc = re.sub(r"<[^>]+>", "", desc_match.group(1)).strip()
            desc = html.unescape(desc)
        print(f"TITLE: {title}")
        print(f"LINK: {link}")
        print(f"DESC: {desc[:500]}")
        print("---")

        # Now fetch the full article
        print("\n=== FULL ARTICLE ===\n")
        r2 = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, link], capture_output=True)
        article_html = r2.stdout.decode("utf-8", errors="replace")

        # Save for inspection
        with open("/tmp/baseball-article.html", "w") as f:
            f.write(article_html)

        # Extract paragraphs
        content_match = re.search(r'class="[^"]*td-post-content[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', article_html, re.DOTALL)
        if not content_match:
            content_match = re.search(r'class="[^"]*entry-content[^"]*"[^>]*>(.*?)</div>\s*</div>', article_html, re.DOTALL)
        if content_match:
            html_content = content_match.group(1)
        else:
            html_content = article_html
            # Try to find main content area
            main_match = re.search(r"<main[^>]*>(.*?)</main>", article_html, re.DOTALL)
            if main_match:
                html_content = main_match.group(1)

        # Remove scripts and styles
        html_content = re.sub(r"<script[^>]*>.*?</script>", "", html_content, flags=re.DOTALL)
        html_content = re.sub(r"<style[^>]*>.*?</style>", "", html_content, flags=re.DOTALL)

        # Extract paragraphs
        paras = re.findall(r"<p[^>]*>(.*?)</p>", html_content, re.DOTALL)
        print(f"Found {len(paras)} paragraphs")
        for p in paras:
            text_para = re.sub(r"<[^>]+>", "", p).strip()
            text_para = html.unescape(text_para)
            if len(text_para) > 15:
                print(text_para[:600])
                print("---")
        break
