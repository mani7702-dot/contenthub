#!/usr/bin/env python3
"""Extract image URL from JSON-LD in the GNN article."""
import subprocess, re, html

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

link = "https://www.goodnewsnetwork.org/high-school-baseball-team-has-all-the-vibes-of-success-but-never-won-a-game-kids-dont-mind/"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, link], capture_output=True)
article_html = r.stdout.decode("utf-8", errors="replace")

# Extract full JSON-LD
json_ld = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', article_html, re.DOTALL)
for i, j in enumerate(json_ld):
    print(f"=== JSON-LD {i} ===")
    print(j[:3000])
    print("---")

# Try to find image URLs
img_urls = re.findall(r'"image"[^}]*"(https?://[^"]+)"', article_html)
print(f"\n=== Image URLs ===")
for u in img_urls[:5]:
    print(u)

# Also search for featured image
featured = re.findall(r'class="[^"]*featured[^"]*"[^>]*>.*?src="([^"]+)"', article_html, re.DOTALL)
print(f"\n=== Featured images ===")
for f in featured[:5]:
    print(f)
