#!/usr/bin/env python3
"""Verify image content using PIL grid sampling."""
from PIL import Image
im = Image.open("assets/images/can-you-watch-rare-cheetah-cubs-live-from-birth-at-the-smithsonian.jpg")
w, h = im.size
print(f"Size: {im.size}, Mode: {im.mode}")
print(f"Top-left: {im.getpixel((0, 0))}, Center: {im.getpixel((im.width//2, im.height//2))}")

# Grid sampling
step_x, step_y = w // 10, h // 10
for y in range(0, h, step_y):
    row = []
    for x in range(0, w, step_x):
        px = im.getpixel((x, y))
        row.append(px)
    print(f"Y={y}: {row}")

# Non-black ratio
non_black = 0
total = 0
for x in range(0, w, 5):
    for y in range(0, h, 5):
        px = im.getpixel((x, y))
        total += 1
        if px != (0, 0, 0):
            non_black += 1
print(f"Non-black: {non_black}/{total} ({100*non_black/total:.1f}%)")

# Color analysis - check if it looks like a natural photo
pixels = [im.getpixel((x, y)) for x in range(0, w, 10) for y in range(0, h, 10)]
r_mean = sum(p[0] for p in pixels) / len(pixels)
g_mean = sum(p[1] for p in pixels) / len(pixels)
b_mean = sum(p[2] for p in pixels) / len(pixels)
print(f"R mean: {r_mean:.1f}, G mean: {g_mean:.1f}, B mean: {b_mean:.1f}")
print(f"Total sampled pixels: {len(pixels)}")
