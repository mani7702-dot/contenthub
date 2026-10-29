#!/usr/bin/env python3
from PIL import Image
im = Image.open("assets/images/do-spiders-dream-what-their-nightly-twitches-might-mean.jpg")
w, h = im.size
step_x, step_y = w // 10, h // 10
print(f"Size: {im.size}, Mode: {im.mode}")
for y in range(0, h, step_y):
    row = [im.getpixel((x, y)) for x in range(0, w, step_x)]
    print(f"Y={y}: {row}")
non_black = sum(1 for x in range(0,w,5) for y in range(0,h,5) if im.getpixel((x,y)) != (0,0,0))
total = sum(1 for _ in range(0,w,5) for _ in range(0,h,5))
print(f"Non-black: {non_black}/{total} ({100*non_black/total:.1f}%)")
# Sample corners
print(f"Top-left: {im.getpixel((0, 0))}")
print(f"Top-right: {im.getpixel((w-1, 0))}")
print(f"Center: {im.getpixel((w//2, h//2))}")