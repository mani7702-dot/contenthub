#!/usr/bin/env python3
"""Fetch Nature page and check redirect."""
import subprocess

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
URL = "https://www.nature.com/articles/s41467-026-77572-3"

# Use curl with -L to follow redirects
p = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, "-w", "\n%{http_code}\n%{url_effective}", URL],
                   capture_output=True)
output = p.stdout.decode("utf-8", errors="replace")

# Split on the last two lines (http_code, url_effective)
parts = output.rsplit("\n", 2)
body = parts[0] if len(parts) >= 3 else output
code = parts[-2] if len(parts) >= 2 else "?"
final_url = parts[-1] if len(parts) >= 1 else "?"

print(f"HTTP Code: {code}")
print(f"Final URL: {final_url}")
print(f"Body length: {len(body)}")
print(f"Body snippet: {body[:500]}")
