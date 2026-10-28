#!/usr/bin/env python3
import subprocess, re
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
url = "https://www.goodnewsnetwork.org/one-teachers-idea-for-daily-positivity-practice-sweeps-through-his-elementary-school/"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True, text=True)
stdout = r.stdout
# Find all paragraphs in the body
paras = re.findall(r"<p[^>]*>(.*?)</p>", stdout, re.DOTALL)
print(f"Total paragraphs: {len(paras)}")
for p in paras:
    text = re.sub(r"<[^>]+>", "", p).strip()
    if len(text) > 20:
        print(text)
        print("---")
