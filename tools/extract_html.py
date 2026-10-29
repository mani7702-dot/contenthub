#!/usr/bin/env python3
"""Extract article text from a ScienceDaily HTML page."""
import sys
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'nav', 'header', 'footer'):
            self.skip = True
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'nav', 'header', 'footer'):
            self.skip = False
        if tag in ('p', 'br', 'li', 'h1', 'h2', 'h3', 'div'):
            self.text.append('\n')
    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)

filepath = sys.argv[1] if len(sys.argv) > 1 else '/tmp/immune_touch.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

parser = TextExtractor()
parser.feed(html)
text = ''.join(parser.text)
# Clean up blank lines
lines = [l.strip() for l in text.split('\n') if l.strip()]
print('\n'.join(lines[:200]))
