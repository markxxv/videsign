#!/usr/bin/env python3
"""Generates index.html (the docs page). Edit specimens here, then run:
   python3 tools/docs.py && python3 build.py"""
import pathlib, html
root = pathlib.Path(__file__).resolve().parent.parent
N = [0]
def spec(title, classes, demo, demo_cls=''):
    N[0] += 1; sid = f's{N[0]}'
    cls = ' '.join(f'<code class="cls">{c}</code>' for c in classes.split())
    return f'''
      <div class="specimen">
        <div class="specimen-head"><span>{title}</span><span class="flex flex-wrap gap-1.5">{cls}</span></div>
        <div class="specimen-demo {demo_cls}" data-snippet="{sid}">
{demo.strip(chr(10))}
        </div>
        <div class="specimen-code"><button class="copy" type="button" data-copy="{sid}"><i data-lucide="copy"></i><span>Copy</span></button><pre id="{sid}"></pre></div>
      </div>'''

def section(id, title, lead, body):
    return f'''
    <section class="doc-section" id="{id}">
      <h2 class="doc-h">{title}</h2>
      <p class="doc-lead">{lead}</p>
{body}
    </section>'''

NAV = []
def S(group, id, title, lead, body):
    NAV.append((group, id, title)); return section(id, title, lead, body)

FACE = lambda n: f'https://i.pravatar.cc/240?img={n}'
PIC = lambda s, w=240, h=160: f'https://picsum.photos/seed/{s}/{w}/{h}'

out = []

# ---------------- Overview
out.append(S('Foundations', 'overview', 'Overview',
 'This design system uses HTML, Tailwind CSS v4 (CDN) and Lucide icons. Its design language comes from techspirit.barcelona. Each component has a short semantic class. All classes use <code class="cls">@apply</code> in one <code class="cls">&lt;style type="text/tailwindcss"&gt;</code> block. The system does not use clamp() or custom font sizes. It uses only the Tailwind scale with breakpoints.',
 '''
      <ol class="numlist col max-w-5xl">
        <li class="numlist-item mb-8"><span class="numlist-n">01</span>Two sizes.<span class="text block mt-3 max-w-[60ch] text-fg/60">The display size is large: Inter Tight, tracking −0.035em, line height 1.02. The text size is small: Geist, 14px. Use the mid size only for card titles. Make hierarchy with size and space. Do not use bold weights for hierarchy.</span></li>
        <li class="numlist-item mb-8"><span class="numlist-n">02</span>One text edge.<span class="text block mt-3 max-w-[60ch] text-fg/60">All text starts on one vertical line (<code class="cls">.col</code>). Numbers, icons and marks hang to the left of this line, in the <code class="cls">hang</code> margin. They do not move the text.</span></li>
        <li class="numlist-item mb-8"><span class="numlist-n">03</span>Mono + six signals.<span class="text block mt-3 max-w-[60ch] text-fg/60">The base is black and white. Six accent colors go from orange to blue. Use an accent only to show meaning: a category, a company or a track.</span></li>
        <li class="numlist-item mb-8"><span class="numlist-n">04</span>Focus by dimming.<span class="text block mt-3 max-w-[60ch] text-fg/60">When you point at one item, the other items dim to 28–30%. Photos are black and white until you point at them. Buttons and bands invert the colors.</span></li>
        <li class="numlist-item"><span class="numlist-n">05</span>Hairlines, not boxes.<span class="text block mt-3 max-w-[60ch] text-fg/60">A 1px line above each section and card separates them. Do not use shadows or card fills. Use round corners only on photos, pills and capsules.</span></li>
      </ol>
      <p class="col mt-12 flex flex-wrap gap-4"><a class="btn btn-sm" href="example.html"><span>Example landing</span><i data-lucide="arrow-up-right"></i></a><a class="btn btn-sm" href="https://github.com/markxxv/videsign"><span>GitHub</span><i data-lucide="arrow-up-right"></i></a></p>'''))

# ---------------- Tokens
sw = lambda name, cls, val: f'<div class="swatch"><div class="swatch-chip {cls}"></div><span><code class="cls">{name}</code></span><span class="faint">{val}</span></div>'
colors = ''.join([sw('bg','bg-bg','var(--bg) · #000 / #fafaf8'), sw('fg','bg-fg','var(--fg) · #fafaf8 / #0b0b0b'), sw('tile','bg-tile','var(--tile) · #1c1c1c / #ececec'), sw('rule','bg-rule','fg · 22%'),
  sw('ink','bg-ink','#000000'), sw('paper','bg-paper','#fafaf8'), sw('graphite','bg-graphite','#1c1c1c'), sw('mist','bg-mist','#ececec')])
