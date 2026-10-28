#!/usr/bin/env python3
"""Extract anode-free battery info from Wikipedia."""
import re

html = open("/tmp/wiki_anode.html", "r", errors="replace").read()
html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r"<[^>]+>", " ", html)
text = re.sub(r"&[a-z]+;", " ", text)
text = re.sub(r"\s+", " ", text)

# Find the main content paragraph about anode-free battery
# Skip the navigation boilerplate
idx = text.find("Type of energy-storing battery")
if idx >= 0:
    print(text[idx:idx+2000])
else:
    print(text[2000:4000])
