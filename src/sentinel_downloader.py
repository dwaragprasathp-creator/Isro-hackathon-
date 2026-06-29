import ee
import geemap
from pathlib import Path

ee.Initialize(project="heatstressai")

# Smaller Hyderabad ROI
roi = ee.Geometry.Rectangle([
    78.30, 17.30,
    78.60, 17.55
])

image = (
    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(roi)
    .filterDate("2024-05-20", "2024-06-05")
    .sort("CLOUDY_PIXEL_PERCENTAGE")
    .first()
    .clip(roi)
)

output = Path("data/raw/sentinel")
output.mkdir(parents=True, exist_ok=True)

outfile = output / "sentinel2_hyderabad.tif"

geemap.ee_export_image(
    image.select(["B2","B3","B4","B8","B11"]),
    filename=str(outfile),
    scale=20,      # reduce resolution
    region=roi,
)

print("✅ Sentinel downloaded successfully")