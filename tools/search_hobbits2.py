#!/usr/bin/env python3
"""Search for the CBC As it Happened article on the wedding ring story."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try CBC search
urls = [
    "https://www.cbc.ca/search/related-news?searchText=patrick+mohr+italian+hobbits+wedding+ring",
    "https://www.bing.com/search?q=patrick+mohr+italian+hobbits+wedding+ring+cbc+as+it+happened",
]

for url in urls:
    print(f"=== {url[:80]} ===")
    r = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
    html = r.stdout
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    
    # Look for relevant snippets
    for keyword in ["Mohr", "hobbit", "wedding ring", "Glendalough", "Poggi", "Malloggi"]:
        idx = text.lower().find(keyword.lower())
        if idx > 0:
            print(f"  [{keyword}] ...{text[max(0,idx-80):idx+200]}...")
            print()
    
    # Also look for links to cbc.ca articles
    links = re.findall(r'href="(https?://[^"]*cbc\.ca[^"]*)"', html)
    unique_links = list(dict.fromkeys(links))[:10]
    if unique_links:
        print(f"  CBC links found:")
        for l in unique_links:
            print(f"    -> {l}")
    print()
