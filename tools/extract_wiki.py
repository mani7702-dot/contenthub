#!/usr/bin/env python3
"""Extract readable text from a Wikipedia HTML file in /tmp."""
import re, sys

with open(sys.argv[1]) as f:
    html = f.read()

# Extract paragraph text
paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
for para in paras:
    text = re.sub(r'<[^>]+>', '', para).strip()
    text = text.replace('&amp;', '&').replace('&#8211;', '–').replace('&#8217;', "'")
    text = re.sub(r'&#\d+;', '', text)
    if len(text) > 30:
        print(text)
        print()
