#!/usr/bin/env python3
"""Search for the baseball story on CBC and other sources."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try searching for this story
search_url = "https://www.google.com/search?q=Dartmouth+High+School+Spartans+baseball+never+won+game+vibes"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, search_url], capture_output=True, text=True)
print(f"Google search page length: {len(r.stdout)}")

# Extract result links and snippets
# Google search results
links = re.findall(r'href="(https?://[^"]+)"', r.stdout)
for l in links:
    if "goodnewsnetwork" not in l and "google" not in l and "gstatic" not in l:
        print(f"  Link: {l}")

# Also try CBC search
cbc_search = "https://www.cbc.ca/search/related?q=Dartmouth+High+Spartans+baseball"
r2 = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, cbc_search], capture_output=True, text=True)
print(f"\nCBC search page length: {len(r2.stdout)}")

# Extract text content
text = re.sub(r"<script[^>]*>.*?</script>", "", r2.stdout, flags=re.DOTALL)
text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
text = re.sub(r"<[^>]+>", "\n", text)
text = html.unescape(text)
lines = [l.strip() for l in text.split("\n") if l.strip() and len(l.strip()) > 30]
for line in lines[:20]:
    print(line[:200])
