## Context

We have a clean dataset of HK people-movement series gathered in `data/` (C&SD identity decomposition, IMMD daily passenger CSV, HKIA 91-day flight window, LegCo briefing PDFs). The motivating problem is on atseed.co/hkborder: it presents IMMD airport HK-resident net-out as if it were "international emigration", which structurally misreads the data by ~30× in magnitude and sometimes by sign.

Constraints:
- Cloudflare Pages is the chosen host (per project requirement).
- Data refreshes daily (IMMD CSV) but the dashboard is read-only — no auth, no user state.
- Most charts are small-multiple time series with ≤ 15 series each; visualization complexity is modest.
- Reader is Hong Kong public + journalists; methodology must be radically transparent.
- Project is solo / small-team; ops budget for "always-on server" is zero.

Stakeholders:
- Project owner: the maintainer (Cantonese-reading, expects TC + EN charts eventually)
- Readers: HK public concerned about migration, journalists, researchers
- Indirect: atseed.co's author (may engage with the methodology)

## Goals / Non-Goals

**Goals:**
- Ship a static dashboard to Cloudflare Pages with 5-7 charts covering: C&SD identity, atseed vs C&SD comparison, HKIA destination mix, GBA cross-border, talent + Anglo emigration tiles.
- Every datum traceable to a primary source on disk (`data/legco_sources/` or pinned IMMD/HKIA caches).
- Daily auto-rebuild via GitHub Actions cron.
- Methodology page that is honest about uncertainty and credits atseed.co fairly.
- Paper MCP used for the first design pass before code is written.

**Non-Goals:**
- Interactive querying / drilldown beyond chart-level toggles.
- Real-time updates (hourly or finer).
- Server-side rendering or SSR-anything.
- Comparison with non-HK jurisdictions.
- Forecasting / modelling — this is a data presentation tool only.
- Bilingual UI in v1 (English-only ships first; TC layer is post-v1).
- Native mobile app.

## Decisions

### D1: Reject Streamlit, choose Observable Framework

**Streamlit was evaluated and explicitly rejected.**

Streamlit needs a long-running Python process to serve every request — every interaction round-trips to the server, which re-runs the script. That's a server architecture. Cloudflare Pages serves static assets; Cloudflare Workers run JS/WASM (no native Python long-process). The only Cloudflare route to host Streamlit is Cloudflare Containers (recently GA), which:
- Costs money per always-on container
- Adds ops overhead (image, health checks, scaling)
- Is overkill for a read-only dashboard with daily refresh

**Observable Framework** (`https://observablehq.com/framework`) is the better fit:
- Static-site generator producing pure HTML+JS that runs entirely in the browser
- Native support for Markdown + JS + data loaders that run at build time (so we materialise IMMD/HKIA aggregations into pre-baked JSON, not at request time)
- Plot/d3 built-in for visualisations (no React/charting library to wire up)
- Deploys to Cloudflare Pages with `wrangler pages deploy` after `npm run build`
- Build time on our data scale (~3 MB IMMD CSV, ~8 MB HKIA cache) is well under a minute

