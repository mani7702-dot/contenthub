#!/usr/bin/env python3
"""Cross-check 2nd source: Search for silver diamine fluoride + JAMA Pediatrics + FDA."""
import subprocess, re, json

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Check Wikipedia for silver diamine fluoride info
urls = [
    "https://en.wikipedia.org/wiki/Silver_diamine_fluoride",
    "https://www.sciencedaily.com/news/health_medicine/dentistry/",
]

for url in urls:
    try:
        p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
        html = p.stdout.decode("utf-8", errors="replace")
        html2 = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        html2 = re.sub(r"<style[^>]*>.*?</style>", "", html2, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", html2)
        text = re.sub(r"\s+", " ", text)
        
        if "silver diamine" in text.lower() or "SDF" in text:
            # Find relevant section
            idx = text.lower().find("silver diamine")
            if idx > 0:
                print(f"=== {url} ===")
                print(text[max(0,idx-300):idx+3000])
                print()
        else:
            print(f"=== {url} === (no relevant content found)")
    except Exception as e:
        print(f"=== {url} === ERROR: {e}")
