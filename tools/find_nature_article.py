#!/usr/bin/env python3
"""Try to find the Nature Publishing Group / Scientific Reports article URL."""
import subprocess, re

ua = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# The Nature article URL from Google News RSS was decoded to:
# https://www.nature.com/articles/s41598-026-00000-0 (but I need the real DOI)
# Let's try searching for the article on nature.com directly
# Also try the UH press release

urls_to_try = [
    "https://www.hawaii.edu/biomed/news/gut-microbiome-aging/",
    "https://manoa.hawaii.edu/medicine/news/gut-microbiome-aging/",
    "https://www.hawaii.edu/news/2026/10/",
    "https://news.google.com/articles/CBMieEFVX3lxTFB1Q0NPVGdLa1hLR3FTUk9kVmY0WWNtMEcyYVVrRFpvU3Z2bGtEMzhuZVdtNTZ5VkhGLXVoQ3Z0c1NBZDdnbm9ONTBRNk5JMzNHcERLck9lU1ZENUFtLVoyOVg4UHVEejFhZDZtQ0pTQy1rVVllcGhLYw?hl=en-US&gl=US&ceid=US:en",
]

for url in urls_to_try:
    print(f"\n--- {url} ---")
    p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, "-H", "Accept: text/html", url], capture_output=True)
    html = p.stdout.decode("utf-8", errors="replace")
    print(f"  Chars: {len(html)}")
    title = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    if title:
        t = title.group(1).strip()
        print(f"  Title: {t[:100]}")
    # Check if there's a redirect
    if "scrollde" in html.lower() or "redirect" in html.lower():
        print("  [Contains redirect/scroll]")

# Try the Nature.com article with proper DOI format
# DOI 10.1038/s41598-026-00000-0 -> nature.com/articles/s41598-026-00000-0
for doi_url in [
    "https://www.nature.com/articles/s41598-026-28345-1",
    "https://www.nature.com/articles/s41598-026-28345-2",
    "https://www.nature.com/articles/s41598-026-28000-1",
]:
    print(f"\n--- {doi_url} ---")
    p = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", ua, "-H", "Accept: text/html", doi_url], capture_output=True)
    html = p.stdout.decode("utf-8", errors="replace")
    print(f"  Chars: {len(html)}")
    title = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    if title:
        print(f"  Title: {title.group(1).strip()[:100]}")
    # Look for the DOI in the page
    doi_match = re.search(r'(s41598-026-\d+)', html)
    if doi_match:
        print(f"  Found DOI: {doi_match.group(1)}")
    # Look for abstract content
    abstract = re.findall(r'<meta name="description" content="(.*?)"', html, re.DOTALL)
    for a in abstract[:1]:
        print(f"  Description: {a[:200]}")
