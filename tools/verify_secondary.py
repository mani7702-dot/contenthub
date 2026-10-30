#!/usr/bin/env python3
"""Fetch SciTechDaily article as secondary source verification."""
import subprocess, re

ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# SciTechDaily article (from Google News RSS)
# The URL was a Google News redirect; let's try the actual SciTechDaily URL
urls = [
    "https://www.sciencedaily.com/releases/2026/10/261026225620.htm",  # We already have this
]

# Try to find the SciTechDaily article directly
for url in [
    "https://scitechdaily.com/gut-microbiome-aging-study/",
    "https://www.sciencetimes.com/gut-microbiome-aging-study",
]:
    p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, url], capture_output=True)
    html = p.stdout.decode("utf-8", errors="replace")
    title = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
    if title and len(html) > 2000:
        print(f"FOUND: {url}")
        print(f"  Title: {title.group(1).strip()[:200]}")
    else:
        print(f"Not found: {url} (chars: {len(html)})")

# Use Google News RSS to find SciTechDaily article
# Let's try fetching with a different Google News URL format
print("\n=== Trying Google News article directly ===")
# The Google News RSS article URL from earlier:
gn_url = "https://news.google.com/rss/articles/CBMiigFBVV95cUxNNDVYb2tVdHdlcnByWElkNmIxOThNVmNIbGRfWUhGcXBpVXBxZU9FYU5CblhycmJ2aXlhbVEtNkVvYXJvUXNVUEFTVUxMa29Ua1BTNVgtT2Nka2NONFFmVzF0NXd1M2ZIaHlqblRQNUctYU85MjNzZjRoTGxpVGJ2OXB4SDJqeHlSSUHSAY8BQVVfeXFMUDE7QTVFYUZrcWRrXzF9lVHhfVGltWi1zYUVEU2pBdFgySWR0U2xLVmxJMUxmZlpySDJmbHcxU3RXNnBRTlNwQWtwVXlkQlhDLXdabXN1cVcxd0hKWk0xak5WMy03ZVNyeXhPOTd3NjEzWHloeGbiZUhJeTdRSVNmdW5xN1B0bEJKbXBXOTlBZUE"
# Actually, the URL had a unicode character issue; let me use the one from the search results
gn_url2 = "https://news.google.com/rss/articles/CBMiigFBVV95cUxNNDVYb2tVdHdlcnByWElkNmIxOThNVmNIbGRfWUhGcXBpVXBxZU9FYU5CblhycmJ2aXlhbVEtNkVvYXJvUXNVUEJSVUxMa29Ua1BTNVgtT2Nka2NONFFmVzF0NXd1M2ZIaHlqblRQNUctYU85MjNzZjRoTGxpVGJ2OXB4SDJqeHlSSUFnfmdB&hl=en-US&gl=US&ceid=US:en"

p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, gn_url2], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
print(f"Google News article chars: {len(html)}")
# Look for any content
if len(html) > 1000:
    # Try extracting content
    html_clean = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html_clean = re.sub(r"<style[^>]*>.*?</style>", "", html_clean, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", html_clean)
    text = re.sub(r"\s+", " ", text)
    # Look for relevant snippets
    for term in ["gut", "microbiome", "aging", "Bifidobacterium"]:
        idx = text.lower().find(term.lower())
        if idx != -1:
            print(f"Found '{term}' at position {idx}: ...{text[idx:idx+200]}...")

# Since search engines are blocked, let's verify via Wikipedia (known good secondary source)
print("\n=== Wikipedia: Dunedin Multiverse/Dunedin Study ===")
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, "https://en.wikipedia.org/wiki/Dunedin_Multidisciplinary_Health_and_Research_Study"], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
title = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
if title:
    print(f"Title: {title.group(1).strip()[:100]}")
# Look for DunedinPACE references
html_clean = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
html_clean = re.sub(r"<style[^>]*>.*?</style>", "", html_clean, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r"<[^>]+>", " ", html_clean)
text = re.sub(r"\s+", " ", text)
for term in ["DunedinPACE", "biological aging", "pace of aging"]:
    idx = text.lower().find(term.lower())
    if idx != -1:
        print(f"Found '{term}': ...{text[idx:idx+200]}...")

print("\n=== Wikipedia: Bifidobacterium ===")
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, "https://en.wikipedia.org/wiki/Bifidobacterium"], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
title = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
if title:
    print(f"Title: {title.group(1).strip()[:100]}")
html_clean = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
html_clean = re.sub(r"<style[^>]*>.*?</style>", "", html_clean, flags=re.DOTALL | re.IGNORECASE)
text = re.sub(r"<[^>]+>", " ", html_clean)
text = re.sub(r"\s+", " ", text)
for term in ["Bifidobacterium adolescentis", "GABA", "folate", "anti-inflammatory"]:
    idx = text.lower().find(term.lower())
    if idx != -1:
        print(f"Found '{term}': ...{text[idx:idx+200]}...")
