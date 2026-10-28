#!/usr/bin/env python3
"""Cross-check Lismore discovery via Antiquity journal and University of Aberdeen."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try the University of Aberdeen news site
urls = [
    "https://www.abdn.ac.uk/news/",
    "https://www.cambridge.org/core/journals/antiquity",
    "https://www.antiquity.ac.uk/",
]

for url in urls:
    print(f"\n=== {url} ===")
    p = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url], capture_output=True, text=True)
    content = p.stdout
    print(f"Page length: {len(content)}")
    text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    if 'lismore' in text.lower():
        idx = text.lower().find('lismore')
        print(text[max(0,idx-300):idx+500])
    elif 'scotland' in text.lower() and 'monastery' in text.lower():
        idx = text.lower().find('scotland')
        print("Found Scotland mention:")
        print(text[max(0,idx-200):idx+500])
    elif 'scotland' in text.lower():
        idx = text.lower().find('scotland')
        print("Found Scotland mention:")
        print(text[max(0,idx-100):idx+300])
    else:
        # Check first 500 chars
        print(text[:500])