accents = ''.join([sw('flame','bg-flame','#fa6e1d · AI'), sw('amber','bg-amber','#ffa234 · Investment'), sw('sand','bg-sand','#ffcf82 · Robotics'), sw('ice','bg-ice','#ceedff · Gaming'), sw('sky','bg-sky','#9fd0ff · Health'), sw('azure','bg-azure','#70adfb · Creativity')])
out.append(S('Foundations', 'tokens', 'Tokens',
 'The <code class="cls">@theme</code> block declares the tokens. The theme colors (bg, fg, tile, rule) are in <code class="cls">@theme inline</code>. They point to CSS variables. Thus one <code class="cls">data-theme</code> attribute on &lt;html&gt; changes the theme. Opacity modifiers such as <code class="cls">text-fg/45</code> and <code class="cls">border-fg/20</code> also work.',
 f'''
      <h3 class="label mt-2">Colors · base (change with the theme)</h3>
      <div class="mb-10 grid grid-cols-2 gap-4 md:grid-cols-4">{colors}</div>
      <h3 class="label">Accents · scale from warm to cold</h3>
      <div class="mb-12 grid grid-cols-2 gap-4 md:grid-cols-6">{accents}</div>
      <h3 class="label">Type scale (Tailwind classes only)</h3>
      <div class="mb-12 overflow-x-auto"><table class="w-full min-w-[640px] text-left text-sm">
        <thead class="text-fg/50"><tr class="border-b border-rule"><th class="py-2 pr-4 font-normal">Role</th><th class="py-2 pr-4 font-normal">Class</th><th class="py-2 pr-4 font-normal">base</th><th class="py-2 pr-4 font-normal">sm</th><th class="py-2 pr-4 font-normal">md</th><th class="py-2 pr-4 font-normal">lg</th><th class="py-2 font-normal">2xl</th></tr></thead>
        <tbody>
          <tr class="border-b border-rule"><td class="py-2 pr-4">Display (big)</td><td class="pr-4"><code class="cls">.display</code></td><td>text-4xl · 36</td><td>text-5xl · 48</td><td>text-6xl · 60</td><td>text-7xl · 72</td><td>text-8xl · 96</td></tr>
          <tr class="border-b border-rule"><td class="py-2 pr-4">Lineup</td><td class="pr-4"><code class="cls">.lineup</code></td><td>text-3xl · 30</td><td>—</td><td>text-5xl · 48</td><td>text-6xl / xl:7xl</td><td>text-8xl</td></tr>
          <tr class="border-b border-rule"><td class="py-2 pr-4">Mid</td><td class="pr-4"><code class="cls">.display-mid</code></td><td>text-2xl · 24</td><td>—</td><td>text-3xl · 30</td><td>text-4xl / xl:5xl</td><td>—</td></tr>
          <tr class="border-b border-rule"><td class="py-2 pr-4">Button</td><td class="pr-4"><code class="cls">.btn</code></td><td>text-2xl</td><td>—</td><td>text-3xl</td><td>text-5xl</td><td>—</td></tr>
          <tr class="border-b border-rule"><td class="py-2 pr-4">Lead</td><td class="pr-4"><code class="cls">.text-lead</code></td><td>text-base</td><td>—</td><td>—</td><td>text-lg</td><td>—</td></tr>
          <tr class="border-b border-rule"><td class="py-2 pr-4">Text / label</td><td class="pr-4"><code class="cls">.text .label</code></td><td colspan="5">text-sm · 14 (all small text on the site has one size)</td></tr>
          <tr><td class="py-2 pr-4">Caption</td><td class="pr-4"><code class="cls">.lineup-card-body</code></td><td colspan="5">text-xs · 12</td></tr>
        </tbody></table></div>
      <h3 class="label">Space, radius, motion</h3>
      <div class="grid gap-4 text-sm md:grid-cols-3">
        <div class="border-t border-rule pt-3"><code class="cls">px-pad</code> 20 → 40px<br><code class="cls">pl-hang</code> 2.1rem → 3.2rem<br><code class="cls">max-w-page</code> 1440px<br><code class="cls">gap-x-3.5 md:gap-x-6</code> columns</div>
        <div class="border-t border-rule pt-3"><code class="cls">rounded-sm</code> peek (4px)<br><code class="cls">rounded-2xl</code> photos, tiles, cards (16px)<br><code class="cls">rounded-full</code> pills, faces, capsules<br>buttons and KPI: no radius</div>
        <div class="border-t border-rule pt-3"><code class="cls">ease-expo</code> cubic-bezier(.22,1,.36,1)<br>200ms opacity · 250ms invert · 300–500ms dim/filter · 450ms unfold/slide<br><code class="cls">animate-blink</code> 1.6s (live)</div>
      </div>'''))

# ---------------- Typography
out.append(S('Foundations', 'type', 'Typography',
 'The system has two fonts and two sizes. Use Display (Inter Tight, in place of Favorit) only for the large size. Use Geist for all small text. <code class="cls">.sup</code> is a small note. It hangs from the cap line of a large word. Use it for track numbers and timer units.',
 spec('Display', 'display', '''
          <p class="display">This may be the last frontier.</p>''') +
 spec('Display mid', 'display-mid', '''
          <h3 class="display-mid max-w-[20ch]">Rebuilding Healthcare’s Front Door with AI</h3>''') +
 spec('Label + text + muted', 'label text muted faint', '''
          <span class="label">The Lineup Is Taking Shape</span>
          <p class="text max-w-[52ch]">Barcelona’s annual gathering exploring the future through the lens of technology.</p>
          <p class="text muted">December 2–3, 2026 · Llotja de Mar</p>
          <p class="text faint">7 days to go</p>''') +
 spec('Superscript annotation', 'sup num', '''
          <p class="display">AI-Native<span class="sup">1</span></p>
          <p class="display num">06<span class="sup">days</span> 09<span class="sup">hours</span></p>''') +
 spec('Lead', 'text-lead measure', '''
          <p class="text-lead measure">Two days exploring the future of the world through the lens of technology.</p>''')))

