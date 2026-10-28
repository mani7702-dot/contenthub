#!/usr/bin/env python3
"""Search for coconut oil jet fuel research on university websites."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try Osaka Metropolitan University's research news
urls = [
    "https://www.omu.ac.jp/en/news/2026/",
    "https://www.omu.ac.jp/en/research/",
    "https://www.google.com/search?q=site:omu.ac.jp+coconut+aviation+fuel",
    "https://www.google.com/search?q=site:osaka-u.ac.jp+coconut+aviation+fuel",
]

for url in urls:
    print(f"\n=== {url} ===")
    p = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url], capture_output=True, text=True)
    print(f"Page length: {len(p.stdout)}")
    text = re.sub(r'<script[^>]*>.*?</script>', '', p.stdout, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    if 'coconut' in text.lower() or 'aviation' in text.lower():
        idx = text.lower().find('coconut')
        if idx < 0:
            idx = text.lower().find('aviation')
        print(text[max(0,idx-300):idx+500])
    else:
        print("No coconut/aviation mention found")
