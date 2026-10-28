#!/usr/bin/env python3
"""Fetch and parse the GNN article from Wayback Machine or live."""
import subprocess, re

UA = "Mozilla/5.0 (ContentHub picker; contact andugulamani722@gmail.com)"

# Try Wayback Machine CDX API
api_url = "http://archive.org/wayback/available?url=goodnewsnetwork.org/village-installs-knitted-traffic-cops-to-slow-down-speeding-drivers/"
r = subprocess.run(["curl", "-s", "--max-time", "20", "-A", UA, api_url], capture_output=True, text=True)
print("Wayback API response:")
print(r.stdout[:500])
