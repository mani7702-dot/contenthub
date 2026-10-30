#!/usr/bin/env python3
"""Fetch article text via curl + regex. Tirith-safe."""
import subprocess, re, sys

def fetch(url):
    result = subprocess.run(
        ['curl', '-s', '--max-time', '15',
         '-A', 'Mozilla/5.0 (ContentHub; contact andugulamani722@gmail.com)',
         url],
        capture_output=True, text=True, timeout=20
    )
    return result.stdout

def extract_paragraphs(html):
    paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
    out = []
    for p in paras:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if clean and len(clean) > 50:
            out.append(clean)
    return out

if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else input().strip()
    html = fetch(url)
    for p in extract_paragraphs(html):
        print(p)
        print('---')
