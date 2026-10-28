#!/usr/bin/env python3
"""Cross-check the lunch tab story against multiple sources."""
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try fetching the GNN article content
urls = [
    "https://www.goodnewsnetwork.org/stranger-anonymously-pays-420-lunch-tab-for-27-disabled-residents-and-caregivers/",
]

for url in urls:
    print(f"\n=== Fetching: {url} ===")
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
    data = r.stdout
    # Try to find relevant text
    text = data.decode("utf-8", errors="replace")
    # Look for the article content
    if "lunch" in text.lower() or "420" in text:
        # Extract readable text
        import re
        # Remove HTML tags
        clean = re.sub(r"<[^>]+>", " ", text)
        clean = re.sub(r"\s+", " ", clean)
        # Find relevant section
        idx = clean.lower().find("lunch tab")
        if idx > 0:
            print(clean[max(0,idx-500):idx+1000])
        else:
            idx = clean.lower().find("420")
            if idx > 0:
                print(clean[max(0,idx-500):idx+1500])
            else:
                print("Could not find relevant content, raw length:", len(clean))
                print(clean[:2000])
    else:
        print("Could not find relevant content in page")
