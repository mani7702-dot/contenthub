#!/usr/bin/env python3
"""Resize image for vision verification if too large."""
from PIL import Image
im = Image.open('assets/images/how-did-a-kangaroo-end-up-3-kilometers-offshore-and-how-did-divers-save-it.jpg')
print(f"Original size: {im.size}")
im.resize((400, 300), Image.Resampling.LANCZOS).save('/tmp/verify_roo.jpg', 'JPEG', quality=85)
print("Saved resized to /tmp/verify_roo.jpg")
