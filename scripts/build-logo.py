#!/usr/bin/env python3
"""Derive the dark-background logo assets from assets/logo.png.

The supplied master is a stacked square lockup: navy + gold artwork on an opaque
white ground, occupying ~8.5% of a 1000x1000 canvas. Three things have to happen
before it can sit on the navy navbar:

  1. trim the white margin, or the art renders ~8px tall at navbar height
  2. turn the white ground into alpha

Colours are left exactly as drawn -- no recolouring anywhere in this pipeline.
It is then recomposed horizontally (icon left, CERO/STUDIO right), because the
square lockup leaves "STUDIO" illegible in a 74px bar.

Usage:  python3 scripts/build-logo.py       (run from the project root)
Requires: Pillow
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "logo.png"
OUT = ROOT / "assets"

# Element bounds measured from the 1000x1000 master.
MARK = (433, 350, 568, 488)   # the C icon
TEXT = (344, 520, 656, 624)   # CERO + STUDIO together, original spacing preserved

NAVY = (10, 17, 40, 255)        # --navy-800
WHITE_PLATE = (255, 255, 255, 255)

WHITE_CUTOFF = 45             # distance-from-white at which a pixel is fully opaque


def to_rgba(img):
    """White ground -> alpha, with a soft ramp so antialiased edges stay smooth."""
    im = img.convert("RGB")
    w, h = im.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    o, p = out.load(), im.load()
    for y in range(h):
        for x in range(w):
            r, g, b = p[x, y]
            dist = 255 - min(r, g, b)          # 0 == pure white
            if dist > 0:
                o[x, y] = (r, g, b, min(255, int(dist / WHITE_CUTOFF * 255)))
    return out.crop(out.getbbox())




def lockup(mark, text, ratio=1.28, gap_ratio=0.26):
    """Horizontal lockup: icon left, wordmark block right, both vertically centred."""
    tw, th = text.size
    mh = round(th * ratio)
    mw = round(mark.size[0] * mh / mark.size[1])
    mark = mark.resize((mw, mh), Image.LANCZOS)
    gap = round(mw * gap_ratio)

    W, H = mw + gap + tw, max(mh, th)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.alpha_composite(mark, (0, (H - mh) // 2))
    out.alpha_composite(text, (mw + gap, (H - th) // 2))
    return out.crop(out.getbbox())


def chip(mark, size, bg, pad=0.12, radius=0.22, sharpen=False):
    """Square icon on a rounded plate, composed at 4x and downsampled.

    The plate guarantees contrast in a browser tab strip, light or dark. Note the
    source icon is only ~135px, so sizes above ~135 are an upscale.
    """
    s = size * 4
    plate = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle(
        [0, 0, s - 1, s - 1], radius=int(s * radius), fill=bg)

    inner = int(s * (1 - pad * 2))
    mw, mh = mark.size
    scale = min(inner / mw, inner / mh)
    m = mark.resize((max(1, int(mw * scale)), max(1, int(mh * scale))), Image.LANCZOS)
    plate.alpha_composite(m, ((s - m.size[0]) // 2, (s - m.size[1]) // 2))

    out = plate.resize((size, size), Image.LANCZOS)
    if sharpen:                                # recover crispness at tab sizes
        out = out.filter(ImageFilter.UnsharpMask(radius=0.6, percent=70, threshold=2))
    return out


def main():
    if not SRC.exists():
        raise SystemExit(f"missing master artwork: {SRC}")

    src = Image.open(SRC)
    mark = to_rgba(src.crop(MARK))                 # the asset's own navy + gold
    text = to_rgba(src.crop(TEXT))

    lk = lockup(mark, text)
    lk.save(OUT / "logo-navbar.png")
    print(f"  logo-navbar.png      {lk.size[0]}x{lk.size[1]}  (true colour)")

    # Favicons keep the logo's TRUE colours (navy and gold both present) on a
    # white plate. The plate is what makes the navy half survive a dark tab strip;
    # a transparent ground would drop it into the background.
    for size, name, sharp in [(16, "favicon-16.png", True),
                              (32, "favicon-32.png", True),
                              (180, "apple-touch-icon.png", False),
                              (512, "favicon-512.png", False)]:
        chip(mark, size, WHITE_PLATE, pad=0.10, sharpen=sharp).save(OUT / name)
        print(f"  {name:<20} {size}x{size}  (true colour on white)")


if __name__ == "__main__":
    main()
