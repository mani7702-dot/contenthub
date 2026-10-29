from PIL import Image
im = Image.open("assets/images/who-was-panther-pat-the-first-woman-to-play-pro-football.jpg")
print(f"Size: {im.size}, Mode: {im.mode}")
w, h = im.size
# Sample grid
non_black = 0
total = 0
for x in range(0, w, 10):
    for y in range(0, h, 10):
        px = im.getpixel((x, y))
        total += 1
        if px != (0, 0, 0):
            non_black += 1
print(f"Non-black: {non_black}/{total} ({100*non_black/total:.1f}%)")
# Print a few pixel values
print(f"Top-left: {im.getpixel((0,0))}, Center: {im.getpixel((w//2, h//2))}, Top-right: {im.getpixel((w-1, 0))}")
