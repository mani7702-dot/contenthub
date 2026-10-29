#!/usr/bin/env python3
"""Check a specific title against existing content."""
import subprocess, sys
title = sys.argv[1]
p = subprocess.run(["grep", "-ril", title, "content/news/", "content/blog/", "content/trending/"], capture_output=True)
found = p.stdout.decode().strip()
if found:
    print(f"COVERED: {found}")
else:
    print("FRESH")
