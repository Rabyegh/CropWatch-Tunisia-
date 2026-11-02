"""ERA5-Land monthly means for the pilot bbox via CDS API (UNTESTED draft).
Needs ~/.cdsapirc and the accepted dataset licence. Monthly product = quick feasibility test.
For daily features later, use the hourly dataset month by month and resample with xarray."""
import cdsapi, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
c = cdsapi.Client()
c.retrieve("reanalysis-era5-land-monthly-means", {
    "product_type": "monthly_averaged_reanalysis",
    "variable": ["2m_temperature", "total_precipitation", "volumetric_soil_water_layer_1"],
    "year": [str(y) for y in range(2017, 2026)],
    "month": [f"{m:02d}" for m in range(1, 13)],
    "time": "00:00",
    "area": [37.3, 8.0, 35.4, 10.0],   # N, W, S, E (replace with bounds from script 01)
    "data_format": "netcdf",
}, str(ROOT/"data/raw/era5land_monthly_pilot.nc"))
# Next: open with xarray, mask with governorate polygons, compute zonal means.
