#!/usr/bin/env python3
"""Crop the service card artwork down to just its visual banner.

Each assets/service-*.png ships as a complete card: a dark collage on top, then a
white panel carrying the label, headline, description and two sub-labels. The
Services section now sets that wording as real HTML, legible at any width, and
readable by screen readers and crawlers, so the baked-in text panel would be a
duplicate.

This finds the boundary where the collage gives way to the white panel and writes
the collage alone as assets/service-0N-banner.png. Originals are never modified.

Usage:  python3 scripts/build-banners.py      (run from the project root)
Requires: Pillow
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

SOURCES = [
    "service-01-custom-ai-agents-v2.png",
    "service-02-ai-commercial-production.png",
    "service-03-ai-founder-avatar.png",
    "service-04-ai-agent-friendly-website.png",
]

PANEL_MEAN = 215     # mean row luminance at or above this reads as blank white
QUIET_RUN = 25       # consecutive blank rows that mark the panel's top padding


def panel_top(img):
    """First row of the trailing white text panel.

    Scanning up from the bottom is unreliable: the panel's own headline is large
    dark type, and a row through a wide headline averages darker than the
    threshold, so the scan halts inside the panel. (That is exactly what made
    cards 02 and 04 crop 15% lower than 01 and 03.)

    Instead scan downward for the first sustained run of blank white rows: the
    padding between the collage and the "SERVICE 0N" label. Text rows below it
    no longer matter.
    """
    px = img.load()
    w, h = img.size
    xs = list(range(0, w, 5))

    means = []
    for y in range(h):
        s = 0
        for x in xs:
            r, g, b = px[x, y]
            s += 0.2126 * r + 0.7152 * g + 0.0722 * b
        means.append(s / len(xs))

    run = 0
    for y in range(h):
        if means[y] >= PANEL_MEAN:
            run += 1
            if run >= QUIET_RUN:
                return y - run + 1          # first row of the blank band
        else:
            run = 0
    return h


def main():
    for name in SOURCES:
        src = ASSETS / name
        if not src.exists():
            print(f"  SKIP (missing): {name}")
            continue

        img = Image.open(src).convert("RGB")
        cut = panel_top(img)
        if cut >= img.size[1] - 4:
            print(f"  SKIP (no white panel found): {name}")
            continue

        banner = img.crop((0, 0, img.size[0], cut))
        out = ASSETS / f"{name[:10]}-banner.png"      # service-0N-banner.png
        banner.save(out, optimize=True)
        pct = 100 * cut / img.size[1]
        print(f"  {out.name}  {banner.size[0]}x{banner.size[1]}  "
              f"aspect {banner.size[0]/banner.size[1]:.2f}  (top {pct:.0f}% of source)")


if __name__ == "__main__":
    main()
