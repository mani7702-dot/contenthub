#!/usr/bin/env python3
from PIL import Image
im = Image.open("assets/images/how-did-einstein-s-equations-reveal-a-hidden-flaw-in-the-universe-s-biggest-puzzle.jpg")
im.resize((400, 300), Image.Resampling.LANCZOS).save("/tmp/verify_einstein.jpg", "JPEG", quality=85)
print("Saved resized image")
