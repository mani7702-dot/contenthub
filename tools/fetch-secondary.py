#!/usr/bin/env python3
"""Extract actual URL from Bing News redirect and fetch the page."""
import subprocess, urllib.parse, re, sys, html as html_module

bing_url = sys.argv[1]
parsed = urllib.parse.urlparse(bing_url)
qs = urllib.parse.parse_qs(parsed.query)
actual = qs.get("url", [bing_url])[0]
actual = urllib.parse.unquote(actual)
print(f"Actual URL: {actual}")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
p = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, "--compressed", actual], capture_output=True)
raw = p.stdout.decode("utf-8", errors="replace")
print(f"Page length: {len(raw)}")

# Extract readable text
raw_clean = re.sub(r"<script[^>]*>.*?</script>", "", raw, flags=re.DOTALL | re.IGNORECASE)
raw_clean = re.sub(r"<style[^>]*>.*?</style>", "", raw_clean, flags=re.DOTALL | re.IGNORECASE)
paras = re.findall(r"<p[^>]*>(.*?)</p>", raw_clean, re.DOTALL | re.IGNORECASE)
for para in paras:
    text = re.sub(r"<[^>]+>", "", para).strip()
    text = html_module.unescape(text)
    if len(text) > 40:
        print(text)
        print()
