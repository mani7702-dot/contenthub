#!/usr/bin/env python3
"""Inspect image content for the Einstein universe article."""
from PIL import Image
import os

img_path = "assets/images/how-did-einstein-s-equations-reveal-a-hidden-flaw-in-the-universe-s-biggest-puzzle.jpg"

if not os.path.exists(img_path):
    print("IMAGE NOT FOUND")
    exit()

im = Image.open(img_path)
print(f"Size: {im.size}, Mode: {im.mode}")

# Grid sampling
w, h = im.size
step_x, step_y = w // 10, h // 10
print("\nGrid sampling (10x10):")
for y in range(0, h, step_y):
    row = [im.getpixel((x, y)) for x in range(0, w, step_x)]
    print(f"  Y={y:4d}: {row}")

# Non-black pixel ratio
non_black = 0
total = 0
for x in range(0, w, 5):
    for y in range(0, h, 5):
        total += 1
        if im.getpixel((x, y)) != (0, 0, 0):
            non_black += 1
print(f"\nNon-black pixels: {non_black}/{total} ({100*non_black/total:.1f}%)")

# Check if it's a photo or artistic
# Natural photos have varied, natural color distributions
# Abstract/art often have saturated geometric blocks
corner_pixels = [im.getpixel((0, 0)), im.getpixel((w-1, 0)), im.getpixel((0, h-1)), im.getpixel((w-1, h-1))]
print(f"Corner pixels: {corner_pixels}")

# Check if mostly black (could be a deep space image)
if non_black/total < 0.3:
    print("WARNING: Low content density - may be mostly black space image")
    # Check if bright spots exist (stars/galaxies)
    bright_pixels = sum(1 for x in range(0,w,3) for y in range(0,h,3) if sum(im.getpixel((x,y))) > 200*3)
    print(f"Bright pixels (>200 each channel): {bright_pixels}")
