import osmnx as ox
from pathlib import Path

place = "Hyderabad, Telangana, India"

print("Downloading buildings...")
buildings = ox.features_from_place(
    place,
    tags={"building": True}
)

print("Downloading major roads...")
roads = ox.features_from_place(
    place,
    tags={
        "highway": [
            "motorway",
            "trunk",
            "primary",
            "secondary",
            "tertiary"
        ]
    }
)

output = Path("data/raw/osm")
output.mkdir(parents=True, exist_ok=True)

buildings.to_file(output / "buildings.geojson", driver="GeoJSON")
roads.to_file(output / "roads.geojson", driver="GeoJSON")

print("=" * 60)
print("OSM DOWNLOAD COMPLETED")
print("=" * 60)
print("Buildings:", len(buildings))
print("Roads:", len(roads))