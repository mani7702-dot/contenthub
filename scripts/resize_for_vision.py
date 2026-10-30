from PIL import Image
im = Image.open("assets/images/how-did-two-electrons-working-together-break-physics-x-ray-energy-limit.jpg")
im.resize((400, 300), Image.Resampling.LANCZOS).save("/tmp/verify_electrons.jpg", "JPEG", quality=85)
print("Saved resized version to /tmp/verify_electrons.jpg")
print(f"Original size: {im.size}")
