# CERO Studio | cerostudio.co

Marketing site. Plain HTML, CSS and vanilla JS, no build step, no framework,
no runtime dependencies. Code is ~150 KB; the card artwork adds ~9.3 MB (see below).

```
index.html          homepage: all markup and copy
portfolio.html      /portfolio, the full work grid
founder.html        /founder, NH Saiem's story
co-founder.html     /co-founder, Zihadul Islam's story
assets/videos/      compressed web videos + posters (see "Video pipeline")
styles.css          design tokens + every style
main.js             reveals, counters, marquee, nav, FAQ, parallax, cursor
scripts/            build-logo.py    : logo + favicons from assets/logo.png
                    build-banners.py : service banners from the full card art
assets/og-image.svg social share card (1200×630), see "Before launch"
_redirects          Cloudflare Pages redirects (.html → extensionless, 301)
_headers            Cloudflare Pages headers (security, caching)
robots.txt, sitemap.xml
```

### Logo assets

`assets/logo.png` is the **master, untouched**, the original artwork as supplied, navy
and gold on white. Use it for light-background contexts: documents, business cards,
invoices, light-mode UI. Nothing in this repo modifies it.

Everything else is derived from it by `scripts/build-logo.py`:

| File | What it is |
| --- | --- |
| `logo-navbar.png` | 476×133 horizontal lockup, icon left, CERO/STUDIO right, white margin trimmed, transparent ground. **Colours untouched.** Used in the navbar (40px) and footer (44px). |
| `favicon-16.png` / `favicon-32.png` | mark only, **true colours** (navy + gold) on a white rounded plate, lightly sharpened |
| `apple-touch-icon.png` | 180×180, same treatment, iOS home screen |
| `favicon-512.png` | 512×512, same treatment, PWA / install icon |

Nothing in this pipeline recolours the artwork any more, every derived asset
carries the logo's own navy and gold. The favicons' white plate is what lets the
navy half survive a dark browser tab strip; on a transparent ground it vanishes.

**Known trade-off:** because the lockup is unmodified, 20.2% of its ink sits
below 1.6:1 contrast against the `#0A1128` navbar. In practice "CERO" reads as
"ERO", and "STUDIO" plus the mark's lower arc are close to invisible. Two ways
out, neither of which changes the artwork's colours: put the lockup on a light
plate, or get a reversed/knockout lockup from whoever drew the original.

The site's gold tokens are derived from this file too, `--gold-2` / `--gold-3`
are the brand `#C9A227` / `#E8C766`, which a pixel sample of the arc corroborates
(`#A17433 → #E8B969` with antialiasing included).

Re-run `python3 scripts/build-logo.py` from the project root after replacing
`assets/logo.png` to regenerate all four.

Two things worth knowing:

- The original is a **stacked square lockup** with the artwork occupying only 8.5% of a
  1000×1000 canvas, and 27% of its ink is navy that disappears on `#0A1128`. That is why
  the navbar build is recomposed horizontally rather than used directly.
- The source is **raster**, and the icon within it is only ~135px across. The navbar
  lockup renders at roughly 3.3× its display size, so it is crisp on 2× and 3× screens,
  but `favicon-512.png` is an upscale and is correspondingly soft. If your designer has
  the vector original (AI/EPS/SVG), dropping in an SVG would sharpen the large icon and
  make the lockup resolution-independent.

## Run locally

Any static server works for looking at the pages, since there is nothing to compile:

```bash
python3 -m http.server 5173
# → http://localhost:5173
```

That server knows nothing about `_redirects` or `_headers`, so `/portfolio` 404s and
every cache header is wrong. To exercise the real routing, run the Cloudflare Pages
emulator instead:

```bash
npx wrangler pages dev . --port 8788
# → http://127.0.0.1:8788
```

It parses both files on startup and reports how many rules it read, which is the
quickest way to catch a malformed rule. Local state lands in `.wrangler/`, gitignored.

## Deploy

The site is on **Cloudflare Pages**, deployed from `main`, with no build step: connect
the repo, leave the build command empty and set the output directory to `/`. Previews
build at `cero-web.pages.dev`; `cerostudio.co` is the production domain.

`www` → apex is a Redirect Rule on the Cloudflare zone, not a file in this repo, because
`_redirects` cannot match on hostname. Routing and headers come from `_redirects` and
`_headers`; nothing else in the repo configures the host.

For a local server that honours those two files, see "Local preview" above.

## Before launch

A short list of things that need your real details:

1. **Email**, no longer shown anywhere on the site. `cerostudio40@gmail.com` survives only in
   the Organization JSON-LD on `index.html`, where it is machine-readable for search engines
   and never rendered. Enquiries are routed through Cal.com. WhatsApp is gone site-wide.
2. **Social links**, Instagram and LinkedIn URLs in the footer and JSON-LD are placeholders
   (`/cerostudio`). Point them at the real profiles.
3. **Founder photos**, done. The Founder / Co-founder section uses
   `assets/founder-ceo.jpg` and `assets/co-founder-coo.jpg`; the monogram placeholder is gone.
4. **Booking links**, done. There is exactly **one** booking pathway across the whole site:
   every CTA reads "Book a Free Strategy Call" and points at `/cerostudio/free-discovery-call`, opening
   in a new tab. The old `/cerostudio/free-automation-audit` link and every "Automation Audit"
   label are gone; do not reintroduce a second pathway. `initAnchors` only intercepts
   `href^="#"`, so absolute URLs are never hijacked by the smooth-scroll handler.
5. **OG image**, social platforms do not render SVG share cards. Convert once and update the
   two `og:image` / `twitter:image` tags to the `.png`:
   ```bash
   rsvg-convert -w 1200 -h 630 assets/og-image.svg -o assets/og-image.png
   # or: npx sharp-cli -i assets/og-image.svg -o assets/og-image.png resize 1200 630
   ```
6. **Founder video**, done. The "Meet the Founder" section on `index.html` plays
   `assets/videos/founder-intro.mp4` behind `assets/videos/founder-intro-poster.webp`. The stats
   bar that used to sit under the hero is gone, replaced by this CTA.
7. **Portfolio**, `portfolio.html` now runs nine real players and a single empty 16:9 slot still
   marked "In Production", which keeps the automation grid an even 2x2. That last slot becomes a
   real card by dropping a `<video>` into it and deleting the badge; the paste-in markup is in a
   comment at the top of the section.

## Notes on the build

**Animation** is Intersection Observer plus CSS transitions. Every revealed element carries
`data-reveal`; stagger inside a grid comes from an inline `--rd` delay (80–120 ms apart), so
reordering cards in the HTML never breaks the cascade. Scroll work, navbar state and the
parallax layers, runs through a single rAF-throttled listener.

**Motion preferences** are respected throughout: `prefers-reduced-motion` disables the parallax,
the cursor dot, the counters and every transition, and reveals resolve immediately.

