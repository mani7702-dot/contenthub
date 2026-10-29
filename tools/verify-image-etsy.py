from PIL import Image
im = Image.open("assets/images/how-is-etsy-keeping-ai-generated-crafts-away-from-buyers.jpg")
print(f"Size: {im.size}, Mode: {im.mode}")
tl = im.getpixel((0, 0))
cx = im.getpixel((im.width//2, im.height//2))
print(f"Top-left: {tl}, Center: {cx}")
w, h = im.size
non_black = sum(1 for x in range(0,w,5) for y in range(0,h,5) if im.getpixel((x,y)) != (0,0,0))
total = sum(1 for _ in range(0,w,5) for _ in range(0,h,5))
print(f"Non-black: {non_black}/{total} ({100*non_black/total:.1f}%)")
# Sample a grid
step_x, step_y = w // 10, h // 10
for y in range(0, h, step_y):
    row = [im.getpixel((x, y)) for x in range(0, w, step_x)]
    print(f"Y={y}: {row[:5]}")
