#!/usr/bin/env python3
"""Minify styles.css and main.js for deployment, and repoint the HTML at them.

The source files keep every comment: they carry the reasoning for the cascade
fights, the reveal gate and the video pipeline, and that reasoning is worth more
than the bytes. This script produces styles.min.css / main.min.js alongside them
and rewrites each page's <link> and <script> to the minified names, stamped with
a fresh ?v= so returning visitors are not served a stale copy from the 7-day
cache that /*.css and /*.js carry.

No dependencies: the transforms are deliberately conservative. Nothing here
renames identifiers or reorders declarations, because a wrong minifier on a file
this small would cost more to debug than the couple of kilobytes it saves.

Usage:
    python3 scripts/build-min.py          # build + rewrite HTML
    python3 scripts/build-min.py --check  # report sizes, touch nothing
"""

from __future__ import annotations

import gzip
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Every HTML file that links the stylesheet or the script. A page missing
# from this list keeps the previous ?v= stamp and silently stops getting the
# cache bust the others get, so add new pages here as they are created.
PAGES = [
    "index.html",
    "portfolio.html",
    "founder.html",
    "co-founder.html",
    "404.html",
    "ai-automation.html",
    "ai-receptionist.html",
    "website-chatbot.html",
    "whatsapp-chatbot.html",
    "website-design.html",
]


def minify_css(src: str) -> str:
    """Strip comments and collapse whitespace.

    The url(...) guard matters: a data: URI in this stylesheet contains SVG
    markup with its own spaces and slashes, and collapsing inside it corrupts
    the image. Those tokens are lifted out, the rest is squeezed, then they go
    back untouched.
    """
    holes: list[str] = []

    def stash(m: re.Match) -> str:
        holes.append(m.group(0))
        return f"\x00{len(holes) - 1}\x00"

    src = re.sub(r'url\((?:"[^"]*"|\'[^\']*\'|[^)]*)\)', stash, src)
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    src = re.sub(r"\s+", " ", src)
    src = re.sub(r"\s*([{}:;,>])\s*", r"\1", src)
    src = re.sub(r";}", "}", src)
    src = re.sub(r"\x00(\d+)\x00", lambda m: holes[int(m.group(1))], src)
    return src.strip()


def minify_js(src: str) -> str:
    """Drop comments and indentation only.

    Scanned character by character rather than with regexes. A regex pass over
    JavaScript cannot tell a quote that opens a string from an apostrophe inside
    a comment, and this file's comments are full of words like "cannot" and
    "it's" -- an earlier regex version treated those as string delimiters and
    silently deleted 90% of the file. The scanner tracks which construct it is
    inside, so quotes in comments and slashes in strings are both inert.

    Statements keep their newlines. This file has no semicolon-free lines, but
    joining them would still be a gamble for ~1 KB, and ASI bugs are miserable
    to track down in production.
    """
    out: list[str] = []
    i, n = 0, len(src)
    quote = None          # active string delimiter, or None
    while i < n:
        c = src[i]
        nxt = src[i + 1] if i + 1 < n else ""

        if quote:
            out.append(c)
            if c == "\\" and i + 1 < n:      # escape: take the next char whole
                out.append(nxt)
                i += 2
                continue
            if c == quote:
                quote = None
            i += 1
            continue

        if c in "'\"`":
            quote = c
            out.append(c)
            i += 1
            continue

        if c == "/" and nxt == "*":          # block comment
            end = src.find("*/", i + 2)
            i = n if end == -1 else end + 2
            continue

        if c == "/" and nxt == "/":          # line comment
            end = src.find("\n", i)
            i = n if end == -1 else end
            continue

        out.append(c)
        i += 1

    text = "".join(out)
    text = re.sub(r"(?m)^[ \t]+", "", text)      # indentation
    text = re.sub(r"(?m)[ \t]+$", "", text)      # trailing space left by comments
    text = re.sub(r"\n{2,}", "\n", text)         # blank-line runs
    return text.strip()


def repoint(path: Path, css: str, js: str, stamp: str) -> int:
    """Rewrite one page's stylesheet and script references. Returns how many it
    matched, which the caller checks.

    The leading slash is captured and put back rather than assumed away: 404.html
    references "/styles.min.css" because the host serves it at any depth, and a
    pattern anchored on "styles" skipped that file silently while the script
    still reported success.
    """
    s = path.read_text(encoding="utf-8")
    s, a = re.subn(r'href="(/?)styles(?:\.min)?\.css\?v=\d+"',
                   lambda m: f'href="{m.group(1)}{css}?v={stamp}"', s)
    s, b = re.subn(r'src="(/?)main(?:\.min)?\.js\?v=\d+"',
                   lambda m: f'src="{m.group(1)}{js}?v={stamp}"', s)
    path.write_text(s, encoding="utf-8")
    return a + b


def report(label: str, before: bytes, after: bytes) -> None:
    gz_b = len(gzip.compress(before))
    gz_a = len(gzip.compress(after))
    print(
        f"  {label:16} {len(before)/1024:7.1f} KB -> {len(after)/1024:7.1f} KB   "
        f"gzip {gz_b/1024:6.1f} -> {gz_a/1024:6.1f} KB  "
        f"({100 - 100*gz_a/gz_b:.0f}% off the wire)"
    )


def main() -> int:
    check = "--check" in sys.argv

    css_src = (ROOT / "styles.css").read_text(encoding="utf-8")
    js_src = (ROOT / "main.js").read_text(encoding="utf-8")
    css_min = minify_css(css_src)
    js_min = minify_js(js_src)

    print("minified:")
    report("styles.css", css_src.encode(), css_min.encode())
    report("main.js", js_src.encode(), js_min.encode())

    if check:
        print("\n--check: nothing written")
        return 0

    (ROOT / "styles.min.css").write_text(css_min, encoding="utf-8")
    (ROOT / "main.min.js").write_text(js_min, encoding="utf-8")

    stamp = str(int(time.time()))
    for name in PAGES:
        n = repoint(ROOT / name, "styles.min.css", "main.min.js", stamp)
        if n != 2:
            print(f"  WARNING: {name} matched {n}/2 references, expected 2")
    print(f"\nwrote styles.min.css + main.min.js; {len(PAGES)} pages repointed at ?v={stamp}")
    print("source files untouched. Run scripts/build-min.py --restore to go back to sources.")
    return 0


def restore() -> int:
    """Point the HTML back at the readable sources, for local debugging."""
    stamp = str(int(time.time()))
    for name in PAGES:
        n = repoint(ROOT / name, "styles.css", "main.js", stamp)
        if n != 2:
            print(f"  WARNING: {name} matched {n}/2 references, expected 2")
    print(f"{len(PAGES)} pages repointed at the unminified sources (?v={stamp})")
    return 0


if __name__ == "__main__":
    raise SystemExit(restore() if "--restore" in sys.argv else main())
