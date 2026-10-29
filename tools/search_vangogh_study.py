#!/usr/bin/env python3
"""Search for the Van Gogh starry night astronomy study via web search."""
import subprocess, re

# Use ddg/html search
url = "https://html.duckduckgo.com/html/?q=van+gogh+starry+night+star+clusters+taurus+july+1889+study+astronomy"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, "-L", url], capture_output=True, text=True)
html = r.stdout

# Extract result links and snippets
results = re.findall(r'class="result__a"[^>]*>.*?href="(https?://[^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)

print("=== Search Results ===")
for i, (link, title) in enumerate(results[:10]):
    title = re.sub(r'<[^>]+>', '', title).strip()
    print(f"{i+1}. {title}")
    print(f"   URL: {link}")
    if i < len(snippets):
        snip = re.sub(r'<[^>]+>', '', snippets[i]).strip()
        print(f"   Snippet: {snip}")
    print()

# Also search for the specific study
url2 = "https://html.duckduckgo.com/html/?q=%22Starry+Night%22+van+Gogh+astro satellite+star+clusters+Taurus+1889"
r2 = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, "-L", url2], capture_output=True, text=True)
results2 = re.findall(r'class="result__a"[^>]*>.*?href="(https?://[^"]+)"[^>]*>(.*?)</a>', r2.stdout, re.DOTALL)
print("\n=== Search 2 Results ===")
for i, (link, title) in enumerate(results2[:10]):
    title = re.sub(r'<[^>]+>', '', title).strip()
    print(f"{i+1}. {title}")
    print(f"   URL: {link}")
    print()
