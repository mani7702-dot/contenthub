#!/usr/bin/env python3
"""Fetch article content from a URL, strip HTML, return text."""
import subprocess, re, sys

UA = "Mozilla/5.0 (ContentHub reader; contact andugulamani722@gmail.com)"

def fetch(url):
    p = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True)
    return p.stdout

def strip_html(data):
    html = data.decode("utf-8", errors="replace")
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'&[a-z]+;', ' ', html)
    html = re.sub(r'\s+', ' ', html).strip()
    return html

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else ""
    if not url:
        print("Usage: fetch-article.py <url>")
        sys.exit(1)
    data = fetch(url)
    text = strip_html(data)
    print(text[:5000])
