#!/usr/bin/env python3
"""Extract more content from the GNN baseball article."""
import subprocess, re, html

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

link = "https://www.goodnewsnetwork.org/high-school-baseball-team-has-all-the-vibes-of-success-but-never-won-a-game-kids-dont-mind/"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, link], capture_output=True)
article_html = r.stdout.decode("utf-8", errors="replace")

# Search for text content around "baseball" or "Dartmouth" or "Spartans"
# Look for all text content between tags
all_text = re.sub(r"<script[^>]*>.*?</script>", "", article_html, flags=re.DOTALL)
all_text = re.sub(r"<style[^>]*>.*?</style>", "", all_text, flags=re.DOTALL)
all_text = re.sub(r"<[^>]+>", "\n", all_text)
all_text = html.unescape(all_text)

# Find the main content portion
lines = [l.strip() for l in all_text.split("\n") if l.strip()]
# Print lines around "Dartmouth" or "Spartans" or "baseball"
start = None
for i, line in enumerate(lines):
    if "Dartmouth" in line or "Spartans" in line or "baseball" in line.lower() or "vibes" in line.lower():
        start = i
        break

if start:
    print(f"Found content around line {start}")
    for i in range(start, min(start+80, len(lines))):
        if len(lines[i]) > 10:
            print(lines[i][:200])
            print("---")
else:
    print("No relevant content found")
    # Print first 50 non-empty lines
    count = 0
    for line in lines:
        if len(line) > 20:
            print(line[:200])
            count += 1
            if count >= 30:
                break
