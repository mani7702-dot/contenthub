#!/usr/bin/env python3
"""Check if any of these terms appear in existing content."""
import os

terms = [
    "microplastic", "lunch tab", "baseball team", "fostered 500",
    "opera house grand staircase", "scottish island historical",
    "man named service", "tape can block", "van gogh starry night",
    "standing-up rocks", "6-day workweek", "soil steaming",
    "128,000", "china met mural", "solar panels vines",
    "isle of jersey marine", "10-year-old dog found",
    "coconut oil jet fuel", "italian hobbits wedding ring",
    "towering figure tolerance atlanta", "australia drying land",
    "positive weekly horoscope", "collab china met huge mural",
]

search_dirs = ["content/news", "content/blog", "content/trending"]

for term in terms:
    found = False
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        for fname in os.listdir(d):
            fpath = os.path.join(d, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read().lower()
                if term.lower() in text:
                    found = True
                    print(f"FOUND: {term} (in {fpath})")
                    break
            except Exception:
                pass
        if found:
            break
    if not found:
        print(f"NOT-FOUND: {term}")
