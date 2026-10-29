from PIL import Image
im = Image.open("assets/images/how-did-scientists-date-128-000-year-old-ice-from-tibet.jpg")
print(f"Size: {im.size}, Mode: {im.mode}")
w, h = im.size
step_x, step_y = w // 10, h // 10
for y in range(0, h, step_y):
    row = [im.getpixel((min(x, w-1), min(y, h-1))) for x in range(0, w, step_x)]
    print(f"Y={y}: {row}")
non_black = 0
total = 0
for y in range(0, h, 5):
    for x in range(0, w, 5):
        total += 1
        if im.getpixel((x, y)) != (0, 0, 0):
            non_black += 1
if total:
    print(f"Non-black: {non_black}/{total} ({100*non_black/total:.1f}%)")
