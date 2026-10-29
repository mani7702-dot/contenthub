from PIL import Image
im = Image.open("assets/images/how-did-scientists-simulate-the-universe-s-first-2-billion-years-in-one-giant-computer.jpg")
im.resize((400, 300), Image.Resampling.LANCZOS).save("/tmp/verify_lumina.jpg", "JPEG", quality=85)
print("Resized to /tmp/verify_lumina.jpg")
