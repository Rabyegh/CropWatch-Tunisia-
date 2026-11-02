# CropWatch Tunisia (Phase 1: research and data feasibility)

Goal of Phase 1: decide, with evidence, whether historical data can support the pilot
(Béja, Jendouba, Le Kef, Siliana; cereals). Output = docs/feasibility-report.md + go/no-go.

Order of work
1. config/regions.yml, config/crops.yml       -> confirm scope
2. scripts/01_boundaries.py                   -> governorate polygons + source/license record
3. scripts/02_era5land_pull.py                -> temperature / soil water / precip (CDS API)
   scripts/02b_chirps_pull.py                 -> rainfall (fill in verified URL first)
4. scripts/03_s2_validpixel_openeo.py         -> Sentinel-2 valid-pixel + NDVI per governorate/date (THE GATE)
5. docs/data-sources.md                       -> fill the catalog while you go
6. docs/feasibility-report.md                 -> go / narrow / monitoring-only

All scripts are UNTESTED drafts: run, read the output, fix. Verify every URL, variable
name and license with the provider before relying on it.

Setup
  python -m venv .venv && source .venv/bin/activate
  pip install geopandas requests pandas pyarrow xarray netcdf4 cdsapi "openeo>=0.30" matplotlib pyyaml
