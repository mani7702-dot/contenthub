from PIL import Image

# Let's crop and examine specific regions to understand the image
im = Image.open("assets/images/who-was-panther-pat-the-first-woman-to-play-pro-football.jpg")
w, h = im.size
print(f"Full image: {w}x{h}")

# Look at top third (likely sky/crowd)
top = im.crop((0, 0, w, h//3))
print(f"\nTop third (Y=0 to {h//3}):")
for y in range(0, h//3, h//30):
    row = [top.getpixel((x, y)) for x in range(0, top.width, top.width//8)]
    print(f"  Y={y}: {row}")

# Look at middle third
mid = im.crop((0, h//3, w, 2*h//3))
print(f"\nMiddle third:")
for y in range(0, mid.height, mid.height//10):
    row = [mid.getpixel((x, y)) for x in range(0, mid.width, mid.width//8)]
    print(f"  Y={y}: {row}")

# Look at bottom third
bot = im.crop((0, 2*h//3, w, h))
print(f"\nBottom third:")
for y in range(0, bot.height, bot.height//10):
    row = [bot.getpixel((x, y)) for x in range(0, bot.width, bot.width//8)]
    print(f"  Y={y}: {row}")
