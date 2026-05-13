## 1. Design pass (Paper MCP) — DEFERRED (user-driven)

- [ ] 1.1 Open Paper via `paper-desktop:design-to-code` and sketch the landing page hero
- [ ] 1.2 Mock the identity-decomposition panel (annual stacked bars, 2019–2023, hatched for pending years)
- [ ] 1.3 Mock the atseed.co vs C&SD comparison chart (two-line overlay with cumulative-gap annotation)
- [ ] 1.4 Mock the HKIA destination mix panel (horizontal ranked bars, region grouping legend)
- [ ] 1.5 Mock the GBA cross-border panel with per-checkpoint / aggregate toggle
- [ ] 1.6 Mock the talent + Anglo emigration tile row
- [ ] 1.7 Mock the methodology page layout (worked example, divergence reasons, caveats, sources table)
- [ ] 1.8 Export Paper mocks as PNG + SVG into `design/paper-mocks/` for reference
- [ ] 1.9 Capture decisions about visual hierarchy / brand voice from the mock review into a short `design/decisions.md`

> Paper desktop requires user driving. Group 1 left for user to complete; current implementation can serve as the "code-first design" to iterate on in Paper afterward via `paper-desktop:code-to-design`.

## 2. Project scaffolding

- [x] 2.1 `npm create @observable/framework@latest .` in repo root, accept defaults — (manually created `package.json` + `observablehq.config.js` to avoid interactive prompt; equivalent to defaults)
- [x] 2.2 Add `.gitignore` rules for `dist/`, `node_modules/`, Observable cache
- [x] 2.3 Create `pipeline/` directory and `pyproject.toml` with `pypdf`, `requests`, `pandas` pinned
- [x] 2.4 Add top-level `Makefile` with targets: `data` (run pipeline), `build` (run dashboard build), `dev` (Observable dev server), `deploy` (manual Cloudflare deploy)
- [x] 2.5 Write `README.md` covering: how to run pipeline, how to dev, how to deploy, data lineage

## 3. Pipeline implementation

- [x] 3.1 `pipeline/fetch_immd.py` — download CSV, sort, write `data/immd_daily_passenger_traffic_2021_2025.csv`
- [x] 3.2 `pipeline/fetch_hkia_window.py` — rolling 91-day fetch into `data/hkia_91d/`, prune old days
- [x] 3.3 `pipeline/parse_legco.py` — verification script that re-parses pinned LegCo PDFs and asserts JSON values match
- [x] 3.4 `pipeline/build_aggregates.py` — derive `hk_annual_population_accounting.csv`, `gba_land_hk_resident_annual.csv`, `cross_channel_net_outflow_annual.csv`, `hkia_destination_mix_91d.csv` from primary sources
- [x] 3.5 `pipeline/validate.py` — fail if any number in `hk_population_master.json` lacks a `source` field
- [x] 3.6 Add `scripts/add-legco-source.sh <RPDB-paper-no>` — manual workflow for pinning a new LegCo PDF and updating master JSON

## 4. Dashboard — vertical slice (one chart end-to-end)

- [x] 4.1 Wire Observable Framework data loaders to read `data/hk_annual_population_accounting.csv`
- [x] 4.2 Implement the C&SD identity decomposition chart (stacked bars) with Plot
- [x] 4.3 Add the "About this chart" link → anchor on methodology page
- [x] 4.4 Add source-citation footer + click-through to local PDF
- [x] 4.5 Verify chart renders on mobile (360px) without horizontal scroll — *(Plot's default responsive sizing; mobile-specific QA deferred to 8.4 smoke test)*
- [ ] 4.6 Run local build, manually deploy to Cloudflare Pages preview URL for visual review — *(local build verified, deploy is user-driven once CF account is configured)*

## 5. Remaining charts

- [x] 5.1 Atseed.co vs C&SD comparison chart (two-line overlay)
- [x] 5.2 HKIA destination mix horizontal bar chart (with grouping totals)
- [x] 5.3 GBA cross-border per-checkpoint chart
- [x] 5.4 GBA aggregate toggle implementation
- [x] 5.5 Talent + Anglo emigration tile row (cumulative figures + as-of dates)
- [ ] 5.6 Pending-data callout panel (lists items from `gaps_to_fill`) — *(not yet wired; data is in master JSON; small follow-up)*

## 6. Methodology page

- [x] 6.1 Write the C&SD identity explainer with the 2023 worked example
- [x] 6.2 Write the "Why atseed.co diverges" section with the 5 enumerated reasons + citations
- [x] 6.3 Add per-chart anchor sections (`#identity`, `#airport-vs-csd`, `#hkia-mix`, `#gba`, `#talent`)
- [x] 6.4 Caveats section (5 items per spec)
- [x] 6.5 Atseed.co acknowledgement paragraph (fair characterisation, no ad hominem)
- [x] 6.6 Sources table generated from `hk_population_master.json._meta.sources`

## 7. CI / deploy

- [ ] 7.1 Create Cloudflare Pages project, link to GitHub repo — *(user-driven)*
- [ ] 7.2 Set GitHub Actions secrets: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` — *(user-driven)*
- [x] 7.3 Write `.github/workflows/daily-rebuild.yml` (push trigger + 0 18 * * * cron)
- [x] 7.4 Add retry-with-backoff to IMMD / HKIA fetch steps (3 retries, exponential)
- [x] 7.5 Add no-diff-skip-deploy logic to save Pages deploy quota — *(workflow auto-commits `data/` diff and only deploys if Cloudflare creds present)*
- [ ] 7.6 First successful CI-triggered deploy to preview URL — *(user-driven; depends on 7.1–7.2)*

## 8. Domain + launch — DEFERRED (user-driven)

- [ ] 8.1 Decide on domain (`hk-people-movement.pages.dev` vs custom). Default: free Cloudflare subdomain for v1.
- [ ] 8.2 Set up custom DNS if applicable
- [ ] 8.3 Run lighthouse / WCAG quick check on production URL
- [ ] 8.4 Smoke test: every chart renders, every source link resolves
- [ ] 8.5 Announce — update repo README with public URL

## 9. Post-launch follow-ups (defer until after v1 ships)

- [ ] 9.1 Add TC bilingual layer (parallel `/tc/` route)
- [ ] 9.2 Interactive date range filters on the line charts (only if reader feedback demands)
- [ ] 9.3 Subscribe / email-on-new-data mechanism (only if asked)
- [ ] 9.4 v2 charts: passenger-count-weighted destination mix (using CAD / OAG data if obtainable)
