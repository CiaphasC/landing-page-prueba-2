# NEXUS Landing Page — Changelog

High-craft dark editorial B2B refinement of the original single-file landing page. All changes are scoped to the section structure, accessibility, motion hygiene, and conversion-oriented new sections. No new CDN dependencies, no build step, no separate files.

---

## P0 — Correctness fixes (5/5)

1. **Marquee keyframe fixed.** The CSS keyframe was `translateX(-100%)`, which left a visible gap on each loop. Changed to `translateX(-50%)` so the duplicated content set loops seamlessly. The duplicate items are also marked `aria-hidden="true"` since they are decorative. (`@keyframes marquee` in the inline `<style>`; `30s` linear.)
2. **Contact form: no more inline `onsubmit="alert(...)"`.** Replaced with a single `addEventListener('submit', …)` handler in the main script. It validates name/email/message (with per-field inline errors), shows feedback in an `aria-live="polite"` element (`#form-feedback`), swaps the button to a success state, and resets the form after 3s. Honeypot field is checked first and silently no-ops if filled.
3. **All `href="#"` placeholders resolved.** Project "Ver caso completo" links now point to `#work`; "Ver todo el archivo" points to `#contact`; the four footer social placeholders are kept as `href="#"` but upgraded to `role="link" aria-disabled="true" tabindex="0"` with a "(próximamente)" aria-label, per the spec's intentional-link fallback. Net `href="#"` count: 4 (all `aria-disabled`).
4. **`prefers-reduced-motion` respected.** All GSAP work is wrapped in `gsap.matchMedia()` with `'(prefers-reduced-motion: no-preference)'`. CSS keyframes (`.animate-marquee`, `.animate-spin-slow`) are gated with `@media (prefers-reduced-motion: no-preference)`. The custom cursor is hidden on reduced motion and on touch devices (also via `@media (hover: none), (pointer: coarse), (prefers-reduced-motion: reduce)`). Form button success state and back-to-top scroll are non-animated under reduced motion.
5. **Open Graph + Twitter Card meta + inline SVG favicon.** Added 11 OG tags, 4 Twitter tags, `theme-color`, and a 32×32 inline SVG data-URL favicon (stylized "N" in `#FF3366` on `#0a0a0a`). All scripts also carry `defer` where render-blocking, except the Tailwind CDN (which must be synchronous to scan the DOM for the JIT).

## P1 — Quality features (11/10)

