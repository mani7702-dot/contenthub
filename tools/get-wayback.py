#!/usr/bin/env python3
"""Try Wayback Machine for the baseball article."""
import subprocess, re, html, gzip

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

original_url = "https://www.goodnewsnetwork.org/high-school-baseball-team-has-all-the-vibes-of-success-but-never-won-a-game-kids-dont-mind/"

# Try Wayback Machine CDX API to find archived snapshots
cdx_url = f"http://archive.org/wayback/available?url={original_url}"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, cdx_url], capture_output=True, text=True)
print("CDX API response:")
print(r.stdout[:500])

import json
try:
    cdx = json.loads(r.stdout)
    if cdx.get("archived_snapshots", {}).get("closest"):
        snapshot_url = cdx["archived_snapshots"]["closest"]["url"]
        print(f"\nWayback snapshot URL: {snapshot_url}")
        
        r2 = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, snapshot_url], capture_output=True, text=True)
        wayback_html = r2.stdout
        print(f"\nWayback page length: {len(wayback_html)}")
        
        with open("/home/ubuntu/contenthub/tools/baseball-wayback.txt", "w") as f:
            # Extract text
            text = re.sub(r"<script[^>]*>.*?</script>", "", wayback_html, flags=re.DOTALL)
            text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
            text = re.sub(r"<[^>]+>", "\n", text)
            text = html.unescape(text)
            f.write(text)
        print("Saved to tools/baseball-wayback.txt")
except Exception as e:
    print(f"Error: {e}")
