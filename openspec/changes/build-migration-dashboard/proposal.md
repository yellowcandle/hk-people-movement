## Why

We've assembled an authoritative dataset on Hong Kong people movement (C&SD population identity, IMMD daily crossings, HKIA flight mix, LegCo briefings) that demonstrates atseed.co/hkborder's "airport HK-resident net outflow ≈ emigration" claim is structurally misleading: the airport-net metric is gross short-trip movement, sign-disagrees with C&SD's identity-derived migration figure by ~530K over 2021-2023, and ignores the 50%+ inflow channel (Top Talent Pass, OWP, returnees). We need a public dashboard that presents the corrected picture — full population accounting alongside atseed.co's framing — so readers can see where the misreading happens and what the data actually says.

## What Changes

- Build a public dashboard (`hk-people-movement.pages.dev` or similar) presenting:
  - C&SD population identity over time (Pop = NatChg + OWP + OtherNet)
  - atseed.co's airport-net series side-by-side with C&SD's "Other net migration" — to show the gap
  - HKIA 91-day rolling destination mix
  - Cross-channel comparison (airport vs land vs C&SD identity)
  - LegCo source citations on every chart
- Use Paper MCP (`paper-desktop:design-to-code`) to mock the dashboard layout first, then implement
- Static-first architecture deployable to Cloudflare Pages (no Python server)
- **Reject Streamlit** as the framework: incompatible with Cloudflare's primary serverless model (would need Cloudflare Containers, an over-complex shape for a read-only data dashboard with ~10 series and rolling daily updates). Use **Observable Framework** (or equivalent static site generator) instead — static HTML+JS, builds at deploy time, runs entirely in browser, fits Pages natively.
- Document data provenance: every figure traceable back to a primary source (CSV, PDF, or LegCo paper) checked into `data/`
- Build a daily-rebuild pipeline (GitHub Actions cron) to refresh IMMD CSV + HKIA flights window

## Capabilities

### New Capabilities
- `migration-dashboard`: Public-facing static dashboard rendering all sourced HK people-movement series, with explicit methodology disclosure on each chart
- `data-pipeline`: Reproducible ingestion of IMMD CSV, HKIA flight API, LegCo PDFs, into canonical JSON/CSV under `data/`, regenerable from source on every build
- `methodology-docs`: First-class methodology page that walks readers through the C&SD population identity, why atseed.co's airport-net diverges, and what each chart is and isn't claiming

### Modified Capabilities
<!-- none — first capabilities in this project -->

## Impact

- **New directories**: `src/` (dashboard source), `pipeline/` (data ingestion scripts), `openspec/specs/` (capability specs after this proposal)
- **Cloudflare Pages**: New project, no existing services touched
- **Dependencies (anticipated)**: Observable Framework or Astro + Plot/d3, GitHub Actions for daily rebuild, `pypdf` (already used) for PDF text extraction
- **Data refresh cadence**: IMMD CSV daily (atseed.co's same source), HKIA flights daily for rolling 91-day window, LegCo PDFs pinned and manually refreshed when new issue lands
- **NOT impacted**: existing `data/` files remain canonical; pipeline regenerates them, doesn't replace them ad-hoc
