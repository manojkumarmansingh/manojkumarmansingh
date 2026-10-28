"""Generate the profile README banner.

Run with: python assets/make_banner.py
Produces assets/banner.png (1280 x 320).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 320
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
OUT = os.path.join(os.path.dirname(__file__), "banner.png")


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def main():
    img = Image.new("RGB", (W, H), "#0B1F26")
    draw = ImageDraw.Draw(img)

    top = (11, 31, 38)
    bottom = (20, 62, 74)
    for y in range(H):
        draw.line([(0, y), (W, y)], fill=lerp(top, bottom, y / H))

    # DNA double helix on the right.
    amp, period = 62, 130
    start_x = 930
    a_pts, b_pts = [], []
    for x in range(start_x, W):
        t = x - start_x
        a_pts.append((x, H / 2 + amp * math.sin(t / period * 2 * math.pi)))
        b_pts.append((x, H / 2 + amp * math.sin(t / period * 2 * math.pi + math.pi)))

    for i in range(0, len(a_pts), 24):
        draw.line([a_pts[i], b_pts[i]], fill=(46, 125, 91), width=2)
    draw.line(a_pts, fill=(126, 217, 173), width=5, joint="curve")
    draw.line(b_pts, fill=(94, 160, 200), width=5, joint="curve")

    name_font = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 46)
    tag_font = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 26)
    sub_font = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans.ttf"), 20)

    draw.text((64, 92), "Manoj Kumar Mansingh", font=name_font, fill=(255, 255, 255))
    draw.text((66, 158), "Biotechnology  ×  Python  ×  Bioinformatics",
              font=tag_font, fill=(126, 217, 173))
    draw.text((66, 206), "M.Sc. Biotechnology (final year)  ·  building tools for biological data",
              font=sub_font, fill=(206, 224, 232))

    img.save(OUT, "PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
