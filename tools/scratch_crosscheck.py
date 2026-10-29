#!/usr/bin/env python3
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

URLS = [
    "https://www.sciencedaily.com/releases/2026/10/261027063704.htm",
    "https://www.scmp.com/tech/science/article/3279664/why-do-our-muscles-weaken-as-we-age-scientists-find-hidden-defence-mechanism",
    "https://en.wikipedia.org/wiki/Sarcopenia",
]

for url in URLS:
    print(f"\n=== {url} ===")
    try:
        p = subprocess.run(
            ["curl", "-s", "--max-time", "30", "-A", UA, url],
            capture_output=True
        )
        html = p.stdout
        text = html.decode("utf-8", errors="replace")
        # strip tags for readability
        paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", text, re.DOTALL)
        if paragraphs:
            for ptext in paragraphs[:30]:
                clean = re.sub(r"<[^>]+>", "", ptext).strip()
                if len(clean) > 30:
                    print(clean[:300])
        else:
            # maybe it's a plain text page
            clean = re.sub(r"<[^>]+>", " ", text).strip()
            print(clean[:2000])
    except Exception as e:
        print(f"ERROR: {e}")
