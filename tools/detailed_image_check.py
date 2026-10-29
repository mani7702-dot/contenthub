#!/usr/bin/env python3
"""Detailed pixel inspection to understand image content."""
from PIL import Image
import sys

img_path = sys.argv[1] if len(sys.argv) > 1 else "assets/images/how-do-t-cells-feel-their-surroundings-to-help-us-stay-healthy.jpg"

im = Image.open(img_path)
w, h = im.size
print(f"Size: {w}x{h}, Mode: {im.mode}")

for y in range(100, h, h // 8):
    for x in range(100, w, w // 8):
        px = im.getpixel((x, y))
        print(f"  ({x}, {y}): {px}")

center_region = im.crop((w//4, h//4, 3*w//4, 3*h//4))
center_data = list(center_region.getdata())
bright = sum(1 for p in center_data if sum(p) > 600)
dark = sum(1 for p in center_data if sum(p) < 50)
print(f"\nCenter region: {bright} bright, {dark} dark, {len(center_data)-bright-dark} mid")
