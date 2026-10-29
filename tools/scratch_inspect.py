#!/usr/bin/env python3
from PIL import Image, ImageStat
im = Image.open("assets/images/how-did-aging-muscles-trade-strength-for-protection.jpg").convert("RGB")
print(f"Size: {im.size}, Mode: {im.mode}")
# Grid sampling
w, h = im.size
step_x, step_y = w // 8, h // 8
for y in range(0, h, step_y):
    row = [im.getpixel((x, y)) for x in range(0, w, step_x)]
    print(f"Y={y}: {row}")
non_black = sum(1 for x in range(0, w, 5) for y in range(0, h, 5) if im.getpixel((x, y)) != (0, 0, 0))
total = sum(1 for _ in range(0, w, 5) for _ in range(0, h, 5))
print(f"Non-black: {non_black}/{total} ({100*non_black/total:.1f}%)")
# Dominant colors
colors = im.getcolors(maxcolors=1000000)
colors.sort(reverse=True)
print("Top 10 colors (count, rgb):")
for cnt, rgb in colors[:10]:
    print(f"  {cnt}: {rgb}")
