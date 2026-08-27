/* ═══════════════════════════════════════════════════════════
   CERO Studio | interactions
   No dependencies. Everything degrades gracefully without JS.
   ═══════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* True when this load is a back/forward history entry rather than a fresh
     visit. Used to skip the splash and to restore scroll position. */
  function isBackForward() {
    try {
      var nav = performance.getEntriesByType('navigation')[0];
      if (nav) return nav.type === 'back_forward';
      return performance.navigation && performance.navigation.type === 2;
    } catch (e) { return false; }
  }

  /* ── Scroll reveal (stagger comes from inline --rd) ─────── */
  function initReveal() {
    // Stands down the head gate's failsafe timer. Deliberately NOT called just
    // because this file loaded: that would only prove the script arrived, and
    // an observer that never fires would still leave the page blank. It is
    // called once the reveal mechanism has demonstrably worked.
    function standDown() {
      if (window.__revealFailsafe) {
        clearTimeout(window.__revealFailsafe);
        window.__revealFailsafe = null;
      }
    }

    var items = $$('[data-reveal]');
    if (reduced || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-in'); });
      standDown();
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      // An observer invokes its callback once for every target shortly after
      // observe(), intersecting or not. Reaching here at all is the proof that
      // the mechanism is alive, which is the right moment to drop the net.
      standDown();
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-in');
        io.unobserve(e.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    items.forEach(function (el) { io.observe(el); });
  }

  /* ── Stat counters ─────────────────────────────────────────
     The markup ships the final numbers, and nothing is written
     until the first animation frame lands. So if rAF is starved
     (background tab, screenshot service, JS off) the honest
     value stays on screen instead of a stranded "0".          */
  function countUp(el) {
    var target = parseFloat(el.dataset.count) || 0;
    if (reduced) { el.textContent = String(target); return; }

    var dur = 1500, start = null;
    function frame(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);           // easeOutCubic
      el.textContent = String(Math.round(target * eased));
      if (p < 1) requestAnimationFrame(frame);
      else el.textContent = String(target);
    }
    requestAnimationFrame(frame);
  }

  function initCounters() {
    var nums = $$('[data-count]');
    if (!nums.length) return;
    if (!('IntersectionObserver' in window)) {
      nums.forEach(function (el) { el.textContent = el.dataset.count; });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        countUp(e.target);
        io.unobserve(e.target);
      });
    }, { threshold: 0.6 });
    nums.forEach(function (el) { io.observe(el); });
  }

  /* ── Marquee: duplicate track for a seamless loop ───────── */
  function initMarquee() {
    var wrap = $('#marquee');
    if (!wrap) return;
    var track = $('.marquee__track', wrap);
    if (!track) return;

    var clone = track.cloneNode(true);
    clone.setAttribute('aria-hidden', 'true');
    wrap.appendChild(clone);

    // Keep speed consistent regardless of content width (~90px/sec).
    var width = track.scrollWidth;
    if (width > 0) {
      var seconds = Math.max(24, Math.round(width / 90));
      track.style.animationDuration = seconds + 's';
      clone.style.animationDuration = seconds + 's';
    }
  }

  /* ── Navbar: scrolled state, mobile menu, active link ───── */
  function initNav() {
    var nav = $('#nav');
    var links = $('#navLinks');
    var toggle = $('#navToggle');
    if (!nav || !links || !toggle) return;

    function setScrolled() {
      nav.classList.toggle('is-scrolled', window.scrollY > 12);
    }
    setScrolled();

    function closeMenu() {
      links.classList.remove('is-open');
      nav.classList.remove('is-menu-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open menu');
      document.body.classList.remove('is-locked');
    }

    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('is-open');
      nav.classList.toggle('is-menu-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.body.classList.toggle('is-locked', open);
    });

    links.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeMenu();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && links.classList.contains('is-open')) {
        closeMenu();
        toggle.focus();
      }
    });

    // Reset the mobile panel if the viewport grows past the breakpoint.
    var mq = window.matchMedia('(min-width: 881px)');
    var onChange = function (e) { if (e.matches) closeMenu(); };
    mq.addEventListener ? mq.addEventListener('change', onChange) : mq.addListener(onChange);

    /* active section highlighting */
    var navLinks = $$('.nav__link', links);
    var sections = navLinks
      .map(function (a) { return document.querySelector(a.getAttribute('href')); })
      .filter(Boolean);

    if ('IntersectionObserver' in window && sections.length) {
      var spy = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          navLinks.forEach(function (a) {
            a.classList.toggle('is-active', a.getAttribute('href') === '#' + e.target.id);
          });
        });
      }, { rootMargin: '-45% 0px -50% 0px' });
      sections.forEach(function (s) { spy.observe(s); });
    }

    return setScrolled;
  }

  /* ── Parallax: background layers drift slower than content ── */
  function initParallax() {
    var layers = $$('[data-parallax]');
    if (reduced || !layers.length) return null;

    return function () {
      var y = window.scrollY;
      layers.forEach(function (el) {
        var rate = parseFloat(el.dataset.parallax) || 0;
        el.style.transform = 'translate3d(0,' + (y * rate).toFixed(1) + 'px,0)';
      });
    };
  }

  /* ── FAQ accordion ─────────────────────────────────────── */
  function initFaq() {
    $$('.faq__item').forEach(function (item) {
      var btn = $('.faq__q', item);
      var panel = $('.faq__a', item);
      if (!btn || !panel) return;

      btn.addEventListener('click', function () {
        var open = item.classList.contains('is-open');

        // Single-open accordion.
        $$('.faq__item.is-open').forEach(function (other) {
          if (other === item) return;
          other.classList.remove('is-open');
          $('.faq__q', other).setAttribute('aria-expanded', 'false');
          var p = $('.faq__a', other);
          setTimeout(function () { if (!other.classList.contains('is-open')) p.hidden = true; }, 380);
        });

        if (open) {
          item.classList.remove('is-open');
          btn.setAttribute('aria-expanded', 'false');
          setTimeout(function () { if (!item.classList.contains('is-open')) panel.hidden = true; }, 380);
        } else {
          panel.hidden = false;
          // Force a synchronous style resolution so the browser registers the
          // 0fr starting row before we flip to 1fr, otherwise the two changes
          // batch into one and the height transition is skipped.
          void panel.offsetHeight;
          item.classList.add('is-open');
          btn.setAttribute('aria-expanded', 'true');
        }
      });
    });
  }

  /* ── Smooth anchor scrolling with a fixed-nav offset ───── */
  function initAnchors() {
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href^="#"]');
      if (!a) return;
      var id = a.getAttribute('href');
      if (!id || id === '#') return;
      var target = document.querySelector(id);
      if (!target) return;

      e.preventDefault();
      var top = target.getBoundingClientRect().top + window.scrollY - 62;
      window.scrollTo({ top: Math.max(top, 0), behavior: reduced ? 'auto' : 'smooth' });
      history.replaceState(null, '', id);
    });
  }

  /* ── One rAF-throttled scroll listener for everything ──── */
  function initScrollLoop(handlers) {
    var fns = handlers.filter(Boolean);
    if (!fns.length) return;
    var ticking = false;

    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        fns.forEach(function (fn) { fn(); });
        ticking = false;
      });
    }, { passive: true });
  }

  /* ── First-load splash teardown ─────────────────────────────
     The head gate decides whether the splash plays; CSS runs the animation.
     This only clears the flag and removes the node once it is done, so the
     overlay never lingers in the tree. Deliberately not load-bearing: if this
     never runs, the CSS animation has already made the overlay invisible and
     inert.                                                                   */
  function initSplash() {
    var el = $('#splash');
    if (!el || !document.documentElement.classList.contains('splash-on')) return;
    setTimeout(function () {
      document.documentElement.classList.remove('splash-on');
      if (el.parentNode) el.parentNode.removeChild(el);
    }, 1400);
  }

  /* ── Scroll position across the /founder round trip ─────────
     Clicking a founder card is a real navigation, so coming back is a fresh
     document load. Chrome usually restores the old scroll position itself, but
     it decides where to land before the lazy images below the fold and the
     async webfonts have settled, and on a page this tall it can give up and
     leave you at the top.

     So: remember the position on the way out, and put it back on the way in,
     but only when the browser has not already done it. A bfcache restore needs
     nothing at all, and neither does a normal fresh visit. Only a back/forward
     entry that landed at the top gets corrected. */
  function initScrollMemory() {
    if (!('sessionStorage' in window)) return;
    if ('scrollRestoration' in history) history.scrollRestoration = 'auto';

    var KEY = 'cero:scroll:' + location.pathname;

    function save() {
      try { sessionStorage.setItem(KEY, String(Math.round(window.scrollY))); } catch (e) {}
    }
    window.addEventListener('pagehide', save);
    window.addEventListener('beforeunload', save);
    // A tab switch or a phone call can discard the page without either event.
    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'hidden') save();
    });

    if (!isBackForward()) return;

    var saved;
    try { saved = parseInt(sessionStorage.getItem(KEY), 10); } catch (e) { return; }
    if (!saved || saved < 4) return;

    // Retry across a few frames: the target only becomes reachable once the
    // images below the fold have taken up their space.
    var tries = 0;
    (function settle() {
      if (window.scrollY > 4) return;              // browser got there first
      var max = document.documentElement.scrollHeight - window.innerHeight;
      window.scrollTo(0, Math.min(saved, Math.max(max, 0)));
      if (++tries < 12 && Math.abs(window.scrollY - saved) > 4) {
        setTimeout(settle, 60);
      }
    })();
  }

  /* ── Trailing cursor dot ────────────────────────────────────
     A decorative layer on top of the native cursor, which is never hidden.

     One rAF loop, running continuously, lerping the dot toward the pointer at a
     fixed rate. The previous version parked the loop once it caught up and woke
     it on the next mousemove; that saved a few frames but meant a slow drag
     restarted the loop over and over, and every restart showed as a hitch. A
     single uninterrupted loop is what makes it feel smooth.

     Position is written only through translate3d, so the dot lives on the
     compositor and never triggers layout. The 4.5px centring offset is CSS
     (a negative margin), not arithmetic in the loop.

     Never starts on touch devices or under prefers-reduced-motion.            */
  function initCursor() {
    var dot = $('#cursorDot');
    if (!dot) return;
    if (reduced) return;
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

    var mouseX = 0, mouseY = 0;   // where the pointer is
    var dotX = 0, dotY = 0;       // where the dot has got to
    var SPEED = 0.15;             // lower = longer trail
    var seen = false;
    var awake = true;

    document.addEventListener('mousemove', function (e) {
      mouseX = e.clientX;
      mouseY = e.clientY;
      if (!seen) {                // first sighting: appear in place, do not fly in
        seen = true;
        dotX = mouseX; dotY = mouseY;
        dot.classList.add('is-on');
      }
    }, { passive: true });

    function animate() {
      dotX += (mouseX - dotX) * SPEED;
      dotY += (mouseY - dotY) * SPEED;
      dot.style.transform = 'translate3d(' + dotX.toFixed(2) + 'px,' + dotY.toFixed(2) + 'px,0)';
      if (awake) requestAnimationFrame(animate);
    }
    requestAnimationFrame(animate);

    // A hidden tab throttles rAF to a crawl anyway; stopping outright means the
    // dot is not mid-interpolation toward a stale point when the tab returns.
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        awake = false;
      } else if (!awake) {
        awake = true;
        dotX = mouseX; dotY = mouseY;
        requestAnimationFrame(animate);
      }
    });

    // Grow over anything clickable, so the dot reads as a pointer cue. Scale is
    // its own property, so this never disturbs the transform the loop owns.
    document.addEventListener('mouseover', function (e) {
      var hit = e.target.closest && e.target.closest('a,button,input,textarea,select,summary,[role="tab"]');
      dot.classList.toggle('is-over', !!hit);
    }, { passive: true });

    document.addEventListener('mouseleave', function () { dot.classList.remove('is-on'); });
    document.addEventListener('mouseenter', function () { if (seen) dot.classList.add('is-on'); });
  }

  /* ── "Back to CERO Studio" ──────────────────────────────────
     Following the href would be a forward navigation: a brand new history entry
     for the homepage, which lands at the top and leaves the entry the reader
     came from stranded behind it. Going back through history instead returns
     them to the exact spot they left, and initScrollMemory covers the case where
     the browser does not manage it alone.

     Only when they actually arrived from this site. On a cold landing (a shared
     link, a search result) there is nothing to go back to, so the href stands.
     Modified clicks are left alone so open-in-new-tab keeps working. */
  function initBackLinks() {
    var links = $$('a[data-back]');
    if (!links.length) return;

    var cameFromHere = false;
    try {
      cameFromHere = !!document.referrer &&
        new URL(document.referrer).origin === location.origin &&
        new URL(document.referrer).pathname !== location.pathname;
    } catch (e) { cameFromHere = false; }

    if (!cameFromHere || history.length < 2) return;

    links.forEach(function (a) {
      a.addEventListener('click', function (e) {
        if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        e.preventDefault();
        history.back();
      });
    });
  }

  /* ── Boot ──────────────────────────────────────────────── */
  function init() {
    var onNavScroll = initNav();
    var onParallax = initParallax();

    /* Each piece is independent, so one throwing must not take the rest of the
       page down with it. It cost the cursor dot, the back links, the navbar
       scroll state and the parallax once already: a single ReferenceError in
       the middle of this list silently killed everything below it. */
    [initReveal, initCounters, initMarquee, initFaq, initAnchors, initSplash,
     initScrollMemory, initBackLinks, initCursor].forEach(function (fn) {
      try { fn(); } catch (e) { if (window.console) console.error(e); }
    });
    initScrollLoop([onNavScroll, onParallax]);

    var year = document.getElementById('year');
    if (year) year.textContent = String(new Date().getFullYear());
  }

  document.readyState === 'loading'
    ? document.addEventListener('DOMContentLoaded', init)
    : init();
})();
