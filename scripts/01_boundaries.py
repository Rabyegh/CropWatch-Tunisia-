"""Download Tunisia ADM1 boundaries (geoBoundaries gbOpen), keep the 4 pilot governorates.
UNTESTED draft. Check the names printed and adjust NAME_MAP."""
import json, requests, geopandas as gpd, yaml, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
cfg = yaml.safe_load(open(ROOT/"config/regions.yml", encoding="utf-8"))

meta = requests.get("https://www.geoboundaries.org/api/current/gbOpen/TUN/ADM1/", timeout=60).json()
print(json.dumps({k: meta.get(k) for k in ["boundaryName","boundaryYearRepresented","boundarySource","boundaryLicense"]}, indent=2))
gdf = gpd.read_file(meta["gjDownloadURL"])
print(gdf.columns.tolist()); print(sorted(gdf["shapeName"].tolist()))

NAME_MAP = {"Beja":"TN-BJ","Béja":"TN-BJ","Jendouba":"TN-JE","Kef":"TN-KF","Le Kef":"TN-KF","Siliana":"TN-SL"}
gdf["geo_id"] = gdf["shapeName"].map(NAME_MAP)
pilot = gdf.dropna(subset=["geo_id"]).to_crs(cfg["crs_storage"])
assert pilot["geo_id"].nunique() == 4, f"expected 4 pilot regions, got {pilot['geo_id'].tolist()}"
pilot["area_km2"] = pilot.to_crs(cfg["crs_area_calc"]).area / 1e6
out = ROOT/"data/interim/pilot_governorates.geojson"
pilot[["geo_id","shapeName","area_km2","geometry"]].to_file(out, driver="GeoJSON")
print("bounds (W,S,E,N):", pilot.total_bounds.round(3)); print(pilot[["geo_id","area_km2"]])
print("RECORD in docs/data-sources.md -> license:", meta.get("boundaryLicense"))
