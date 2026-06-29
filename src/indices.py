from pathlib import Path
import rasterio
import numpy as np

processed = Path("data/processed")

def read_band(name):
    with rasterio.open(processed / f"{name}.tif") as src:
        return src.read(1).astype(np.float32), src.profile

blue, profile = read_band("blue")
green, _ = read_band("green")
red, _ = read_band("red")
nir, _ = read_band("nir")
swir1, _ = read_band("swir1")

# Apply Landsat scale factor
for band in [blue, green, red, nir, swir1]:
    band[band == 0] = np.nan
    band *= 0.0000275
    band -= 0.2

# Calculate indices
ndvi = (nir - red) / (nir + red)
ndwi = (green - nir) / (green + nir)
ndbi = (swir1 - nir) / (swir1 + nir)

profile.update(dtype=rasterio.float32, count=1, compress="lzw")

outputs = {
    "ndvi.tif": ndvi,
    "ndwi.tif": ndwi,
    "ndbi.tif": ndbi
}

for filename, data in outputs.items():
    with rasterio.open(processed / filename, "w", **profile) as dst:
        dst.write(data.astype(np.float32), 1)

print("✅ NDVI, NDWI and NDBI regenerated successfully.")