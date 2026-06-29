import ee
import geemap
from pathlib import Path

# Initialize Earth Engine
ee.Initialize(project="heatstressai")

# Hyderabad Bounding Box
roi = ee.Geometry.Rectangle([78.15, 17.20, 78.75, 17.70])

# SRTM DEM
dem = ee.Image("USGS/SRTMGL1_003").clip(roi)

output = Path("data/raw/srtm")
output.mkdir(parents=True, exist_ok=True)

outfile = output / "hyderabad_dem.tif"

geemap.ee_export_image(
    dem,
    filename=str(outfile),
    scale=30,
    region=roi
)

print("="*60)
print("SRTM DOWNLOADED SUCCESSFULLY")
print("="*60)
print(outfile)