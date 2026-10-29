#!/usr/bin/env python3
"""Deeper image inspection — sample more pixels, check color distribution."""
from PIL import Image
path = "assets/images/how-did-a-lightning-strike-lead-to-a-proposal-when-she-restarted-his-heart-twice.jpg"
im = Image.open(path)
w, h = im.size
print(f"Size: {w}x{h}, Mode: {im.mode}")

# Sample a grid of pixels
samples = []
for x in range(0, w, w // 10):
    for y in range(0, h, h // 10):
        samples.append(im.getpixel((x, y)))

# Analyze color channels
r_vals = [s[0] for s in samples]
g_vals = [s[1] for s in samples]
b_vals = [s[2] for s in samples]
print(f"R: min={min(r_vals)}, max={max(r_vals)}, avg={sum(r_vals)//len(r_vals)}")
print(f"G: min={min(g_vals)}, max={max(g_vals)}, avg={sum(g_vals)//len(g_vals)}")
print(f"B: min={min(b_vals)}, max={max(b_vals)}, avg={sum(b_vals)//len(b_vals)}")

# Check for bright spots (lightning, stars)
bright = sum(1 for s in samples if s[0] > 200 and s[1] > 200 and s[2] > 200)
dark = sum(1 for s in samples if s[0] < 80 and s[1] < 80 and s[2] < 80)
print(f"Bright pixels: {bright}/{len(samples)} ({100*bright//len(samples)}%)")
print(f"Dark pixels: {dark}/{len(samples)} ({100*dark//len(samples)}%)")

# Blue-dominant pixels (sky/night)
blue_dom = sum(1 for s in samples if s[2] > s[0] + 20 and s[2] > s[1] + 20)
print(f"Blue-dominant pixels: {blue_dom}/{len(samples)} ({100*blue_dom//len(samples)}%)")