**Fonts are self-hosted** from `assets/fonts`, declared in the `@font-face` block at the top
of `styles.css`. Both are the variable versions, so one file covers every weight the site uses
(400 to 600 body, 500 to 800 headings), latin subset only, `font-display:swap`. The two files
are preloaded from each document with `crossorigin`, which a font preload needs even
same-origin or the browser fetches the file twice.

This was the single biggest performance win on the site. The Google Fonts setup cost a DNS
lookup, a TLS handshake and a stylesheet round trip before the browser even learned which font
files it needed, then a second connection to fetch them, all in front of first paint. Removing
that chain took FCP from 2.9s to 1.2s.

**Accessibility**: skip link, visible focus rings, real `<button>` elements for the FAQ with
`aria-expanded` / `aria-controls`, a decorative cursor dot that is `aria-hidden` and pointer-inert,
keyboard-dismissable mobile menu (Escape), and a comparison table that reflows to labelled
stacked pairs on small screens.


## Site conventions

**Everything is navy, and the ground is painted once.** Sections no longer carry
backgrounds at all, see "Page background" below. `--navy-800` `#0A1128` is the
base; `--paper` / `--paper-2` / `--surface` survive only as card and component
fills, no longer as section grounds.

`--ink` / `--ink-2` / `--ink-3` are the text ramp on navy, they were a near-black
scale before the flip, so anything reading `var(--ink)` is now light. The class is
`.section--alt`, not `.section--light`; the old name lied once the palette inverted.

**Two deliberate light surfaces remain.** The service info blocks are white
(`#FBFBF9`) by design. The four problem cards are white end to end because the
artwork is, regenerating them on a navy ground is the only way to change that.

## Image-based sections

**Problem** is finished artwork through `.img-grid` / `.img-card`, 2-up on
desktop, single column at ≤880px. The copy is baked into the pixels, so the `alt`
text carries the wording; that is the only version a screen reader or crawler can
read.

**Services** is different. Each row is one card: a *banner* on top, a collage-only
crop of the full card artwork produced by `scripts/build-banners.py`, then an
info block on white (`#FBFBF9`) carrying the label, title, description and two
pills as real HTML. That white block is the one deliberately light surface on the
page, so its type uses a dark scale.

Note `.svc-row .svc-row__title` is deliberately double-classed: `.section--dark
h1,h2,h3` sets `#fff` at (0,2,0), which otherwise renders the title white on
white. That fixes three things the full
cards caused: the baked copy no longer shrinks with the card (it was landing near
9px at the 2-up size), the white text panel is gone from a navy page, and the
wording is selectable, translatable and indexable.

`build-banners.py` finds the collage/panel boundary by scanning **downward** for a
sustained run of blank white rows. Scanning up from the bottom fails: a row
through a wide headline averages dark enough to halt the scan inside the panel,
which is why cards 02 and 04 first cropped 15% lower than 01 and 03. All four now
cut identically at 1600×648 (2.47:1). The full-card originals stay on disk as the
masters, re-run the script after replacing any of them.

**Page weight is ~9.0 MB of PNG** (5.4 MB service banners + 3.6 MB problem) against
83 KB of code. Everything is `loading="lazy"`, so first paint is unaffected, but a
mobile visitor still pulls all of it on scroll. WebP would cut roughly 70–80% with
no visible change.

## Our Work

**All work now lives on `/portfolio`.** The homepage `#work` section is a teaser:
eyebrow, "See Our Work in Action", one line of copy and a gold button through to
the portfolio. Nothing else. It takes the standard `--sp-8` padding on both sides
like the sections around it, so a section that is three elements tall still reads
as a deliberate band rather than a collapsed one.

The two case-study players that used to sit here are gone, and so are their files
(see "Deleted video files" below).

`portfolio.html` carries two groups with **two different frame shapes**:

| Group | Ratio | Grid | Card cap |
| --- | --- | --- | --- |
| AI Automation Systems | 16:9, screen recordings | 2 up, 1 below 880px | none, fills the column |
| AI Video Production | 9:16, Reels/Shorts cuts | 3 up, 2 below 1024px, 1 below 620px | 320px, centred in its track |

`.work__slot` owns the box, the rounding and the gold hairline in both, so a player
dropped inside inherits all of it; only the `aspect-ratio` differs, set by
`.work-grid--vertical`. The 320px cap on vertical cards is the point of that
modifier: a 9:16 frame allowed to fill a half-page column towers over everything
near it and reads as upscaled, where a phone-shaped frame reads as premium.

`.work-grid--vertical` is excluded from the 880px single-column rule via
`:not()`, not by source order, so it can step 3 → 2 → 1 on its own breakpoints
without the shared rule collapsing it early.

Empty slots use `.work__slot--empty`: same box, hairline turned dashed, shadow
dropped, one "In Production" badge centred inside. They read as a frame waiting to
be filled rather than a player that failed to load. Turning one into a real card is
dropping a `<video>` in and deleting the badge; the paste-in markup is in a comment
at the top of the section.

### Deleted video files

`custom-ai-agent.mp4`, `ai-commercial-oreo.mp4` and both their posters were removed
when the homepage cards went. **The two masters in `assets/` are untouched**, so
re-running `scripts/build-videos.py` regenerates the web versions and the posters in
one command. The notes below describe that pipeline and still apply.

`scripts/build-videos.py` prepares the sources. Two things had to change before
these could ship:

**The index was at the end of the file.** Both originals were written with the
`moov` atom after `mdat`, which means a browser must download the entire file
before it can show one frame. On a 40 MB video that is not a slow start, it is a
player that appears broken. `-movflags +faststart` moves the index to the front.
Verified by reading the atom order back: `ftyp moov free mdat`.

**The bitrate was for delivery, not for the web.** 1920x1080 at 9 to 10 Mbps,
about 40 MB for 35 seconds. Re-encoded at CRF 24 the payload drops by roughly
three quarters with no visible difference at this size.

| Source | Ships as | Size |
| --- | --- | --- |
| `custom agent.mp4` | `custom-ai-agent.mp4` | 39.7 MB to 8.4 MB |
| `AI commercial for oreo.mp4` | `ai-commercial-oreo.mp4` | 41.8 MB to 11.2 MB |

Posters are frame one of each source, so a card shows the opening frame rather
than a black box. `preload="metadata"` is deliberate: without it every visitor
pays for both files on load whether or not they press play.

**The two originals are still in `assets/`, 81 MB between them.** Nothing on the
site links to them; they are the masters `scripts/build-videos.py` reads, and now
the only way back to the deleted web versions, so do not delete them casually. They
will still be uploaded with everything else if the folder is deployed as is, so move
them out of `assets/` before shipping rather than removing them.

## Cursor dot

