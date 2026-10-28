#!/usr/bin/env python3
"""Extract ALL text content from the GNN article."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

url = "https://www.goodnewsnetwork.org/village-installs-knitted-traffic-cops-to-slow-speeding-drivers/"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True, text=True)
stdout = r.stdout

# Save to file for inspection
with open("/home/ubuntu/contenthub/tools/gnn-article.html", "w") as f:
    f.write(stdout)

# Extract everything between the article content markers
# Look for the main content area
content_start = stdout.find("entry-content")
if content_start < 0:
    content_start = stdout.find("td-post-content")

if content_start >= 0:
    # Find the opening div after this
    div_start = stdout.find(">", content_start)
    # Find the matching closing div - just take a chunk
    content_html = stdout[div_start:div_start+50000]
    
    # Extract all text content between tags
    # Remove script and style tags
    content_html = re.sub(r"<script[^>]*>.*?</script>", "", content_html, flags=re.DOTALL)
    content_html = re.sub(r"<style[^>]*>.*?</style>", "", content_html, flags=re.DOTALL)
    
    # Extract text from paragraphs
    paras = re.findall(r"<p[^>]*>(.*?)</p>", content_html, re.DOTALL)
    print(f"=== Paragraphs found: {len(paras)} ===")
    for p in paras:
        text = re.sub(r"<[^>]+>", "", p).strip()
        # Decode HTML entities
        text = text.replace("&amp;", "&").replace("&rsquo;", "'").replace("&lsquo;", "'")
        text = text.replace("&ldquo;", '"').replace("&rdquo;", '"').replace("&mdash;", "—").replace("&ndash;", "–")
        if len(text) > 10:
            print(text[:500])
            print("---")
else:
    print("Could not find content section")
    # Just dump all paragraphs
    paras = re.findall(r"<p[^>]*>(.*?)</p>", stdout, re.DOTALL)
    print(f"Total paragraphs in page: {len(paras)}")
    for p in paras:
        text = re.sub(r"<[^>]+>", "", p).strip()
        if len(text) > 30:
            print(f"  {text[:300]}")
