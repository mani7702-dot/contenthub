#!/usr/bin/env python3
"""Extract key facts from ScienceDaily EV battery article."""
import re

html = open("/tmp/ev_battery.html", "r", errors="replace").read()
html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r"<[^>]+>", " ", html)
text = re.sub(r"&[a-z]+;", " ", text)
text = re.sub(r"\s+", " ", text)

keywords = ["300 nanometer", "150 nanometer", "10 nanometer", "microscopic tube",
            "MXene", "secondary sputtering", "copper foil", "four times",
            "surface area", "dendrite", "protective layer", "lithium fluoride",
            "LiPF6", "KAIST", "Advanced Functional"]
for kw in keywords:
    idx = text.lower().find(kw.lower())
    if idx >= 0:
        print(f">>> {kw}")
        print(text[max(0, idx - 100):idx + 300])
        print()
