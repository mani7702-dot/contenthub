#!/usr/bin/env python3
"""Verify downloaded image content using PIL pixel inspection."""
from PIL import Image
import sys

img_path = sys.argv[1] if len(sys.argv) > 1 else "assets/images/how-do-t-cells-feel-their-surroundings-to-help-us-stay-healthy.jpg"

im = Image.open(img_path)
print(f"Size: {im.size}, Mode: {im.mode}")
# Sample various regions
w, h = im.size
print(f"Top-left: {im.getpixel((0, 0))}")
print(f"Top-right: {im.getpixel((w-1, 0))}")
print(f"Center: {im.getpixel((w//2, h//2))}")
print(f"Bottom-left: {im.getpixel((0, h-1))}")
print(f"Bottom-right: {im.getpixel((w-1, h-1))}")
# Check corner brightness patterns
corners = [im.getpixel((0,0)), im.getpixel((w-1,0)), im.getpixel((0,h-1)), im.getpixel((w-1,h-1))]
avg_corner = tuple(sum(c)//4 for c in zip(*corners))
print(f"Avg corner: {avg_corner}")
# Resize for vision_analyze if needed
im_small = im.resize((400, 300), Image.Resampling.LANCZOS)
im_small.save("/tmp/verify_img.jpg", "JPEG", quality=85)
print("Saved /tmp/verify_img.jpg for vision analysis")
