#!/usr/bin/env python3
"""Resize image for vision verification."""
from PIL import Image
im = Image.open("assets/images/how-did-a-lightning-strike-lead-to-a-proposal-when-she-restarted-his-heart-twice.jpg")
im.resize((400, 300), Image.Resampling.LANCZOS).save("/tmp/verify_lightning.jpg", "JPEG", quality=85)
print("Resized and saved to /tmp/verify_lightning.jpg")
