"""Export daily CHIRPS v3 rainfall zonal means through Google Earth Engine.

First run authenticates in a browser. Set ``EE_PROJECT`` to a Google Cloud
project registered for Earth Engine, or pass ``--project`` explicitly.
"""
import argparse
import pathlib

import ee
import geopandas as gpd

ROOT = pathlib.Path(__file__).resolve().parents[1]
COLLECTION_ID = "UCSB-CHC/CHIRPS/V3/DAILY_SAT"
DEFAULT_START = "2017-09-01"
DEFAULT_END = "2025-07-01"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=None, help="Registered Earth Engine Cloud project")
    parser.add_argument("--start", default=DEFAULT_START, help="Inclusive ISO start date")
    parser.add_argument("--end", default=DEFAULT_END, help="Exclusive ISO end date")
    parser.add_argument("--description", default="chirps_v3_daily_pilot")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project = args.project
    if project is None:
        import os

        project = os.environ.get("EE_PROJECT")
    if not project:
        raise SystemExit(
            "Set EE_PROJECT or pass --project with a Google Cloud project "
            "registered for Earth Engine."
        )

    boundary_path = ROOT / "data/interim/pilot_governorates.geojson"
    if not boundary_path.exists():
        raise SystemExit(
            f"Missing {boundary_path}. Run scripts/01_boundaries.py first."
        )

    ee.Authenticate()
    ee.Initialize(project=project)

    gdf = gpd.read_file(boundary_path)[["geo_id", "geometry"]]
    if gdf["geo_id"].isna().any() or gdf["geo_id"].duplicated().any():
        raise ValueError("Boundary file must contain one non-null, unique geo_id per region.")
    fc = ee.FeatureCollection(gdf.__geo_interface__)

    collection = (
        ee.ImageCollection(COLLECTION_ID)
        .filterDate(args.start, args.end)
        .select("precipitation")
    )

    def per_image(image: ee.Image) -> ee.FeatureCollection:
        date = image.date().format("YYYY-MM-dd")
        return image.reduceRegions(
            collection=fc,
            reducer=ee.Reducer.mean(),
            scale=5566,
        ).map(lambda feature: feature.set("date", date))

    table = collection.map(per_image).flatten().select(["geo_id", "date", "mean"])
    task = ee.batch.Export.table.toDrive(
        collection=table,
        description=args.description,
        fileFormat="CSV",
    )
    task.start()
    print(
        f"Export started for {COLLECTION_ID}: {args.start} through {args.end} "
        f"(end exclusive). Check the Earth Engine Tasks tab or Drive."
    )


if __name__ == "__main__":
    main()