# ---------------- Layout
out.append(S('Foundations', 'layout', 'Grid and layout',
 '<code class="cls">.wrap</code> is a 1440px container with 20/40px side space. <code class="cls">.col</code> is the single text edge (hang indent). <code class="cls">.hang</code> puts an item in the margin to the left of the edge. <code class="cls">.grid-12</code> is a 12-column grid. <code class="cls">.section</code> sets the vertical space between sections.',
 spec('wrap · col · hang', 'wrap col hang section-head divider', '''
          <div class="wrap !px-0">
            <div class="col relative border-l border-dashed border-flame/60">
              <span class="hang text-flame">01</span>
              <div class="section-head"><span class="label !mb-0">Section label</span><a class="link" href="#">See all</a></div>
              <p class="display-mid divider pt-4">Text edge starts here; numbers hang in the margin.</p>
            </div>
          </div>''') +
 spec('12-column grid', 'grid-12', '''
          <div class="grid-12">
            <div class="col-span-12 md:col-span-7 rounded-2xl bg-tile p-4">7</div>
            <div class="col-span-12 md:col-span-5 rounded-2xl bg-tile p-4">5</div>
          </div>''')))

# ---------------- Links & buttons
out.append(S('Components', 'links', 'Links',
 'A link has a 1px bottom border. In display text, the border is 0.04em. On hover, the opacity goes to 70%. On <code class="cls">.link-grow</code> and <code class="cls">.nav-link</code>, the line grows from left to right.',
 spec('Links', 'link link-icon link-grow nav-link', '''
          <p class="flex flex-wrap gap-6"><a class="link" href="#">Register now</a><a class="link-grow" href="#">Relive past editions</a><a class="nav-link" href="#">Cases</a><a class="link-icon" href="#">Read the manifesto <i data-lucide="arrow-right"></i></a></p>
          <p class="display mt-6"><a class="link" href="#">Register now</a></p>''')))

out.append(S('Components', 'buttons', 'Buttons',
 'A button is a rectangle with a 1px border and the display font. It has no round corners. On hover, the colors invert (fg and bg) in 250ms. Buttons also work on light backgrounds and bands. They get their colors from currentColor and the tokens.',
 spec('Outline / solid', 'btn btn-solid', '''
          <div class="flex flex-wrap items-center gap-4">
            <a class="btn" href="#"><span>See the full agenda</span><i data-lucide="arrow-right"></i></a>
            <a class="btn btn-solid" href="#">Register</a>
          </div>''') +
 spec('Sizes', 'btn-sm btn btn-lg', '''
          <div class="flex flex-wrap items-end gap-4">
            <a class="btn btn-sm" href="#">Small</a>
            <a class="btn" href="#">Default</a>
            <a class="btn btn-lg" href="#">Large</a>
          </div>''') +
 spec('States & round', 'btn[disabled] btn-round', '''
          <div class="flex flex-wrap items-center gap-4">
            <button class="btn" type="button" disabled>Sold out</button>
            <button class="btn-round" type="button" aria-label="Menu"><i data-lucide="menu"></i></button>
            <button class="btn-round" type="button" aria-label="Close"><i data-lucide="x"></i></button>
            <button class="btn-round" type="button" aria-label="Next"><i data-lucide="arrow-right"></i></button>
          </div>''') +
 spec('On positive band', 'band btn', '''
          <div class="band px-6"><a class="btn" href="#"><span>Full agenda</span><i data-lucide="arrow-right"></i></a></div>''', '!p-0') +
 '''      <p class="text muted -mt-4 mb-10"><code class="cls">.fab</code> is the floating call to action: <code class="cls">&lt;a class="fab" href="#"&gt;&lt;span class="btn"&gt;Register&lt;/span&gt;&lt;/a&gt;</code>. It shows after the first screen (the script adds <code class="cls">.is-on</code>). On phones, it is filled and large. You can see it at the bottom right of this page.</p>'''))

out.append(S('Components', 'switch', 'Switch',
 'The switch is a capsule with a sliding knob: <code class="cls">.switch</code> (button role="switch") contains <code class="cls">.switch-track</code>, <code class="cls">.switch-knob</code> and two <code class="cls">.switch-opt</code> items. <code class="cls">aria-checked</code> holds the state. With <code class="cls">data-switch="theme"</code>, the switch changes the light/dark theme. The page keeps this choice.',
 spec('Theme & language', 'switch switch-track switch-knob switch-opt', '''
          <div class="flex flex-wrap items-center gap-8">
            <button class="switch" type="button" role="switch" aria-checked="false" data-switch="theme" aria-label="Light theme">
              <span class="switch-track" aria-hidden="true"><span class="switch-knob"></span><span class="switch-opt"><i data-lucide="sun"></i></span><span class="switch-opt"><i data-lucide="moon"></i></span></span>
            </button>
            <button class="switch" type="button" role="switch" aria-checked="false" aria-label="Language">
              <span class="switch-track" aria-hidden="true"><span class="switch-knob"></span><span class="switch-opt">RU</span><span class="switch-opt">EN</span></span>
            </button>
          </div>''')))

out.append(S('Components', 'chips', 'Chips, pills, meta',
 '<code class="cls">.chip</code> with <code class="cls">.dot</code> shows a category with a color dot. Set the color with a utility such as bg-flame. <code class="cls">.pill</code> is an outlined pill. <code class="cls">.pill-live</code> adds a blinking dot. <code class="cls">.meta</code> is a row for date, category and status.',
 spec('Meta row', 'meta chip dot pill pill-live pill-solid', '''
          <p class="meta"><span>02/12 · 15:30</span><span class="chip"><i class="dot bg-flame"></i>AI-Native</span><span class="pill pill-live"><i class="dot"></i>Live experiment</span><span class="muted">Keynote</span></p>
          <p class="meta mt-4"><span class="chip"><i class="dot bg-flame"></i>AI</span><span class="chip"><i class="dot bg-amber"></i>Investment</span><span class="chip"><i class="dot bg-sand"></i>Robotics</span><span class="chip"><i class="dot bg-ice"></i>Gaming</span><span class="chip"><i class="dot bg-sky"></i>Health</span><span class="chip"><i class="dot bg-azure"></i>Creativity</span><span class="pill pill-solid">New</span></p>''')))