`#cursorDot` is a 9px semi-transparent gold dot that eases toward the pointer
each frame (`EASE = 0.18` in `initCursor`, higher = tighter follow). It is an
extra layer, the native cursor is never hidden, grows to 20px over anything
clickable, and never initialises on touch devices or under
`prefers-reduced-motion`. The rAF loop parks itself once the dot catches up
rather than running continuously.


## Hero

Text only, one centred column: pill badge, headline, a single subtext line, two
buttons, the reassurance row, then the scroll cue. There is no side visual, the
rotating card stack that used to sit there is gone, along with its CSS and its
`initStack()` in `main.js`.

It carries the "What We Build" copy that previously headed the Services section.
Services now leads with a centred `Our Services for Businesses` header
(`.sec-head--center`).

## Page background

There is exactly one painted ground on the site: `.page-bg`, a `position:fixed`
layer at `z-index:-1` holding the base gradient, two large radial glows and the
grain. Because it is fixed, nothing scrolls out from under a section and no seam
can appear between them.

Every section is transparent. Do **not** reintroduce `background` on a section,
`.grain` (removed), or per-section `.section__glow` / `.hero__glow` / `.cta__glow`
(all removed), each of those is what produced the visible horizontal bands.
Section-edge hairlines on the stats bar, marquee and CTA were removed for the
same reason. Verified by sampling the left gutter down the page: it drifts
`rgb(11,19,43) → rgb(10,17,40) → rgb(31,32,37)` with no step above ~1.3/255.

`.section--dark` and `.section--alt` now only carry text colours, not grounds.

## Process, vertical timeline

`.steps` is a plain ordered list: a 44px numbered marker, then title and copy,
five rows down the page under the section heading. The list is `max-width:660px`
with `margin-inline:auto` so it centres on the same axis as the centred heading
(measured: both mid-points land on the viewport centre at 1440px).

The connecting rule is `.steps__item::before`, drawn **per item**, from below
its own marker down into the gap, rather than as one line behind the whole list.
That way it cannot overshoot past the last marker; `:last-child` just sets
`content:none`. It sits at `left:22px`, which is the marker's centre, and the
marker is `z-index:1` above it so the rule appears to start at the circle's edge.

This replaced a sticky/stacking-card treatment (`.stack-track` / `.stack-pin`,
plus `initStepStack()` in `main.js`) that pinned the section and animated cards
onto a pile as you scrolled. All of it is gone, CSS, markup and JS. If anything
here ever regains a `position:sticky`, note that an ancestor with
`overflow:hidden` silently kills it: `.section` must stay overflow-visible and
`body` uses `overflow-x:clip`, not `hidden`, for that reason.

## /founder and /co-founder, the story pages

`founder.html` and `co-founder.html` are the site's only documents besides the
homepage. They are the same page in two instances: identical structure, classes
and CSS, differing only in copy, photographs and schema. It reuses `styles.css` and
`main.js` wholesale; every init in `main.js` is guarded against its elements
being absent, so the homepage-only ones (counters, marquee, FAQ) simply no-op.

Two things differ from `index.html` and must stay that way:

- **Every in-page anchor is prefixed `index.html#…`**, nav links, footer links
  and both logos. A bare `#services` here scrolls to nothing.
- **No splash.** The overlay is a first-load treatment for the homepage; replaying
  it on an internal navigation would read as a page reload. The gate script and
  the markup are both omitted.

The page has no intro quote card. It opens on the `<h1>` lede, and the founder's
quote lives only on the homepage, so the two cannot drift apart.

The URL is `/founder`, not `/founder.html`: Cloudflare Pages strips `.html`
automatically, and our `_redirects` rules override its default 308 with a 301 to
the extensionless form. Links in the markup point at `founder.html` so the page
also works from the filesystem and the local preview server; the host redirects
the `.html` form to the clean one.

**Layout.** `.story` is a vertical timeline with a spine down the centre.
Chapters carrying a photograph (`.story__ch--media`) are two columns and
alternate sides, `.story__ch--flip` swaps the grid columns, and only the columns
swap: the copy stays left-aligned either way, because right-aligned body text is
markedly harder to read. Chapters without a photograph (`.story__ch--solo`) sit
centred on the spine at a narrower measure, so no row is ever left half empty.
Below 880px the spine moves to the left edge and every chapter stacks
photo-over-text. Verified at 1440/820/420px: nodes centred on the spine, images
alternating L/R/L/R, no horizontal scroll at any width.

The homepage Founder's Message links here from both the name and the portrait
(`.msg__link` / `.msg__photo-link`). Those two anchors are the only change to
that section, its grid, copy and photo are untouched.

### Story images

`scripts/build-story-images.py` derives the four story photographs from the
originals in `assets/`. It exists because the originals arrive with **spaces in
their filenames** (which would need percent-encoding in every href) and at full
camera size, one is a 1.8 MB PNG of a photograph, the wrong container entirely.

| Source | Derivative | Result |
| --- | --- | --- |
| `school days.jpeg` | `school-days.jpeg` | copied as-is (already small) |
| `after school when move dhaka.jpeg` | `after-school-when-move-dhaka.jpeg` | copied as-is |
| `travel time.webp` | `travel-time.webp` | 582 KB → 74 KB |
| `when start cero.png` | `when-start-cero.jpg` | 1782 KB → 85 KB |

Note the script copies bytes rather than re-encoding when a source is already
under 1000px and already in the target container, re-encoding a finished JPEG
at q82 came out *larger* than the original while also losing a generation.

**`when start cero.png` is byte-identical to `founder & CEO`**, the same
photograph as the homepage portrait, which therefore appears twice on this page.
Drop a different photo in and re-run the script to fix it.

## Scroll position across the /founder round trip

`initScrollMemory()` in `main.js`. Clicking the founder card is a real
navigation, so coming back is a fresh document load. Chrome usually restores the
old position itself, but it decides where to land before the lazy images below
the fold and the async webfonts have settled, and on a page this tall it can give
up and leave you at the top.

The fix records `scrollY` in `sessionStorage` on `pagehide`, `beforeunload` and
`visibilitychange`, then puts it back only when all three of these hold: the load
is a `back_forward` navigation entry, the browser has not already scrolled
somewhere itself, and a saved value exists. It retries across up to 12 frames,
because the target is only reachable once the images below the fold have taken up
their space. A bfcache restore needs none of this and is left alone.

The splash gate in `index.html` skips the animation on `back_forward` loads for
the same reason: a full-screen animation on a Back press reads as a reload, and
it covers the moment the position is being restored.

Verified over CDP with a real round trip: scroll to 9344px, click the card,
land on /founder.html, press Back, arrive at 9344px. Zero drift, splash skipped.

## No em dashes

The site contains none, by request. Two things to check, not one: a grep for the
literal character, and a grep for its HTML entity form (ampersand, `mdash`,
semicolon). Three em dashes survived the first sweep because they were written as
the entity in the process section, and a literal-character grep does not match
those.

