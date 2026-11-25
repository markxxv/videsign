# Videsign — design system

Videsign is a design system for static websites.
It uses plain HTML, Tailwind CSS v4 (browser build from a CDN) and Lucide icons (CDN).
Its design language comes from a detailed analysis of [techspirit.barcelona](https://techspirit.barcelona/).

- `index.html` — the documentation. Each component has a live demo, its class names and a code snippet.
- `example.html` — a full landing page. It uses only Videsign components.

Live site (after you enable GitHub Pages): https://markxxv.github.io/videsign/

## Files

| File | Purpose |
|---|---|
| `index.html` | Documentation page (generated from `tools/docs.py`). |
| `example.html` | Example landing page. |
| `videsign.js` | Small behavior layer: lineup card, tracks, switch, drawer, menu, countdown, word reveal, count-up, peek, floating button. No dependencies. |
| `src/videsign.css` | **Source of truth** for tokens and components (`@theme` + `@apply`). |
| `src/head.html` | Shared `<head>` part: fonts, Tailwind CDN, Lucide CDN, favicon. |
| `build.py` | Copies `src/head.html` and `src/videsign.css` into every page, between the `VIDESIGN` markers. |
| `tools/docs.py` | Generates `index.html`. |

## Quick start

1. Copy `example.html` and give it a new name.
2. Keep the two marker blocks in `<head>` (`VIDESIGN:HEAD` and `VIDESIGN:CSS`).
3. Write your markup with the component classes.
4. Add `<script src="videsign.js"></script>` before `</body>`.

## Change the system

1. Edit `src/videsign.css` (tokens and components) or `src/head.html`.
2. Run `python3 build.py`. The script updates the style block in all pages.
3. To change the documentation, edit `tools/docs.py`. Then run `python3 tools/docs.py && python3 build.py`.

Do not edit the `<style type="text/tailwindcss">` block in a page directly. The next build replaces it.

## Publish on GitHub Pages

1. Open the repository **Settings → Pages**.
2. Set **Source** to *Deploy from a branch*.
3. Select the branch `main` and the folder `/ (root)`.
4. Push **Save**. The site opens at https://markxxv.github.io/videsign/.

The site is static. It needs no build step on GitHub. The `.nojekyll` file stops Jekyll processing.

## Rules

- Do not use `clamp()`.
- Do not use custom font sizes (`text-[..]`). Use the Tailwind scale with breakpoints, for example `text-sm lg:text-base` or `text-4xl md:text-6xl lg:text-7xl`.
- Give each component a short semantic class. Define it with `@apply` in `src/videsign.css`.
- Use utilities only for one-off changes (for example `max-w-[22ch]` or `text-flame`).
- The system has no three.js/WebGL backgrounds. `.hero-bg` and `.feature-media` are empty slots for them.

The current build has 0 `clamp()` and 0 arbitrary `text-[..]` sizes.

## Tokens

Theme colors change with `data-theme="dark|light"` on `<html>`. Dark is the default.

| Token | Class examples | Value |
|---|---|---|
| `bg` | `bg-bg`, `text-bg` | `#000` (dark) / `#fafaf8` (light) |
| `fg` | `text-fg`, `border-fg`, `text-fg/45` | `#fafaf8` / `#0b0b0b` |
| `tile` | `bg-tile` | `#1c1c1c` / `#ececec` |
| `rule` | `border-rule` | fg at 22% |
| `ink`, `paper`, `graphite`, `mist` | `bg-paper` … | fixed neutrals |
| `flame` | `text-flame`, `bg-flame` | `#fa6e1d` (AI) |
| `amber` | | `#ffa234` (Investment) |
| `sand` | | `#ffcf82` (Robotics) |
| `ice` | | `#ceedff` (Gaming) |
| `sky` | | `#9fd0ff` (Health) |
| `azure` | | `#70adfb` (Creativity) |

Other tokens:

- Fonts: `font-display` (Inter Tight), `font-sans` (Geist), `font-mono` (Geist Mono).
- Tracking: `tracking-display` (−0.035em), `tracking-mid` (−0.03em).
- Line height: `leading-display` (1.02), `leading-mid` (1.05), `leading-list` (1.2).
- Space: `px-pad` (20px → 40px from `md`), `pl-hang` / `-left-hang` (2.1rem → 3.2rem).
- Container: `max-w-page` (1440px).
- Easing: `ease-expo` = `cubic-bezier(0.22, 1, 0.36, 1)`.
- Animation: `animate-blink` (live dot).

### Type scale

| Role | Class | base | sm | md | lg | xl | 2xl |
|---|---|---|---|---|---|---|---|
| Display | `.display` | 4xl | 5xl | 6xl | 7xl | 7xl | 8xl |
| Lineup | `.lineup` | 3xl | 3xl | 5xl | 6xl | 7xl | 8xl |
| Mid | `.display-mid` | 2xl | 2xl | 3xl | 4xl | 5xl | 5xl |
| Button | `.btn` | 2xl | 2xl | 3xl | 5xl | 5xl | 5xl |
| Text, label | `.text`, `.label` | sm | | | | | |
| Card caption | `.lineup-card-body` | xs | | | | | |

### Font substitutions

| Original | Videsign | Reason |
|---|---|---|
| Favorit (Dinamo, commercial) | **Inter Tight** 400 (Google Fonts) | Free, close grotesk shapes, Cyrillic support. |
| Geist 400/600 | **Geist** 400/600 (Google Fonts) | Same font. |
| — | **Geist Mono** (code snippets in the docs) | Matches Geist. |

To use Favorit, add its `@font-face` and keep the `--font-display` stack (Favorit is the second name in the stack).

## Classes

**Layout:** `wrap`, `col`, `hang`, `grid-12`, `section`, `section-sm`, `section-head`, `divider`, `divider-strong`

**Typography:** `display`, `display-mid`, `text`, `text-lead`, `label`, `muted`, `faint`, `sup`, `num`, `measure`, `prose-stack`

**Links:** `link`, `link-big`, `link-grow`, `link-icon`, `nav-link`

**Buttons:** `btn`, `btn-solid`, `btn-sm`, `btn-lg`, `btn-round`, `fab`

**Switch:** `switch`, `switch-track`, `switch-knob`, `switch-opt` (`data-switch="theme"` for the theme)

**Chips:** `chip`, `dot`, `pill`, `pill-solid`, `pill-live`, `meta`

**Header and menu:** `header`, `header-bar`, `header-nav`, `header-actions`, `menu`, `menu-top`, `menu-list`, `menu-link`, `menu-foot`, `logo`

**Hero:** `hero`, `hero-bg`, `horizon`, `hero-title`, `lockup`, `lockup-a|b|c`, `hero-foot`, `hero-info`, `hero-actions`

**Band and KPI:** `band`, `band-row`, `kpi`, `kpi-cell`, `kpi-value`, `kpi-label`

**Peek:** `peek`, `peek-frame`, `peek-img`, `peek-caption`, `peek-title`, `peek-count`

**Lineup:** `lineup`, `lineup-item`, `lineup-media` (`is-pair`), `lineup-face`, `lineup-icon`, `lineup-num`, `lineup-name`, `lineup-sub`, `lineup-more`, `lineup-note`, `lineup-card`, `lineup-card-img`, `lineup-card-icon`, `lineup-card-body`

**Tracks:** `tracks`, `tracks-sm`, `track`, `track-btn`, `track-mark`, `track-name`, `track-body`

**Numbered list:** `numlist`, `numlist-item`, `numlist-n`

**Feature and cards:** `feature`, `feature-body`, `feature-title`, `feature-desc`, `feature-media`, `sessions`, `session`, `session-title`, `session-desc`

**People:** `people`, `people-3`, `person`, `person-photo`, `person-name`, `person-org`, `person-role`

**Mosaic:** `mosaic`, `tile`, `tile-cap`, `tile-6x3`, `tile-6x2`, `tile-4x3`, `tile-4x2`, `tile-3x3`, `tile-3x2`

**Other:** `countdown`, `countdown-unit`, `reveal`, `tier`, `logos`, `logos-lg`, `logo-mark`, `scrim`, `drawer`, `drawer-grab`, `drawer-close`, `footer`, `info-grid`, `info-key`

**Forms:** `form`, `field`, `field-full`, `field-label`, `field-hint`, `field-error`, `input`, `input-big`, `textarea`, `select-wrap`, `select`, `check`, `choice`

**State classes (set by `videsign.js`):** `is-on`, `is-active`, `is-open`, `is-hot`, `is-seen`

## The Lineup pattern (cases and services)

The section "The Lineup Is Taking Shape" is the core pattern. Use it for cases and services.

**Desktop:**

- The list is one paragraph of large display text (max 24ch wide, line height 1.2).
- Each item has three parts: a media pill, a name and a sub-label.
- The media pill sits in the line like a letter. It is 0.74em high and 1.12em wide, fully round, and black and white.
- The sub-label (company or category) has an accent color. The default is fg at 45%.
- A « / » at 25% opacity separates the items.
- The last item is a dimmed "and many more…" link.

**Hover or focus:**

1. The other items dim to 28%.
2. The active item photo gets its color. An icon pill inverts.
3. A preview card (200px, rounded-2xl, tile color) follows the pointer.

**Phone (below 768px):**

- The paragraph becomes a list. Each row has a 1px top line.
- The media is 64×80px on the left. The name and the sub-label are on two lines (30px text).
- A tap shows the card at the bottom of the screen. A second tap on a link opens the link.

**Variants:**

- People — `img.lineup-face`.
- Services — `span.lineup-icon` with a Lucide icon, plus an optional `lineup-num` number.
- Cases — `a.lineup-item` links with thumbnails. `lineup-media is-pair` shows two images.

**Card data:** set `data-img` or `data-icon`, `data-title`, `data-sub`, `data-text` and `data-meta` on each item. Put an empty `<div class="lineup-card" aria-hidden="true"></div>` next to the list.

```html
<p class="lineup">
  <a class="lineup-item" href="/cases/prosper" data-img="prosper.jpg" data-title="Prosper AI"
     data-sub="AI-Native · Product" data-text="Voice-agent console." data-meta="2025">
    <span class="lineup-media"><img class="lineup-face" alt="" src="prosper-thumb.jpg"></span>
    <span class="lineup-name">Prosper AI</span> <span class="lineup-sub text-flame">AI-Native</span>
  </a>
  <a class="lineup-more" href="/cases">all cases…</a>
</p>
<div class="lineup-card" aria-hidden="true"></div>
```

## Analysis of the original design

### 1. Two sizes, two fonts
The site uses one large size (`clamp(34px, 5.4vw, 88px)`) and one small size (14px).
Favorit is used only for the large size. Geist is used for all small text.
A mid size (0.56 × large) is used only for card titles.
Hierarchy comes from size and empty space. Bold weights are not used.
In Videsign, responsive Tailwind steps replace the fluid size.

### 2. One text edge and a hanging margin
All text starts on one vertical line (`.col`, left padding 3.2rem).
Track numbers and animated orbs hang to the left of this line.
Thus the text edge stays clean, and the marks do not push the text.

### 3. Monochrome and six signals
The base is black (#000) and off-white (#fafaf8).
Six accent colors go from warm to cold: #fa6e1d, #ffa234, #ffcf82, #ceedff, #9fd0ff, #70adfb.
Each color is one event track. The site uses color only to show meaning: a company name, a category dot.

### 4. Positive and negative
Dark is the default. A light theme is "the other side of the horizon".
Key bands (key facts, agenda) invert the page: fg background, bg text.
Buttons invert on hover. The same rule works in both themes because all colors come from two variables.

### 5. Hairlines, not boxes
A 1px line above each block separates the content. Cards have no fill and no shadow.
Only photos (16px), the peek frame (4px), pills and capsules have round corners. Buttons are square.

### 6. Attention by dimming
On hover, the site dims the other items. It does not highlight the active item.
The lineup dims to 28%, the tracks dim to 30%, the manifesto words start at 16%.
Photos are grayscale (contrast 1.12, brightness 0.86) until you point at them.

### 7. Motion
One easing for all large moves: `cubic-bezier(0.22, 1, 0.36, 1)`.
Durations: 200ms opacity, 250ms invert, 300–500ms dim and filter, 450ms drawer and accordion, 1.4s photo cross-fade.
The accordion opens with `grid-template-rows: 0fr → 1fr`. It does not measure the height.
`prefers-reduced-motion` stops all transitions.

### 8. Components on the original site
- Hero: a centered title and a bottom footer with logo, description, countdown and links.
- Two capsule switches: theme (sun/moon) and language (CAT/EN).
- Key-facts band with count-up numbers and a rotating "peek" photo link.
- Lineup of speakers (see above).
- Featured session with a WebGL orb, a meta row, chips, a "live" pill and portraits.
- Two session cards side by side.
- "See the full agenda" outlined button.
- Mosaic of past editions with hidden captions.
- Countdown with superscript units.
- Partner tiers with white logos.
- Footer info grid (When, Where, Contact, Organised by).
- Floating "Register" button. It shows after the hero.
- Manifesto drawer (right side on desktop, bottom sheet on phones) with a word-by-word reveal.
- Tracks accordion with orbs in the hanging margin.

### 9. Responsive behavior
The site has two main breakpoints: 760px and 920px. Videsign uses `md` (768px) and `lg` (1024px).
On phones: the side space goes from 40px to 20px. The hang goes from 3.2rem to 2.1rem.
The lineup becomes a list. The KPI grid goes to two columns. The footer goes to one column.
The floating button becomes filled and large.

### 10. Not in the original (derived)
The original has no navigation bar, no forms and no marquee.
Videsign adds a header, a mobile menu and forms. They use the same rules: hairlines, two sizes, dimming and inversion.
Videsign does not include a marquee.
