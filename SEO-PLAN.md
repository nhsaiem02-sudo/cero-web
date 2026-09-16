# CERO Studio SEO Plan

Site: cerostudio.co, hosted on Netlify.
Audience: local businesses across the UK, US, Canada and Europe. We serve all industries, no single niche.
Primary language: English. German pages come later under /de/.

## Pages to build

Service pages: /ai-receptionist (covers AI voice agent too), /website-chatbot, /whatsapp-chatbot, /messenger-chatbot, /ai-automation, /ai-avatar, /website-design

Use-case pages: /missed-calls, /appointment-booking-automation

Later: /de/ki-telefonassistent, /de/impressum, /de/datenschutz

## Content rules

- Never show fixed prices or price ranges. Use a "What affects the cost" section instead.
- Every service page: keyword H1 hero, problem, how it works, use cases for local businesses, what affects the cost, FAQ, CTA.
- CTA link: https://cal.com/cerostudio/free-discovery-call
- Buyers search in plain words ("AI receptionist", "answering service"), not jargon ("voice agent", "lead follow-up automation"). Write for business owners, not tech people.
- Every new page must be added to sitemap.xml and linked from the homepage services section and the footer.

## Stack notes

- Plain HTML, CSS and vanilla JS. No build step. Do not add a framework.
- Header and footer are repeated in every HTML page. Update every page when changing nav or footer links.
- sitemap.xml is updated by hand. Add every new page to it in the same commit.
- Hosted on Netlify. Don't touch vercel.json or _headers.

## Timeline

- Week 1 (Sep 16-22): technical SEO.
- Week 2 (Sep 23-29): service pages.
- Week 3 (Sep 30-Oct 6): use-case pages and case study.
- Week 4 (Oct 7-13): authority and blog.
