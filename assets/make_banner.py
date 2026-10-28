"""Generate the profile README banner.

Run with: python assets/make_banner.py
Produces assets/banner.png (1280 x 320).

Text sizes are chosen so that the banner stays legible when it is scaled down
to a phone width of about 360px, where it renders at roughly 28% of full size.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 320
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
OUT = os.path.join(os.path.dirname(__file__), "banner.png")

NAME = "Manoj Kumar Mansingh"
TAGLINE = "Biotechnology  ×  Python  ×  Bioinformatics"

# Width available for text before the helix starts.
TEXT_W = 1040


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def fit_font(draw, text, font_path, max_size, max_width):
    """Largest font size at which text fits inside max_width."""
    size = max_size
    while size > 10:
        font = ImageFont.truetype(font_path, size)
        if draw.textlength(text, font=font) <= max_width:
            return font, size
        size -= 2
    return ImageFont.truetype(font_path, 10), 10


def main():
    img = Image.new("RGB", (W, H), "#0B1F26")
    draw = ImageDraw.Draw(img)

    top, bottom = (11, 31, 38), (20, 62, 74)
    for y in range(H):
        draw.line([(0, y), (W, y)], fill=lerp(top, bottom, y / H))

    # DNA double helix on the right.
    amp, period, start_x = 60, 120, 1145
    a_pts, b_pts = [], []
    for x in range(start_x, W):
        t = x - start_x
        a_pts.append((x, H / 2 + amp * math.sin(t / period * 2 * math.pi)))
        b_pts.append((x, H / 2 + amp * math.sin(t / period * 2 * math.pi + math.pi)))
    for i in range(0, len(a_pts), 24):
        draw.line([a_pts[i], b_pts[i]], fill=(46, 125, 91), width=2)
    draw.line(a_pts, fill=(126, 217, 173), width=5, joint="curve")
    draw.line(b_pts, fill=(94, 160, 200), width=5, joint="curve")

    bold = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
    name_font, name_size = fit_font(draw, NAME, bold, 96, TEXT_W)
    tag_font, tag_size = fit_font(draw, TAGLINE, bold, 56, TEXT_W)

    draw.text((64, 96), NAME, font=name_font, fill=(255, 255, 255))
    draw.text((66, 96 + name_size + 26), TAGLINE, font=tag_font, fill=(126, 217, 173))

    img.save(OUT, "PNG")
    print(f"wrote {OUT} {img.size} name={name_size}px tagline={tag_size}px")
    print(f"at 360px wide: name ~{name_size * 360 / W:.1f}px, tagline ~{tag_size * 360 / W:.1f}px")


if __name__ == "__main__":
    main()
