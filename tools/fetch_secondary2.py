#!/usr/bin/env python3
"""Fetch secondary sources via Google News article redirect decoding."""
import subprocess, re, sys
import urllib.parse

ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Google News RSS provides article URLs that redirect. Let's try fetching the
# Google News article pages which often embed the source article content.
# The Google News RSS entries have specific article URLs.

urls = [
    # Nature Scientific Reports article (from Google News RSS)
    ("Nature Sci Rep (from GN)", "https://news.google.com/articles/CBMieEFVX3lxTFB1Q0NPVGdLa1hLR3FTUk9kVmY0WWNtMEcyYVVrRFpvU3Z2bGtEMzhuZVdtNTZ5VkhGLXVoQ3Z0c1NBZDdnbm9ONTBRNk5JMzNHcERLck9lU1ZENUFtLVoyOVg4UHVEejFhZDZtQ0pTQy1rVVllcGhLYw?hl=en-US&gl=US&ceid=US:en"),
    # SciTechDaily (from Google News RSS)  
    ("SciTechDaily", "https://news.google.com/articles/CBMiigFBVV95cUxNNDVYb2tVdHdlcnByWElkNmIxOThNVmNIbGRfWUhGcXBpVXBxZU9FYU5CblhycmJ2aXlhbVEtNkVvYXJvUXNVUEFTVUxMa29Ua1BTNVgtT2Nka2NONFFmVzF0NXd1M2ZIaHlqblRQNUctYU85MjNzZjRoTGxpVGJ2OXB4SDJqeHlSSUHSAY8BQVVfeXFMUDE7QTVFYUZrcWRrXzF9lVHhfVGltWi1zYUVEU2pBdFgySWR0U2xLVmxJMUxmZlpySDJmbHcxU3RXNnBRTlNwQWtwVXlkQlhDLXdabXN1cVcxd0hKWk0xak5WMy03ZVNyeXhPOTd3NjEzWHloeGdiZUhJeTdRSVNmdW5xN1B0bEJKbXBXOTlBZUE?hl=en-US&gl=US&ceid=US:en"),
    # UH press release (from Google News RSS)
    ("UH Press Release", "https://news.google.com/articles/CBMijwFBVV95cUxPYzFuQlNIcmRwSHNBa3YwYUZZQ1pGeW00c001WUZpZGFuNkNxYlVVdzR0S282aW1lYzRXcG5vcTZLZGoyX1prN1FHdjZhRVJpMnNVeGhJZ01DSnFXVFpJamZPVktBd2tvRzR3ZzViamZPZWd0VnBVM1V0MDFWdEFCSUQ3aEd2Njl3d3hJb25MNA?hl=en-US&gl=US&ceid=US:en"),
]

# Actually, let's just try the actual source URLs directly
real_urls = [
    ("SciTechDaily", "https://www.sciencedaily.com/releases/2026/10/261026225620.htm"),
    # UH press release is at the UH site
]

# Try fetching the actual University of Hawaii press release
# The Google News RSS said: "Gut bacteria tied to biological aging, new UH study finds - University of Hawaii System"
uh_urls = [
    "https://www.hawaii.edu/news/2026/10/27/gut-bacteria-aging/",
    "https://www.hawaii.edu/news/2026/10/28/gut-bacteria-aging/",
]

for url in uh_urls:
    print(f"\n--- {url} ---")
    p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, url], capture_output=True)
    html = p.stdout.decode("utf-8", errors="replace")
    print(f"  Chars: {len(html)}")
    title = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    if title and "not found" not in title.group(1).lower():
        print(f"  Title: {title.group(1).strip()[:150]}")
    elif len(html) > 5000:
        # Look for any matching article links on the October 2026 page
        pass

# Let's try fetching the UH October 2026 news page and find the article
print("\n--- Searching UH October 2026 news page ---")
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, "https://www.hawaii.edu/news/2026/10/"], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
# Find links containing "gut" or "microbiome" or "aging"
links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL)
for href, text in links:
    if re.search(r'gut|microbiome|aging|aging|biome', text, re.IGNORECASE) or re.search(r'gut|microbiome|aging', href, re.IGNORECASE):
        print(f"  Link: {href}")
        print(f"  Text: {re.sub(r'<[^>]+>', '', text).strip()[:100]}")

# Also try the Nature article directly - find the real DOI
print("\n--- Trying Nature article with correct URL ---")
# From Google News RSS, the Nature article title was:
# "Gut microbiome signatures associate with DNA methylation-based biological aging | Scientific Reports - Nature"
# Let's search Nature for it
p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, "https://www.nature.com/search?query=gut+microbiome+DNA+methylation+biological+aging"], capture_output=True)
html = p.stdout.decode("utf-8", errors="replace")
# Find article links
article_links = re.findall(r'href="(https?://[^"]*nature\.com[^"]*s41598[^"]*)"', html)
if article_links:
    print(f"  Found Nature article links:")
    for link in article_links[:3]:
        print(f"    {link}")
else:
    # Try finding any s41598 link
    article_links = re.findall(r'href="([^"]*s41598[^"]*)"', html)
    print(f"  s41598 links found: {len(article_links)}")
    for link in article_links[:3]:
        print(f"    {link}")
    # Show the page title to see if it's a real page
    title = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    if title:
        print(f"  Search page title: {title.group(1).strip()[:100]}")
