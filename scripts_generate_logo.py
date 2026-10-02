"""One-off script to generate a placeholder LegalEase logo. Not part of the app."""
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 420, 160
INK = (25, 25, 25, 255)

img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

cx, cy = 80, 70
beam_top = (cx, cy - 45)
beam_left = (cx - 42, cy - 10)
beam_right = (cx + 42, cy - 10)

draw.line([beam_left, beam_right], fill=INK, width=3)
draw.line([beam_top, (cx, cy + 10)], fill=INK, width=3)
draw.line([(cx - 2, cy - 45), (cx + 2, cy - 45)], fill=INK, width=3)

for side in (beam_left, beam_right):
    sx, sy = side
    draw.line([side, (sx - 16, sy + 34)], fill=INK, width=2)
    draw.line([side, (sx + 16, sy + 34)], fill=INK, width=2)
    draw.arc([sx - 16, sy + 10, sx + 16, sy + 50], start=10, end=170, fill=INK, width=2)

draw.line([(cx - 30, cy + 10), (cx + 30, cy + 10)], fill=INK, width=3)
draw.polygon([(cx, cy + 10), (cx - 10, cy + 28), (cx + 10, cy + 28)], outline=INK)
draw.line([(cx - 20, cy + 60), (cx + 20, cy + 60)], fill=INK, width=4)
draw.line([(cx, cy + 10), (cx, cy + 60)], fill=INK, width=3)

font = None
for candidate in (
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    "/System/Library/Fonts/Times.ttc",
):
    try:
        font = ImageFont.truetype(candidate, 46)
        break
    except OSError:
        continue
if font is None:
    font = ImageFont.load_default()

draw.text((160, 55), "LegalEase", font=font, fill=INK)

img.save("Image/Logo.png")
print("Logo saved to Image/Logo.png")
