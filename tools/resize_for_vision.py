#!/usr/bin/env python3
"""Resize image for vision verification."""
from PIL import Image

im = Image.open("assets/images/how-did-a-tiny-laser-beam-make-computer-memory-1000-times-faster.jpg")
print(f"Original size: {im.size}")
im = im.convert("RGB")
im = im.resize((400, 300), Image.LANCZOS)
im.save("/tmp/verify_laser.jpg", "JPEG", quality=85)
print("Saved to /tmp/verify_laser.jpg (400x300)")
