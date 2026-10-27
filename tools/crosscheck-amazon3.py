#!/usr/bin/env python3
"""Cross-check Amazon conservation with Wikipedia + Rainforest Trust."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Wikipedia: Noel Kempff Mercado National Park
urls = [
    "https://en.wikipedia.org/wiki/Noel_Kempff_Mercado_National_Park",
    "https://en.wikipedia.org/wiki/Rainforest_Trust",
    "https://en.wikipedia.org/wiki/It%C3%A9nez_River",
]

for url in urls:
    try:
        p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
        html = p.stdout.decode("utf-8", errors="replace")
        html2 = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        html2 = re.sub(r"<style[^>]*>.*?</style>", "", html2, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", html2)
        text = re.sub(r"\s+", " ", text)
        
        print(f"=== {url} ===")
        # Print key sentences
        sentences = text.split(". ")
        for s in sentences[:50]:
            s_lower = s.lower()
            if any(k in s_lower for k in ["amazon", "bolivia", "iténez", "itenez", "rainforest trust", "70 million", "conservation", "jaguar", "giant otter", "mammoth", "protected area", "reserve"]):
                print(f"  {s.strip()[:300]}")
        print()
    except Exception as e:
        print(f"=== {url} === ERROR: {e}")
