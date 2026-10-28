#!/usr/bin/env python3
"""Search Nature.com for the T-cell stiffness paper."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Search Nature.com for T cell stiffness paper
search_url = "https://www.nature.com/search?query=T+cell+stiffness+tissue+mechanical+Mandl&journal=nature-immunology"
p = subprocess.run(["curl", "-s", "-L", "--max-time", "25", "-A", UA, search_url], capture_output=True)
text = p.stdout.decode("utf-8", errors="replace")

# Extract all article links from nature.com
article_links = re.findall(r'href="(/articles/s41590[^"]+)"', text)
print("Found s41590 article links:")
for link in set(article_links):
    print(f"  https://www.nature.com{link}")

if not article_links:
    # Try broader search - get all article links with titles
    all_links = re.findall(r'href="(/articles/[^"]+)"', text)
    print(f"Found {len(set(all_links))} unique article links:")
    for link in list(set(all_links))[:10]:
        print(f"  https://www.nature.com{link}")
    
    # Also try extracting titles
    for m in re.finditer(r'<a[^>]*href="/articles/[^"]*"[^>]*>(.*?)</a>', text, re.S):
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        title = re.sub(r'\s+', ' ', title)
        if len(title) > 10 and ('t cell' in title.lower() or 'stiff' in title.lower() or 'immune' in title.lower() or 'tissue' in title.lower()):
            print(f"  -> {title[:120]}")