## Back links that do not lose your place

Both story pages carry two "Back to CERO Studio" routes, the text link at the top
and the ghost button at the end, and both are marked `data-back`.

`initBackLinks()` in `main.js` intercepts them and calls `history.back()` instead
of following the href. Following the href would be a *forward* navigation: a
brand new history entry for the homepage, which lands at the top and strands the
entry the reader came from behind it. Going back through history returns them to
the exact spot they left.

It only intercepts when `document.referrer` is same-origin and a different path,
so a cold landing (shared link, search result) still follows the href and reaches
the homepage normally. Modified clicks are left alone so open-in-new-tab works.

Verified over CDP, both directions:

```
homepage @9946 -> click co-founder card -> /co-founder -> back link -> homepage @9946   (0px)
homepage @9318 -> click founder card    -> /founder    -> back link -> homepage @9318   (0px)
cold load /co-founder -> back link -> /index.html                                        (href fallback)
```

## Story image ratios

`.story__fig img` crops to 4:5. `.story__fig--wide img` relaxes that to 4:3 for
landscape sources: `zihadul-roots.jpg` is a 4:3 group photo, and forcing it into
the portrait crop cuts roughly a fifth off each side, which is enough to clip a
person out of the shot.

## A note on the co-founder image sources

The three photographs were identified by screenshots of file-manager icons, so
the names in the request describe the screenshots, not the files. The actual
sources already sat in `assets/`:

| Screenshot showed | Real file | Derivative |
| --- | --- | --- |
| outdoor / green | `with cero founder in winter.jpg` | `zihadul-roots.jpg` |
| after ssc | `after ssc.jpg` | `zihadul-ssc.jpg` |
| dark / studio | `when start ceor.png` | `zihadul-cero.jpg` |

Note `when start ceor.png` and `when start cero.png` differ by one transposed
letter and are **different photographs**: "ceor" belongs to the co-founder page,
"cero" to the founder page. Confirmed by checksum, not by eye.

## Text-only chapters carry a panel

`.story__ch--solo .story__body` gets the homepage `.msg` card treatment: a faint
gradient surface, a gold hairline and real padding. Without it a short paragraph
floats alone in a very tall row and the chapter reads as unfinished next to one
carrying a photograph. With it, every chapter is one solid block on one side of
the spine, whether that block is a picture or a piece of writing.

It cannot be made full-width instead, which is the obvious first instinct. The
spine runs down the centre, so a block spanning both halves sits underneath the
line, which is the exact bug that was reported and fixed earlier. Widening
happens *inside* the half: the panel fills its column and `.story__text` drops
its 56ch cap to use the space.

Measured at 1440px after the change, chapter heights run 324px to 622px on both
pages, a 1.9x spread. Before the panels and the two added photographs the short
chapters were roughly a quarter the height of the tall ones.

### Which photograph sits where

| /founder | | /co-founder | |
| --- | --- | --- | --- |
| Where it starts | school-days | Where it starts | founders-together |
| A plan that did not hold | after-school-when-move-dhaka | School after school | zihadul-ssc |
| Genuinely lost | travel-time | The quiet years | zihadul-outdoor |
| Buying the laptop | founders-together | Building CERO | zihadul-cero |
| Building it for real | when-start-cero | | |

On /founder, "A second real shot" (Aug 2025) sits **above** "The thing that
stuck" (Finding AI): school came first, AI followed in November. Both are
text-only.

Chapter order and left/right placement are coupled. `story__ch--flip` is
positional (even chapters flip), so reordering chapters means recomputing the
flip class on every one of them, not just the pair that moved. The safe edit is
to parse the whole `<ol>` into records, reorder, and re-emit.

`founders-together.jpg` is deliberately on both pages. It is a different frame
from `with cero founder in winter.jpg` (same day, same spot), which is why
`zihadul-roots.jpg` still exists in `assets/` but is no longer referenced by
either page.

## The story hero

The heading and nothing else, centred on the navy ground. Earlier versions put a
scrolling photo marquee and then a static fanned photo arc above it; both are
gone, markup and CSS. `.story__lede` no longer carries grid placement, a z-index
or a text shadow, because those existed only to lift it clear of photographs
behind it.

**The section's top padding has a hard floor of 104px.** It has two jobs: clear
the fixed navbar, and clear the back link, which is absolutely positioned inside
that padding and ends 87px down. A clamp on a spacing token cannot do the second
job, because the token shrinks with the viewport while the back link does not.
Between 620 and 880px the padding fell to 84px and the heading landed on top of
the link. `max(104px, ...)` states the floor outright.

Measured at 1440, 900, 700 and 420 on both pages: back link 68..87, heading
starts at 104, a steady 17px clear, no horizontal overflow.

A note on measuring this page: `getBoundingClientRect()` is unreliable here,
because `data-reveal` elements are mid-transform while the reveal runs and the
numbers swing by about 30px between runs. Use `offsetTop` and `offsetHeight`,
which are layout positions and ignore the transform.

## Cursor dot

`#cursorDot` is a 9px semi-transparent gold dot that eases toward the pointer
each frame (`EASE = 0.18` in `initCursor`, higher = tighter follow). It is an
extra layer, the native cursor is never hidden, grows to 20px over anything
clickable, and never initialises on touch devices or under
`prefers-reduced-motion`. The rAF loop parks itself once the dot catches up
rather than running continuously.


## Hero

Text only, one centred column: pill badge, headline, a single subtext line, two
buttons, the reassurance row, then the scroll cue. There is no side visual, the
rotating card stack that used to sit there is gone, along with its CSS and its
`initStack()` in `main.js`.

It carries the "What We Build" copy that previously headed the Services section.
Services now leads with a centred `Our Services for Businesses` header
(`.sec-head--center`).

## Page background

There is exactly one painted ground on the site: `.page-bg`, a `position:fixed`
layer at `z-index:-1` holding the base gradient, two large radial glows and the
grain. Because it is fixed, nothing scrolls out from under a section and no seam
can appear between them.

Every section is transparent. Do **not** reintroduce `background` on a section,
`.grain` (removed), or per-section `.section__glow` / `.hero__glow` / `.cta__glow`
(all removed), each of those is what produced the visible horizontal bands.
Section-edge hairlines on the stats bar, marquee and CTA were removed for the
same reason. Verified by sampling the left gutter down the page: it drifts
`rgb(11,19,43) → rgb(10,17,40) → rgb(31,32,37)` with no step above ~1.3/255.

`.section--dark` and `.section--alt` now only carry text colours, not grounds.

## Process, vertical timeline

`.steps` is a plain ordered list: a 44px numbered marker, then title and copy,
five rows down the page under the section heading. The list is `max-width:660px`
with `margin-inline:auto` so it centres on the same axis as the centred heading
(measured: both mid-points land on the viewport centre at 1440px).

