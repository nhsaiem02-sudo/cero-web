#!/usr/bin/env python3
"""Derive the founder-story images for /founder from the originals in assets/.

The originals arrive with spaces in their filenames and at full camera size.
One is a 1.8 MB PNG of a photograph. Both are problems: a space in a filename
has to be percent-encoded in every href, and a PNG is the wrong container for a
photo. This writes web-sized derivatives under the hyphenated names the page
references. Originals are never modified.

The story blocks render at roughly 520px CSS wide, so 1000px covers a 2x screen.

NOTE: several of the sources below were pruned from the repo in a later cleanup,
so this script now prints "SKIP (missing)" for them. That is expected, not a
fault. The PAIRS table is kept because it is the record of where each derivative
came from. Three of the pruned sources were byte-identical to their derivative,
so nothing was lost; the rest were higher-resolution masters. Every one of them
is still in the first commit and can be brought back with:

    git checkout 013ec8e -- "assets/<name>"

Usage:  python3 scripts/build-story-images.py     (run from the project root)
Requires: Pillow
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
MAX_W = 1000

# source (as delivered)              -> derivative (as referenced by founder.html)
PAIRS = [
    ("school days.jpeg",                    "school-days.jpeg"),
    ("after school when move dhaka.jpeg",   "after-school-when-move-dhaka.jpeg"),
    ("travel time.webp",                    "travel-time.webp"),
    # PNG in, JPEG out: the source is a 1.8 MB photograph, which PNG cannot
    # compress. Same pixels, ~5% of the bytes.
    ("when start cero.png",                 "when-start-cero.jpg"),

    # Co-founder story (/co-founder). Note "ceor" in the third source name is
    # the file as delivered, not a typo here; it is a different photograph from
    # "when start cero.png", which belongs to the founder page.
    # ("with cero founder in winter.jpg", "zihadul-roots.jpg") was dropped: the
    # co-founder page swapped that slot for founders-together.jpg, so the
    # derivative had no referrer. The source stays as a master.
    ("after ssc.jpg",                       "zihadul-ssc.jpg"),
    ("when start ceor.png",                 "zihadul-cero.jpg"),

    # Used on BOTH story pages: "Where it starts" on /co-founder and "A second
    # real shot" on /founder. Note this is a different frame from
    # "with cero founder in winter.jpg" (same day, same spot, different shot),
    # confirmed by pixel diff, not by eye.
    ("founders in winter.jpg",              "founders-together.jpg"),
    # Trailing space in the source name is the file as delivered.
    ("zihadul .jpg",                        "zihadul-outdoor.jpg"),
]


def main():
    for src_name, out_name in PAIRS:
        src = ASSETS / src_name
        if not src.exists():
            print(f"  SKIP (missing): {src_name}")
            continue

        img = Image.open(src)
        out = ASSETS / out_name

        # Already small enough and already in the right container: copy the bytes
        # rather than re-encoding. Re-encoding a finished JPEG at q82 can easily
        # come out *larger* than the original while also losing a generation.
        if img.width <= MAX_W and src.suffix.lower() == out.suffix.lower():
            out.write_bytes(src.read_bytes())
            kb = out.stat().st_size / 1024
            print(f"  {out_name:38s} {img.width}x{img.height}  {kb:7.0f} KB (copied as-is)")
            continue

        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")
        if img.width > MAX_W:
            h = round(img.height * MAX_W / img.width)
            img = img.resize((MAX_W, h), Image.LANCZOS)
        if out.suffix in (".jpg", ".jpeg"):
            img.convert("RGB").save(out, "JPEG", quality=82, optimize=True, progressive=True)
        elif out.suffix == ".webp":
            img.save(out, "WEBP", quality=82, method=6)
        else:
            img.save(out, optimize=True)

        before = src.stat().st_size / 1024
        after = out.stat().st_size / 1024
        print(f"  {out_name:38s} {img.width}x{img.height}  "
              f"{before:7.0f} KB -> {after:6.0f} KB")


if __name__ == "__main__":
    main()
