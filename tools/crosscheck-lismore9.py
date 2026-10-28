#!/usr/bin/env python3
"""Cross-check: extract actual text from Antiquity project gallery."""
import subprocess, re, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://www.antiquity.ac.uk/projgall/ellis2401/"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", url], capture_output=True)
text = r.stdout.decode("utf-8", errors="replace")
# Strip HTML tags more broadly and look for content
# Remove script/style
text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
# Extract all text
words = re.sub(r'<[^>]+>', ' ', text)
words = re.sub(r'\s+', ' ', words).strip()
# Look for key mentions
for term in ["Lismore", "Moluag", "monastery", "precious", "metal", "crucible", "cross", "slab", "burial", "650", "1040"]:
    if term.lower() in words.lower():
        # Find context
        idx = words.lower().find(term.lower())
        start = max(0, idx - 50)
        end = min(len(words), idx + term.__len__() + 200)
        print(f"[{term}]: ...{words[start:end]}...")
        print()
