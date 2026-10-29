#!/usr/bin/env python3
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

URLS = [
    "https://www.sciencedaily.com/releases/2026/10/261027063704.htm",
    "https://www.medicalnewstoday.com/articles/why-do-muscles-weaken-with-age",
    "https://www.healthline.com/health/sarcopenia",
]

for url in URLS:
    print(f"\n=== {url} ===")
    try:
        p = subprocess.run(
            ["curl", "-sL", "--max-time", "30", "-A", UA, url],
            capture_output=True
        )
        html = p.stdout.decode("utf-8", errors="replace")
        paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL)
        if paragraphs:
            for ptext in paragraphs[:20]:
                clean = re.sub(r"<[^>]+>", "", ptext).strip()
                if len(clean) > 30:
                    print(clean[:300])
        else:
            clean = re.sub(r"<[^>]+>", " ", html).strip()
            print(clean[:1500])
    except Exception as e:
        print(f"ERROR: {e}")
