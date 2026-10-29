from PIL import Image
im = Image.open("assets/images/how-did-scientists-date-128-000-year-old-ice-from-tibet.jpg")
im.resize((400, 300), Image.LANCZOS).save("/tmp/verify_ice.jpg", "JPEG", quality=85)
print("Resized to /tmp/verify_ice.jpg")
