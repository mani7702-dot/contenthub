#!/usr/bin/env python3
"""Fetch the corroborating articles found via Google News RSS search."""
import subprocess, re, base64

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# These are the Google News article URLs decoded - let's try fetching the original sources
# Based on RSS results: Sci.News, SciTechDaily, Earth.com, UniverseToday, OpenAccessGov
urls = [
    ("Sci.News - Dark Energy", "https://scinews.com/dark-energy-mathematicians-challenge-standard-cosmological-model-universe.html"),
    ("Sci.News - Search", "https://scinews.com/?s=dark+energy"),
    ("Earth.com", "https://www.earth.com/"),
    ("Universe Today", "https://www.universetoday.com/82935/dark-energy/"),
]

for name, url in urls:
    print(f"=== {name}: {url} ===")
    p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, url],
                       capture_output=True)
    html = p.stdout.decode("utf-8", errors="replace")
    print(f"Length: {len(html)} bytes")
    if len(html) > 500:
        paras = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL)
        count = 0
        for para in paras:
            text = re.sub(r"<[^>]+>", "", para).strip()
            text = re.sub(r"&amp;", "&", text)
            text = re.sub(r"&lt;", "<", text)
            text = re.sub(r"&gt;", ">", text)
            text = re.sub(r"&#39;", "'", text)
            text = re.sub(r"&quot;", '"', text)
            text = re.sub(r"&nbsp;", " ", text)
            if len(text) > 60:
                print(text[:300])
                print()
                count += 1
                if count >= 3:
                    break
    print()
