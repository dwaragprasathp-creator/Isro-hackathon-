import rasterio
import numpy as np
import pandas as pd
from pathlib import Path
from rasterio.enums import Resampling

processed = Path("data/processed")

# -----------------------------
# Read Landsat Features
# -----------------------------
with rasterio.open(processed / "ndvi.tif") as src:
    ndvi = src.read(1)

with rasterio.open(processed / "ndwi.tif") as src:
    ndwi = src.read(1)

with rasterio.open(processed / "ndbi.tif") as src:
    ndbi = src.read(1)

with rasterio.open(processed / "lst.tif") as src:
    lst = src.read(1)

# -----------------------------
# DEM
# -----------------------------
with rasterio.open("data/raw/srtm/hyderabad_dem.tif") as src:

    dem = src.read(
        1,
        out_shape=lst.shape,
        resampling=Resampling.bilinear
    )

# -----------------------------
# Weather Layers
# -----------------------------
with rasterio.open(processed / "air_temperature.tif") as src:

    air = src.read(
        1,
        out_shape=lst.shape,
        resampling=Resampling.bilinear
    )

with rasterio.open(processed / "humidity.tif") as src:

    humidity = src.read(
        1,
        out_shape=lst.shape,
        resampling=Resampling.bilinear
    )

with rasterio.open(processed / "wind_speed.tif") as src:

    wind = src.read(
        1,
        out_shape=lst.shape,
        resampling=Resampling.bilinear
    )

# -----------------------------
# Build DataFrame
# -----------------------------
df = pd.DataFrame({

    "ndvi": ndvi.flatten(),

    "ndwi": ndwi.flatten(),

    "ndbi": ndbi.flatten(),

    "elevation": dem.flatten(),

    "air_temperature": air.flatten(),

    "humidity": humidity.flatten(),

    "wind_speed": wind.flatten(),

    "lst": lst.flatten()

})

# -----------------------------
# Remove invalid values
# -----------------------------
df = df.replace([np.inf, -np.inf], np.nan)

df = df.dropna()

# -----------------------------
# Save
# -----------------------------
output = processed / "feature_stack_ai.csv"

df.to_csv(output, index=False)

print("=" * 60)
print("AI FEATURE STACK CREATED")
print("=" * 60)

print(df.head())

print()

print("Rows :", len(df))

print("Saved :", output)