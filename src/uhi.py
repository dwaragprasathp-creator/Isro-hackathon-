import rasterio
import numpy as np
from pathlib import Path

processed = Path("data/processed")

# Load LST
with rasterio.open(processed / "lst.tif") as src:
    lst = src.read(1)
    profile = src.profile

# Calculate mean temperature
mean_temp = np.nanmean(lst)

# Urban Heat Island Intensity
uhi = lst - mean_temp

profile.update(dtype=rasterio.float32)

output = processed / "uhi.tif"

with rasterio.open(output, "w", **profile) as dst:
    dst.write(uhi.astype(rasterio.float32), 1)

print("=" * 50)
print("Urban Heat Island Map Created")
print("=" * 50)
print("Average Temperature :", round(mean_temp, 2), "°C")
print("Saved:", output)