The connecting rule is `.steps__item::before`, drawn **per item**, from below
its own marker down into the gap, rather than as one line behind the whole list.
That way it cannot overshoot past the last marker; `:last-child` just sets
`content:none`. It sits at `left:22px`, which is the marker's centre, and the
marker is `z-index:1` above it so the rule appears to start at the circle's edge.

This replaced a sticky/stacking-card treatment (`.stack-track` / `.stack-pin`,
plus `initStepStack()` in `main.js`) that pinned the section and animated cards
onto a pile as you scrolled. All of it is gone, CSS, markup and JS. If anything
here ever regains a `position:sticky`, note that an ancestor with
`overflow:hidden` silently kills it: `.section` must stay overflow-visible and
`body` uses `overflow-x:clip`, not `hidden`, for that reason.

## /founder and /co-founder, the story pages

`founder.html` and `co-founder.html` are the site's only documents besides the
homepage. They are the same page in two instances: identical structure, classes
and CSS, differing only in copy, photographs and schema. It reuses `styles.css` and
`main.js` wholesale; every init in `main.js` is guarded against its elements
being absent, so the homepage-only ones (counters, marquee, FAQ) simply no-op.

Two things differ from `index.html` and must stay that way:

- **Every in-page anchor is prefixed `index.html#…`**, nav links, footer links
  and both logos. A bare `#services` here scrolls to nothing.
- **No splash.** The overlay is a first-load treatment for the homepage; replaying
  it on an internal navigation would read as a page reload. The gate script and
  the markup are both omitted.

The page has no intro quote card. It opens on the `<h1>` lede, and the founder's
quote lives only on the homepage, so the two cannot drift apart.

The URL is `/founder`, not `/founder.html`: Cloudflare Pages strips `.html`
automatically, and our `_redirects` rules override its default 308 with a 301 to
the extensionless form. Links in the markup point at `founder.html` so the page
also works from the filesystem and the local preview server; the host redirects
the `.html` form to the clean one.

**Layout.** `.story` is a vertical timeline with a spine down the centre.
Chapters carrying a photograph (`.story__ch--media`) are two columns and
alternate sides, `.story__ch--flip` swaps the grid columns, and only the columns
swap: the copy stays left-aligned either way, because right-aligned body text is
markedly harder to read. Chapters without a photograph (`.story__ch--solo`) sit
centred on the spine at a narrower measure, so no row is ever left half empty.
Below 880px the spine moves to the left edge and every chapter stacks
photo-over-text. Verified at 1440/820/420px: nodes centred on the spine, images
alternating L/R/L/R, no horizontal scroll at any width.

The homepage Founder's Message links here from both the name and the portrait
(`.msg__link` / `.msg__photo-link`). Those two anchors are the only change to
that section, its grid, copy and photo are untouched.

### Story images

`scripts/build-story-images.py` derives the four story photographs from the
originals in `assets/`. It exists because the originals arrive with **spaces in
their filenames** (which would need percent-encoding in every href) and at full
camera size, one is a 1.8 MB PNG of a photograph, the wrong container entirely.

| Source | Derivative | Result |
| --- | --- | --- |
| `school days.jpeg` | `school-days.jpeg` | copied as-is (already small) |
| `after school when move dhaka.jpeg` | `after-school-when-move-dhaka.jpeg` | copied as-is |
| `travel time.webp` | `travel-time.webp` | 582 KB → 74 KB |
| `when start cero.png` | `when-start-cero.jpg` | 1782 KB → 85 KB |

Note the script copies bytes rather than re-encoding when a source is already
under 1000px and already in the target container, re-encoding a finished JPEG
at q82 came out *larger* than the original while also losing a generation.

**`when start cero.png` is byte-identical to `founder & CEO`**, the same
photograph as the homepage portrait, which therefore appears twice on this page.
Drop a different photo in and re-run the script to fix it.

## Scroll position across the /founder round trip

`initScrollMemory()` in `main.js`. Clicking the founder card is a real
navigation, so coming back is a fresh document load. Chrome usually restores the
old position itself, but it decides where to land before the lazy images below
the fold and the async webfonts have settled, and on a page this tall it can give
up and leave you at the top.

The fix records `scrollY` in `sessionStorage` on `pagehide`, `beforeunload` and
`visibilitychange`, then puts it back only when all three of these hold: the load
is a `back_forward` navigation entry, the browser has not already scrolled
somewhere itself, and a saved value exists. It retries across up to 12 frames,
because the target is only reachable once the images below the fold have taken up
their space. A bfcache restore needs none of this and is left alone.

The splash gate in `index.html` skips the animation on `back_forward` loads for
the same reason: a full-screen animation on a Back press reads as a reload, and
it covers the moment the position is being restored.

Verified over CDP with a real round trip: scroll to 9344px, click the card,
land on /founder.html, press Back, arrive at 9344px. Zero drift, splash skipped.

## No em dashes

The site contains none, by request. Two things to check, not one: a grep for the
literal character, and a grep for its HTML entity form (ampersand, `mdash`,
semicolon). Three em dashes survived the first sweep because they were written as
the entity in the process section, and a literal-character grep does not match
those.

## Back links that do not lose your place

Both story pages carry two "Back to CERO Studio" routes, the text link at the top
and the ghost button at the end, and both are marked `data-back`.

`initBackLinks()` in `main.js` intercepts them and calls `history.back()` instead
of following the href. Following the href would be a *forward* navigation: a
brand new history entry for the homepage, which lands at the top and strands the
entry the reader came from behind it. Going back through history returns them to
the exact spot they left.

It only intercepts when `document.referrer` is same-origin and a different path,
so a cold landing (shared link, search result) still follows the href and reaches
the homepage normally. Modified clicks are left alone so open-in-new-tab works.

Verified over CDP, both directions:

```
homepage @9946 -> click co-founder card -> /co-founder -> back link -> homepage @9946   (0px)
homepage @9318 -> click founder card    -> /founder    -> back link -> homepage @9318   (0px)
cold load /co-founder -> back link -> /index.html                                        (href fallback)
```

## Story image ratios

`.story__fig img` crops to 4:5. `.story__fig--wide img` relaxes that to 4:3 for
landscape sources: `zihadul-roots.jpg` is a 4:3 group photo, and forcing it into
the portrait crop cuts roughly a fifth off each side, which is enough to clip a
person out of the shot.

## A note on the co-founder image sources

The three photographs were identified by screenshots of file-manager icons, so
the names in the request describe the screenshots, not the files. The actual
sources already sat in `assets/`:

