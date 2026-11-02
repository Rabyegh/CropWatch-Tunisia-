# CropWatch Tunisia

CropWatch Tunisia is a regional cereal-monitoring and early-warning project for
northwestern Tunisia. It combines satellite observations, weather and soil
moisture data, rainfall estimates, land-cover information, and official
agricultural statistics to support evidence-based monitoring of cereal
conditions.

The project is being developed in stages:

1. Establish a reliable, reproducible data foundation.
2. Measure the availability and quality of historical observations.
3. Build regional crop-condition indicators.
4. Validate indicators against available agricultural statistics.
5. Develop seasonal monitoring and 14-day early-warning products.

The initial pilot covers Béja, Jendouba, Le Kef, and Siliana, with wheat and
barley represented as one combined cereals class until crop-specific labels are
available.

## Current pilot scope

| Governorate | Stable ID |
|---|---|
| Béja | `TN-BJ` |
| Jendouba | `TN-JE` |
| Le Kef | `TN-KF` |
| Siliana | `TN-SL` |

- **Season:** November through June
- **Initial crop class:** cereals
- **Storage CRS:** EPSG:4326
- **Area-calculation CRS:** EPSG:32632 (to be verified with the boundary workflow)

The stable IDs in [`config/regions.yml`](config/regions.yml) are the join keys
for regions. Do not join datasets using display names.

## Repository layout

```text
config/
  crops.yml                 Crop classes and crop-calendar placeholders
  regions.yml               Pilot regions, IDs, CRS, and season window
docs/
  data-sources.md           Data catalog, licenses, and access constraints
  feasibility-report.md     Evidence, limitations, and project decision
notebooks/
  data_exploration/         Exploratory analysis and visualizations
scripts/
  01_boundaries.py          Download and prepare pilot governorate polygons
  02_era5land_pull.py       Download ERA5-Land monthly climate variables
  02b_chirps_pull.py        CHIRPS v3 rainfall-download placeholder
  03_s2_validpixel_openeo.py
                            Compute Sentinel-2 valid-pixel and NDVI indicators
src/
  common/                   Shared Python package code
data/
  raw/                      Downloaded source data
  interim/                  Intermediate processed data
```

The full project requirements and implementation blueprint are available in
[`CropWatch_Tunisia_Project_Documentation.docx`](CropWatch_Tunisia_Project_Documentation.docx).

## Data sources

The project is designed to use:

- **Sentinel-2 L2A:** optical imagery, cloud-screened with the scene
  classification layer, accessed through openEO.
- **ERA5-Land:** temperature, precipitation, and soil-water reanalysis from
  the Copernicus Climate Data Store.
- **CHIRPS v3:** high-resolution rainfall estimates from the Climate Hazards
  Center.
- **ESA WorldCover:** land-cover information for a potential cropland mask.
- **SoilGrids:** static soil-property context.
- **geoBoundaries:** administrative boundaries for the four pilot regions.
- **INGC and Office des Céréales:** official agricultural statistics where
  definitions, years, and geographic coverage can be verified.

Source versions, licenses, retrieval dates, access methods, and caveats should
be recorded in [`docs/data-sources.md`](docs/data-sources.md).

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the current project dependencies:

```bash
pip install geopandas requests pandas pyarrow xarray netcdf4 cdsapi "openeo>=0.30" matplotlib pyyaml
```

Additional provider accounts and configuration are required for some workflows:

- A CDS account with the ERA5-Land dataset license accepted.
- A Copernicus Data Space account for openEO authentication.
- Network access to the relevant provider endpoints.

## Recommended workflow

Run the workflows in this order for a new environment or data release.

### 1. Prepare boundaries

```bash
python scripts/01_boundaries.py
```

Check the printed governorate names before continuing. If the names returned by
geoBoundaries differ, update `NAME_MAP` in the script. The workflow writes
`data/interim/pilot_governorates.geojson` and prints the source license to
record in the data catalog.

### 2. Run a small Sentinel-2 test

Start with one governorate and one season:

```bash
python scripts/03_s2_validpixel_openeo.py TN-BJ
```

Inspect the valid-pixel fraction and NDVI output and check the credit cost on
the Copernicus account before scaling to all four governorates and multiple
seasons. The current workflow uses Sentinel-2 SCL classes 4–7 as valid pixels;
the treatment of class 7 (unclassified) must be evaluated using real data.

### 3. Download climate data

With CDS credentials configured, run:

```bash
python scripts/02_era5land_pull.py
```

The ERA5-Land request is a feasibility-stage monthly pull. Verify the current
CDS dataset name, variable names, request fields, units, and geographic bounds
against the live catalogue before relying on the output.

The CHIRPS workflow is intentionally blocked until the exact CHIRPS v3 file
pattern and product choice (final or preliminary, timestep, domain, and format)
have been verified from the provider:

```bash
python scripts/02b_chirps_pull.py
```

Do not replace its placeholder with an unverified URL.

### 4. Document and analyze

Update [`docs/data-sources.md`](docs/data-sources.md) as data are tested.
Manually inspect the INGC and Office des Céréales sources, then complete
[`docs/feasibility-report.md`](docs/feasibility-report.md) with:

- Sentinel-2 observation coverage and valid-pixel rates.
- Climate-data coverage and sanity checks.
- Available official statistics and their definitions.
- Cropland-mask suitability.
- License and access constraints.
- A decision to proceed, narrow the scope, operate as monitoring-only, or stop.

Later analysis should produce a heatmap of governorate × 10-day window ×
season and use it to support the monitoring and early-warning workflows.

## Development principles

- Treat all provider URLs, collection IDs, variable names, and licenses as
  externally verifiable configuration, not assumptions.
- Start with small spatial and temporal requests before scaling.
- Preserve stable region IDs across every intermediate and final dataset.
- Keep raw downloads separate from processed data.
- Record data provenance, units, missing values, and transformations.
- Distinguish a vegetation or rainfall anomaly from confirmed crop damage.
- Validate indicators against independent observations before operational use.

## Project status

The repository currently contains feasibility-stage scripts and documentation.
The workflows are drafts and should be run, inspected, and corrected against
the current provider APIs before being used for production analysis.
