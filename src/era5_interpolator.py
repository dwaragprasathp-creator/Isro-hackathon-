import pandas as pd
import numpy as np
import rasterio
from scipy.interpolate import griddata
from pyproj import Transformer
from pathlib import Path

print("=" * 60)
print("ERA5 INTERPOLATION (REPROJECTED)")
print("=" * 60)

# ---------------------------------------------------
# Read processed ERA5
# ---------------------------------------------------
df = pd.read_csv("data/processed/era5_processed.csv")

# ---------------------------------------------------
# Read Landsat Grid
# ---------------------------------------------------
with rasterio.open("data/processed/ndvi.tif") as src:
    profile = src.profile
    transform = src.transform
    width = src.width
    height = src.height

# ---------------------------------------------------
# Convert ERA5 coordinates
# EPSG:4326 -> EPSG:32644
# ---------------------------------------------------
transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32644",
    always_xy=True
)

utm_x, utm_y = transformer.transform(
    df["longitude"].values,
    df["latitude"].values
)

points = np.column_stack((utm_x, utm_y))

# ---------------------------------------------------
# Landsat Pixel Coordinates
# ---------------------------------------------------
cols, rows = np.meshgrid(
    np.arange(width),
    np.arange(height)
)

cols, rows = np.meshgrid(
    np.arange(width),
    np.arange(height)
)

xs, ys = rasterio.transform.xy(
    transform,
    rows,
    cols,
    offset="center"
)

grid_x = np.array(xs)
grid_y = np.array(ys)

# ---------------------------------------------------
# Variables
# ---------------------------------------------------
variables = {
    "air_temperature": df["air_temperature"].values,
    "humidity": df["humidity"].values,
    "wind_speed": df["wind_speed"].values
}

output = Path("data/processed")

for name, values in variables.items():

    print(f"Interpolating {name}...")

    raster = griddata(
        points,
        values,
        (grid_x, grid_y),
        method="linear"
    )

    # Fill NaN with nearest neighbour
    mask = np.isnan(raster)

    if np.any(mask):
        raster[mask] = griddata(
            points,
            values,
            (grid_x[mask], grid_y[mask]),
            method="nearest"
        )

    profile.update(
        dtype=rasterio.float32,
        count=1,
        compress="lzw"
    )

    outfile = output / f"{name}.tif"

    with rasterio.open(outfile, "w", **profile) as dst:
        dst.write(
            raster.astype(np.float32),
            1
        )

    print(f"Saved : {outfile}")

print("=" * 60)
print("Interpolation Finished")