#!/usr/bin/env python3
"""Verify downloaded image content using PIL pixel inspection."""
from PIL import Image
import os

img_path = "assets/images/how-did-a-tiny-laser-beam-make-computer-memory-1000-times-faster.jpg"

if not os.path.exists(img_path):
    print(f"ERROR: Image not found at {img_path}")
else:
    im = Image.open(img_path)
    w, h = im.size
    mode = im.mode
    print(f"Size: {w}x{h}, Mode: {mode}")
    print(f"File size: {os.path.getsize(img_path)} bytes")
    
    # Sample grid
    step_x, step_y = w // 10, h // 10
    print("\n=== Grid sampling ===")
    for y in range(0, h, step_y):
        row = []
        for x in range(0, w, step_x):
            pixel = im.getpixel((x, y))
            row.append(pixel)
        print(f"Y={y}: {row}")
    
    # Non-black pixel ratio
    non_black = sum(1 for x in range(0,w,5) for y in range(0,h,5) if im.getpixel((x,y)) != (0,0,0))
    total = sum(1 for _ in range(0,w,5) for _ in range(0,h,5))
    print(f"\nNon-black: {non_black}/{total} ({100*non_black/total:.1f}%)")
    
    # Check corners and center
    print(f"\nTop-left: {im.getpixel((0, 0))}")
    print(f"Top-right: {im.getpixel((w-1, 0))}")
    print(f"Center: {im.getpixel((w//2, h//2))}")
    print(f"Bottom-left: {im.getpixel((0, h-1))}")
    print(f"Bottom-right: {im.getpixel((w-1, h-1))}")
    
    # Determine image type
    # Check if it's a photo (natural colors) vs abstract/art
    # Get average pixel values
    pixels = list(im.getdata())
    avg_r = sum(p[0] for p in pixels) / len(pixels) if pixels else 0
    avg_g = sum(p[1] for p in pixels) / len(pixels) if pixels else 0
    avg_b = sum(p[2] for p in pixels) / len(pixels) if pixels else 0
    print(f"\nAverage RGB: ({avg_r:.1f}, {avg_g:.1f}, {avg_b:.1f})")
    
    # Check color variance (photos have high variance, solid colors have low)
    r_var = sum((p[0] - avg_r) ** 2 for p in pixels) / len(pixels) if pixels else 0
    g_var = sum((p[1] - avg_g) ** 2 for p in pixels) / len(pixels) if pixels else 0
    b_var = sum((p[2] - avg_b) ** 2 for p in pixels) / len(pixels) if pixels else 0
    print(f"Color variance: R={r_var:.1f}, G={g_var:.1f}, B={b_var:.1f}")
    print(f"Overall std-dev: {(r_var + g_var + b_var)**0.5 / 255 * 100:.1f}%")
