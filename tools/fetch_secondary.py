#!/usr/bin/env python3
"""Extract article text from Google News redirect URLs and secondary sources."""
import subprocess, re, sys

urls = [
    "https://www.scientificreports.com/articles/s41598-026-00000-0",
    "https://news.google.com/rss/articles/CBMieEFVX3lxTFB1Q0NPVGdLa1hLR3FTUk9kVmY0WWNtMEcyYVVrRFpvU3Z2bGtEMzhuZVdtNTZ5VkhGLXVoQ3Z0c1NBZDdnbm9ONTBRNk5JMzNHcERLck9lU1ZENUFtLVoyOVg4UHVEejFhZDZtQ0pTQy1rVVllcGhLYw?oc=5",
]

ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

for url in urls:
    print(f"\n{'='*60}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", ua, url], capture_output=True)
    html = p.stdout.decode("utf-8", errors="replace")
    print(f"Chars: {len(html)}")
    title = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    if title:
        print(f"Title: {title.group(1).strip()}")
    # Extract paragraphs
    html_clean = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html_clean = re.sub(r"<style[^>]*>.*?</style>", "", html_clean, flags=re.DOTALL | re.IGNORECASE)
    paras = re.findall(r"<p[^>]*>(.*?)</p>", html_clean, re.DOTALL | re.IGNORECASE)
    for para in paras[:15]:
        clean = re.sub(r"<[^>]+>", "", para).strip()
        if len(clean) > 40:
            print(f"  PARA: {clean[:300]}")