# ---------------- Header / hero
out.append(S('Sections', 'header', 'Header and menu',
 'The original site has no navigation bar. Its logo is in the hero, and its switches are in the corners. This header uses the same rules: a framed logo, small links with a growing line and the theme capsule. On phones, a round button opens a full-screen menu. When you point at one menu link, the other links dim.',
 spec('Header', 'header header-bar header-nav header-actions logo nav-link btn-round', '''
          <div class="relative h-28 overflow-hidden rounded-2xl border border-rule">
            <header class="header">
              <div class="header-bar">
                <a class="logo" href="#"><span>Videsign</span><span>Studio</span><span>2026</span></a>
                <nav class="header-nav"><a class="nav-link" href="#">Services</a><a class="nav-link" href="#">Cases</a><a class="nav-link" href="#">Contact</a></nav>
                <div class="header-actions">
                  <button class="btn-round md:hidden" type="button" data-menu="menu" aria-label="Open menu"><i data-lucide="menu"></i></button>
                </div>
              </div>
            </header>
          </div>''', '!p-3') +
 spec('Mobile menu (open it)', 'menu menu-top menu-list menu-link menu-foot', '''
          <button class="btn btn-sm" type="button" data-menu="menu"><span>Open menu</span><i data-lucide="menu"></i></button>''') +
 spec('Logo lockup', 'logo', '''
          <span class="logo"><span>Tech Spirit</span><span>Barcelona</span><span>2026</span></span>''')))

out.append(S('Sections', 'hero', 'Hero',
 'The title is at the center of the first screen. The hero footer (description and links) is at the bottom. It uses the same <code class="cls">.col</code> edge as all text below. <code class="cls">.hero-bg</code> is an empty slot for the WebGL/three.js layer. Now it contains only the CSS line <code class="cls">.horizon</code>. <code class="cls">.lockup</code> is a grid that puts the second and third words in one column.',
 spec('Hero', 'hero hero-bg horizon lockup lockup-a lockup-b lockup-c hero-foot hero-info hero-actions', '''
          <section class="hero !min-h-160 !pb-64 rounded-2xl border border-rule">
            <div class="hero-bg"><span class="horizon"></span></div>
            <h1 class="lockup"><span class="lockup-a">The</span> <span class="lockup-b">last</span> <span class="lockup-c">frontier</span></h1>
            <div class="hero-foot"><div class="col">
              <span class="logo"><span>Tech Spirit</span><span>Barcelona</span><span>2026</span></span>
              <p class="hero-info"><span>Barcelona’s annual gathering exploring the future.</span><span>December 2–3, 2026 · Llotja de Mar</span></p>
              <p class="hero-actions"><a class="link" href="#">Register now</a><a class="link" href="#">See the agenda</a></p>
            </div></div>
          </section>''', '!p-0')))

out.append(S('Sections', 'band', 'Band, KPI, peek',
 '<code class="cls">.band</code> is a full-width band in positive: it inverts the page (fg background, bg text). Put the key sentence in it as display text. <code class="cls">.peek</code> rotates photos. On hover, the photo gets its color, the frame shrinks and the caption line grows. <code class="cls">.kpi</code> is a bordered grid with an offset shadow of two lines.',
 spec('Band + peek', 'band band-row peek peek-frame peek-img peek-caption peek-title peek-count', '''
          <section class="band">
            <div class="wrap band-row">
              <div class="col"><p class="display max-w-[22ch]"><span data-count="2">2</span> days. <span data-count="100" data-suffix="+">100+</span> speakers.</p></div>
              <a class="peek" href="#">
                <span class="peek-frame"><img class="peek-img is-on" alt="" src="https://picsum.photos/seed/vd-b1/800/600"><img class="peek-img" alt="" src="https://picsum.photos/seed/vd-b2/800/600"></span>
                <span class="peek-caption"><span class="peek-title">Relive past editions</span><span class="peek-count"><span data-peek-n>01</span> / 02</span></span>
              </a>
            </div>
          </section>''', '!p-0') +
 spec('KPI', 'kpi kpi-cell kpi-value kpi-label', '''
          <div class="col"><div class="kpi">
            <p class="kpi-cell"><span class="kpi-value">2</span><span class="kpi-label">days</span></p>
            <p class="kpi-cell"><span class="kpi-value">100+</span><span class="kpi-label">speakers</span></p>
            <p class="kpi-cell"><span class="kpi-value">4,000+</span><span class="kpi-label">attendees</span></p>
            <p class="kpi-cell"><span class="kpi-value">6</span><span class="kpi-label">tracks</span></p>
          </div></div>''', '!pb-12')))

# ---------------- LINEUP
def person(name, org, color, img, sess, when):
    return f'<span class="lineup-item" data-img="{FACE(img)}" data-title="{name}" data-sub="{org}" data-text="{sess}" data-meta="{when}"><span class="lineup-media"><img class="lineup-face" alt="" src="{FACE(img)}"></span><span class="lineup-name">{name}</span> <span class="lineup-sub {color}">{org}</span></span>'
