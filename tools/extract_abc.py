#!/usr/bin/env python3
"""Extract article from ABC News for cross-checking the kangaroo rescue."""
import re, subprocess

url = "https://www.abc.net.au/news/2026-10-21/kangaroo-rescued-from-sea-boston-bay-port-lincoln/107291116"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
p = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="ignore")

with open('/tmp/abc_kangaroo.html', 'w') as f:
    f.write(html)

# Try to find article content
article = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
if article:
    content = article.group(1)
else:
    # Find paragraphs
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
    body_paras = []
    for p_content in paragraphs:
        text = re.sub(r'<[^>]+>', '', p_content)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 30:
            body_paras.append(text)
    content = '\n'.join(body_paras[:20])

text = re.sub(r'<[^>]+>', ' ', content)
text = re.sub(r'&amp;', '&', text)
text = re.sub(r'&nbsp;', ' ', text)
text = re.sub(r'&#8217;|&amp;#x27;', "'", text)
text = re.sub(r'&quot;|&#8220;|&#8221;', '"', text)
text = re.sub(r'\s+', ' ', text)
print(text[:8000])
