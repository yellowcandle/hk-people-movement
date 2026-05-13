## ADDED Requirements

### Requirement: Dashboard is a static site deployable to Cloudflare Pages
The dashboard SHALL build to a directory of static HTML/CSS/JS assets that Cloudflare Pages can serve directly, with no server-side runtime requirement at request time.

#### Scenario: Build output is static
- **WHEN** the build command runs in CI
- **THEN** all output files are HTML, CSS, JS, JSON, or image assets
- **AND** no Node/Python process is required to serve requests
- **AND** `wrangler pages deploy <dist-dir>` succeeds with zero functions

#### Scenario: Streamlit is rejected
- **WHEN** a contributor proposes Streamlit as the framework
- **THEN** the rejection rationale (Streamlit needs a long-running Python server, Cloudflare Pages serves static assets only, dashboard is read-only with daily refresh — Containers shape is overkill) MUST be cited in the design doc

### Requirement: Population identity panel renders C&SD accounting
The dashboard SHALL include a panel showing the C&SD population identity (ΔPop = NaturalChange + OWP + OtherNet) decomposed annually for the years where all components are publicly available.

#### Scenario: Identity panel shows all available years
- **WHEN** the dashboard loads
- **THEN** a chart shows annual stacked bars for 2019–2023 (or latest year where all 4 components are sourced)
- **AND** each component has a distinct color and is labelled
- **AND** the source citation reads "C&SD Annual Digest of Statistics 2024, Tables 1.1 + 1.12"

#### Scenario: Pending years are visually flagged
- **WHEN** a year has natural change but no OWP figure yet (e.g., 2024)
- **THEN** the bar for that year is rendered with a hatched / faded fill
- **AND** a tooltip says "OWP figure pending C&SD Annual Digest 2025 (expected Sep 2026)"

### Requirement: Side-by-side comparison of atseed.co metric vs C&SD identity
The dashboard SHALL include a chart that overlays atseed.co's IMMD HK-resident airport-net-out series against C&SD's "Other Net Migration" series for the same years, so the magnitude and sign disagreement is visually obvious.

#### Scenario: Both series rendered with same time axis
- **WHEN** the comparison chart loads
- **THEN** atseed.co metric and C&SD "Other Net Migration" appear as two lines on the same axes for 2021–2023
- **AND** the sign convention is explicitly noted in the chart header (positive = inflow under C&SD convention, positive = outflow under IMMD raw)
- **AND** the cumulative gap (e.g., "−485K vs +42K = 527K disagreement over 3 years") is shown as an annotation

### Requirement: HKIA flight destination mix is shown
The dashboard SHALL render the rolling 91-day HKIA outbound flight composition by destination region.

#### Scenario: Region mix is shown as ranked bars
- **WHEN** the mix panel loads
- **THEN** a horizontal bar chart shows ops% by region (Mainland China, SE Asia, Japan, Taiwan, South Korea, Australia/NZ/Pacific, USA, Europe, South Asia, UK/Ireland, Middle East, Canada, Africa)
- **AND** the window dates (start / end of 91-day rolling) are visible in the chart header
- **AND** Mainland China + Taiwan + Japan + South Korea + SE Asia are grouped as "Short-haul leisure-dominant" with a separate total

### Requirement: GBA cross-border flow chart isolates aggregate corridor
The dashboard SHALL include a chart of GBA land cross-border HK-resident net flow aggregated across all land control points by year, illustrating that single-checkpoint noise (e.g., Lok Ma Chau vehicle vs spur-line) cancels at corridor level.

#### Scenario: Per-checkpoint vs aggregate views
- **WHEN** the GBA panel loads in "per-checkpoint" mode
- **THEN** each of the 8 land control points has its own annual net-out bar for 2023, 2024, 2025
- **AND** the user can toggle to "aggregate" mode that sums across all checkpoints, showing a much smaller net-out per year
- **AND** the legend explains the toggle's meaning

### Requirement: Every chart cites its source
Every chart on the dashboard SHALL display a source citation that names the primary publisher, document, and table or URL.

#### Scenario: Click-through to source
- **WHEN** the user clicks a chart's source citation
- **THEN** the link opens the source document (LegCo PDF, IMMD CSV, gov.hk press release, etc.) in a new tab
- **AND** if the source is local (checked into `data/legco_sources/`), the link resolves to the local file

### Requirement: Talent Pass + emigration corridor stats are surfaced
The dashboard SHALL include cumulative-to-date figures for the Top Talent Pass and emigration to UK/Canada/Australia, with the date the figure was last reported.

#### Scenario: Cumulative tile renders
- **WHEN** the talent / emigration panel loads
- **THEN** tiles show: Top Talent Pass cumulative applications / approvals / arrived (with as-of date), Anglo emigration 2021–2024 cumulative (172,750), good-conduct certificate annual flow latest year (14,400 for 2023)
- **AND** each tile cites its source paper

### Requirement: Mobile-readable layout
The dashboard SHALL be readable on mobile widths (≥ 360px).

#### Scenario: Mobile rendering
- **WHEN** the dashboard is rendered at 360px width
- **THEN** all charts reflow vertically, no horizontal scroll is required
- **AND** legends and source citations remain legible

### Requirement: Methodology page is one click away
The dashboard SHALL link to the methodology page from every chart and from a persistent top-nav item.

#### Scenario: Methodology link present everywhere
- **WHEN** any chart is visible
- **THEN** an "About this chart" or "?" icon links to the methodology page
- **AND** the methodology page covers C&SD identity, why atseed.co diverges, and known caveats
