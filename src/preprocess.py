from pathlib import Path
import numpy as np
import rasterio
from rasterio.mask import mask
import geopandas as gpd
from loader import LandsatLoader

# -----------------------------
# Load Landsat Scene
# -----------------------------
loader = LandsatLoader()

# Hyderabad Boundary
boundary = gpd.read_file("data/raw/boundary/hyderabad_boundary.geojson")

# Output Folder
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

# Bands to Process
bands = [
    "blue",
    "green",
    "red",
    "nir",
    "swir1",
    "swir2",
    "thermal",
    "qa"
]

print("=" * 60)
print("PREPROCESSING LANDSAT DATA")
print("=" * 60)

for band in bands:

    file = loader.bands[band]

    with rasterio.open(file) as src:

        # Match CRS
        boundary_proj = boundary.to_crs(src.crs)

        # Clip
        clipped, transform = mask(
            src,
            boundary_proj.geometry,
            crop=True
        )

        profile = src.profile

        profile.update(
            height=clipped.shape[1],
            width=clipped.shape[2],
            transform=transform,
            compress="lzw"
        )

        outfile = output_dir / f"{band}.tif"

        with rasterio.open(outfile, "w", **profile) as dst:
            dst.write(clipped)

        print(f"✓ {band} saved")

print("\nPreprocessing Completed Successfully!")