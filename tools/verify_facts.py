#!/usr/bin/env python3
"""Extract key numerical facts from PMC article."""
import subprocess, re

ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

pmc_url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC13365576/"
p = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", ua, pmc_url], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")

# Strip to text
html_clean = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
html_clean = re.sub(r"<style[^>]*>.*?</style>", "", html_clean, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r"<[^>]+>", " ", html_clean)
text = re.sub(r"&amp;", "&", text)
text = re.sub(r"&lt;", "<", text)
text = re.sub(r"&gt;", ">", text)
text = re.sub(r"&nbsp;", " ", text)
text = re.sub(r"\s+", " ", text)

# Find key numbers
for term in ["R2 =", "R2=", "0.152", "15%", "123", "monocyte", "0.032", "2.5", "0.15", "0.408", "0.428"]:
    idx = text.find(term)
    if idx != -1:
        context = text[max(0, idx-50):idx+150].strip()
        print(f"[{term}] ...{context}...")

# Also look for the specific statement about variance explained
for pattern in [r"0\.152", r"15\.2%", r"15 percent", r"fifteen percent", r"R2\s*=\s*0\.15", r"explains?.*?15"]:
    matches = re.findall(pattern, text)
    if matches:
        print(f"Pattern '{pattern}': {matches[:5]}")

# Print the key sentence about R2=0.152
for sent in re.split(r'[.!?]', text):
    if "0.152" in sent or "R2" in sent or "variance" in sent.lower():
        print(f"\nSENTENCE: {sent.strip()[:300]}")
