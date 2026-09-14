Compressed web videos and their poster frames.

Served from /assets/videos/ so they pick up the 1-year immutable Cache-Control
header configured for /assets/* in vercel.json, netlify.toml and _headers.

Re-encode from the masters in videos-raw/ (gitignored). Every file here is
remuxed with +faststart so playback starts before the whole file arrives.

Still missing: founder-intro.mp4 and founder-intro-poster.jpg, referenced by the
Founder CTA section on index.html.
