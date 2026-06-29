from pathlib import Path
import rasterio
import pandas as pd
import numpy as np

processed = Path("data/processed")

files = {
    "ndvi": "ndvi.tif",
    "ndwi": "ndwi.tif",
    "ndbi": "ndbi.tif",
    "lst": "lst.tif",
    "risk": "heat_risk.tif"
}

arrays = {}

# Read rasters
for name, file in files.items():
    with rasterio.open(processed / file) as src:
        arrays[name] = src.read(1)

# Find smallest common size
min_rows = min(arr.shape[0] for arr in arrays.values())
min_cols = min(arr.shape[1] for arr in arrays.values())

# Crop and flatten
for key in arrays:
    arrays[key] = arrays[key][:min_rows, :min_cols].flatten()

df = pd.DataFrame(arrays)

df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna()

outfile = processed / "training_dataset.csv"
df.to_csv(outfile, index=False)

print("=" * 60)
print("DATASET CREATED")
print("=" * 60)
print("Rows :", len(df))
print("Columns :", list(df.columns))
print("Saved :", outfile)