import rasterio

files = [
    "data/processed/thermal.tif",
    "data/processed/qa.tif",
    "data/processed/cloud_mask.tif"
]

for f in files:
    with rasterio.open(f) as src:
        print(f)
        print("Width :", src.width)
        print("Height:", src.height)
        print("CRS   :", src.crs)
        print("-" * 40)