| Screenshot showed | Real file | Derivative |
| --- | --- | --- |
| outdoor / green | `with cero founder in winter.jpg` | `zihadul-roots.jpg` |
| after ssc | `after ssc.jpg` | `zihadul-ssc.jpg` |
| dark / studio | `when start ceor.png` | `zihadul-cero.jpg` |

Note `when start ceor.png` and `when start cero.png` differ by one transposed
letter and are **different photographs**: "ceor" belongs to the co-founder page,
"cero" to the founder page. Confirmed by checksum, not by eye.

## Text-only chapters carry a panel

`.story__ch--solo .story__body` gets the homepage `.msg` card treatment: a faint
gradient surface, a gold hairline and real padding. Without it a short paragraph
floats alone in a very tall row and the chapter reads as unfinished next to one
carrying a photograph. With it, every chapter is one solid block on one side of
the spine, whether that block is a picture or a piece of writing.

It cannot be made full-width instead, which is the obvious first instinct. The
spine runs down the centre, so a block spanning both halves sits underneath the
line, which is the exact bug that was reported and fixed earlier. Widening
happens *inside* the half: the panel fills its column and `.story__text` drops
its 56ch cap to use the space.

Measured at 1440px after the change, chapter heights run 324px to 622px on both
pages, a 1.9x spread. Before the panels and the two added photographs the short
chapters were roughly a quarter the height of the tall ones.

### Which photograph sits where

| /founder | | /co-founder | |
| --- | --- | --- | --- |
| Where it starts | school-days | Where it starts | founders-together |
| A plan that did not hold | after-school-when-move-dhaka | School after school | zihadul-ssc |
| Genuinely lost | travel-time | The quiet years | zihadul-outdoor |
| Buying the laptop | founders-together | Building CERO | zihadul-cero |
| Building it for real | when-start-cero | | |

On /founder, "A second real shot" (Aug 2025) sits **above** "The thing that
stuck" (Finding AI): school came first, AI followed in November. Both are
text-only.

Chapter order and left/right placement are coupled. `story__ch--flip` is
positional (even chapters flip), so reordering chapters means recomputing the
flip class on every one of them, not just the pair that moved. The safe edit is
to parse the whole `<ol>` into records, reorder, and re-emit.

`founders-together.jpg` is deliberately on both pages. It is a different frame
from `with cero founder in winter.jpg` (same day, same spot), which is why
`zihadul-roots.jpg` still exists in `assets/` but is no longer referenced by
either page.

## The story hero: a static photo arc

The timeline's photographs fanned into a fixed arc with the heading laid on top.
Nothing moves; an earlier scrolling marquee was replaced by this.

Each card carries one inline number, `--a`, its signed distance off centre in
the range -1 to 1 (`--aa` is the same value unsigned, `--dyf` its eased drop).
Size, tilt, drop and opacity are all derived from it **in CSS**:

```
--k:   calc(1 - var(--falloff) * var(--aa) * var(--aa))
--rot: calc(var(--a) * var(--rotmax))
--dy:  calc(var(--dyf) * var(--dymax))
```

That is the point of the indirection: a breakpoint flattens the whole curve by
changing three variables, instead of every card needing new inline values. Left
to shrink proportionally, the outermost cards fell to about 75px on a phone, too
small to read as photographs; the mobile rules use a gentler falloff so they stay
near 105px while the arc still curves.

The drop is `margin-top`, not `translate`, so the flex container's own height
grows to contain it. With translate the outer cards hang out of a box sized only
by the centre card.

Arc and heading share one grid cell, so the box is as tall as whichever is
taller and the text lands vertically centred over the photographs (measured:
`h1 offsetTop 30` in a 244px hero with a 184px heading, which is exactly
centred). The heading is `z-index:6` with a text shadow; `.arc-hero::after` is a
radial well of darkness at `z-index:5`, above the cards and below the text, so
the words never fight a bright patch. Cards themselves sit at about 0.7 opacity
with `brightness(.66)`, and clear to full on hover.

Desktop: centre 196px, outermost 114px, tilts 0 to 19 degrees. Below 560px a
five-card arc drops its outermost pair, leaving three still centred on the same
axis; a four-card arc keeps all four, since hiding a pair leaves too little to
curve.

There are no subtitles on either page. The heading over the arc is the whole hero.

## Cursor dot

`#cursorDot` is a 9px semi-transparent gold dot that eases toward the pointer
each frame (`EASE = 0.18` in `initCursor`, higher = tighter follow). It is an
extra layer, the native cursor is never hidden, grows to 20px over anything
clickable, and never initialises on touch devices or under
`prefers-reduced-motion`. The rAF loop parks itself once the dot catches up
rather than running continuously.


## Hero

Text only, one centred column: pill badge, headline, a single subtext line, two
buttons, the reassurance row, then the scroll cue. There is no side visual, the
rotating card stack that used to sit there is gone, along with its CSS and its
`initStack()` in `main.js`.

It carries the "What We Build" copy that previously headed the Services section.
Services now leads with a centred `Our Services for Businesses` header
(`.sec-head--center`).

## Page background

There is exactly one painted ground on the site: `.page-bg`, a `position:fixed`
layer at `z-index:-1` holding the base gradient, two large radial glows and the
grain. Because it is fixed, nothing scrolls out from under a section and no seam
can appear between them.

Every section is transparent. Do **not** reintroduce `background` on a section,
`.grain` (removed), or per-section `.section__glow` / `.hero__glow` / `.cta__glow`
(all removed), each of those is what produced the visible horizontal bands.
Section-edge hairlines on the stats bar, marquee and CTA were removed for the
same reason. Verified by sampling the left gutter down the page: it drifts
`rgb(11,19,43) → rgb(10,17,40) → rgb(31,32,37)` with no step above ~1.3/255.

`.section--dark` and `.section--alt` now only carry text colours, not grounds.

## Process, vertical timeline

`.steps` is a plain ordered list: a 44px numbered marker, then title and copy,
five rows down the page under the section heading. The list is `max-width:660px`
with `margin-inline:auto` so it centres on the same axis as the centred heading
(measured: both mid-points land on the viewport centre at 1440px).

The connecting rule is `.steps__item::before`, drawn **per item**, from below
its own marker down into the gap, rather than as one line behind the whole list.
That way it cannot overshoot past the last marker; `:last-child` just sets
`content:none`. It sits at `left:22px`, which is the marker's centre, and the
marker is `z-index:1` above it so the rule appears to start at the circle's edge.

This replaced a sticky/stacking-card treatment (`.stack-track` / `.stack-pin`,
plus `initStepStack()` in `main.js`) that pinned the section and animated cards
onto a pile as you scrolled. All of it is gone, CSS, markup and JS. If anything
here ever regains a `position:sticky`, note that an ancestor with
`overflow:hidden` silently kills it: `.section` must stay overflow-visible and
`body` uses `overflow-x:clip`, not `hidden`, for that reason.

## /founder and /co-founder, the story pages

