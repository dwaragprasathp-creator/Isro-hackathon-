import rasterio
import numpy as np

with rasterio.open("data/processed/lst.tif") as src:
    lst = src.read(1)

# Mean + 1 Standard Deviation
threshold = np.nanmean(lst) + np.nanstd(lst)

hotspots = np.where(lst >= threshold, 1, 0)

print("=" * 50)
print("Hotspot Detection")
print("=" * 50)
print("Threshold:", round(threshold, 2), "°C")
print("Hotspot Pixels:", np.sum(hotspots))