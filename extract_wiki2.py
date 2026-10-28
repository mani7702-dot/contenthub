#!/usr/bin/env python3
import re
with open('/home/ubuntu/contenthub/wiki_haysville.html', 'r', errors='replace') as f:
    html = f.read()
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()
# Find Education section
idx = text.find('Education')
print(text[idx:idx+1500])
