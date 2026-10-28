#!/usr/bin/env python3
"""Search Nature.com for the T-cell stiffness paper - more targeted."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# The paper should be in Nature Immunology. Let's check the Nature Immunology recent articles page
# and also try searching with the key terms from the press release
search_urls = [
    "https://www.nature.com/ni/articles?searchType=journalNode&query=t+cell+stiffness+tissue",
    "https://www.nature.com/ni/volumes/57/issues/11",
    "https://www.nature.com/ni/volumes/57/issues/10",
]

for search_url in search_urls:
    print(f"\n{'='*60}")
    print(f"URL: {search_url}")
    print(f"{'='*60}")
    p = subprocess.run(["curl", "-s", "-L", "--max-time", "25", "-A", UA, search_url], capture_output=True)
    text = p.stdout.decode("utf-8", errors="replace")
    
    # Extract article links and titles from Nature Immunology
    for m in re.finditer(r'href="(/articles/s41590-[^"]+)"[^>]*>(.*?)</a>', text, re.S):
        title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        title = re.sub(r'\s+', ' ', title)
        print(f"  -> https://www.nature.com{m.group(1)} | {title[:120]}")

    # Also check for any T cell or stiffness mentions
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'\s+', ' ', clean)
    for kw in ['stiffness', 'tissue stiffness', 'mechano', 'collagen gel']:
        idx = clean.lower().find(kw.lower())
        if idx > 0:
            print(f"--- Found \"{kw}\" at pos {idx} ---")
            print(clean[max(0, idx-100):idx+300])
            print()

# Let's also try a direct search for "tissue stiffness" on nature.com
search_url3 = "https://www.nature.com/search?query=%22tissue+stiffness%22+OR+%22tissue+stiff%22+T+cell+Nature+Immunology&journal=nature-immunology"
print(f"\n{'='*60}")
print(f"URL: {search_url3}")
print(f"{'='*60}")
p3 = subprocess.run(["curl", "-s", "-L", "--max-time", "25", "-A", UA, search_url3], capture_output=True)
text3 = p3.stdout.decode("utf-8", errors="replace")
clean3 = re.sub(r'<[^>]+>', '\n', text3)
clean3 = re.sub(r'\n\s*\n', '\n', clean3).strip()
# Find articles mentioning T cell and stiffness
lines = clean3.split('\n')
for i, line in enumerate(lines):
    if 't cell' in line.lower() or 'stiff' in line.lower():
        print(f"  Line {i}: {line.strip()[:200]}")
