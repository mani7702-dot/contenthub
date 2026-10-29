#!/usr/bin/env python3
"""Resize and verify image content for ContentHub articles."""
from PIL import Image
import sys

path = sys.argv[1] if len(sys.argv) > 1 else ""
if not path:
    print("Usage: verify-image.py <image_path>")
    sys.exit(1)

im = Image.open(path)
print(f"Size: {im.size}, Mode: {im.mode}")
print(f"Top-left: {im.getpixel((0, 0))}, Center: {im.getpixel((im.width//2, im.height//2))}")

# Resize for vision_analyze
im.thumbnail((400, 400), Image.Resampling.LANCZOS)
im.save("/tmp/verify.jpg", "JPEG", quality=85)
print("Resized to /tmp/verify.jpg")
