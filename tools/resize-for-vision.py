#!/usr/bin/env python3
"""Resize image to <=400px width for vision_analyze."""
from PIL import Image
import sys, os

src = sys.argv[1]
dst = "/tmp/verify.jpg"
im = Image.open(src).convert("RGB")
w, h = im.size
new_w = min(400, w)
new_h = round(h * new_w / w)
im.resize((new_w, new_h), Image.Resampling.LANCZOS).save(dst, "JPEG", quality=85)
print(f"Resized: {w}x{h} -> {new_w}x{new_h}, saved to {dst}")
