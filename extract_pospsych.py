#!/usr/bin/env python3
import re
with open('/home/ubuntu/contenthub/wiki_pospsych.html', 'r', errors='replace') as f:
    html = f.read()
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()
# Find section about applications/education
idx = text.find('Education')
if idx == -1:
    idx = text.find('school')
print(text[idx:idx+1500])
