#!/usr/bin/env python3
"""Extract more article content and search for second source."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://www.goodnewsnetwork.org/anonymously-pays-dinner-tab-for-27-disability-staff-in-south-korea/"
r = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, url], capture_output=True)
text = r.stdout.decode("utf-8", errors="replace")

# Try different patterns for article content
patterns = [
    r'class="td-post-content">(.*?)<div class="',
    r'<article[^>]*>(.*?)</article>',
    r'class="entry-content[^"]*"[^>]*>(.*?)(?:</div>\s*<div|<footer)',
]

for pat in patterns:
    m = re.search(pat, text, re.DOTALL)
    if m:
        clean = re.sub(r'<[^>]+>', '\n', m.group(1))
        clean = re.sub(r'\n\s*\n', '\n', clean)
        clean_lines = [l.strip() for l in clean.split('\n') if l.strip() and len(l.strip()) > 30]
        print(f"=== Pattern: {pat[:40]}... ===")
        for line in clean_lines[:30]:
            print(f"  {line[:300]}")
        print("---")

# Also search for Korean news sources
print("\n=== Searching for Korean sources ===")
search_url = "https://www.google.com/search?q=%22Incheon%22+%22420%22+%22disabled%22+%22lunch%22+2026"
r2 = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, search_url], capture_output=True, text=True)
# Check if we get results
if "Incheon" in r2.text or "420" in r2.text:
    clean = re.sub(r'<[^>]+>', ' ', r2.text)
    clean = re.sub(r'\s+', ' ', clean)
    idx = clean.find("Incheon")
    if idx > 0:
        print(clean[max(0,idx-200):idx+500])
else:
    print("Google search blocked or no results")
