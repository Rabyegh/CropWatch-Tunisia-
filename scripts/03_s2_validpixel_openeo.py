"""THE GATE: Sentinel-2 L2A valid-pixel fraction + mean NDVI per governorate.
UNTESTED draft (openEO on Copernicus Data Space; free account, limited credits).
START SMALL: one governorate, one season. Check credit cost before scaling.
Usage: python 03_s2_validpixel_openeo.py TN-BJ"""
import openeo, geopandas as gpd, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
SEASON = ("2022-11-01", "2023-06-30")           # change per run
GEO_ID = sys.argv[1] if len(sys.argv) > 1 else "TN-BJ"

gdf = gpd.read_file(ROOT/"data/interim/pilot_governorates.geojson")
geom = gdf[gdf.geo_id == GEO_ID].geometry.iloc[0]
w, s, e, n = geom.bounds

conn = openeo.connect("openeo.dataspace.copernicus.eu").authenticate_oidc()
cube = conn.load_collection("SENTINEL2_L2A", temporal_extent=SEASON,
                            spatial_extent={"west": w, "south": s, "east": e, "north": n, "crs": "EPSG:4326"},
                            bands=["B04", "B08", "SCL"])
scl = cube.band("SCL")
# Valid SCL classes: 4 vegetation, 5 bare soil, 6 water, 7 unclassified. Excluded: 0 nodata, 1 saturated, 3 shadow, 8/9/10 cloud/cirrus, 11 snow.
valid = (scl == 4) | (scl == 5) | (scl == 6) | (scl == 7)
red, nir = cube.band("B04"), cube.band("B08")
ndvi = ((nir - red) / (nir + red)).mask(~valid)

feature = {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"geo_id": GEO_ID}, "geometry": geom.__geo_interface__}]}
v = valid.resample_spatial(resolution=60).aggregate_spatial(feature, reducer="mean")
nd = ndvi.resample_spatial(resolution=60).aggregate_spatial(feature, reducer="mean")
v.execute_batch(str(ROOT/f"data/raw/s2_valid_{GEO_ID}_{SEASON[0][:4]}.csv"), out_format="CSV")
nd.execute_batch(str(ROOT/f"data/raw/s2_ndvi_{GEO_ID}_{SEASON[0][:4]}.csv"), out_format="CSV")
# Next: heatmap (governorate x 10-day window x season) in notebooks/data_exploration/.
# No cropland mask yet: add ESA WorldCover cropland mask before Phase 3.
