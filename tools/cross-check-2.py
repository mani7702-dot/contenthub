#!/usr/bin/env python3
"""Try to cross-check the knitted traffic cops story via multiple methods."""
import subprocess, re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Try fetching from local news sources directly
urls_to_try = [
    # BBC local news for the West Midlands
    "https://www.bbc.co.uk/news/england/west_midlands",
    # ITV Central (covers Warwickshire)
    "https://www.itv.com/news/central",
    # Try a web search that might embed snippets
    "https://www.bing.com/search?q=%22Fillongley%22+%22knitted%22+traffic+cops",
]

for url in urls_to_try:
    r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, url], capture_output=True, text=True)
    stdout = r.stdout
    
    # Extract text
    text = re.sub(r"<script[^>]*>.*?</script>", "", stdout, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    
    # Search for knitted/Fillongley mentions
    has_knitted = "knitted" in text.lower()
    has_fillongley = "fillongley" in text.lower()
    
    print(f"URL: {url}")
    print(f"  Length: {len(stdout)} bytes")
    print(f"  Has 'knitted': {has_knitted}")
    print(f"  Has 'fillongley': {has_fillongley}")
    
    if has_knitted or has_fillongley:
        # Find context
        for term in ["knitted", "fillongley"]:
            idx = 0
            while True:
                idx = text.lower().find(term, idx)
                if idx < 0:
                    break
                print(f"  Context ({term}): ...{text[max(0,idx-100):idx+200]}...")
                idx += 1
    print()
