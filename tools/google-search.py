#!/usr/bin/env python3
"""Extract relevant text from Google search results."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

search_url = "https://www.google.com/search?q=Dartmouth+High+School+Spartans+baseball+never+won+vibes+success+Canada"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, "-L", search_url], capture_output=True, text=True)
print(f"Page length: {len(r.stdout)}")

# Extract search result snippets
text = re.sub(r"<script[^>]*>.*?</script>", "", r.stdout, flags=re.DOTALL)
text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
text = re.sub(r"<[^>]+>", "\n", text)
text = html.unescape(text)
lines = [l.strip() for l in text.split("\n") if l.strip() and len(l.strip()) > 30]
for line in lines[:30]:
    print(line[:250])
