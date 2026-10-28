#!/usr/bin/env python3
"""Extract anode-free battery info from Wikipedia."""
import re

html = open("/tmp/wiki_anode.html", "r", errors="replace").read()
html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r"<[^>]+>", " ", html)
text = re.sub(r"&[a-z]+;", " ", text)
text = re.sub(r"\s+", " ", text)

idx = text.lower().find("anode")
if idx >= 0:
    print(text[max(0, idx - 200):idx + 1000])
else:
    print("No mention of anode-free battery found on Wikipedia page")
