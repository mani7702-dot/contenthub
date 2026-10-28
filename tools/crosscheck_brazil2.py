#!/usr/bin/env python3
"""Fetch the Brazilian Senate PEC 221 page and verify the vote count."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = "https://www25.senado.leg.br/web/atividade/materias/-/materia/174386"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True, text=True)
html = r.stdout
print(f"=== Status: fetched {len(html)} bytes ===")

# Look for key facts
for pattern in [r"75.*1", r"PEC[.\s]*221", r"seis dias", r"6.*dia", r"trabalho", r"senado.*vota", r"aprovou"]:
    matches = re.findall(pattern, html, re.IGNORECASE)
    if matches:
        print(f"Pattern '{pattern}': {matches[:5]}")

# Extract text content
text = re.sub(r"<[^>]+>", " ", html)
text = re.sub(r"\s+", " ", text).strip()
# Search for PEC 221 mentions
idx = text.lower().find("pec")
if idx >= 0:
    print(f"\n=== Context around 'PEC' ===")
    print(text[max(0,idx-200):idx+500])
idx2 = text.lower().find("75 a 1")
if idx2 >= 0:
    print(f"\n=== Context around '75 a 1' ===")
    print(text[max(0,idx2-200):idx2+500])
