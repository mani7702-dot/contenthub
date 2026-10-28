#!/usr/bin/env python3
"""Extract ScienceDaily article details."""
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
urls = [
    "https://www.sciencedaily.com/releases/2026/10/261026225620.htm",
    "https://www.sciencedaily.com/releases/2026/10/261026225617.htm",
]
for url in urls:
    print(f"\n{'='*60}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
    text = p.stdout.decode("utf-8", errors="replace")
    print(f"Length: {len(text)} chars")
    # Try to extract the main article text from ScienceDaily
    import re
    # Find the article body section
    m = re.search(r'<div id="text"><div>(.*?)</div>\s*</div>', text, re.S)
    if m:
        body = m.group(1)
        # strip HTML tags
        body = re.sub(r'<[^>]+>', '\n', body)
        body = re.sub(r'\s+', ' ', body).strip()
        print(body[:4000])
    else:
        # Try finding paragraphs
        m = re.findall(r'<p>(.*?)</p>', text, re.S)
        for para in m[:30]:
            clean = re.sub(r'<[^>]+>', '', para)
            clean = re.sub(r'\s+', ' ', clean).strip()
            if len(clean) > 30:
                print(clean)
