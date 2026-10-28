#!/usr/bin/env python3
"""Resize image for vision verification."""
from PIL import Image

src = "/home/ubuntu/contenthub/assets/images/how-did-a-dartmouth-high-school-baseball-team-stay-smiling-through-6-winless-seasons.jpg"
dst = "/home/ubuntu/contenthub/tools/verify_baseball2.jpg"

im = Image.open(src)
print(f"Original size: {im.size}, mode: {im.mode}")

# Resize to 400px width
new_w = 400
ratio = new_w / im.width
new_h = int(im.height * ratio)
im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
im_resized.save(dst, "JPEG", quality=85)
print(f"Resized to: ({new_w}, {new_h}), saved to {dst}")
