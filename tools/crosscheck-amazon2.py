#!/usr/bin/env python3
"""Get full Amazon conservation article text."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

url = "https://www.goodnewsnetwork.org/ngo-celebrates-70-million-amazon-acres-conserved-after-protecting-are-called-a-link-of-life/"
p = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
html2 = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
html2 = re.sub(r"<style[^>]*>.*?</style>", "", html2, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r"<[^>]+>", " ", html2)
text = re.sub(r"\s+", " ", text)

idx = text.find("Sunrise on the Itenez")
if idx > 0:
    print(text[idx:idx+5000])
else:
    idx = text.find("Rainforest Trust")
    if idx > 0:
        print(text[idx:idx+5000])
    else:
        print(text[2000:7000])
