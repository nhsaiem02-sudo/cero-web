#!/usr/bin/env python3
"""Prepare the Our Work case study videos for the web.

The sources are 1920x1080 H.264 at roughly 9-10 Mbps, about 43 MB for 35
seconds, and both were written with the moov atom AFTER mdat. That second part
is the blocking problem: with the index at the end of the file, a browser has to
download the whole thing before it can show a single frame, so the player just
sits there. -movflags +faststart moves the index to the front and playback can
begin immediately.

While remuxing anyway, the bitrate comes down to something appropriate for a
marketing page. CRF 24 at this resolution is visually indistinguishable and cuts
the payload by roughly three quarters.

Also grabs frame one of each as a poster, so the card shows the opening frame
rather than a black box before play.

Usage:  python3 scripts/build-videos.py     (run from the project root)
Requires: ffmpeg
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

PAIRS = [
    ("custom agent.mp4",          "custom-ai-agent.mp4"),
    ("AI commercial for oreo.mp4", "ai-commercial-oreo.mp4"),
]


def run(args):
    subprocess.run(args, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    for src_name, out_name in PAIRS:
        src = ASSETS / src_name
        if not src.exists():
            print(f"  SKIP (missing): {src_name}")
            continue

        out = ASSETS / out_name
        run(["ffmpeg", "-y", "-i", str(src),
             "-c:v", "libx264", "-crf", "24", "-preset", "medium",
             "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "128k",
             "-movflags", "+faststart",
             str(out)])

        poster = out.with_name(out.stem + "-poster.jpg")
        run(["ffmpeg", "-y", "-i", str(src),
             "-vf", "select=eq(n\\,0)", "-vframes", "1", "-q:v", "4",
             str(poster)])

        before = src.stat().st_size / 1024 / 1024
        after = out.stat().st_size / 1024 / 1024
        pk = poster.stat().st_size / 1024
        print(f"  {out_name:26s} {before:6.1f} MB -> {after:5.1f} MB   "
              f"poster {poster.name} ({pk:.0f} KB)")


if __name__ == "__main__":
    main()