people = '\n            '.join([
  person('Susana Amorós','Nimble Diagnostics','text-sky',5,'Rebuilding Healthcare’s Front Door','03/12 · 12:00'),
  person('Víctor Durán','Prosper AI','text-sky',11,'Rebuilding Healthcare’s Front Door','03/12 · 12:00'),
  person('Bernat Farrero','Factorial','text-flame',13,'The Unfiltered Truth About Scaling Up','02/12 · 11:45'),
  person('Jorgina Prado','Protofy','text-sand',9,'From bits to atoms','02/12 · 17:00'),
  person('Marcos Valera','ElevenLabs','text-flame',12,'AI has a voice. Would you give it your job?','02/12 · 15:30'),
  person('Mateo Valero','BSC','text-sand',60,'Chips for the next decade','03/12 · 10:00')])
def service(i, icon, name, sub, color, text, meta):
    return f'<span class="lineup-item" data-icon="{icon}" data-title="{name}" data-sub="{sub}" data-text="{text}" data-meta="{meta}"><span class="lineup-media"><span class="lineup-icon"><i data-lucide="{icon}"></i></span></span><span class="lineup-name">{name}<span class="lineup-num">{i:02d}</span></span> <span class="lineup-sub {color}">{sub}</span></span>'
services = '\n            '.join([
  service(1,'pen-tool','Brand identity','Strategy','text-flame','Logo, type, colour and rules that scale.','4–8 weeks'),
  service(2,'layout-grid','Product design','UX/UI','text-amber','From first flow to production-ready UI.','6–16 weeks'),
  service(3,'layers','Design systems','Tokens','text-sand','One source of truth for design and code.','4–10 weeks'),
  service(4,'clapperboard','Motion','WebGL','text-ice','Motion language, 3D and real-time scenes.','2–8 weeks'),
  service(5,'code','Development','Front-end','text-sky','Static sites and front-ends shipped with the system.','4–12 weeks')])
def case(name, sub, color, seed, text, year, pair=False):
    media = f'<img class="lineup-face" alt="" src="{PIC(seed)}">' + (f'<img class="lineup-face" alt="" src="{PIC(seed+"b")}">' if pair else '')
    return f'<a class="lineup-item" href="#" data-img="{PIC(seed,400,400)}" data-title="{name}" data-sub="{sub}" data-text="{text}" data-meta="{year}"><span class="lineup-media{" is-pair" if pair else ""}">{media}</span><span class="lineup-name">{name}</span> <span class="lineup-sub {color}">{sub.split(" · ")[0]}</span></a>'
cases = '\n            '.join([
  case('Nimble Diagnostics','Health · Brand + product','text-sky','vd-c1','A calmer patient app: bookings up 38%.','2025'),
  case('Prosper AI','AI-Native · Product','text-flame','vd-c2','Voice-agent console for healthcare teams.','2025'),
  case('Protofy','Robotics · Identity','text-sand','vd-c3','An identity that moves like its machines.','2024'),
  case('Orbit Games','Gaming · Motion + web','text-ice','vd-c4','A launch site with a real-time world.','2023', True),
  case('Llotja Studio','Creativity · Art direction','text-azure','vd-c5','Campaign for a 600-year-old building.','2023')])

out.append(S('Lineup', 'lineup', 'Lineup — «The Lineup Is Taking Shape»',
 '''This is the main pattern for <b>cases and services</b>. On desktop, it is one paragraph of large display text. Each item has a media pill, a name and a sub-label. A « / » separates the items. The media (face, thumbnail or icon) sits in the line like a letter. It is 0.74em high and 1.12em wide, fully round, and black and white. An accent color shows the sub-label (company or category). <b>On hover or focus</b>, the other items dim to 28%. The photo gets its color. A preview card (200px, rounded-2xl, tile) moves with the pointer. <b>On phones</b>, the paragraph becomes a list. Each row has a top line, 64×80 media on the left, and the name and sub-label on two lines. A tap shows the card at the bottom of the screen. A second tap on a link opens it. The card gets its data from <code class="cls">data-img | data-icon</code>, <code class="cls">data-title</code>, <code class="cls">data-sub</code>, <code class="cls">data-text</code> and <code class="cls">data-meta</code>. Put an empty <code class="cls">.lineup-card</code> next to the list.''',
 spec('People (original)', 'lineup lineup-item lineup-media lineup-face lineup-name lineup-sub lineup-more lineup-card', f'''
          <div class="col">
          <span class="label">The Lineup Is Taking Shape</span>
          <p class="lineup">
            {people}
            <a class="lineup-more" href="#">and many more…</a>
          </p>
          <div class="lineup-card" aria-hidden="true"></div>
          </div>''') +
 spec('Services (icons + numbers)', 'lineup lineup-icon lineup-num lineup-card-icon', f'''
          <div class="col">
          <span class="label">What we do</span>
          <p class="lineup">
            {services}
            <a class="lineup-more" href="#">and something new…</a>
          </p>
          <div class="lineup-card" aria-hidden="true"></div>
          </div>''') +
 spec('Cases (thumbnails, links, pair)', 'lineup a.lineup-item lineup-media.is-pair', f'''
          <div class="col">
          <span class="label">Selected cases</span>
          <p class="lineup">
            {cases}
            <a class="lineup-more" href="#">all cases…</a>
          </p>
          <div class="lineup-card" aria-hidden="true"></div>
          </div>''') +
 '''      <div class="grid gap-4 text-sm md:grid-cols-3">
        <div class="border-t border-rule pt-3"><b class="font-semibold">States</b><br><code class="cls">.lineup.is-active</code>: one item has focus. All items go to 28%.<br><code class="cls">.lineup-item.is-on</code>: the active item. It is at 100%, its photo has color, and its icon inverts.<br><code class="cls">.lineup-card.is-on</code>: the card is visible.</div>
        <div class="border-t border-rule pt-3"><b class="font-semibold">How the parts work together</b><br>One display size, one accent color for the sub-label, and media that acts like a letter. The « / » separators at 25% give rhythm without lines. The list dims other items. It does not highlight the active item. Tracks and the menu use the same method.</div>
        <div class="border-t border-rule pt-3"><b class="font-semibold">Accessibility</b><br>The script adds <code class="cls">tabindex="0"</code> to items that are not links. Focus shows the card next to the item. The card has <code class="cls">aria-hidden</code> because it repeats the data. <code class="cls">prefers-reduced-motion</code> stops the transitions.</div>
      </div>'''))

