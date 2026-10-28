#!/usr/bin/env python3
"""Cross-check the teacher positivity story with a web search."""
import subprocess, json

# Use the search tool to find corroborating articles
queries = [
    "Tyler Richards Rex Elementary School positive affirmations Kansas",
    "Shane Paulus Rex Elementary Haysville Kansas positivity practice",
    "Kansas elementary school daily positive affirmations children",
]

for q in queries:
    print(f"\n=== Query: {q} ===")
    # Try bing search via the search-bing tool
    result = subprocess.run([
        "python3", "/home/ubuntu/contenthub/tools/google-search.py", q
    ], capture_output=True, text=True, timeout=30)
    print(result.stdout[:2000] if result.stdout else result.stderr[:2000])
