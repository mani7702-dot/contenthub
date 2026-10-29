#!/usr/bin/env python3
"""Resize a large image for vision_analyze."""
from PIL import Image
import sys

path = sys.argv[1]
im = Image.open(path)
w, h = im.size
new_w = 400
new_h = int(h * new_w / w)
im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
im_resized.save("/tmp/verify_magma.jpg", "JPEG", quality=85)
print(f"Resized to /tmp/verify_magma.jpg ({new_w}x{new_h})")