Alternatives considered:
- **Astro + d3/Plot**: also static, more flexible, but more wiring. Use Observable Framework first; migrate to Astro only if we hit a wall (e.g., need MDX components Observable doesn't have).
- **Next.js with static export**: heavier, doesn't add value here.
- **Streamlit on Cloudflare Containers**: rejected per above.
- **Streamlit on Streamlit Cloud / Hugging Face Spaces**: not on Cloudflare (violates the project constraint), and Streamlit's interaction model still doesn't fit a read-only daily-refresh dashboard.

### D2: Paper MCP drives the first design pass

Before writing dashboard code, use `paper-desktop:design-to-code` to mock the dashboard layout in Paper (a design tool), get the user's feedback on visual hierarchy / chart ordering / annotations, then translate the approved mock to Observable Framework Markdown + Plot calls. This means the chart taxonomy is settled before any Plot specifications are written.

The Paper mock should cover:
- Landing / hero ("HK people movement — what the data actually says")
- Identity decomposition panel
- atseed.co vs C&SD comparison
- HKIA destination mix
- GBA cross-border (with per-checkpoint / aggregate toggle)
- Talent + Anglo emigration tiles
- Methodology / sources page

### D3: Data pipeline as separate concern from rendering

The pipeline (`pipeline/` directory, Python) is responsible for: fetching upstream sources, parsing them, writing canonical files under `data/`. The dashboard build (Observable Framework) reads only from `data/` and never reaches out to the network at build time. This means:
- The pipeline can run on a different cadence than the dashboard build.
- The dashboard build is reproducible offline given a snapshot of `data/`.
- A failure in upstream fetch doesn't break the dashboard build (last-good `data/` remains).

Pipeline scripts:
- `pipeline/fetch_immd.py` — downloads the IMMD CSV, sorts rows, writes to `data/immd_daily_passenger_traffic_2021_present.csv`
- `pipeline/fetch_hkia_window.py` — fetches missing days within the rolling 91-day window
- `pipeline/parse_legco.py` — extracts pinned numbers from `data/legco_sources/*.pdf` and writes to `data/hk_population_master.json` (currently hand-authored; this script reproduces the hand-authoring with traceability)
- `pipeline/build_aggregates.py` — computes derived CSVs (`hk_annual_population_accounting.csv`, `gba_land_hk_resident_annual.csv`, etc.)
- `pipeline/validate.py` — fails the build if any number lacks a `source` field

### D4: GitHub Actions cron + Cloudflare Pages auto-deploy

Workflow `.github/workflows/daily-rebuild.yml`:
- Triggers: push to `main`, daily cron `0 18 * * *` UTC (= 02:00 HKT)
- Steps: checkout → run `pipeline/*.py` → run `npm run build` (Observable Framework) → `wrangler pages deploy dist/`
- Cloudflare credentials via GitHub Actions secret `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID`
- If pipeline produces no diff, skip deploy (saves Cloudflare deploy quota)

### D5: Translations are post-v1

The dataset and primary sources are bilingual TC/EN (LegCo bilingual, IMMD CSV English headers, HKIA API English). Ship English-first to keep v1 small. Add TC as a parallel route once the chart taxonomy is stable. Don't block v1 on i18n machinery.

### D6: All numbers checked into git

Every primary source is checked into `data/legco_sources/` (PDFs ≤ 12 MB each). The IMMD CSV (3 MB) and HKIA JSON cache (~8 MB) are also in git. This is intentional — the dataset is small, and git history of `data/` becomes a record of when numbers were revised by C&SD. The repo will grow ~5 MB/year at this rate; acceptable.

## Risks / Trade-offs

- **Risk:** HKIA flight API has no documented stability; could break or rate-limit.
  → **Mitigation:** rolling window means partial cache is still useful; pipeline tolerates missing days. If API breaks entirely, fall back to CAD's annual aggregate. Document API as "best-effort source".

- **Risk:** IMMD URL or CSV schema changes silently.
  → **Mitigation:** `pipeline/validate.py` asserts expected columns; build fails loudly. Pin the URL with a checksum on the README; track on a per-quarter manual check.

- **Risk:** LegCo PDFs are visually formatted; parsing tables from PDFs is brittle.
  → **Mitigation:** Numbers are hand-extracted into `data/hk_population_master.json` at first; `parse_legco.py` is a *verification* script that cross-checks the JSON against the PDF, not the source of truth. Numbers are pinned in JSON.

- **Risk:** atseed.co author / readers may interpret the dashboard as adversarial.
  → **Mitigation:** Methodology page acknowledges atseed.co fairly. Tone is "here's the additional data" not "they're wrong". Lead with C&SD's identity, not with the comparison chart.

- **Risk:** "Other Net Migration" 2024 is a known gap until Sep 2026; readers may demand it.
  → **Mitigation:** Show the partial year clearly with a hatched bar and an explicit "pending" note. Add a `gaps_to_fill` panel that lists known data gaps and ETAs.

- **Risk:** Observable Framework is younger than Astro/Next; small community.
  → **Mitigation:** It's by the same team that built D3 and Observable Notebooks; production-stable. Worst case: migrate to Astro + Plot (no rewrite of data layer, just template).

- **Risk:** Cloudflare Pages cold-start / cache invalidation on rapid deploys.
  → **Mitigation:** Set short cache TTL (1 hour) on HTML, long on assets (hashed filenames). Daily deploys are fine; we won't hit invalidation rate limits.

- **Trade-off:** No interactive querying. Readers can't filter by date range or drill into a single control point.
  → **Acceptance:** v1 is a presentation, not a tool. Add interactivity only if reader feedback shows it's needed.

## Migration Plan

This is greenfield (no prior dashboard). Deploy steps:
1. Local Observable Framework scaffolding alongside `data/`
2. First chart wired (identity decomposition) end-to-end as a vertical slice
3. Connect GitHub Actions → first manual deploy to Pages
4. Add remaining charts iteratively, deploying after each
5. Cut over the public domain when chart set is complete + methodology page is written

Rollback: Cloudflare Pages keeps prior deploys; rollback is one click in dashboard or `wrangler pages deployment rollback`. No data migration concerns since the dashboard is read-only.

## Open Questions

- Domain choice — use `hk-people-movement.pages.dev` (free Cloudflare subdomain) for v1, or register a custom domain?
- Chart library — Observable Plot covers everything in the spec, but does the user want a specific brand / style language? Defer to the Paper MCP mock.
- Should the GBA per-checkpoint vs aggregate toggle default to per-checkpoint (more honest about the noise) or aggregate (more legible)? Decide during user testing.
- Bilingual TC layer — should it be a separate route (`/tc/`) or runtime toggle? Defer to v2.
- Mobile chart sizes — Observable Plot's default sizing can crowd on 360px; need to validate after first slice ships.