`founder.html` and `co-founder.html` are the site's only documents besides the
homepage. They are the same page in two instances: identical structure, classes
and CSS, differing only in copy, photographs and schema. It reuses `styles.css` and
`main.js` wholesale; every init in `main.js` is guarded against its elements
being absent, so the homepage-only ones (counters, marquee, FAQ) simply no-op.

Two things differ from `index.html` and must stay that way:

- **Every in-page anchor is prefixed `index.html#…`**, nav links, footer links
  and both logos. A bare `#services` here scrolls to nothing.
- **No splash.** The overlay is a first-load treatment for the homepage; replaying
  it on an internal navigation would read as a page reload. The gate script and
  the markup are both omitted.

The page has no intro quote card. It opens on the `<h1>` lede, and the founder's
quote lives only on the homepage, so the two cannot drift apart.

The URL is `/founder`, not `/founder.html`: Cloudflare Pages strips `.html`
automatically, and our `_redirects` rules override its default 308 with a 301 to
the extensionless form. Links in the markup point at `founder.html` so the page
also works from the filesystem and the local preview server; the host redirects
the `.html` form to the clean one.

**Layout.** `.story` is a vertical timeline with a spine down the centre.
Chapters carrying a photograph (`.story__ch--media`) are two columns and
alternate sides, `.story__ch--flip` swaps the grid columns, and only the columns
swap: the copy stays left-aligned either way, because right-aligned body text is
markedly harder to read. Chapters without a photograph (`.story__ch--solo`) sit
centred on the spine at a narrower measure, so no row is ever left half empty.
Below 880px the spine moves to the left edge and every chapter stacks
photo-over-text. Verified at 1440/820/420px: nodes centred on the spine, images
alternating L/R/L/R, no horizontal scroll at any width.

The homepage Founder's Message links here from both the name and the portrait
(`.msg__link` / `.msg__photo-link`). Those two anchors are the only change to
that section, its grid, copy and photo are untouched.

### Story images

`scripts/build-story-images.py` derives the four story photographs from the
originals in `assets/`. It exists because the originals arrive with **spaces in
their filenames** (which would need percent-encoding in every href) and at full
camera size, one is a 1.8 MB PNG of a photograph, the wrong container entirely.

| Source | Derivative | Result |
| --- | --- | --- |
| `school days.jpeg` | `school-days.jpeg` | copied as-is (already small) |
| `after school when move dhaka.jpeg` | `after-school-when-move-dhaka.jpeg` | copied as-is |
| `travel time.webp` | `travel-time.webp` | 582 KB → 74 KB |
| `when start cero.png` | `when-start-cero.jpg` | 1782 KB → 85 KB |

Note the script copies bytes rather than re-encoding when a source is already
under 1000px and already in the target container, re-encoding a finished JPEG
at q82 came out *larger* than the original while also losing a generation.

**`when start cero.png` is byte-identical to `founder & CEO`**, the same
photograph as the homepage portrait, which therefore appears twice on this page.
Drop a different photo in and re-run the script to fix it.

## Scroll position across the /founder round trip

`initScrollMemory()` in `main.js`. Clicking the founder card is a real
navigation, so coming back is a fresh document load. Chrome usually restores the
old position itself, but it decides where to land before the lazy images below
the fold and the async webfonts have settled, and on a page this tall it can give
up and leave you at the top.

The fix records `scrollY` in `sessionStorage` on `pagehide`, `beforeunload` and
`visibilitychange`, then puts it back only when all three of these hold: the load
is a `back_forward` navigation entry, the browser has not already scrolled
somewhere itself, and a saved value exists. It retries across up to 12 frames,
because the target is only reachable once the images below the fold have taken up
their space. A bfcache restore needs none of this and is left alone.

The splash gate in `index.html` skips the animation on `back_forward` loads for
the same reason: a full-screen animation on a Back press reads as a reload, and
it covers the moment the position is being restored.

Verified over CDP with a real round trip: scroll to 9344px, click the card,
land on /founder.html, press Back, arrive at 9344px. Zero drift, splash skipped.

## No em dashes

The site contains none, by request. Two things to check, not one: a grep for the
literal character, and a grep for its HTML entity form (ampersand, `mdash`,
semicolon). Three em dashes survived the first sweep because they were written as
the entity in the process section, and a literal-character grep does not match
those.

## Back links that do not lose your place

Both story pages carry two "Back to CERO Studio" routes, the text link at the top
and the ghost button at the end, and both are marked `data-back`.

`initBackLinks()` in `main.js` intercepts them and calls `history.back()` instead
of following the href. Following the href would be a *forward* navigation: a
brand new history entry for the homepage, which lands at the top and strands the
entry the reader came from behind it. Going back through history returns them to
the exact spot they left.

It only intercepts when `document.referrer` is same-origin and a different path,
so a cold landing (shared link, search result) still follows the href and reaches
the homepage normally. Modified clicks are left alone so open-in-new-tab works.

Verified over CDP, both directions:

```
homepage @9946 -> click co-founder card -> /co-founder -> back link -> homepage @9946   (0px)
homepage @9318 -> click founder card    -> /founder    -> back link -> homepage @9318   (0px)
cold load /co-founder -> back link -> /index.html                                        (href fallback)
```

## Story image ratios

`.story__fig img` crops to 4:5. `.story__fig--wide img` relaxes that to 4:3 for
landscape sources: `zihadul-roots.jpg` is a 4:3 group photo, and forcing it into
the portrait crop cuts roughly a fifth off each side, which is enough to clip a
person out of the shot.

## A note on the co-founder image sources

The three photographs were identified by screenshots of file-manager icons, so
the names in the request describe the screenshots, not the files. The actual
sources already sat in `assets/`:

| Screenshot showed | Real file | Derivative |
| --- | --- | --- |
| outdoor / green | `with cero founder in winter.jpg` | `zihadul-roots.jpg` |
| after ssc | `after ssc.jpg` | `zihadul-ssc.jpg` |
| dark / studio | `when start ceor.png` | `zihadul-cero.jpg` |

Note `when start ceor.png` and `when start cero.png` differ by one transposed
letter and are **different photographs**: "ceor" belongs to the co-founder page,
"cero" to the founder page. Confirmed by checksum, not by eye.

## Text-only chapters carry a panel

`.story__ch--solo .story__body` gets the homepage `.msg` card treatment: a faint
gradient surface, a gold hairline and real padding. Without it a short paragraph
floats alone in a very tall row and the chapter reads as unfinished next to one
carrying a photograph. With it, every chapter is one solid block on one side of
the spine, whether that block is a picture or a piece of writing.

It cannot be made full-width instead, which is the obvious first instinct. The
spine runs down the centre, so a block spanning both halves sits underneath the
line, which is the exact bug that was reported and fixed earlier. Widening
happens *inside* the half: the panel fills its column and `.story__text` drops
its 56ch cap to use the space.