# ---------------- Tracks etc
out.append(S('Components', 'tracks', 'Tracks (accordion)',
 'This is a large list. A click opens an item. Hover does not open it. Hover only wakes the line: the other lines dim to 30%. The mark hangs in the hang margin. (On the original site, the mark is an animated orb.) The item opens with a <code class="cls">grid-template-rows: 0fr → 1fr</code> animation. The script does not measure the height. With <code class="cls">data-single</code>, only one item can be open. Use this list for a process or a detailed list of services.',
 spec('Tracks', 'tracks track track-btn track-mark track-name track-body tracks-sm', '''
          <div class="col">
          <ul class="tracks" data-single>
            <li class="track"><button class="track-btn" type="button" aria-expanded="false"><span class="track-mark"><i data-lucide="sparkles"></i></span><span class="track-name">AI-Native<span class="sup">1</span></span></button>
              <div class="track-body"><p>What does a company look like when it is built with AI from day one?</p></div></li>
            <li class="track"><button class="track-btn" type="button" aria-expanded="false"><span class="track-mark"><i data-lucide="trending-up"></i></span><span class="track-name">Investment<span class="sup">2</span></span></button>
              <div class="track-body"><p>Where is capital going next, and what does it take to access it?</p></div></li>
            <li class="track"><button class="track-btn" type="button" aria-expanded="false"><span class="track-mark"><i data-lucide="cpu"></i></span><span class="track-name">Robotics &amp; Hardware<span class="sup">3</span></span></button>
              <div class="track-body"><p>Intelligence is leaving the screen and entering the physical world.</p></div></li>
          </ul>
          </div>''')))

out.append(S('Components', 'numlist', 'Numbered list',
 'The number is small text. It hangs to the left of the edge, at cap height. The text does not move.',
 spec('Numbered', 'numlist numlist-item numlist-n', '''
          <div class="col"><ol class="numlist">
            <li class="numlist-item"><span class="numlist-n">01</span>Discover</li>
            <li class="numlist-item"><span class="numlist-n">02</span>Define</li>
            <li class="numlist-item"><span class="numlist-n">03</span>Deliver</li>
          </ol></div>''')))

out.append(S('Components', 'feature', 'Feature, cards, people',
 'A card is not a box. It is a 1px top line, a meta row, a title, text and people. <code class="cls">.feature</code> uses 7/5 columns with a media slot on the right. (On the original site, the slot holds an orb.) People photos are 4:5 and black and white. They get their color on hover.',
 spec('Feature', 'feature feature-body feature-title feature-desc feature-media people person person-photo person-name person-org person-role', '''
          <article class="feature">
            <div class="feature-body">
              <p class="meta"><span>02/12 · 15:30</span><span class="chip"><i class="dot bg-flame"></i>AI-Native</span><span class="pill pill-live"><i class="dot"></i>Live experiment</span></p>
              <h3 class="feature-title">AI has a voice. Would you give it your job?</h3>
              <div class="feature-desc"><p>Three Barcelona startups and their voice agents put to the test.</p></div>
              <ul class="people">
                <li class="person"><img class="person-photo" alt="" src="https://i.pravatar.cc/300?img=12"><span><span class="person-name">Marcos Valera</span><span class="person-org text-flame">ElevenLabs</span><span class="person-role">Host</span></span></li>
                <li class="person"><img class="person-photo" alt="" src="https://i.pravatar.cc/300?img=33"><span><span class="person-name">Dani Diestre</span><span class="person-org text-flame">Autentic AI</span></span></li>
                <li class="person"><img class="person-photo" alt="" src="https://i.pravatar.cc/300?img=52"><span><span class="person-name">Emilio Bujosa</span><span class="person-org text-flame">Supersonik</span></span></li>
              </ul>
            </div>
            <div class="feature-media"></div>
          </article>''') +
 spec('Sessions / case cards', 'sessions session session-title session-desc', '''
          <ul class="sessions !mt-0">
            <li class="session">
              <p class="meta"><span>03/12 · 12:00</span><span class="chip"><i class="dot bg-sky"></i>Health</span><span class="muted">Keynote</span></p>
              <h4 class="session-title">Rebuilding Healthcare’s Front Door with AI</h4>
              <div class="session-desc"><p>Before a patient sees a doctor, calls must be answered and appointments scheduled.</p></div>
            </li>
            <li class="session">
              <p class="meta"><span>02/12 · 11:45</span><span class="chip"><i class="dot bg-flame"></i>AI-Native</span><span class="muted">Panel</span></p>
              <h4 class="session-title">The Unfiltered Truth About Scaling Up</h4>
              <div class="session-desc"><p>Size matters. Or does it?</p></div>
            </li>
          </ul>''')))

