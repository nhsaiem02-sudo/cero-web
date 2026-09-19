# CERO Studio SEO Plan

Site: cerostudio.co, served by Cloudflare Pages from main, previews at
cero-web.pages.dev.
Audience: local businesses across the UK, US, Canada and Europe. We serve all industries, no single niche.
Primary language: English. German pages come later under /de/.

## Pages to build

Six pages, built in this order. The order is the decision; the week bands are
guidance and slip together if a page takes longer than planned.

1. /ai-receptionist - includes appointment booking as a section (see cuts below)
2. /website-chatbot
3. /whatsapp-chatbot - also covers Messenger as a section
4. /website-design
5. /missed-calls - ON HOLD, see cuts below. Skip to /ai-avatar if still unchecked.
6. /ai-avatar - lowest priority

Shipped: /ai-automation (also the template every page below is copied from).

Later: /de/ki-telefonassistent, /de/impressum, /de/datenschutz

### Cuts and holds

- /messenger-chatbot is cut. Messenger is a section on /whatsapp-chatbot.
- /appointment-booking-automation is cut. Appointment booking is a section
  inside /ai-receptionist, not a page of its own. Nothing else should link to
  the old slug; it was never built, so no redirect is owed.
- /missed-calls is deferred until its keyword volume is checked. Do not start
  it on the strength of the order alone - it is fifth only if the data supports
  a page. If the volume does not justify one, it becomes a section on
  /ai-receptionist alongside appointment booking, and the list is five pages.

## Content rules

- Never show fixed prices or price ranges. Use a "What affects the cost" section instead.
- Every service page: keyword H1 hero, problem, how it works, use cases for local businesses, what affects the cost, FAQ, CTA.
- CTA link: https://cal.com/cerostudio/free-discovery-call
- Every new page ships with the full five-item checklist in CLAUDE.md: sitemap.xml,
  homepage service card, footer link, _redirects line and two _headers blocks.
  CLAUDE.md is the authority on that list; do not work from a shorter version of it.

## Target keywords (Ahrefs free tool, Sep 2026, volumes are ranges)

- Homepage: "ai automation agency" (UK >1000, Easy; SERP is real agencies). Supporting: "ai agency", "ai automation agency uk".
- /ai-receptionist: H1 targets "ai receptionist" (US >1000, UK >100, Hard). Section heading targets "ai answering service for business" (US Easy). Also use "ai receptionist for small business" and mention "ai voice agent" in body text, not headings.
- /whatsapp-chatbot: H1 targets "whatsapp chatbot for business" (US >100, Easy). Messenger covered in a section below.
- /website-chatbot: target "ai chatbot for website", not generic "chatbot" or "ai chatbot" (those searchers want ChatGPT).
- /website-design: target "website design for small business" (UK >100, Medium).
- /ai-avatar: target "ai avatar video for business". Generic "ai avatar" searchers want free generators.
- Avoid as primary targets: "chatbot", "ai chatbot", "messenger chatbot" (UK <100), "ai voice agent" as a heading (searchers want platforms).
- Blog idea for later: "average cost of website design for small business uk" (UK >100, Easy). No prices published, explain cost factors only.

## Stack notes

- Plain HTML, CSS and vanilla JS. No build step. Do not add a framework.
- Header and footer are repeated in every HTML page. Update every page when changing nav or footer links.
- sitemap.xml is updated by hand. Add every new page to it in the same commit.
- Redirects and headers live in _redirects and _headers, the only host config in the
  repo. netlify.toml and vercel.json are deleted: the site is on Cloudflare Pages and
  neither was read by anything. An earlier note here said _headers was hands-off;
  that predates the migration and is wrong - a new page must edit it.

## Timeline

- Week 1 (Sep 16-22): technical SEO.
- Week 2 (Sep 23-29): service pages.
- Week 3 (Sep 30-Oct 6): use-case pages and case study.
- Week 4 (Oct 7-13): authority and blog.

### Hard deadline: Oct 14 2026

Claude Code access ends Oct 14 2026. All code work must be complete before
then - every page built, every checklist item closed, everything merged.

Week 4 ends Oct 13, so the plan has one day of slack against this date. Work
that needs Claude Code comes first inside each week; anything that can be done
by hand later (copy edits, keyword checks, the blog) gives way if a week slips.
The one open decision that costs code time is the /missed-calls keyword check;
settle it early rather than late.
