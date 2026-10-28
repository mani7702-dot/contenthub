#!/usr/bin/env python3
import subprocess, re
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
url = "https://www.goodnewsnetwork.org/one-teachers-idea-for-daily-positivity-practice-sweeps-through-his-elementary-school/"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True, text=True)
stdout = r.stdout
meta_desc = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', stdout)
if meta_desc:
    print(f"=== Meta description ===")
    print(meta_desc.group(1))
title_match = re.search(r"<title>(.*?)</title>", stdout)
if title_match:
    print(f"\n=== Title ===")
    print(title_match.group(1))
content_match = re.search(r'class="[^"]*td-post-content[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', stdout, re.DOTALL)
if not content_match:
    content_match = re.search(r'class="[^"]*entry-content[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', stdout, re.DOTALL)
if content_match:
    html = content_match.group(1)
    paras = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL)
    print(f"\n=== Article paragraphs ({len(paras)}) ===")
    for p in paras:
        text = re.sub(r"<[^>]+>", "", p).strip()
        if len(text) > 10:
            print(text)
            print("---")
else:
    print("Could not find article content div")
    paras = re.findall(r"<p[^>]*>(.*?)</p>", stdout, re.DOTALL)
    print(f"Total paragraphs: {len(paras)}")
    for p in paras:
        text = re.sub(r"<[^>]+>", "", p).strip()
        if len(text) > 30:
            print(f"  {text[:200]}")
