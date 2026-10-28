#!/usr/bin/env python3
import re
with open('/home/ubuntu/contenthub/wiki_haysville.html', 'r', errors='replace') as f:
    html = f.read()
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()
# Find the relevant part about schools/education
idx = text.find('Haysville')
print(text[idx:idx+2000])
