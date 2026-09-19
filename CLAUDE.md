# CERO Studio — repo guide

## Read this first

**Before any SEO or content work, read [SEO-PLAN.md](SEO-PLAN.md).** That file is the
source of truth for site structure, page inventory, content rules and timeline. Do not
write, edit or restructure page copy, metadata, headings, sitemap entries or internal
links without reading it first.

"SEO or content work" includes: creating or editing any page under the site, writing or
rewriting headings and body copy, titles and meta descriptions, schema/structured data,
`sitemap.xml`, `robots.txt`, internal linking, URL/slug changes, redirects, and blog posts.

## Git workflow

**Never commit directly to main. Work on a branch and wait for my approval before merging.**

## Non-negotiables (details in SEO-PLAN.md)

- **No prices.** Never publish fixed prices or price ranges. Use a "What affects the cost"
  section instead.
- **CTA link is always** `https://cal.com/cerostudio/free-discovery-call`.
- Use the keyword targets in the Target keywords section of SEO-PLAN.md. Plain buyer
  language over jargon: never use 'voice agent' or 'lead follow-up automation' in
  headings.
- **Service pages follow the fixed section order**: keyword H1 hero → problem → how it
  works → use cases for local businesses → what affects the cost → FAQ → CTA.
- **Every new page ships with five things.** A page is not done until all five exist:
  1. an entry in `sitemap.xml`
  2. a link in the homepage services section
  3. a link in the footer (see the footer rule below)
  4. a line in `_redirects`, `/<page>.html /<page> 301`
  5. two blocks in `_headers`, one for `/<page>` and one for `/<page>.html`, both
     `Cache-Control: public, max-age=0, must-revalidate`

  `_headers` needs both the extensionless and the `.html` path because Cloudflare allows
  only one splat per pattern, so `/*.html` matches nothing and every file that needs a
  cache policy has to be named. Miss the `_headers` blocks and the page still loads, just
  on Cloudflare's default - which is the same value, so nothing visibly breaks; add them
  anyway so the policy is enforced by the file rather than inherited by luck.
- **New service pages start as a copy of `ai-automation.html`.** It is the template: each
  section is commented with what to edit, and it uses only existing CSS classes, so a new
  page needs no stylesheet changes. Use `.svc-rows--compact` for the use-case list.
- **Each new service page gets one line in the footer Services column**, and that line goes
  in *every* HTML file, not just the new one. The footer is copied per page, so a link added
  in one place only exists on one page.
- **After editing `styles.css` or `main.js`, run `python3 scripts/build-min.py`.** The pages
  load the minified files, so an unbuilt change does nothing. Add any new page to `PAGES` in
  that script or it keeps a stale `?v=` stamp.

If a request conflicts with SEO-PLAN.md, say so and ask before deviating — don't silently
override the plan.

## Site facts

- Domain: cerostudio.co, served by Cloudflare Pages from `main`, with previews at
  `cero-web.pages.dev`. Routing and headers live in `_redirects` and `_headers`; those
  two files are the only host config in the repo. `www` -> apex is a Redirect Rule on
  the Cloudflare zone, not a file here, because `_redirects` cannot match on hostname.
- Local server is `npx wrangler pages dev . --port 8788`, which reads `_redirects` and
  `_headers` the way production does. A plain static server does not.
- Audience: local businesses in the UK, US, Canada and Europe; all industries.
- Primary language English; German pages land later under `/de/`.
