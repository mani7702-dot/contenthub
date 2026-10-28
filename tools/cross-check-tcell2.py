#!/usr/bin/env python3
"""Search for the Nature Immunology paper and the McGill press release."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# The ScienceDaily article mentions McGill and Nature Immunology
# Let's search for the actual Nature paper
# Try the Nature search for the paper based on key authors/keywords
urls = [
    "https://www.nature.com/ni/volumes/57",
    "https://www.nature.com/ni/articles",
    "https://www.mcgill.ca/news/stories",
]

for url in urls:
    print(f"\n{'='*60}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    p = subprocess.run(["curl", "-s", "-L", "--max-time", "25", "-A", UA, url], capture_output=True)
    text = p.stdout.decode("utf-8", errors="replace")
    print(f"Length: {len(text)} chars")
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    print(clean[:1500])

# Also try a direct search for the paper title on nature.com
print("\n\n=== Searching Nature Immunology ===")
search_url = "https://www.nature.com/search?query=t+cell+stiffness+tissue+resident+memory+mandl&journal=nature-immunology"
p2 = subprocess.run(["curl", "-s", "-L", "--max-time", "25", "-A", UA, search_url], capture_output=True)
text2 = p2.stdout.decode("utf-8", errors="replace")
clean2 = re.sub(r'<[^>]+>', '\n', text2)
clean2 = re.sub(r'\n\s*\n', '\n', clean2)
clean2 = re.sub(r'\s+', ' ', clean2).strip()
print(f"Search result length: {len(text2)} chars")
# Find titles and links
for m in re.finditer(r'(https://www\.nature\.com/articles/s41590[^\s"<>\)]+)', text2):
    print(f"  Found: {m.group(1)}")
for m in re.finditer(r'(<a[^>]*href="(/articles/[^"]+)"[^>]*>(.*?)</a>)', text2, re.S):
    href = m.group(1)
    title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
    if 't cell' in title.lower() or 'stiff' in title.lower() or 'immune' in title.lower() or 'tissue' in title.lower():
        print(f"  {href} - {title[:120]}")
