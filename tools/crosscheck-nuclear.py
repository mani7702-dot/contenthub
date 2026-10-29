#!/usr/bin/env python3
"""Cross-check nuclear testing fallout facts with scientific sources."""
import subprocess, re, urllib.parse

UA = "Mozilla/5.0 (ContentHub reader; contact andugulamani722@gmail.com)"

def fetch(url):
    p = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url], capture_output=True)
    return p.stdout.decode("utf-8", errors="replace")

def strip_html(text):
    html = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'&[a-z#0-9]+;', ' ', html)
    html = re.sub(r'\s+', ' ', html).strip()
    return html

# Source 2: Wikipedia on Carbon-14 bomb pulse
url1 = "https://en.wikipedia.org/wiki/Carbon-14"
html1 = fetch(url1)
text1 = strip_html(html1)
# Find bomb pulse section
idx = text1.lower().find("bomb pulse")
if idx >= 0:
    print("=== Wikipedia Carbon-14 - Bomb Pulse section ===")
    print(text1[idx:idx+1500])
else:
    print("Bomb pulse section not found in Wikipedia Carbon-14")
    # Try nuclear testing page
    idx2 = text1.lower().find("atmospheric nuclear")
    if idx2 >= 0:
        print(text1[idx2:idx2+1500])

print("\n\n=== Wikipedia Nuclear Testing ===")
url2 = "https://en.wikipedia.org/wiki/Nuclear_weapons_tests_of_the_United_States"
html2 = fetch(url2)
text2 = strip_html(html2)
idx2 = text2.find("Test Ban")
if idx2 >= 0:
    print(text2[max(0,idx2-200):idx2+1000])

print("\n\n=== Wikipedia Radiocarbon Dating ===")
url3 = "https://en.wikipedia.org/wiki/Radiocarbon_dating"
html3 = fetch(url3)
text3 = strip_html(html3)
idx3 = text3.find("bomb")
if idx3 >= 0:
    print(text3[idx3:idx3+1500])