out.append(S('Components', 'mosaic', 'Mosaic',
 'This is a dense grid (grid-flow-dense) of tiles with different sizes and rounded-2xl corners. The caption is hidden. On desktop, it shows on hover. On touch screens, it shows when the tile crosses the middle of the screen. Sizes: <code class="cls">.tile-6x3 .tile-6x2 .tile-4x3 .tile-4x2 .tile-3x3 .tile-3x2</code> (columns × rows on the 12-column grid).',
 spec('Mosaic', 'mosaic tile tile-cap tile-6x3 tile-3x3 tile-3x2', '''
          <div class="mosaic">
            <figure class="tile tile-6x3"><img alt="" src="https://picsum.photos/seed/vd-t1/1200/800"><figcaption class="tile-cap"><span>Opening keynote</span><em>2025</em></figcaption></figure>
            <figure class="tile tile-3x3"><img alt="" src="https://picsum.photos/seed/vd-t2/600/800"><figcaption class="tile-cap"><span>Backstage</span><em>2024</em></figcaption></figure>
            <figure class="tile tile-3x3">Empty tile</figure>
          </div>''')))

out.append(S('Components', 'countdown', 'Countdown',
 'The countdown uses display digits with tabular-nums. The units are in <code class="cls">.sup</code>. Set <code class="cls">data-countdown</code> to an ISO date with a time zone.',
 spec('Countdown', 'countdown countdown-unit sup', '''
          <span class="label">Counting down to 2 December</span>
          <p class="countdown" data-countdown="2026-12-02T09:00:00+01:00">
            <span class="countdown-unit"><span data-unit="d">00</span><span class="sup">days</span></span>
            <span class="countdown-unit"><span data-unit="h">00</span><span class="sup">hours</span></span>
            <span class="countdown-unit"><span data-unit="m">00</span><span class="sup">minutes</span></span>
            <span class="countdown-unit"><span data-unit="s">00</span><span class="sup">seconds</span></span>
          </p>''')))

out.append(S('Components', 'reveal', 'Word reveal',
 'For a manifesto: each word starts at 16% opacity. The words light up as you scroll. In a <code class="cls">.drawer</code>, they light up in sequence. Add the <code class="cls">data-reveal</code> attribute to the paragraph.',
 spec('Reveal', 'reveal word data-reveal', '''
          <p class="reveal" data-reveal>The horizon is no longer ahead of us. We’re already crossing it.</p>''')))

out.append(S('Components', 'drawer', 'Drawer',
 'On desktop, the drawer opens from the right (640px). On phones, it opens from the bottom as a sheet with a grab bar. The scrim is at 55%. To close the drawer, click outside it, click Close or push Esc. The slide takes 450ms with ease-expo.',
 spec('Drawer trigger', 'drawer scrim drawer-grab drawer-close', '''
          <button class="link-icon cursor-pointer" type="button" data-open="doc-drawer">Read the manifesto <i data-lucide="arrow-right"></i></button>''')))

out.append(S('Sections', 'partners', 'Partners and logos',
 'A line and a label separate the tiers. Logos are white on black at 80% opacity, and 100% on hover. This page uses text placeholders (<code class="cls">.logo-mark</code>). For SVG logos, put an &lt;img&gt; in each &lt;li&gt;.',
 spec('Tiers', 'tier logos logos-lg logo-mark', '''
          <div class="tier"><span class="label">Main partners</span>
            <ul class="logos logos-lg"><li class="logo-mark">CaixaBank</li><li class="logo-mark">Damm</li><li class="logo-mark">EAE</li><li class="logo-mark">MWCapital</li></ul></div>
          <div class="tier"><span class="label">Global partners</span>
            <ul class="logos"><li class="logo-mark">adamo</li><li class="logo-mark">airbnb</li><li class="logo-mark">bis</li><li class="logo-mark">Danone</li><li class="logo-mark">deel.</li><li class="logo-mark">esade</li><li class="logo-mark">olx</li></ul></div>''')))

out.append(S('Sections', 'forms', 'Forms',
 'The original site has no forms. These forms use the same design language. Fields have only a bottom line, like the dividers. Labels are small, dimmed text. On focus, the line changes to fg. <code class="cls">.input-big</code> is a field with display text. <code class="cls">.choice</code> is a checkbox pill (CSS <code class="cls">:has(:checked)</code>).',
 spec('Form', 'form field field-full field-label field-hint field-error input input-big textarea select-wrap select check choice', '''
          <form class="form" onsubmit="event.preventDefault()">
            <label class="field field-full"><span class="field-label">Project name</span><input class="input input-big" type="text" placeholder="What comes next"></label>
            <label class="field"><span class="field-label">Email</span><input class="input" type="email" placeholder="you@company.com"><span class="field-hint">We reply within a day.</span></label>
            <label class="field"><span class="field-label">Phone</span><input class="input" type="tel" value="+34 000" aria-invalid="true"><span class="field-error">Check the number</span></label>
            <label class="field"><span class="field-label">Budget</span><span class="select-wrap"><select class="select"><option>€10–25k</option><option>€25–60k</option></select><i data-lucide="chevron-down"></i></span></label>
            <div class="field"><span class="field-label">Services</span><div class="flex flex-wrap gap-2"><label class="choice"><input type="checkbox" checked>Brand</label><label class="choice"><input type="checkbox">Product</label><label class="choice"><input type="checkbox">Motion</label></div></div>
            <label class="field field-full"><span class="field-label">Message</span><textarea class="textarea" placeholder="A few lines are enough"></textarea></label>
            <label class="check field-full"><input type="checkbox">I agree to the privacy policy.</label>
            <p class="field-full"><button class="btn" type="submit"><span>Send</span><i data-lucide="arrow-right"></i></button></p>
          </form>''')))

