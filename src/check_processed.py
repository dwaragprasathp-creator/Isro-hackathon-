import rasterio
from pathlib import Path

processed = Path("data/processed")

files = [
    "ndvi.tif",
    "ndwi.tif",
    "ndbi.tif",
    "lst.tif",
    "heat_risk.tif"
]

for file in files:
    path = processed / file

    with rasterio.open(path) as src:
        print(f"{file}")
        print(f"Width : {src.width}")
        print(f"Height: {src.height}")
        print(f"CRS   : {src.crs}")
        print("-" * 40)