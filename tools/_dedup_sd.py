#!/usr/bin/env python3
"""Check ScienceDaily titles against existing content for dedup."""
import subprocess, xml.etree.ElementTree as ET, gzip, os

url = "https://www.sciencedaily.com/rss/top.xml"
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
p = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True)
data = p.stdout
if data[:2] == b"\x1f\x8b":
    data = gzip.decompress(data)
idx = data.rfind(b"</rss>")
if idx >= 0:
    data = data[:idx+6]
root = ET.fromstring(data)
dirs = ["content/news", "content/blog", "content/trending"]
existing = []
for d in dirs:
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".md"):
                existing.append(os.path.join(d, f))
existing_text = " | ".join(existing)

rows = []
for it in root.iter("item"):
    t = (it.findtext("title") or "").strip()
    l = (it.findtext("link") or "").strip()
    if t and len(t) > 25:
        rows.append((t, l))

for i, (t, l) in enumerate(rows, 1):
    # grep each title against existing content
    p2 = subprocess.run(
        ["grep", "-ril", t, "content/news/", "content/blog/", "content/trending/"],
        capture_output=True
    )
    found = p2.stdout.decode().strip() if p2.stdout.decode().strip() else None
    status = "COVERED" if found else "FRESH"
    print(f"{i}. [{status}] {t}")
    if found:
        print(f"   -> {found.splitlines()[:1]}")
    else:
        print(f"   URL: {l}")
