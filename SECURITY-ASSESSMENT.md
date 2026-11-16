# Security Assessment — Math Competition Readiness Hub

**Scope:** static site (`index.html`, `sites.json`, assets) served via GitHub Pages; client-side JS only; third-party: Leaflet (unpkg CDN), OpenStreetMap tiles, GoatCounter analytics.
**Method:** static review — secret scan, DOM-XSS sink analysis, SCA (dependency review), transport/config/CSP review.
**Date:** 2026-11 · **Assessor:** automated review (Claude Code).

> No server-side code exists, so classic web-app classes (SQLi, auth, SSRF, deserialization) are **not applicable**. Risk centers on client-side XSS, supply-chain, and hardening.

## Summary

| ID | Finding | Category | Severity | Status |
|----|---------|----------|----------|--------|
| V-01 | DOM-XSS via unescaped external data in finder | XSS | **Medium** | ✅ Fixed |
| V-02 | No Subresource Integrity (SRI) on CDN Leaflet | Supply-chain | **Medium** | ✅ Fixed |
| V-03 | No Content-Security-Policy | Hardening | **Medium** | ✅ Fixed (meta CSP) |
| V-04 | Inline event handlers / inline script require `unsafe-inline` | Hardening | Low | ⚠️ Accepted / tracked |
| V-05 | Third-party scripts (Leaflet, GoatCounter) | Supply-chain | Low | ⚠️ Accepted (SRI on Leaflet; GC has none) |
| V-06 | Owner email exposed in `mailto:` | Info disclosure | Low | ⚠️ Accepted (by design) |
| V-07 | Lead data stored in `localStorage` | Privacy | Low | ⚠️ Accepted |
| V-08 | No automated SCA / dependency monitoring | Process | Low | 🔲 Open (recommend Dependabot) |
| V-09 | Secret scan of repo | Secrets | — | ✅ Pass (none found) |

**Deps (SCA):** Leaflet **1.9.4** (latest; no known CVEs at review time). `python-pptx`, `Pillow`, `lxml` are **dev-only** (deck generation) and **not shipped** to users. Recommend confirming with `pip-audit` / Dependabot in CI.

---

## Findings

### V-01 — DOM-XSS via unescaped external data  ·  Medium  ·  ✅ Fixed
**Where:** `index.html` finder `render()` — school name/city/state from `sites.json` written via `innerHTML` and Leaflet `bindPopup` without escaping.
**Risk:** `sites.json` is generated from an external Google Sheet. A crafted school name (e.g. `<img src=x onerror=…>`) would execute in visitors' browsers.
**Fix:** added `esc()` HTML-escaper; all data-derived fields escaped before insertion into markup and map popups. CVSS ~5.4 (AV:N/UI:R).

### V-02 — No SRI on CDN-loaded Leaflet  ·  Medium  ·  ✅ Fixed
**Where:** `<link>`/`<script>` for `unpkg.com/leaflet@1.9.4`.
**Risk:** if unpkg/package is compromised, arbitrary JS executes (supply-chain).
**Fix:** added `integrity="sha384-…"` + `crossorigin="anonymous"` to both (hashes computed from the pinned 1.9.4 artifacts). Version is already pinned (not `@latest`).

### V-03 — No Content-Security-Policy  ·  Medium  ·  ✅ Fixed
**Fix:** added a `<meta http-equiv="Content-Security-Policy">` restricting origins — `default-src 'self'`; scripts limited to self/unpkg/gc.zgo.at; images to self/OSM tiles/unpkg/GoatCounter; `connect-src` to self + GoatCounter; `base-uri 'self'`; `form-action 'self'`.
**Residual:** requires `'unsafe-inline'` for script/style because the app is a single inline file (see V-04). `frame-ancestors`/HSTS can't be set via meta on GitHub Pages (no custom headers).

### V-04 — Inline handlers require `unsafe-inline`  ·  Low  ·  ⚠️ Tracked
Inline `onclick` (`copyEmail`, `printKit`) and the inline `<script>`/`<style>` force `script-src/style-src 'unsafe-inline'`, weakening CSP's XSS protection.
**Recommendation:** externalize JS/CSS into files and adopt nonce/hash-based CSP (removes `unsafe-inline`). Tracked as a hardening issue.

### V-05 — Third-party scripts  ·  Low  ·  ⚠️ Accepted
Leaflet (now SRI-pinned) and GoatCounter (`gc.zgo.at`, no SRI available for the versioned loader). GoatCounter is privacy-friendly (no cookies/PII). Accept, or self-host the counter for stricter control.

### V-06 — Owner email in `mailto:`  ·  Low  ·  ⚠️ By design
`vineetagrwal@gmail.com` appears in `mailto:` links → scrapable (spam). Intentional contact path. Mitigate later with a form backend (Formspree) instead of `mailto`.

### V-07 — Lead data in `localStorage`  ·  Low  ·  ⚠️ Accepted
Interest-form entries are kept in the visitor's own browser only (not transmitted). No cross-user exposure. Clear on submit if undesired.

### V-08 — No automated SCA  ·  Low  ·  🔲 Open
Add **Dependabot** (or `pip-audit` in CI) so Leaflet / dev-deps are monitored for future CVEs.

### V-09 — Secret scan  ·  ✅ Pass
`git grep` for `github_pat_`, `ghp_`, `Bearer`, AWS keys, PEM blocks across tracked files → **none**. PATs used during setup were passed via ephemeral `GIT_ASKPASS` and never committed or written to `.git/config`.

---

## Enterprise-readiness checklist
- [x] No secrets in repo
- [x] XSS sinks escaped
- [x] CDN deps pinned + SRI
- [x] CSP (meta) in place
- [x] All `target="_blank"` use `rel="noopener noreferrer"`
- [x] HTTPS enforced (GitHub Pages)
- [ ] Headers via meta only — no HSTS/`frame-ancestors` (GitHub Pages limitation; use a CDN/proxy for full headers)
- [ ] Strict CSP without `unsafe-inline` (needs JS/CSS externalization — V-04)
- [ ] Automated SCA / Dependabot (V-08)