out.append(S('Sections', 'footer', 'Footer',
 'The footer has four key/value columns below a line. The key is at 50%. On phones, each fact has its own row. The bottom has space for the floating button.',
 spec('Info grid', 'footer info-grid info-key', '''
          <div class="col"><div class="info-grid">
            <div><span class="info-key">When</span><span>2 and 3 December 2026</span></div>
            <div><span class="info-key">Where</span><span>Llotja de Mar, Barcelona</span></div>
            <div><span class="info-key">Contact</span><a class="link" href="#">hello@techbarcelona.com</a></div>
            <div><span class="info-key">Organised by</span><a class="link" href="#">Tech Barcelona</a></div>
          </div></div>''')))

# ---------------- page
groups = []
for g, i, t in NAV:
    if not groups or groups[-1][0] != g: groups.append((g, []))
    groups[-1][1].append((i, t))
nav = ''.join(f'<span class="doc-nav-group">{g}</span>' + ''.join(f'<a href="#{i}">{t.split(" — ")[0]}</a>' for i, t in items) for g, items in groups)
menu_links = ''.join(f'<a class="menu-link" href="#{i}">{t.split(" — ")[0]}</a>' for i, t in [(x[1], x[2]) for x in NAV if x[1] in ('tokens','buttons','lineup','tracks','forms')])

page = f'''<!doctype html>
<html lang="en" data-theme="dark">
<head>
  <!-- VIDESIGN:HEAD -->
  <!-- /VIDESIGN:HEAD -->
  <title>Videsign — design system</title>
  <meta name="description" content="Videsign: design system on HTML + Tailwind CSS v4 + Lucide, based on techspirit.barcelona.">
  <!-- VIDESIGN:CSS -->
  <!-- /VIDESIGN:CSS -->
</head>
<body>
<!-- generated by tools/docs.py — edit there, then run: python3 tools/docs.py && python3 build.py -->
<div class="flex">
  <aside class="doc-nav" aria-label="Sections">
    <a class="logo !mb-2 !text-fg" href="#top"><span>Videsign</span><span>Design</span><span>System</span></a>
    {nav}
    <span class="doc-nav-group">More</span><a href="example.html">Example landing →</a>
  </aside>
  <main class="min-w-0 flex-1" id="top">
    <header class="flex items-center justify-between gap-4 px-pad pt-6 pb-4">
      <span class="label !mb-0 muted">v1.0 · Tailwind v4 · Lucide</span>
      <div class="header-actions">
        <a class="nav-link hidden text-sm sm:inline" href="example.html">Example</a>
        <button class="switch" type="button" role="switch" aria-checked="false" data-switch="theme" aria-label="Light theme">
          <span class="switch-track" aria-hidden="true"><span class="switch-knob"></span><span class="switch-opt"><i data-lucide="sun"></i></span><span class="switch-opt"><i data-lucide="moon"></i></span></span>
        </button>
        <button class="btn-round lg:hidden" type="button" data-menu="menu" aria-label="Open menu"><i data-lucide="menu"></i></button>
      </div>
    </header>
    <div class="px-pad pt-16 pb-20 md:pt-28">
      <div class="col">
        <span class="label">Design system based on techspirit.barcelona</span>
        <h1 class="display max-w-[14ch]">Two sizes. One edge. Light by dimming.</h1>
      </div>
    </div>
{''.join(out)}
  </main>
</div>

<a class="fab" href="example.html" data-after="#overview"><span class="btn">Example</span></a>

<div class="menu" id="menu" role="dialog" aria-label="Menu">
  <div class="menu-top">
    <span class="logo"><span>Videsign</span><span>Design</span><span>System</span></span>
    <button class="btn-round" type="button" data-menu="menu" aria-label="Close menu"><i data-lucide="x"></i></button>
  </div>
  <nav class="menu-list">{menu_links}<a class="menu-link" href="example.html">Example</a></nav>
  <div class="menu-foot"><span>Videsign</span><a class="link" href="https://github.com/markxxv/videsign">GitHub</a></div>
</div>

<div class="scrim" id="doc-drawer-scrim" hidden></div>
<aside class="drawer" id="doc-drawer" data-scrim="doc-drawer-scrim" role="dialog" aria-modal="true" aria-label="Manifesto" hidden>
  <span class="drawer-grab"></span>
  <button class="drawer-close" type="button" data-close>Close</button>
  <span class="label mb-6">Manifesto</span>
  <p class="reveal" data-reveal>For centuries, technology amplified what humans can do. Now, we’re giving them our ability to think.</p>
  <p class="reveal" data-reveal>And this may be the last frontier we cross as humans alone.</p>
  <p class="display"><a class="link" href="#">Register now</a></p>
</aside>

<script src="videsign.js"></script>
</body>
</html>
'''
(root/'index.html').write_text(page)
print('index.html written,', len(NAV), 'sections')
