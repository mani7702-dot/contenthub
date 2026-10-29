#!/usr/bin/env python3
"""Fetch HTML content of a given URL via curl, print to stdout."""
import sys, subprocess
UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"
url = sys.argv[1]
r = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True)
data = r.stdout
print(data.decode("utf-8", errors="replace"))
