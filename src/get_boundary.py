import osmnx as ox
from pathlib import Path

# Create output folder
output = Path("data/raw/boundary")
output.mkdir(parents=True, exist_ok=True)

print("Downloading Hyderabad boundary...")

gdf = ox.geocode_to_gdf("Hyderabad, Telangana, India")

outfile = output / "hyderabad_boundary.geojson"

gdf.to_file(outfile, driver="GeoJSON")

print("Boundary saved to:")
print(outfile)