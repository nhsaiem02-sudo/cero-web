#!/usr/bin/env python3
"""Resize and convert the page's heavy artwork to WebP.

The four service banners and four problem cards were the site's whole
performance problem: 9.2 MB of the 10.3 MB image payload, all of it PNG, and all
of it roughly three times larger than it ever renders. PNG is a lossless format
built for line art; these are dense illustrations, so it is the wrong container.

Each is resized to 1100px wide, which is 2x the ~530px both sets actually
display at, and written as WebP at quality 80.

The source PNGs are deliberately kept. They are the masters, and the <picture>
elements name them as the fallback for browsers without WebP support. A browser
that understands WebP never requests them.

Usage:  python3 scripts/build-webp.py      (run from the project root)
Requires: Pillow
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

TARGET_W = 1100      # 2x the ~530px these render at
QUALITY = 80

SOURCES = [
    "service-01-banner.png",
    "service-02-banner.png",
    "service-03-banner.png",
    "service-04-banner.png",
    "problem-01-manual-work.png",
    "problem-02-production-cost.png",
    "problem-03-visibility.png",
    "problem-04-website.png",
]


def main():
    before = after = 0
    for name in SOURCES:
        src = ASSETS / name
        if not src.exists():
            print(f"  SKIP (missing): {name}")
            continue

        img = Image.open(src)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")
        if img.width > TARGET_W:
            h = round(img.height * TARGET_W / img.width)
            img = img.resize((TARGET_W, h), Image.LANCZOS)

        out = ASSETS / (Path(name).stem + ".webp")
        img.save(out, "WEBP", quality=QUALITY, method=6)

        b = src.stat().st_size / 1024
        a = out.stat().st_size / 1024
        before += b
        after += a
        print(f"  {out.name:34s} {img.width}x{img.height}  "
              f"{b:7.0f} KB -> {a:6.0f} KB  ({100 - 100 * a / b:.0f}% smaller)")

    if before:
        print(f"\n  total {before / 1024:.1f} MB -> {after / 1024:.2f} MB  "
              f"({100 - 100 * after / before:.0f}% saved)")


if __name__ == "__main__":
    main()