Measured at 1440px after the change, chapter heights run 324px to 622px on both
pages, a 1.9x spread. Before the panels and the two added photographs the short
chapters were roughly a quarter the height of the tall ones.

### Which photograph sits where

| /founder | | /co-founder | |
| --- | --- | --- | --- |
| Where it starts | school-days | Where it starts | founders-together |
| A plan that did not hold | after-school-when-move-dhaka | School after school | zihadul-ssc |
| Genuinely lost | travel-time | The quiet years | zihadul-outdoor |
| Buying the laptop | founders-together | Building CERO | zihadul-cero |
| Building it for real | when-start-cero | | |

On /founder, "A second real shot" (Aug 2025) sits **above** "The thing that
stuck" (Finding AI): school came first, AI followed in November. Both are
text-only.

Chapter order and left/right placement are coupled. `story__ch--flip` is
positional (even chapters flip), so reordering chapters means recomputing the
flip class on every one of them, not just the pair that moved. The safe edit is
to parse the whole `<ol>` into records, reorder, and re-emit.

`founders-together.jpg` is deliberately on both pages. It is a different frame
from `with cero founder in winter.jpg` (same day, same spot), which is why
`zihadul-roots.jpg` still exists in `assets/` but is no longer referenced by
either page.

## The story hero: a photo marquee

Above each heading, `.pmarq` ticks that page's own timeline photographs slowly
right to left. Pure CSS: the track holds the card set twice and slides exactly
one set's width, so the instant it wraps, copy two is sitting precisely where
copy one started.

**The spacing is `margin-right` on each card, never `gap` on the track.** With
gap, a track of 2N cards is `2N*W + (2N-1)*G` wide, so translating -50% lands
half a gap short and the seam shows as a stutter once per cycle. A trailing
margin makes every card occupy exactly `W+G`, and half of `2N*(W+G)` is one whole
set. Verified: half-track and one-set advance agree to 0.00px on both pages.

Durations are set inline per page (`--dur`), chosen so both pages travel at the
same 29 px/s regardless of card count. Hovering the marquee pauses it.

It is full bleed by living **outside** `.container`, as a direct child of the
section, so plain `width:100%` reaches both edges. The usual
`width:100vw; margin-left:50%; translate:-50%` trick is wrong here: `100vw`
counts the scrollbar, so it ran 5px past the viewport and put a horizontal
scroll on the page (scrollWidth 1435 against clientWidth 1430).

Cards are 162x231 on desktop and 120x171 below 620px. They are decorative:
every photograph appears again in the timeline below with real alt text, so the
container is `aria-hidden` and the images carry empty alt.

The back link sits at `position:absolute`, top left under the navbar, 11.5px. In
flow it pushed the marquee down and read as a heading above it. It stays first in
the DOM, so it is still the first thing a keyboard reaches.

## Cursor dot

One rAF loop, running continuously, lerping toward the pointer at `SPEED = 0.15`.
The earlier version parked the loop once it caught up and woke it on the next
mousemove. That saved frames but meant a slow drag restarted the loop over and
over, and every restart showed as a hitch.

Position is written only through `translate3d`, so the dot stays on the
compositor and never triggers layout. There is deliberately **no transition on
transform**: the easing is the loop's job, and a transition layered on top of a
lerp is what makes a trailing dot feel rubbery. The 4.5px centring offset is a
negative margin in CSS, so the loop can write raw `clientX` and `clientY`.

Kept as a solid gold dot rather than `mix-blend-mode: difference`. Difference
turns gold into a muddy cyan over the navy and inverts hard over the white
service panels.

Never starts on touch or under reduced motion. `pointer-events:none`, checked
with `elementFromPoint` directly under the dot.

## init() is fault-isolated, and why

Every piece runs inside its own try/catch. That is not defensive habit, it is a
scar. A rewrite of `initCursor` silently deleted `initScrollMemory` along with
it, because the two sat between the same pair of comment markers. `init()` then
threw a ReferenceError partway down its list and **everything below it stopped
running**: the back links, the cursor dot, the navbar scroll state and the
parallax, on all three pages. The files parsed, `node --check` passed, and the
pages looked normal. Only tracing markers through `init()` found it.

## Performance

Measured with Lighthouse, mobile emulation, medians of three runs. Run these
interleaved if you repeat them: this machine's load swings Total Blocking Time
by seconds, and a single run can read 20 points low.

| | score | FCP | LCP | transfer |
| --- | --- | --- | --- | --- |
| original | 77 | 2.9s | 4.7s | 5375 KB |
| after WebP + fetchpriority | 81 | 2.9s | 4.1s | 550 KB |
| after self-hosted fonts + posters | **93** | **1.2s** | **3.2s** | **490 KB** |

Three changes got there:

**`scripts/build-webp.py`** resizes the four service banners and four problem
cards to 1100px, which is 2x their measured 535px render, and writes WebP at q80.
8.9 MB becomes 0.41 MB. They render through `<picture>` with the source PNG as
the fallback; a WebP-capable browser never requests it. `picture{display:contents}`
keeps the wrapper out of the box tree so the existing descendant rules still match
and nothing shifts.

**Self-hosted fonts**, described above. This is what moved FCP.

**Posters at display size.** `scripts/build-videos.py` used to write a full 1920px
first frame, 115 KB, which was the page's largest contentful paint. Now 1100px,
82 KB and 24 KB.

The quality dial stayed high on purpose. Measured as PSNR against the lossless
frame at the same 1100px scale:

| | custom-ai-agent | ai-commercial-oreo |
| --- | --- | --- |
| 1920px q:v 4 (what it replaced) | 40.8 dB, 114 KB | 43.2 dB, 34 KB |
| 1100px q:v 6 (first attempt) | 38.1 dB, 47 KB | 42.2 dB, 11 KB |
| **1100px q:v 2 (shipped)** | **41.0 dB, 82 KB** | **43.2 dB, 24 KB** |

q:v 6 was a real 2.7 dB regression on the first poster for 35 KB. The resize is
where the saving comes from; the quality dial is not worth spending. What ships
now measures slightly *better* than the original while still being 28% smaller.

There is no `<picture>` fallback available for a video poster: the attribute
takes a single URL, so WebP would simply show nothing on a browser that cannot
decode it. These stay JPEG.

`fetchpriority="low"` is on every below-fold image. The navbar logo keeps
`fetchpriority="high"`.

**There is no minification step, deliberately.** It was tried and reverted: it
saved about 30 KB and cost a build step that silently swallowed edits to
`styles.css` and `main.js`. Those two files remain the ones you edit and the ones
the browser downloads.

### What is left

FCP is now bound by the CSS itself, LCP by the first poster. Lighthouse still
reports about 15 KB of unused CSS. Neither is worth chasing yet.
