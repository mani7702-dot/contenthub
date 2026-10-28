#!/usr/bin/env python3
"""Fetch and display the baseball team GNN article full content."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

link = "https://www.goodnewsnetwork.org/high-school-baseball-team-has-all-the-vibes-of-success-but-never-won-a-game-kids-dont-mind/"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, link], capture_output=True)
article_html = r.stdout.decode("utf-8", errors="replace")

print(f"Article HTML length: {len(article_html)}")

# Try to find main content area - td-post-content or entry-content
content_match = re.search(r'class="[^"]*td-post-content[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', article_html, re.DOTALL)
if not content_match:
    content_match = re.search(r'class="[^"]*entry-content[^"]*"[^>]*>(.*?)</div>\s*</div>', article_html, re.DOTALL)
if not content_match:
    content_match = re.search(r'class="td-post-content[^"]*"[^>]*>(.*?)(?:</div>\s*</div>\s*</div>)', article_html, re.DOTALL)

if content_match:
    html_content = content_match.group(1)
    print(f"\nFound content section, length: {len(html_content)}")
else:
    article_match = re.search(r'<article[^>]*>(.*?)</article>', article_html, re.DOTALL)
    if article_match:
        html_content = article_match.group(1)
        print(f"\nFound article tag, length: {len(html_content)}")
    else:
        html_content = article_html
        print("\nNo content section found, using full page")

# Remove scripts and styles
html_content = re.sub(r"<script[^>]*>.*?</script>", "", html_content, flags=re.DOTALL)
html_content = re.sub(r"<style[^>]*>.*?</style>", "", html_content, flags=re.DOTALL)

# Extract paragraphs
paras = re.findall(r"<p[^>]*>(.*?)</p>", html_content, re.DOTALL)
print(f"\n=== Found {len(paras)} paragraphs ===\n")
for p in paras:
    text_para = re.sub(r"<[^>]+>", "", p).strip()
    text_para = html.unescape(text_para)
    if len(text_para) > 15:
        print(text_para[:600])
        print("---")

# Also extract any blockquotes
quotes = re.findall(r"<blockquote[^>]*>(.*?)</blockquote>", article_html, re.DOTALL)
if quotes:
    print("\n=== Blockquotes ===\n")
    for q in quotes:
        text_q = re.sub(r"<[^>]+>", "", q).strip()
        text_q = html.unescape(text_q)
        if text_q:
            print(text_q[:400])
            print("---")

# Extract all links
links = re.findall(r'href="(https?://[^"]+)"', article_html)
external_links = [l for l in links if "goodnewsnetwork" not in l and "w3.org" not in l and "wordpress" not in l and "schema.org" not in l]
print(f"\n=== External links ({len(external_links)}) ===")
for l in external_links[:15]:
    print(f"  -> {l}")
