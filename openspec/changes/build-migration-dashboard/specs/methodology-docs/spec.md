## ADDED Requirements

### Requirement: Methodology page explains C&SD population identity
The methodology page SHALL state and explain the C&SD identity (ΔPop = NaturalChange + OWP + OtherNet) in plain language, with a worked example using 2023 figures.

#### Scenario: Worked example present
- **WHEN** the reader visits `/methodology`
- **THEN** the page shows: "2022 → 2023: Pop +190,000 = NaturalChange (−21,499) + OWP (+40,818) + Other Net (+170,681)"
- **AND** the page explains what each component does and does NOT include

### Requirement: Page explains why atseed.co's airport-net diverges from C&SD's "Other Net"
The methodology page SHALL contain a section titled "Why atseed.co's number differs" that lists the structural reasons in order of magnitude.

#### Scenario: Divergence reasons enumerated
- **WHEN** the reader visits the divergence section
- **THEN** at least these reasons are listed, each with one sentence:
  1. Short-trip round-trips don't fully cancel within window (timing noise)
  2. Talent admission inflow (new arrivals enter as "Mainland Visitor" / "Other Visitor", not as HK Resident)
  3. Returning emigrants for medical care, family, etc. show as HK Resident *arrivals* without being permanent returners
  4. OWP holders not yet on HKID still classified as Mainland Visitor on entry
  5. Cross-border land emigration (50K+ stock in Guangdong) entirely outside the airport sample
- **AND** each reason cites the LegCo paper or C&SD table that evidences it

### Requirement: Per-chart "About this chart" disclosure exists
Each chart on the dashboard SHALL link to a section of the methodology page that explains what the chart shows, what it does NOT show, and what to be careful about reading into it.

#### Scenario: Anchor links resolve
- **WHEN** the reader clicks the "?" on the airport-vs-CSD comparison chart
- **THEN** the methodology page opens scrolled to `#airport-vs-csd` which contains the chart's caveats

### Requirement: Data caveats are listed prominently
The methodology page SHALL list known data caveats in a dedicated section.

#### Scenario: Caveat list
- **WHEN** the reader visits the caveats section
- **THEN** these caveats appear with one sentence each:
  - 2024 OWP not yet published; "Other Net Migration" 2024 cannot be computed until C&SD Annual Digest 2025 (~Sep 2026)
  - LegCo "Hong Kong in figures" provisional figures get revised; latest mid-year figure may differ from prior issue
  - HKIA flight API only retains ~91 days; older composition is approximated by the rolling window assumption
  - Talent Pass cumulative figures count *approvals*, not arrivals; arrivals lag and are reported separately
  - Mainland HK resident stock is a 2020 census figure; no interim update before 2026 census

### Requirement: Acknowledgement of atseed.co
The methodology page SHALL include a paragraph acknowledging atseed.co/hkborder as the prompt for this work, characterising its data choice fairly (IMMD daily, restricted to Airport HK-Resident rows) and identifying which of its claims are defensible vs which mislead.

#### Scenario: Fair characterisation
- **WHEN** the acknowledgement section renders
- **THEN** it states: airport data IS the cleanest IMMD signal among the control points (atseed.co is right about that), AND net flow DOES cancel round-trips in expectation (atseed.co is right about that), BUT labelling airport-net as "international emigration" is misleading because the airport sample misses the major inflow channels and the magnitude doesn't reconcile with C&SD's identity
- **AND** the section avoids ad hominem language and addresses methodology only

### Requirement: Source catalog is exhaustive
The methodology page SHALL include a "Sources" section listing every primary document used, with link, retrieval date, and one-line description.

#### Scenario: Each source has a row
- **WHEN** the sources section renders
- **THEN** every entry from `data/hk_population_master.json._meta.sources` is listed in a table
- **AND** each row has columns: short name, full title, publisher, retrieval date, link
