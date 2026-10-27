import subprocess, os, gzip

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Fetch just the badge story
slug = "badge-sends-to-space"
url = "https://www.bbc.co.uk/news/articles/cq78pzl85nglo"

p = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "25", "-A", UA, url], capture_output=True, timeout=30)
data = p.stdout

# Print first 1000 chars to see what we got
text = data.decode(errors='replace')
print(f"Length: {len(data)}")
# Look for key content
if "article" in text[:2000].lower():
    print("Contains article content")
# Check if it's a Cloudflare challenge
if "just a moment" in text.lower() or "checking your browser" in text.lower():
    print("CLOUDFLARE CHALLENGE BLOCKED")
# Print a portion to see what we actually got
print("First 2000 chars:")
print(text[:2000])
