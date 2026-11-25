/* VIDESIGN — tiny behaviour layer. No dependencies. Load after the markup, after lucide. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var fine = matchMedia('(hover: hover)').matches;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // pointer type of the last press: touch screens on hybrid devices report (hover: hover) too
  var lastPointer = fine ? 'mouse' : 'touch';
  addEventListener('pointerdown', function (e) { lastPointer = e.pointerType; }, true);
  var touchy = function () { return lastPointer === 'touch' || lastPointer === 'pen' && !fine; };

  /* 0. Docs: build code snippets from live demos BEFORE icons are swapped to SVG */
  $$('[data-snippet]').forEach(function (demo) {
    var target = document.getElementById(demo.getAttribute('data-snippet'));
    if (!target) return;
    var lines = demo.innerHTML.replace(/^\n+|\s+$/g, '').split('\n');
    var ind = Math.min.apply(null, lines.filter(function (l) { return l.trim(); }).map(function (l) { return l.match(/^\s*/)[0].length; }));
    target.textContent = lines.map(function (l) { return l.slice(ind); }).join('\n').replace(/=""/g, '');
  });
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = document.getElementById(b.getAttribute('data-copy'));
      if (t && navigator.clipboard) navigator.clipboard.writeText(t.textContent).then(function () {
        var l = b.querySelector('span'); if (!l) return; var o = l.textContent; l.textContent = 'Copied'; setTimeout(function () { l.textContent = o; }, 1200);
      });
    });
  });

  /* 1. Icons */
  if (window.lucide) lucide.createIcons();

  /* 2. Switches: [role=switch].switch toggles aria-checked. data-switch="theme" also flips the theme */
  var root = document.documentElement;
  try { var saved = localStorage.getItem('vd-theme'); if (saved) root.setAttribute('data-theme', saved); } catch (e) {}
  $$('.switch[role="switch"]').forEach(function (sw) {
    if (sw.dataset.switch === 'theme') sw.setAttribute('aria-checked', root.getAttribute('data-theme') === 'light' ? 'true' : 'false');
    sw.addEventListener('click', function () {
      var on = sw.getAttribute('aria-checked') !== 'true';
      sw.setAttribute('aria-checked', on ? 'true' : 'false');
      if (sw.dataset.switch === 'theme') {
        root.classList.add('t-anim');
        root.setAttribute('data-theme', on ? 'light' : 'dark');
        try { localStorage.setItem('vd-theme', on ? 'light' : 'dark'); } catch (e) {}
        $$('.switch[data-switch="theme"]').forEach(function (o) { o.setAttribute('aria-checked', on ? 'true' : 'false'); });
        setTimeout(function () { root.classList.remove('t-anim'); }, 700);
      }
    });
  });

  /* 3. Lineup: hover/focus/tap one item → others dim, floating card follows the pointer */
  $$('.lineup').forEach(function (list) {
    var card = list.parentNode.querySelector('.lineup-card') || $('#' + list.dataset.card);
    var cur = null, prev = null;   // prev = item that was active before this tap (focus also activates)
    list.addEventListener('pointerdown', function () { prev = cur; }, true);
    function fill(item) {
      if (!card) return;
      var d = item.dataset, html = '';
      if (d.img) html += '<img class="lineup-card-img" alt="" src="' + d.img + '">';
      else if (d.icon) html += '<span class="lineup-card-icon"><i data-lucide="' + d.icon + '"></i></span>';
      html += '<span class="lineup-card-body">';
      if (d.title) html += '<span>' + d.title + '</span>';
      if (d.sub) html += '<em>' + d.sub + '</em>';
      if (d.text) html += '<span>' + d.text + '</span>';
      if (d.meta) html += '<em>' + d.meta + '</em>';
      card.innerHTML = html + '</span>';
      if (d.icon && window.lucide) lucide.createIcons({ root: card });
    }
    function show(item) {
      if (cur === item) return; cur = item;
      fill(item);
      list.classList.add('is-active');
      $$('.lineup-item', list).forEach(function (x) { x.classList.toggle('is-on', x === item); });
      if (card) card.classList.add('is-on');
    }
    function hide() {
      cur = null; list.classList.remove('is-active');
      $$('.lineup-item.is-on', list).forEach(function (x) { x.classList.remove('is-on'); });
      if (card) card.classList.remove('is-on');
    }
    function place(x, y) {
      if (!card || innerWidth < 768) { if (card) card.style.transform = ''; return; }
      card.style.transform = 'translate(' + Math.max(12, Math.min(innerWidth - 212, x)) + 'px,' + Math.max(12, Math.min(innerHeight - 320, y)) + 'px)';
    }
    $$('.lineup-item', list).forEach(function (it) { if (!it.hasAttribute('tabindex') && it.tagName !== 'A') it.tabIndex = 0; });
    list.addEventListener('mouseover', function (e) { if (touchy()) return; var it = e.target.closest('.lineup-item'); if (it) show(it); });
    list.addEventListener('mouseleave', function () { if (!touchy()) hide(); });
    list.addEventListener('click', function (e) {
      if (!touchy()) return; var it = e.target.closest('.lineup-item'); if (!it) return;
      if (prev === it) { if (it.tagName !== 'A') { e.preventDefault(); hide(); } return; }   // 2nd tap on a link follows it
      e.preventDefault(); show(it);
    });
    list.addEventListener('focusin', function (e) { var it = e.target.closest('.lineup-item'); if (!it) return; show(it); var r = it.getBoundingClientRect(); place(r.right + 16, r.top - 160); });
    list.addEventListener('focusout', function (e) { if (!list.contains(e.relatedTarget)) hide(); });
    addEventListener('pointermove', function (e) { if (cur && e.pointerType === 'mouse') place(e.clientX + 24, e.clientY - 130); }, { passive: true });
    addEventListener('scroll', function () { if (touchy() && cur) { var r = list.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight) hide(); } }, { passive: true });
  });

  /* 4. Track list: click/tap unfolds; hover only "wakes" the line */
  $$('.tracks').forEach(function (list) {
    $$('.track', list).forEach(function (tr) {
      var btn = $('.track-btn', tr);
      if (!btn) return;
      btn.addEventListener('click', function () {
        var open = !tr.classList.contains('is-open');
        if (list.dataset.single !== undefined) $$('.track.is-open', list).forEach(function (o) { o.classList.remove('is-open'); $('.track-btn', o).setAttribute('aria-expanded', 'false'); });
        tr.classList.toggle('is-open', open); btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        list.classList.toggle('is-active', !!$('.track.is-open', list));
      });
      tr.addEventListener('mouseenter', function () { if (touchy()) return; tr.classList.add('is-hot'); list.classList.add('is-active'); });
      tr.addEventListener('mouseleave', function () { if (touchy()) return; tr.classList.remove('is-hot'); list.classList.toggle('is-active', !!$('.track.is-open', list)); });
    });
  });

  /* 5. Drawer: [data-open="id"], [data-close], scrim, Esc */
  function openDrawer(d) {
    var s = $('#' + d.dataset.scrim); d.hidden = false; if (s) s.hidden = false;
    requestAnimationFrame(function () { requestAnimationFrame(function () { d.classList.add('is-on'); if (s) s.classList.add('is-on'); }); });
    document.body.style.overflow = 'hidden';
    // words inside a drawer light up in sequence, like the original manifesto
    var ws = $$('.word', d); ws.forEach(function (w) { w.classList.remove('is-on'); });
    ws.forEach(function (w, i) { setTimeout(function () { w.classList.add('is-on'); }, reduce ? 0 : 350 + i * 70); });
  }
  function closeDrawer(d) { var s = $('#' + d.dataset.scrim); d.classList.remove('is-on'); if (s) s.classList.remove('is-on'); document.body.style.overflow = ''; setTimeout(function () { if (!d.classList.contains('is-on')) { d.hidden = true; if (s) s.hidden = true; } }, 450); }
  $$('[data-open]').forEach(function (b) { b.addEventListener('click', function () { var d = $('#' + b.dataset.open); if (d) openDrawer(d); }); });
  $$('.drawer').forEach(function (d) {
    $$('[data-close]', d).forEach(function (b) { b.addEventListener('click', function () { closeDrawer(d); }); });
    var s = $('#' + d.dataset.scrim); if (s) s.addEventListener('click', function () { closeDrawer(d); });
  });
  addEventListener('keydown', function (e) { if (e.key !== 'Escape') return; $$('.drawer.is-on').forEach(closeDrawer); $$('.menu.is-on').forEach(function (m) { toggleMenu(m, false); }); });

  /* 6. Mobile menu */
  function toggleMenu(m, on) { m.classList.toggle('is-on', on); document.body.style.overflow = on ? 'hidden' : ''; $$('[data-menu="' + m.id + '"]').forEach(function (b) { b.setAttribute('aria-expanded', on ? 'true' : 'false'); }); }
  $$('[data-menu]').forEach(function (b) { b.addEventListener('click', function () { var m = $('#' + b.dataset.menu); if (m) toggleMenu(m, !m.classList.contains('is-on')); }); });
  $$('.menu a').forEach(function (a) { a.addEventListener('click', function () { toggleMenu(a.closest('.menu'), false); }); });

  /* 7. Floating CTA: shows once the hero is gone */
  $$('.fab').forEach(function (f) {
    var after = $(f.dataset.after || '.hero');
    function tick() { var y = after ? after.getBoundingClientRect().bottom : innerHeight; f.classList.toggle('is-on', y < innerHeight * 0.6); }
    addEventListener('scroll', tick, { passive: true }); tick();
  });

  /* 8. Countdown: data-countdown="2026-12-02T09:00:00+01:00" with [data-unit=d|h|m|s] inside */
  $$('[data-countdown]').forEach(function (c) {
    var end = new Date(c.dataset.countdown).getTime();
    function pad(n) { return (n < 10 ? '0' : '') + n; }
    function tick() {
      var t = Math.max(0, end - Date.now()) / 1000;
      var v = { d: Math.floor(t / 86400), h: Math.floor(t % 86400 / 3600), m: Math.floor(t % 3600 / 60), s: Math.floor(t % 60) };
      $$('[data-unit]', c).forEach(function (u) { u.textContent = pad(v[u.dataset.unit]); });
    }
    tick(); setInterval(tick, 1000);
  });

  /* 9. Count-up numbers: <span data-count="4000" data-suffix="+">4,000+</span> */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return; io.unobserve(e.target);
        var el = e.target, to = +el.dataset.count, suf = el.dataset.suffix || '', t0 = null;
        if (reduce) return;
        (function step(ts) { if (!t0) t0 = ts; var k = Math.min(1, (ts - t0) / 1400), v = Math.round(to * (1 - Math.pow(1 - k, 4)));
          el.textContent = v.toLocaleString('en-US') + suf; if (k < 1) requestAnimationFrame(step); })(performance.now());
      });
    }, { threshold: 0.6 });
    $$('[data-count]').forEach(function (el) { io.observe(el); });
  }

  /* 10. Word reveal: words light up as the paragraph crosses the viewport */
  var all = $$('[data-reveal]');
  var reveals = all.filter(function (p) { return !p.closest('.drawer'); });
  all.forEach(function (p) {
    p.innerHTML = p.textContent.trim().split(/\s+/).map(function (w) { return '<span class="word">' + w + '</span>'; }).join(' ');
  });
  function lightWords() {
    reveals.forEach(function (p) {
      var r = p.getBoundingClientRect(), ws = $$('.word', p);
      var k = Math.min(1, Math.max(0, (innerHeight * 0.85 - r.top) / (r.height + innerHeight * 0.35)));
      var n = Math.round(k * ws.length);
      ws.forEach(function (w, i) { w.classList.toggle('is-on', i < n); });
    });
  }
  if (reveals.length) { addEventListener('scroll', lightWords, { passive: true }); lightWords(); }

  /* 11. Peek: cross-fades images every 3s, updates the counter */
  $$('.peek').forEach(function (pk) {
    var imgs = $$('.peek-img', pk), n = $('[data-peek-n]', pk), i = 0;
    if (imgs.length < 2) return;
    setInterval(function () { imgs[i].classList.remove('is-on'); i = (i + 1) % imgs.length; imgs[i].classList.add('is-on'); if (n) n.textContent = (i < 9 ? '0' : '') + (i + 1); }, 3200);
  });

  /* 12. Mosaic on touch: caption shows when the tile crosses the middle of the screen */
  if (!fine && 'IntersectionObserver' in window) {
    var mo = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.classList.toggle('is-seen', e.isIntersecting); }); }, { rootMargin: '-45% 0px -45% 0px' });
    $$('.tile').forEach(function (t) { mo.observe(t); });
  }
})();
