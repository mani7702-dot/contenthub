#!/usr/bin/env python3
"""Extract all readable text from GNN baseball article."""
import subprocess, re, html

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

link = "https://www.goodnewsnetwork.org/high-school-baseball-team-has-all-the-vibes-of-success-but-never-won-a-game-kids-dont-mind/"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, link], capture_output=True)
article_html = r.stdout.decode("utf-8", errors="replace")

# Look for JSON-LD data
json_ld = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', article_html, re.DOTALL)
if json_ld:
    print("=== JSON-LD data ===")
    for j in json_ld:
        try:
            data = j.strip()
            print(data[:1000])
            print("---")
        except:
            pass

# Look for articleBody in JSON
all_json = re.findall(r'"articleBody"\s*:\s*"([^"]+)"', article_html)
if all_json:
    print("\n=== Article body from JSON ===")
    for body in all_json:
        decoded = html.unescape(body)
        print(decoded[:2000])
        print("---")

# Look for content in div with class 'td-post-content' or similar
# Try a broader regex
content_divs = re.findall(r'class="td-post-content[^"]*"[^>]*>(.*?)</div>', article_html, re.DOTALL)
for i, div in enumerate(content_divs):
    print(f"\n=== Content div {i} (len={len(div)}) ===")
    # Extract all text and paragraphs
    text = re.sub(r"<script[^>]*>.*?</script>", "", div, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    # Extract paragraphs
    paras = re.findall(r"<p[^>]*>(.*?)</p>", text, re.DOTALL)
    for p in paras:
        t = re.sub(r"<[^>]+>", "", p).strip()
        t = html.unescape(t)
        if t:
            print(t[:500])
            print("---")
    # Also extract raw text
    raw = re.sub(r"<[^>]+>", "\n", text)
    raw = html.unescape(raw)
    lines = [l.strip() for l in raw.split("\n") if l.strip()]
    for l in lines:
        if len(l) > 20:
            print(f"[raw] {l[:300]}")

# Look for any content between <p> tags throughout the whole article
print("\n=== ALL paragraphs in entire page ===")
all_paras = re.findall(r"<p[^>]*>(.*?)</p>", article_html, re.DOTALL)
for p in all_paras:
    t = re.sub(r"<[^>]+>", "", p).strip()
    t = html.unescape(t)
    if len(t) > 50:  # Only meaningful paragraphs
        print(t[:500])
        print("---")