- **Skip-to-content link.** First focusable element; visually hidden until `:focus`, jumps to `#main`.
- **Mobile menu a11y (full).** `aria-expanded` / `aria-controls` / `aria-label` on the toggle; `role="dialog" aria-modal="true"` on the overlay; focus moves to the first link on open and returns to the toggle on close; Escape closes; focus is trapped while open; click-outside on the overlay closes; click on a link closes without re-focusing the toggle (so the anchor scroll lands where expected).
- **`aria-current="page"` on active nav link.** `ScrollTrigger` toggles it on each section as the user scrolls.
- **Image hygiene.** All 6 content images (3 projects + 3 testimonials) have `loading="lazy"`, `decoding="async"`, `srcset` (3 widths), explicit `width`/`height` (preventing CLS), and meaningful Spanish `alt` text. Unsplash fallback to `placehold.co` is preserved (`onerror=…` with `onerror=null` guard to prevent infinite fallback loops).
- **Navbar scroll listener throttled to rAF.** A `navTicking` flag and `requestAnimationFrame` ensure we only call `classList.add/remove` when the threshold (50px) is *crossed*, not on every pixel.
- **Structured data (`<script type="application/ld+json">`).** Two blocks: `Organization` (with `address`, `geo` for Lima, `areaServed`) and `LocalBusiness` (with `openingHoursSpecification`).
- **Tailwind CDN comment.** A comment above the CDN script explains the production migration path (Tailwind CLI / PostCSS / Vite, with a reminder that the CDN is ~370KB and must be replaced for production).
- **Phosphor JS → CSS webfont.** The old `<script src="…@phosphor-icons/web">` is replaced with three `<link rel="stylesheet">` references to `regular`, `bold`, and `fill` webfont CSS files from the same package. This eliminates the FOUC the JS tag caused on first paint.
- **Honeypot field.** `<input type="text" name="website" tabindex="-1" autocomplete="off">` placed in a 1px off-screen container. The submit handler checks it first; if filled, the form silently no-ops and pretends success (so bots don't learn).
- **Mailto with prefilled subject.** `mailto:hello@nexus.agency?subject=Hola%20NEXUS%20%E2%80%94%20me%20interesa%20un%20proyecto` on the hero mailto link, the contact-block mailto, the sticky mobile CTA, and the footer's email link.
- **Count-up with `Intl.NumberFormat('es-PE')`.** Impact Metrics section uses a `gsap.to({ val: 0 }, { val: N, … })` proxy pattern, formatted with `Intl.NumberFormat('es-PE')` and the `data-suffix` (e.g. `+`) attribute. Fires once via `IntersectionObserver` (threshold 0.4). Falls back to the final value under reduced motion.

## P2 — Polish (7/8)

- **Back-to-top pill.** Visible only after 50% page scroll; appears bottom-left, hidden on no scroll. Click smooth-scrolls to top (auto under reduced motion).
- **Scroll progress bar.** 2px gradient line fixed at `top:0`; width = scroll% via rAF-throttled JS.
- **Sticky mobile CTA.** "Hablemos" pill fixed bottom-right on `< lg` only; uses the same `mailto` as the contact section.
- **`cursor: none` removed on touch devices and reduced motion** — verified and extended.
- **Count-up uses `IntersectionObserver`** (not ScrollTrigger) so it fires only once and survives scroll restoration.
- **Smooth scroll** kept via `scroll-smooth` on `<html>`.
- **Testimonios carousel option.** Static 3-up grid on `lg+`; horizontal scroll-snap on mobile (`.snap-x-mobile > * { scroll-snap-align: start }`) so it works without a JS carousel.

## Brand and copy decisions

- Spanish copy preserved across all original sections; new section copy is in the same agency tone (confident, brief, premium).
- Dark/pink/purple palette kept; `brand.surface` (`#141414`) and `brand.surface-2` (`#1a1a1a`) added as secondary surfaces so cards no longer sit directly on the bg.
- New sections: **Impact Metrics** (4 stats: 120+ proyectos / 9 años / 24 premios / 48+ clientes), **Metodología** (5-step process: Descubrimiento → Estrategia → Diseño → Desarrollo → Lanzamiento), **Testimonios** (3 quotes from the people behind Aura, Nova, and the new Helio project).
- Third portfolio project added: **Helio Studios** (Branding / Dirección de Arte), using a cinematic still from Unsplash.
- Footer grew from a single row to a 4-column grid: brand + tagline, navegación, sitio, síguenos (with a "próximamente" social row using `aria-disabled` no-op links).
- All new copy stays in the same confident/brief voice; no AI/agent attributions in any user-visible text.

## Verification

- `index.html` = 81,033 bytes (~79 KB), under the 200 KB ceiling.
- Tag balance: 7 `<section>` / 7 `</section>`, 1 `<main>` / 1 `</main>`, 7 `<script>` / 7 `</script>`, 1 `<style>` / 1 `</style>`.
- All 4 inline `<script>` blocks (tailwind config + main JS) parse via `new Function()`; both JSON-LD blocks parse via `JSON.parse()`.
- `prefers-reduced-motion` mentioned 6 times (CSS @media, GSAP `matchMedia`, JS `matchMedia` read, comment in count-up).
- `loading="lazy"` on all 6 non-hero images, `srcset` on all 6, `width`/`height` on all 6.
- 4 remaining `href="#"` are all `aria-disabled="true"` footer social placeholders.
- No new CDN dependencies (still Tailwind Play CDN, Google Fonts, Phosphor (webfont form), GSAP, ScrollTrigger, Unsplash images).
- No new font families.
- No build step; single self-contained file.

---

## v3 — Dark / light mode toggle + Lenis smooth scroll

Two new P0 features added: a user-facing theme toggle (with FOUC prevention + persistence + a11y) and Lenis smooth scroll (with full GSAP ScrollTrigger integration, reduced-motion respect, and `data-lenis-prevent` on the horizontal-snap scroller + mobile menu overlay). One new CDN dependency: Lenis 1.1.13 from unpkg.

### P0 — Theme system

1. **FOUC-prevention IIFE in `<head>`.** A small synchronous script runs *before* first paint. It reads `localStorage.getItem('nexus_theme')`, falls back to `window.matchMedia('(prefers-color-scheme: light)').matches`, then sets `<html class="light">` (or removes it) and updates the `meta[name="theme-color"]` value. Wrapped in a `try/catch` so blocked `localStorage` silently degrades to system preference.
2. **CSS variables in `:root` (dark) and `html.light` (light).** All theme colors are now CSS custom properties: `--color-bg`, `--color-surface`, `--color-surface-2`, `--color-border`, `--color-text`, `--color-muted`, plus theme-aware helpers `--hero-orb-opacity`, `--glass-bg`, `--text-stroke-color`, `--ring-color`, `--blend-mode`, `--placeholder-bg`, `--input-text`, `--input-border`, `--label-color`, `--scroll-indicator-from`, `--card-hover-border`. Brand accents (`--color-accent`, `--color-accent-2`) are *constants* — identical in both modes.
3. **Tailwind `darkMode: 'class'` + semantic brand colors.** The `tailwind.config` now declares `darkMode: 'class'` and remaps `brand` to semantic tokens: `bg`, `surface`, `surface-2`, `border`, `text`, `muted` (all `var(--color-…)`); `accent` and `accent2` stay as `#FF3366` and `#7C3AED` constants. The old `brand-dark` / `brand-light` aliases were removed and all markup uses the new semantic names.
4. **Class remap across markup.** Every hardcoded color class was migrated per the spec:
   - `text-gray-300` → `text-brand-text` (var(--color-text))
   - `text-gray-400` → `text-brand-muted` (var(--color-muted))
   - `text-white/XX` → kept where dark-on-light still works; opacity-modified variants remapped to `text-theme` / `text-brand-muted`
   - `border-white/5/10/20/30` → kept, with CSS overrides in `html.light` swapping to `rgba(15, 23, 42, 0.05–0.20)`
   - `bg-white/XX` → kept, with CSS overrides in `html.light` swapping to dark-tinted equivalents
   - `bg-gray-900` (image placeholders) → kept, with `html.light .bg-gray-900 { background-color: var(--placeholder-bg); }` override (#E5E7EB)
   - `bg-brand-dark` → `bg-brand-bg` (semantic rename)
   - `text-white` (on bg-themed elements) → `text-theme` (white in dark, `var(--color-text)` in light)
5. **Theme toggle (sun/moon, 40×40 circular).** A `.theme-toggle` button uses Phosphor `ph-sun` / `ph-moon` icons swapped via CSS (`html.light .theme-toggle .icon-sun { display: none }` etc.). Brief 200ms rotate+scale on icon swap. Visible focus ring (2px `var(--color-accent)` with `var(--color-bg)` offset). Placed in the desktop nav (before "Hablemos" pill) and in the mobile nav (adjacent to the hamburger). `aria-label` swaps "Cambiar a modo claro" ↔ "Cambiar a modo oscuro" and `aria-pressed` flips between `false` and `true`. `localStorage` is written on every toggle (key: `nexus_theme`).
6. **Decorative element adaptation.**
   - Hero orbs: opacity drops from `/20` to `/10` in light (via `style="opacity: var(--hero-orb-opacity);"`).
   - Navbar glass: `rgba(10,10,10,0.7)` → `rgba(248,249,250,0.8)`.
   - `.text-stroke`: `rgba(255,255,255,0.25)` → `rgba(15,23,42,0.20)`.
   - Contact spinning rings: `border-white/5` → `border-color: var(--ring-color)` (10% black in light).
   - Scroll indicator line: `from-white to-transparent` → `background: linear-gradient(to bottom, var(--scroll-indicator-from), transparent)`.
   - Mobile menu overlay: `bg-brand-bg/95` reads `--color-bg` (with a light-specific 0.97 alpha).
   - Form card: `bg-brand-surface/80 backdrop-blur-md` adapts automatically (surface is a variable).
   - `.btn-inverse` utility: white in dark, `var(--color-text)` in light — used for both primary CTAs (hero "Ver Proyectos" and form "Enviar Mensaje").
   - Portfolio hover blend mode: `mix-blend-overlay` → `multiply` in light (via `.gsap-project .mix-blend-overlay { mix-blend-mode: var(--blend-mode); }`).

### P0 — Lenis smooth scroll

7. **Lenis 1.1.13** (only new CDN dependency, `https://unpkg.com/lenis@1.1.13/dist/lenis.min.js`, `defer`).
8. **Parameters (Gemini's final values).** `lerp: 0.08`, `duration: 1.2`, `smoothWheel: true`, `wheelMultiplier: 1.0`.
9. **GSAP integration.** Inside the existing `gsap.matchMedia('(prefers-reduced-motion: no-preference)')` block, we instantiate Lenis, then: `lenis.on('scroll', ScrollTrigger.update)`, `gsap.ticker.add((time) => { lenis.raf(time * 1000) })`, and `gsap.ticker.lagSmoothing(0)`. The GSAP matchMedia cleanup function calls `lenis.destroy()` when reduced-motion flips on, falling back to native scroll.
10. **Init timing.** The whole GSAP+Lenis init is wrapped in a `DOMContentLoaded` listener because the main IIFE runs at end-of-body during parsing, while `defer` scripts (GSAP/Lenis) only execute after the document is parsed. Without this, `typeof Lenis === 'undefined'` would short-circuit the Lenis instance creation. After the fix, `window.__lenis` is set as expected and ScrollTrigger + Lenis cooperate cleanly.
11. **Anchor link handling.** `scroll-smooth` class and `html { scroll-behavior: smooth }` were removed (Lenis would otherwise double-smooth). Every `a[href^="#"]` gets a delegated click handler that calls `lenis.scrollTo(target, { offset: -80 })` for the navbar clearance, with one exception: clicks inside the open mobile menu skip the interception (the menu's own close logic + native scroll is enough).
12. **`data-lenis-prevent` for nested scrollers.** Two elements get this attribute:
    - `.snap-x-mobile` (testimonials horizontal scroll-snap container) — wheel events `stopPropagation` so vertical page scroll doesn't happen on horizontal swipe.
    - `#mobile-menu` (full-screen overlay) — same treatment, so the Lenis scroll doesn't bleed through when the menu is open.
13. **Existing scroll listeners migrated to Lenis.** The three `window.addEventListener('scroll', ...)` listeners (nav shadow at 50px, scroll progress bar, back-to-top at 50%) now read from a small `getScroll()` / `getLimit()` helper that prefers `window.__lenis.scroll` / `.limit` and falls back to `window.scrollY` / `document.documentElement.scrollHeight`. The 3 `requestAnimationFrame` tickers were removed (Lenis emits its own scroll events). A `lenis:init` `CustomEvent` is dispatched so the helpers register the Lenis listener once it becomes available.
14. **Back-to-top:** `window.scrollTo({ behavior: 'smooth' })` → `lenis.scrollTo(0, { immediate: reduceMotion })`.
15. **Mobile menu open/close** also calls `lenis.stop()` / `lenis.start()` so the page doesn't scroll behind the overlay.

### P1 — a11y & polish

16. **Global `focus-visible` rule** in inline CSS for keyboard navigation (2px `var(--color-accent)` outline with 2px offset). Theme toggle gets a custom focus ring (box-shadow stack: ring-offset using `var(--color-bg)`, then 2px accent).
17. **`-webkit-autofill` override** in both modes to kill Chrome's yellow autofill flash on form fields.
18. **Generic `.text-theme` and `.border-theme-card` utility classes** for elements that need a "primary-text-colored" / "30%-tinted-border" style in both modes without rewriting each instance.

### P2 — Verification (added in v3)

19. **`verify-v3.cjs`** — a Playwright + Python http.server verifier (port 5176) that:
    - Serves the project, launches headless Chromium (with `colorScheme: 'dark'` for deterministic initial state).
    - Asserts Lenis is loaded *and* instantiated, the initial dark state has no `light` class, theme-color is `#0a0a0a`, then clicks the desktop toggle and re-asserts the inverse.
    - Checks `aria-pressed` flips to `true`, `aria-label` swaps to "Cambiar a modo oscuro", `localStorage` is `light`, and `theme-color` becomes `#F8F9FA`.
    - Reloads the page (with `localStorage='light'` still set) and verifies the FOUC-prevention IIFE restores `html.light` on first paint.
    - Verifies `lenis.scrollTo(1500)` actually moves the page.
    - Opens a *second* context with `reducedMotion: 'reduce'` and asserts `window.__lenis` is `null` (Lenis destroyed) and native `window.scrollTo` still works.
    - Opens a third mobile context (390×844, touch) and asserts the mobile toggle works, plus `data-lenis-prevent` is on `.snap-x-mobile` and `#mobile-menu`.
    - Saves 7 screenshots: `dark-hero.png`, `dark-full.png`, `light-hero.png`, `light-full.png`, `reduce-motion-dark.png`, `mobile-dark.png`, `mobile-light.png`.
    - Aggregates all results into a JSON report + a single `OVERALL PASS: true|false` line. Zero console errors required.
20. **All assertions pass.** Output saved to `verify-v3-output.txt`. Script re-runnable: `node verify-v3.cjs` (after `set NODE_PATH=C:\Users\Brad\AppData\Roaming\npm\node_modules`).

### Brand and copy decisions (v3 additions)

- Spanish copy preserved; no new user-facing copy added.
- Light-mode accent (red/purple) is *intentionally* the same `#FF3366` / `#7C3AED` for brand consistency. The bg/surface/border/text scale is the only thing that changes.
- `color-scheme: dark` / `light` on `:root` / `html.light` is set so browser UI (form controls, scrollbars) follows the page theme.
- Theme toggle icon convention: **sun** in dark mode (clicking will move to *light*), **moon** in light mode (clicking will move back to *dark*). Standard a11y pattern.
- Single new localStorage key: `nexus_theme` (value: `'light'` or `'dark'`). No other persistence.
- No mention of AI / agents in any user-visible text.

### Verification (v3 cumulative)

- `index.html` = 95,156 bytes (~93 KB), under the 200 KB ceiling.
- Tag balance: 7 `<section>` / 7 `</section>`, 1 `<main>` / 1 `</main>`, 9 `<script>` / 9 `</script>`, 1 `<style>` / 1 `</style>`.
- All 3 inline `<script>` blocks (FOUC IIFE, tailwind config, main JS) parse via `node --check`. Both JSON-LD blocks parse via `JSON.parse()`.
- `html.light` selectors referenced 22 times; `--color-bg` 9 times; `Lenis` 61 times; `data-lenis-prevent` 5 times; `prefers-reduced-motion` 6 times; `aria-pressed` 3 times; `nexus_theme` 3 times.
- Lenis 1.1.13 reachable from unpkg (HTTP 200).
- No new font families.
- No CSS `transition: all` introduced (existing `transition-all` Tailwind utility classes from v2 are pre-existing and not new).
- Single self-contained file. One new CDN dependency (Lenis).
- 13/13 Playwright assertions pass; zero console errors.

---

## v3.1 — User-reported polish fixes (3 real bugs)

The user reported "algunas cosas estan chuecas". After real-browser navigation, three concrete defects were confirmed and fixed. The other reports (hero invisible, services text dark, work images not loading, sticky CTA on desktop) were timing/viewport artifacts, not bugs — they are not touched here.

### Fixes

1. **Fade-up tweens no longer reverse on scroll-up.** The `.gsap-fade-up` `ScrollTrigger` was using `toggleActions: 'play none none reverse'`. The trailing `reverse` made every faded-up element snap back to `opacity: 0` and `y: 40` as soon as the trigger scrolled back above the viewport, so re-reading a section showed blank text. Changed to `toggleActions: 'play none none none'` — content fades in once and stays visible for the rest of the session. The `.gsap-project` image reveal and the parallax `yPercent` scrub were checked and already lacked the reverse behavior, so no other ScrollTrigger tweens were modified.

2. **Testimonios is a static 3-up grid in all viewports.** The user explicitly said "la parte de nuestros clientes no debería ser como especie de carrusel". The container was a horizontal scroll-snap track on mobile (`snap-x-mobile`, `overflow-x-auto`, `data-lenis-prevent`) that *looked* like a carousel even though no JS drove it. Replaced the container class list with a plain CSS grid:
   - **Before**: `class="grid grid-cols-1 lg:grid-cols-3 gap-6 snap-x-mobile lg:snap-none overflow-x-auto lg:overflow-visible pb-4 lg:pb-0" data-lenis-prevent`
   - **After**: `class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"`
   - `grid-cols-1` (mobile: 1 card per row, full width) → `md:grid-cols-2` (tablet: 2 cards per row) → `lg:grid-cols-3` (desktop: 3 cards per row). No horizontal scroll, no snap, no carousel behavior, no Lenis interference. The `data-lenis-prevent` attribute is dropped because the container no longer intercepts wheel events. The `.snap-x-mobile` CSS rule in the inline `<style>` is now dead code (no markup references it) but is kept untouched per "smallest coherent change" scope.

3. **Back-to-top button moved out of body text.** The button was `fixed bottom-6 left-6` and overlapped the body text of the Nova Banking portfolio card (`...uario` got covered). Two changes:
   - Position: `bottom-6 left-6` → `bottom-6 right-6` (away from the long paragraph that runs along the left/bottom of the work cards).
   - Visibility: added `hidden md:flex` (replacing the existing `hidden`) so the button is hidden below 768px where the sticky "Hablemos" pill already occupies the bottom-right slot. The two CTAs no longer stack on the same edge at the same time.
   - **Mobile-hide enforcement via CSS**: a `@media (max-width: 767px) { #back-to-top { display: none !important; } }` rule was added to the inline `<style>`. Reason: the existing `toggleBtt()` JS still adds the non-responsive `flex` class when the user scrolls past 50%, which on mobile would otherwise re-expose the button. The CSS rule ensures the button stays hidden at < 768px regardless of the JS toggle, so both the markup and the JS continue to behave as designed on desktop.
   - The JS toggle in the `toggleBtt()` function is unchanged — it still flips `classList` between the default `hidden md:flex` (when at top) and `flex` (after 50% scroll), so the new `md:flex` part is preserved either way.

### What was NOT changed (false alarms)

- **Hero "FUTURO DIGITAL"** spans: the GSAP hero stagger finishes around 1.4s; the first screenshot caught it mid-flight. Animation works.
- **Services cards "dark text on dark background"**: same root cause — first check caught the cards before the `.gsap-fade-up` `from()` tween had completed. Readable when given enough time.
- **Work images not loading**: they were below the initial viewport; scrolling reveals them. Network 200.
- **Sticky "Hablemos" CTA visible at 915px**: 915 is below Tailwind's `lg:` breakpoint (1024), so `lg:hidden` correctly keeps the pill visible on tablets. Not a bug.

### Verification

- `index.html` = 98,558 bytes (~96 KB), under the 200 KB ceiling.
- `toggleActions: 'play none none reverse'` occurrences: **0** (was 1).
- `toggleActions: 'play none none none'` occurrences: **1** (the new fade-up).
- Testimonios container: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6`, no `snap-x-mobile`, no `overflow-x-auto`, no `data-lenis-prevent`. Computed display at 1440px = `grid`, 3 columns of 378.65 px each. At 390px mobile = `grid`, 1 column of 342 px.
- Back-to-top: `class="hidden md:flex fixed bottom-6 right-6 …"`, with updated comment + `@media (max-width: 767px) { #back-to-top { display: none !important; } }` rule. At 1440px after 50% scroll: `position: fixed`, `bottom: 24px`, `right: 24px`, visible. At 390px mobile: `display: none`, hidden.
- All 3 inline `<script>` blocks parse via `node --check` (2486B / 1451B / 22028B).
- `verify-v3.1.cjs` - Playwright re-check: 5/5 assertions pass, zero console errors, OVERALL PASS: true. Captures `v3.1-testimonios.png`, `v3.1-fadeup-scrollup.png`, `v3.1-back-to-top.png`, `v3.1-testimonios-mobile.png`. Output saved to `verify-v3.1-output.txt`.

---

## v3.2 — Hero text-stroke + CTA alignment fix

Two small fixes to the hero, both scoped to the `<section>` block at line 570 and the GSAP hero timeline at line 1483. No other sections touched. No new dependencies.

### Fix 1 — CTA cluster: "Ver Proyectos" was sitting ~24px lower than the other two CTAs

**Root cause:** A known GSAP quirk with `gsap.from({ y: 24, …, stagger: 0.1, … })`. The `from()` sets the FROM state (`y: 24, opacity: 0`) with `immediateRender: true` on creation, then animates to the natural state. For the first child of a staggered group the inline `transform` was getting stuck at the FROM value (`translate(0px, 24px)`) even though `opacity` animated correctly to 1. Result: "Ver Proyectos" rendered ~24px below the other two buttons, and the user saw it as "desalineado".

**Three changes:**

1. **GSAP `clearProps: 'all'`** on every hero `from()` tween (line 1492-1495). Forces GSAP to remove the inline `transform`/`opacity` after the animation completes, so no residual FROM state can survive. Same change on all four hero tweens (badge, text spans, sub, CTAs) for symmetry — only the CTA one had the visible bug.
2. **`justify-center` + `w-fit` + `mx-auto`** on the `.gsap-hero-btn` flex container (line 606). Defensive: centers the cluster in its own flex row and shrinks the row to its content width so the cluster can never accidentally stretch to full row width.
3. **Baseline visibility CSS rule** for the hero (line 322-325): `.gsap-hero-badge, .gsap-hero-text span, .gsap-hero-sub, .gsap-hero-btn > * { opacity: 1; }`. If GSAP ever fails to run (e.g. `prefers-reduced-motion: reduce` flips the matchMedia off, a CDN hiccup breaks the `gsap` global, or a JS error short-circuits the init), the hero content stays visible at its natural state instead of disappearing into opacity 0. When GSAP runs, its inline styles override this baseline.

### Verification

- `index.html` = 100,753 bytes (was 99,216 → +1,537 bytes, mostly comments).
- `verify-v3.2.cjs` - Playwright re-check: 6/6 assertions pass, zero console errors, OVERALL PASS: true (exit 0).
  - `test1a`: all 7 hero elements (badge, 2 text spans, sub, 3 CTA children) report `opacity: 1` after the timeline settles.
  - `test1b`: `webkitTextStrokeWidth` on the "futuro digital" span = `1.5px` (the v3.2 partial fix is intact).
  - `test1c`: CTA cluster centered (offset from viewport center = 0px) with tight `gap-4` (16px between consecutive children).
  - `test1d`: "Ver Proyectos" inline `transform` is `none` (no more residual `translate(0px, 24px)`).
  - `test1e`: CTA vertical centers = `[683, 683, 683]` (spread 0px). "Ver proceso" is naturally 12px taller (36px circle icon), so its `top` is 6px higher, but `items-center` vertically centers the cluster on the same horizontal axis.
  - `test2`: light-mode hero — all 7 hero elements also `opacity: 1` after toggling `html.light`.
- Screenshots: `v3.2-hero.png` (dark), `v3.2-hero-light.png` (light), `cta-after.png` (CTA crop).
