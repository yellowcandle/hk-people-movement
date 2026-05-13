## ADDED Requirements

### Requirement: Pipeline regenerates all derived data from primary sources
The pipeline SHALL ingest every primary source listed in `data/hk_population_master.json._meta.sources` and regenerate the derived CSV/JSON outputs under `data/`, deterministically, from a single command.

#### Scenario: Clean rebuild
- **WHEN** the user runs the rebuild command on a clean checkout (no `data/` derivatives present)
- **THEN** the pipeline downloads the IMMD CSV, fetches the 91 days of HKIA flight JSON, parses the LegCo PDFs that are pinned in `data/legco_sources/`
- **AND** writes `data/hk_population_master.json`, `data/hk_annual_population_accounting.csv`, `data/hkia_destination_mix_91d.csv`, `data/gba_land_hk_resident_annual.csv`, `data/cross_channel_net_outflow_annual.csv`
- **AND** the build exits 0

#### Scenario: Diff is empty when sources unchanged
- **WHEN** the rebuild runs twice in a row with no upstream changes
- **THEN** `git diff data/` is empty

### Requirement: IMMD CSV is fetched directly from immd.gov.hk
The pipeline SHALL fetch the IMMD daily passenger traffic CSV directly from `https://www.immd.gov.hk/opendata/eng/transport/immigration_clearance/statistics_on_daily_passenger_traffic.csv`, the same upstream atseed.co uses.

#### Scenario: Fresh fetch and dedup
- **WHEN** the pipeline runs at deploy time
- **THEN** the latest CSV is downloaded
- **AND** rows are sorted by (date, control_point, direction) before writing to disk so the file is diff-stable

### Requirement: HKIA flight window is rolling
The pipeline SHALL maintain a rolling 91-day window of per-day JSON files from `hongkongairport.com/flightinfo-rest/rest/flights/past?...`, dropping days older than the API's retention window and adding new days as they become available.

#### Scenario: New day fetch
- **WHEN** the pipeline runs and the latest cached day is older than yesterday
- **THEN** each missing day from latest-cached+1 through yesterday is fetched
- **AND** files older than 91 days are deleted to keep `data/hkia_91d/` bounded

### Requirement: LegCo PDFs are pinned, not refetched
The pipeline SHALL treat every PDF under `data/legco_sources/` as pinned: it MUST NOT re-download a PDF whose filename matches an existing local file.

#### Scenario: Pinned PDFs survive rebuilds
- **WHEN** the pipeline runs
- **THEN** `data/legco_sources/*.pdf` is read-only from the pipeline's perspective
- **AND** when a new LegCo issue is published, the contributor must manually add the PDF via `scripts/add-legco-source.sh <RPDB-paper-no>` which fetches the new file and updates the master JSON

### Requirement: Every derived datum is traceable to a source
Every numerical value in `data/hk_population_master.json` SHALL have a `source` field naming the document and (where applicable) the table or section it came from.

#### Scenario: Source missing causes build failure
- **WHEN** a contributor adds a new number without a `source` field
- **THEN** a validation step in the pipeline fails the build
- **AND** the error message names the offending key

### Requirement: Build runs in CI on a daily schedule
The pipeline SHALL run via GitHub Actions both on push and on a daily cron at 02:00 HKT, with the deploy step gated on the build passing.

#### Scenario: Daily refresh
- **WHEN** the daily cron triggers
- **THEN** the pipeline runs, IMMD CSV and HKIA window are refreshed, the dashboard rebuilds
- **AND** Cloudflare Pages auto-deploys the new build

#### Scenario: Failed upstream
- **WHEN** an upstream source (IMMD or HKIA API) is unreachable
- **THEN** the build retries up to 3 times with exponential backoff
- **AND** if all retries fail, the build aborts and the previously-deployed dashboard remains live (no auto-rollback noise needed since Pages keeps prior deploy)
