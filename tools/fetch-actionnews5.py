#!/usr/bin/env python3
"""Fetch and display Action News 5 article."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub reader; contact andugulamani722@gmail.com)"

def fetch(url):
    p = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url], capture_output=True)
    return p.stdout

def strip_html(data):
    html = data.decode("utf-8", errors="replace")
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'&[a-z#0-9]+;', ' ', html)
    html = re.sub(r'\s+', ' ', html).strip()
    return html

url = "https://www.actionnews5.com/article/news/local/lightning-strike-proposal-wisconsin-kettle-moraine/539-video/"
data = fetch(url)
text = strip_html(data)
print(text[:5000])
