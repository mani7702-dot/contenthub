#!/usr/bin/env python3
"""Fetch secondary sources for cross-checking the Einstein/dark-energy story."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# UC Davis press release
urls = [
    ("UC Davis Press Release", "https://www.news.ucdavis.edu/einstein-equations-may-explain-universe-without-dark-energy"),
    ("SciTechDaily", "https://scitechdaily.com/einsteins-equations-may-explain-the-universe-without-dark-energy/"),
]

for name, url in urls:
    print(f"=== {name}: {url} ===")
    p = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url],
                       capture_output=True)
    html = p.stdout.decode("utf-8", errors="replace")
    if len(html) < 200:
        print("EMPTY RESPONSE")
        print()
        continue
    
    # Extract paragraphs
    paras = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL)
    count = 0
    for para in paras:
        text = re.sub(r"<[^>]+>", "", para).strip()
        text = re.sub(r"&amp;", "&", text)
        text = re.sub(r"&lt;", "<", text)
        text = re.sub(r"&gt;", ">", text)
        text = re.sub(r"&nbsp;", " ", text)
        text = re.sub(r"&#39;", "'", text)
        text = re.sub(r"&quot;", '"', text)
        if len(text) > 60:
            print(text[:300])
            print()
            count += 1
            if count >= 5:
                break
    print(f"=== Total paras: {len(paras)} ===")
    print()
