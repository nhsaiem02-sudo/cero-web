# CERO Studio SEO Plan

Site: cerostudio.co, hosted on Netlify.
Audience: local businesses across the UK, US, Canada and Europe. We serve all industries, no single niche.
Primary language: English. German pages come later under /de/.

## Pages to build

Week 2: /ai-automation, /ai-receptionist, /website-design, /website-chatbot

Week 3: /whatsapp-chatbot (also covers Messenger), /missed-calls, /appointment-booking-automation, /ai-avatar (lowest priority)

Later: /de/ki-telefonassistent, /de/impressum, /de/datenschutz

/messenger-chatbot is cut. Messenger is a section on /whatsapp-chatbot.

## Content rules

- Never show fixed prices or price ranges. Use a "What affects the cost" section instead.
- Every service page: keyword H1 hero, problem, how it works, use cases for local businesses, what affects the cost, FAQ, CTA.
- CTA link: https://cal.com/cerostudio/free-discovery-call
- Every new page must be added to sitemap.xml and linked from the homepage services section and the footer.

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
- Hosted on Netlify. Don't touch vercel.json or _headers.

## Timeline

- Week 1 (Sep 16-22): technical SEO.
- Week 2 (Sep 23-29): service pages.
- Week 3 (Sep 30-Oct 6): use-case pages and case study.
- Week 4 (Oct 7-13): authority and blog.
